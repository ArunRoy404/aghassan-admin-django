import numpy as np
import cv2
from PIL import Image
from psd_tools import PSDImage
import base64

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Product, ProductPSD
from .serializers import ProductSerializer
from rest_framework import generics
class ProductListAPI(generics.ListAPIView):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            "success": True,
            "message": "Products retrieved successfully",
            "error": None,
            "status": 200,
            "data": response.data
        })

class ProductDetailAPI(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({
            "success": True,
            "message": "Product retrieved successfully",
            "error": None,
            "status": 200,
            "data": response.data
        })

class GenerateMockupAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def bezier_calc(self, u, v, h_pts, v_pts):
        def B(i, t): return [(1-t)**3, 3*t*(1-t)**2, 3*t**2*(1-t), t**3][i]
        x, y = 0, 0
        for i in range(4):
            for j in range(4):
                coeff = B(i, v) * B(j, u)
                x += h_pts[i*4+j] * coeff
                y += v_pts[i*4+j] * coeff
        return x, y

    def run_warp_math(self, canvas_w, canvas_h, layer_data, user_img):
        scale = 2
        sw, sh = canvas_w * scale, canvas_h * scale
        
        mesh = layer_data['placedLayer']['warp']['customEnvelopeWarp']['meshPoints']
        
        if mesh and isinstance(mesh[0], dict) and 'x' in mesh[0]:
            h_pts = [m['x'] * scale for m in mesh]
            v_pts = [m['y'] * scale for m in mesh]
        else:
            h_pts = [v * scale for v in next(m['values'] for m in mesh if m['type'] == 'horizontal')]
            v_pts = [v * scale for v in next(m['values'] for m in mesh if m['type'] == 'vertical')]
        
        subdiv = 60 
        grid_u = np.linspace(0, 1, subdiv)
        grid_v = np.linspace(0, 1, subdiv)
        dst_pts = np.zeros((subdiv, subdiv, 2), dtype=np.float32)
        for i, v in enumerate(grid_v):
            for j, u in enumerate(grid_u):
                dst_pts[i, j] = self.bezier_calc(u, v, h_pts, v_pts)

        map_x = np.full((sh, sw), -1, dtype=np.float32)
        map_y = np.full((sh, sw), -1, dtype=np.float32)
        img_h, img_w = user_img.shape[:2]
        
        for i in range(subdiv - 1):
            for j in range(subdiv - 1):
                src_q = np.array([[j*img_w/subdiv, i*img_h/subdiv], [(j+1)*img_w/subdiv, i*img_h/subdiv], 
                                 [(j+1)*img_w/subdiv, (i+1)*img_h/subdiv], [j*img_w/subdiv, (i+1)*img_h/subdiv]], dtype=np.float32)
                dst_q = np.array([dst_pts[i, j], dst_pts[i, j+1], dst_pts[i+1, j+1], dst_pts[i+1, j]], dtype=np.float32)

                H, _ = cv2.findHomography(dst_q, src_q)
                if H is None:
                    continue

                min_c = np.floor(np.min(dst_q, axis=0)).astype(int)
                max_c = np.ceil(np.max(dst_q, axis=0)).astype(int)
                
                min_x, min_y = max(0, min_c[0]), max(0, min_c[1])
                max_x, max_y = min(sw, max_c[0]), min(sh, max_c[1])
                
                for py in range(min_y, max_y):
                    for px in range(min_x, max_x):
                        v_src = H @ np.array([px, py, 1.0])
                        if v_src[2] == 0: continue
                        v_src /= v_src[2]
                        if 0 <= v_src[0] < img_w and 0 <= v_src[1] < img_h:
                            map_x[py, px], map_y[py, px] = v_src[0], v_src[1]

        warped_high_res = cv2.remap(user_img, map_x, map_y, 
                                   interpolation=cv2.INTER_LANCZOS4, 
                                   borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))

        final_warp = cv2.resize(warped_high_res, (canvas_w, canvas_h), interpolation=cv2.INTER_AREA)

        b, g, r, a = cv2.split(final_warp)
        a = cv2.GaussianBlur(a, (3, 3), 0)
        final_warp = cv2.merge([b, g, r, a])

        return final_warp

    def get_psd_layer_by_name(self, psd_obj, name):
        for layer in psd_obj:
            if layer.name == name:
                return layer.composite()
        return None

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({
                "success": False,
                "message": "No image provided",
                "error": "Image file is missing in the request",
                "status": 400
            }, status=400)
            
        product_psds = product.psd_files.all()
        if not product_psds.exists():
            return Response({
                "success": False,
                "message": "PSD missing",
                "error": "No PSD files attached to this product",
                "status": 400
            }, status=400)
            
        img_array = np.frombuffer(image_file.read(), np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_UNCHANGED)
        if img is None:
            return Response({
                "success": False,
                "message": "Invalid image",
                "error": "The provided image format is not supported or corrupted",
                "status": 400
            }, status=400)
            
        if len(img.shape) > 2 and img.shape[2] == 3:
            user_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        elif len(img.shape) > 2 and img.shape[2] == 4:
            user_img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
        else:
            user_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGBA)
            
        previews = []
        try:
            for product_psd in product_psds:
                psd_path = product_psd.psd_file.path
                psd_json = product_psd.structure_json
                
                if not psd_json:
                    continue # Skip if no JSON structure
                    
                psd_obj = PSDImage.open(psd_path)
                canvas_w, canvas_h = psd_obj.width, psd_obj.height
                final_image = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))

                layers_data = psd_json.get('children', [])
                
                for layer_data in layers_data:
                    name = layer_data.get('name', 'Unknown')
                    
                    if 'placedLayer' in layer_data:
                        warped_arr = self.run_warp_math(canvas_w, canvas_h, layer_data, user_img)
                        warped_pil = Image.fromarray(warped_arr)
                        final_image.alpha_composite(warped_pil)
                    else:
                        psd_layer_img = self.get_psd_layer_by_name(psd_obj, name)
                        if psd_layer_img:
                            layer_canvas = Image.new("RGBA", (canvas_w, canvas_h), (0,0,0,0))
                            left = layer_data.get('left', 0)
                            top = layer_data.get('top', 0)
                            layer_canvas.paste(psd_layer_img, (left, top))
                            final_image.alpha_composite(layer_canvas)
                
                from io import BytesIO
                response_io = BytesIO()
                final_image.save(response_io, format='PNG')
                img_data = response_io.getvalue()
                
                base64_img = base64.b64encode(img_data).decode('utf-8')
                previews.append(f"data:image/png;base64,{base64_img}")
            
            return Response({
                "success": True,
                "message": f"Successfully generated {len(previews)} mockup(s)",
                "error": None,
                "status": 200,
                "preview": previews
            })
            
        except Exception as e:
            return Response({
                "success": False,
                "message": "Failed to generate mockups",
                "error": str(e),
                "status": 500
            }, status=500)

# Web Views
@login_required
def upload_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        thumbnail = request.FILES.get('thumbnail')
        psd_files = request.FILES.getlist('psd_files')
        
        # Get the JSON data from client-side processing
        import json
        psd_data_raw = request.POST.get('psd_data', '[]')
        try:
            psd_data = json.loads(psd_data_raw)
        except json.JSONDecodeError:
            psd_data = []

        # Create product
        product = Product.objects.create(
            name=name,
            description=description,
            thumbnail=thumbnail
        )

        # Create PSD entries (matching by index)
        for i, psd in enumerate(psd_files):
            structure = None
            if i < len(psd_data):
                structure = psd_data[i].get('structure')
            
            ProductPSD.objects.create(
                product=product, 
                psd_file=psd,
                structure_json=structure
            )

        return redirect('product_list')

    return render(request, 'products/upload.html')

@login_required
def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/list.html', {'products': products})

@login_required
def delete_product(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        product.delete()
    return redirect('product_list')
