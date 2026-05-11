from django.db import models
from datetime import timedelta

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="产品名称")
    registration_no = models.CharField(max_length=100, unique=True, verbose_name="注册证号")
    specification = models.CharField(max_length=100, verbose_name="规格")
    model = models.CharField(max_length=100, verbose_name="型号")
    shelf_life_months = models.PositiveIntegerField(verbose_name="保质期（月）")

    class Meta:
        verbose_name = "产品"
        verbose_name_plural = "产品管理"

    def __str__(self):
        return f"{self.name} ({self.registration_no})"


class ProductBatch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="产品")
    batch_no = models.CharField(max_length=50, verbose_name="生产批号")
    production_date = models.DateField(verbose_name="生产日期")
    quantity = models.PositiveIntegerField(verbose_name="入库数量")
    expiry_date = models.DateField(verbose_name="到期日期", blank=True, null=True)

    class Meta:
        verbose_name = "批次库存"
        verbose_name_plural = "批次库存管理"

    def save(self, *args, **kwargs):
        if self.production_date and self.product.shelf_life_months:
            self.expiry_date = self.production_date + timedelta(days=self.product.shelf_life_months * 30)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.batch_no}"