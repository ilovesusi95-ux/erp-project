from django.db import models
from datetime import date, timedelta

class Supplier(models.Model):
    name = models.CharField(max_length=100, verbose_name="名称")
    address = models.TextField(verbose_name="地址", blank=True)
    production_license = models.CharField(max_length=100, verbose_name="生产许可证号", blank=True)
    contact_phone = models.CharField(max_length=20, verbose_name="联系电话", blank=True)

    class Meta:
        verbose_name = "供应商"
        verbose_name_plural = "供应商管理"

    def __str__(self):
        return self.name


class RegistrationCertificate(models.Model):
    name = models.CharField(max_length=200, verbose_name="注册证名称")
    number = models.CharField(max_length=100, unique=True, verbose_name="注册证号")
    shelf_life_months = models.PositiveIntegerField(verbose_name="保质期（月）", default=24)

    class Meta:
        verbose_name = "注册证"
        verbose_name_plural = "注册证管理"

    def __str__(self):
        return f"{self.name} ({self.number})"


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="商品名称")
    sku = models.CharField(max_length=50, unique=True, verbose_name="商品编码")
    specification = models.CharField(max_length=100, verbose_name="规格", blank=True)
    model = models.CharField(max_length=100, verbose_name="型号", blank=True)
    registration = models.ForeignKey(
        RegistrationCertificate, 
        on_delete=models.PROTECT, 
        verbose_name="注册证",
        null=True, blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="售价", default=0)

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品管理"

    def __str__(self):
        return self.name


class Inbound(models.Model):
    registration = models.ForeignKey(RegistrationCertificate, on_delete=models.PROTECT, verbose_name="注册证")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="商品", null=True, blank=True)
    batch_number = models.CharField(max_length=50, verbose_name="生产批号")
    production_date = models.DateField(verbose_name="生产日期", null=True, blank=True)
    expiry_date = models.DateField(verbose_name="到期日期", null=True, blank=True)
    quantity = models.PositiveIntegerField(verbose_name="数量")
    inbound_date = models.DateTimeField(auto_now_add=True, verbose_name="入库时间")

    class Meta:
        verbose_name = "入库记录"
        verbose_name_plural = "入库系统"

    def save(self, *args, **kwargs):
        # 自动解析生产日期（批号前8位是YYYYMMDD）
        if not self.production_date and len(self.batch_number) >= 8:
            try:
                ymd = self.batch_number[:8]
                if ymd.isdigit():
                    self.production_date = date(int(ymd[:4]), int(ymd[4:6]), int(ymd[6:8]))
            except:
                pass

        # 自动计算到期日期
        if self.production_date and self.registration:
            months = self.registration.shelf_life_months
            total_days = int(months * 30.44)
            self.expiry_date = self.production_date + timedelta(days=total_days)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.registration.name} - {self.batch_number} x{self.quantity}"
