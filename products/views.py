from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, ProductPSD
from .serializers import ProductSerializer
from rest_framework import generics

# API Views
class ProductListAPI(generics.ListAPIView):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer

class ProductDetailAPI(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Web Views
@login_required
def upload_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        thumbnail = request.FILES.get('thumbnail')
        psd_files = request.FILES.getlist('psd_files')

        # Create product
        product = Product.objects.create(
            name=name,
            description=description,
            thumbnail=thumbnail
        )

        # Create PSD entries
        for psd in psd_files:
            ProductPSD.objects.create(product=product, psd_file=psd)

        return redirect('product_list')

    return render(request, 'products/upload.html')

@login_required
def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/list.html', {'products': products})
