from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="商品名称")
    sku = models.CharField(max_length=50, unique=True, verbose_name="商品编码")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="售价")
    stock = models.PositiveIntegerField(default=0, verbose_name="当前库存")

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品管理"

    def __str__(self):
        return self.name