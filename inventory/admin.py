from django.contrib import admin
from .models import Product, ProductBatch

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'registration_no', 'specification', 'model', 'shelf_life_months')
    search_fields = ('name', 'registration_no')
    list_filter = ('shelf_life_months',)

@admin.register(ProductBatch)
class ProductBatchAdmin(admin.ModelAdmin):
    list_display = ('product', 'batch_no', 'production_date', 'quantity', 'expiry_date')
    search_fields = ('batch_no',)
    list_filter = ('production_date', 'expiry_date')
    autocomplete_fields = ('product',)