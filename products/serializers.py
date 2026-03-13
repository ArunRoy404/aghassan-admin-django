from rest_framework import serializers
from .models import Product, ProductPSD

class ProductPSDLeanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPSD
        fields = ['id', 'psd_file', 'uploaded_at']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'thumbnail', 'created_at']
