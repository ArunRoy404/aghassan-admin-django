from rest_framework import serializers
from .models import Product, ProductPSD

class ProductPSDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPSD
        fields = ['id', 'psd_file', 'structure_json', 'uploaded_at']

class ProductSerializer(serializers.ModelSerializer):
    psd_files = ProductPSDSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'thumbnail', 'psd_files', 'created_at']
