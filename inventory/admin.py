from django.contrib import admin
from .models import Supplier, RegistrationCertificate, Product, Inbound

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'production_license', 'contact_phone')
    search_fields = ('name', 'production_license', 'contact_phone')

@admin.register(RegistrationCertificate)
class RegistrationCertificateAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'shelf_life_months')
    search_fields = ('name', 'number')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'specification', 'model', 'registration', 'price')
    search_fields = ('name', 'sku')
    list_filter = ('registration',)

@admin.register(Inbound)
class InboundAdmin(admin.ModelAdmin):
    list_display = ('registration', 'product', 'batch_number', 'production_date', 'expiry_date', 'quantity', 'inbound_date')
    search_fields = ('batch_number', 'registration__name', 'product__name')
    list_filter = ('registration', 'product', 'expiry_date')
    readonly_fields = ('production_date', 'expiry_date')  # 自动计算的字段只读
