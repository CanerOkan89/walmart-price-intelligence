from rest_framework import serializers
from .models import Product, PriceEntry

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class PriceEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceEntry
        fields = '__all__'