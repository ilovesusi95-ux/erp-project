from django.contrib import admin
from .models import Product, Supplier, RegistrationCertificate, Batch

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'specification', 'model', 'registration', 'price', 'stock')
    search_fields = ('name', 'sku')
    list_filter = ('registration',)

@admin.register(RegistrationCertificate)
class RegistrationCertificateAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'shelf_life_months')
    search_fields = ('name', 'number')

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('product', 'batch_number', 'production_date', 'expiry_date', 'stock')
    search_fields = ('batch_number', 'product__name')
    list_filter = ('product', 'expiry_date')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'production_license', 'contact_phone')
    search_fields = ('name', 'production_license', 'contact_phone')
