from rest_framework import serializers
from .models import Product, ProductPSD

class ProductPSDLeanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPSD
        fields = ['id', 'psd_file', 'uploaded_at']

class ProductSerializer(serializers.ModelSerializer):
    mockup = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'thumbnail', 'created_at', 'mockup']

        def get_mockup(self, obj):
            request = self.context.get('request', None)

            mockups = obj.psd_files.filter(psd_type='mockup')
            res = []

            for m in mockups:
                width, height = 0, 0

                # SAFE structure_json handling
                if isinstance(m.structure_json, dict):
                    children = m.structure_json.get('children', [])
                    for child in children:
                        if isinstance(child, dict) and 'placedLayer' in child:
                            pl = child.get('placedLayer', {})
                            width = pl.get('width', 0)
                            height = pl.get('height', 0)
                            break

                    if width == 0 and height == 0:
                        width = m.structure_json.get('width', 0)
                        height = m.structure_json.get('height', 0)

                # SAFE image handling
                thumbnail_url = None
                if getattr(m, "image_without_warp", None):
                    try:
                        if request:
                            thumbnail_url = request.build_absolute_uri(m.image_without_warp.url)
                        else:
                            thumbnail_url = m.image_without_warp.url
                    except Exception:
                        thumbnail_url = None

                res.append({
                    'id': m.id,
                    'name': m.name,
                    'width': width,
                    'height': height,
                    'thumbnail': thumbnail_url
                })

            return res