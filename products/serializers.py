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
            width = 0
            height = 0

            structure = m.structure_json

            if isinstance(structure, dict):
                children = structure.get('children', [])
            elif isinstance(structure, list):
                children = structure
            else:
                children = []

            for child in children:
                if isinstance(child, dict) and 'placedLayer' in child:
                    placed = child.get('placedLayer', {})
                    width = placed.get('width', 0)
                    height = placed.get('height', 0)
                    break

            if width == 0 and height == 0 and isinstance(structure, dict):
                width = structure.get('width', 0)
                height = structure.get('height', 0)

            thumbnail_url = None
            if getattr(m, "image_without_warp", None):
                try:
                    if request:
                        thumbnail_url = request.build_absolute_uri(m.image_without_warp.url)
                    else:
                        thumbnail_url = m.image_without_warp.url
                except:
                    thumbnail_url = None

            res.append({
                'id': m.id,
                'name': m.name,
                'width': width,
                'height': height,
                'thumbnail': thumbnail_url
            })

        return res
