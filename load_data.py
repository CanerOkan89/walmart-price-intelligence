from django.core.management.base import BaseCommand
import pandas as pd
from decimal import Decimal
from tracker.models import Product, PriceEntry

class Command(BaseCommand):
    help = 'Load Walmart data from CSV'

    def handle(self, *args, **options):
        csv_file = "data/WMT_Grocery_202209.csv"
        chunk_size = 5000  # Smaller chunks for stability
        total_products = 0
        total_prices = 0
        
        self.stdout.write(f"Loading data from {csv_file}...")
        
        for chunk_num, chunk in enumerate(pd.read_csv(csv_file, chunksize=chunk_size, low_memory=False)):
            self.stdout.write(f"Processing chunk {chunk_num + 1} ({len(chunk)} rows)...")
            
            for _, row in chunk.iterrows():
                try:
                    sku = str(row['SKU']).strip()
                    if not sku or sku == 'nan':
                        continue
                    
                    price_current = self.clean_price(row['PRICE_CURRENT'])
                    if not price_current:
                        continue
                    
                    # Create product
                    product, created = Product.objects.get_or_create(
                        sku=sku,
                        defaults={
                            'product_name': str(row['PRODUCT_NAME'])[:500],
                            'brand': str(row['BRAND'])[:200] if pd.notna(row['BRAND']) else None,
                            'department': str(row['DEPARTMENT'])[:100],
                            'category': str(row['CATEGORY'])[:200],
                            'subcategory': str(row['SUBCATEGORY'])[:200] if pd.notna(row['SUBCATEGORY']) else None,
                            'breadcrumbs': str(row['BREADCRUMBS'])[:500] if pd.notna(row['BREADCRUMBS']) else None,
                            'product_url': str(row['PRODUCT_URL']) if pd.notna(row['PRODUCT_URL']) else None,
                            'product_size': str(row['PRODUCT_SIZE'])[:100] if pd.notna(row['PRODUCT_SIZE']) else None,
                        }
                    )
                    
                    if created:
                        total_products += 1
                    
                    # Create price entry
                    price_entry, created = PriceEntry.objects.get_or_create(
                        product=product,
                        shipping_location=str(row['SHIPPING_LOCATION']),
                        run_date=pd.to_datetime(row['RunDate']),
                        defaults={
                            'price_retail': self.clean_price(row['PRICE_RETAIL']) or price_current,
                            'price_current': price_current,
                            'promotion': str(row['PROMOTION'])[:500] if pd.notna(row['PROMOTION']) else None,
                            'tid': str(row['tid']),
                        }
                    )
                    
                    if created:
                        total_prices += 1
                        
                except Exception as e:
                    self.stdout.write(f"Error: {e}")
                    continue
            
            self.stdout.write(f"Progress: {total_products} products, {total_prices} prices")
        
        self.stdout.write(f"Final: {total_products} products, {total_prices} prices loaded!")
    
    def clean_price(self, price_str):
        if pd.isna(price_str):
            return None
        try:
            return Decimal(str(price_str).replace('$', '').replace(',', ''))
        except:
            return None