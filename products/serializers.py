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
        mockups = obj.psd_files.filter(psd_type='mockup')
        res = []
        for m in mockups:
            width = 0
            height = 0
            if m.structure_json:
                children = m.structure_json.get('children', [])
                for child in children:
                    if 'placedLayer' in child:
                        width = child['placedLayer'].get('width', 0)
                        height = child['placedLayer'].get('height', 0)
                        break
                
                if width == 0 and height == 0:
                    width = m.structure_json.get('width', 0)
                    height = m.structure_json.get('height', 0)
            thumbnail_url = None
            if m.image_without_warp:
                request = self.context.get('request')
                if request:
                    thumbnail_url = request.build_absolute_uri(m.image_without_warp.url)
                else:
                    thumbnail_url = m.image_without_warp.url

            res.append({
                'id': m.id,
                'name': m.name,
                'width': width,
                'height': height,
                'thumbnail': thumbnail_url
            })
        return res
