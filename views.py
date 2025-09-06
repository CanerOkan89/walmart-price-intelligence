from rest_framework import generics
from .models import Product, PriceEntry
from .serializers import ProductSerializer, PriceEntrySerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class PriceEntryListView(generics.ListAPIView):
    queryset = PriceEntry.objects.all()
    serializer_class = PriceEntrySerializer

class PriceEntryDetailView(generics.RetrieveAPIView):
    queryset = PriceEntry.objects.all()
    serializer_class = PriceEntrySerializer