from django.contrib import admin
from .models import Product, Supplier

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'stock')
    search_fields = ('name', 'sku')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'production_license', 'contact_phone')
    search_fields = ('name', 'production_license', 'contact_phone')
