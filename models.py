from django.db import models
from django.utils import timezone

class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True, primary_key=True)
    product_name = models.CharField(max_length=500)
    brand = models.CharField(max_length=200, blank=True, null=True)
    department = models.CharField(max_length=100)
    category = models.CharField(max_length=200)
    subcategory = models.CharField(max_length=200, blank=True, null=True)
    breadcrumbs = models.CharField(max_length=500, blank=True, null=True)
    product_url = models.URLField(max_length=1000, blank=True, null=True)
    product_size = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.product_name} ({self.sku})"

class PriceEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prices")
    shipping_location = models.CharField(max_length=20)
    price_retail = models.DecimalField(max_digits=10, decimal_places=2)
    price_current = models.DecimalField(max_digits=10, decimal_places=2)
    promotion = models.CharField(max_length=500, blank=True, null=True)
    run_date = models.DateTimeField()
    tid = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['product', 'shipping_location', 'run_date']