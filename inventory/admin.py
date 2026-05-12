from django.contrib import admin
from .models import Supplier, RegistrationCertificate, Product, InboundOrder, InboundItem

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

class InboundItemInline(admin.TabularInline):
    model = InboundItem
    extra = 3  # 默认显示3行空白，方便一次添加多个商品
    fields = ('registration', 'product', 'batch_number', 'production_date', 'expiry_date', 'quantity')
    readonly_fields = ('production_date', 'expiry_date')

@admin.register(InboundOrder)
class InboundOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'inbound_date', 'supplier')
    inlines = [InboundItemInline]
    search_fields = ('order_number',)

@admin.register(InboundItem)
class InboundItemAdmin(admin.ModelAdmin):
    list_display = ('inbound_order', 'registration', 'product', 'batch_number', 'quantity', 'production_date', 'expiry_date')
    search_fields = ('batch_number',)
    list_filter = ('inbound_order', 'registration')
