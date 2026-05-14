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


class Specification(models.Model):
    registration = models.ForeignKey(
        RegistrationCertificate, 
        on_delete=models.CASCADE, 
        related_name='specifications',
        verbose_name="所属注册证"
    )
    name = models.CharField(max_length=100, verbose_name="规格名称")

    class Meta:
        verbose_name = "规格"
        verbose_name_plural = "产品配置管理"
        unique_together = [['registration', 'name']]

    def __str__(self):
        return self.name


class SpecModel(models.Model):
    specification = models.ForeignKey(
        Specification, 
        on_delete=models.CASCADE, 
        related_name='models',
        verbose_name="所属规格"
    )
    name = models.CharField(max_length=100, verbose_name="型号名称")

    # 新增：针对一次性使用术后引流管套件的配置选项
    DRAINAGE_BALL_CHOICES = [
        ('100ml', '100ml'),
        ('200ml', '200ml'),
    ]
    DRAINAGE_BAG_CHOICES = [
        ('无引流袋', '无引流袋'),
        ('700ml引流袋', '700ml引流袋'),
        ('1000ml引流袋', '1000ml引流袋'),
    ]
    PUNCTURE_NEEDLE_CHOICES = [
        ('无穿刺针', '无穿刺针'),
        ('配穿刺针', '配穿刺针'),
        ('配可折弫穿刺针', '配可折弫穿刺针'),
    ]

    drainage_ball = models.CharField(
        max_length=20, 
        choices=DRAINAGE_BALL_CHOICES, 
        blank=True, 
        null=True, 
        verbose_name="引流球规格"
    )
    drainage_bag = models.CharField(
        max_length=20, 
        choices=DRAINAGE_BAG_CHOICES, 
        blank=True, 
        null=True, 
        verbose_name="是否搭配引流袋"
    )
    puncture_needle = models.CharField(
        max_length=20, 
        choices=PUNCTURE_NEEDLE_CHOICES, 
        blank=True, 
        null=True, 
        verbose_name="是否搭配穿刺针"
    )

    class Meta:
        verbose_name = "型号"
        verbose_name_plural = "型号管理"
        unique_together = [['specification', 'name']]

    def __str__(self):
        return self.name


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


class InboundOrder(models.Model):
    order_number = models.CharField(max_length=50, unique=True, verbose_name="入库单号")
    inbound_date = models.DateField(auto_now_add=True, verbose_name="入库日期")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="供应商")
    note = models.TextField(verbose_name="备注", blank=True)

    class Meta:
        verbose_name = "入库单"
        verbose_name_plural = "入库单管理"

    def __str__(self):
        return self.order_number


class InboundItem(models.Model):
    inbound_order = models.ForeignKey(InboundOrder, on_delete=models.CASCADE, verbose_name="入库单", related_name='items')
    registration = models.ForeignKey(RegistrationCertificate, on_delete=models.PROTECT, verbose_name="注册证")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="商品", null=True, blank=True)
    batch_number = models.CharField(max_length=50, verbose_name="生产批号")
    production_date = models.DateField(verbose_name="生产日期", null=True, blank=True)
    expiry_date = models.DateField(verbose_name="到期日期", null=True, blank=True)
    quantity = models.PositiveIntegerField(verbose_name="数量")

    class Meta:
        verbose_name = "入库明细"
        verbose_name_plural = "入库明细"

    def save(self, *args, **kwargs):
        if not self.production_date and len(self.batch_number) >= 8:
            try:
                ymd = self.batch_number[:8]
                if ymd.isdigit():
                    self.production_date = date(int(ymd[:4]), int(ymd[4:6]), int(ymd[6:8]))
            except:
                pass

        if self.production_date and self.registration:
            months = self.registration.shelf_life_months
            total_days = int(months * 30.44)
            self.expiry_date = self.production_date + timedelta(days=total_days)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.inbound_order.order_number} - {self.batch_number} x{self.quantity}"


# ====================== 新增：SKU数据库模块 ======================
class SkuDatabase(models.Model):
    PRODUCT_TYPE = "一次性使用术后引流管套件"
    MODEL_TYPE = "III型"

    SPECIFICATION_CHOICES = [
        ('Fr10', 'Fr10'),
        ('Fr12', 'Fr12'),
        ('Fr14', 'Fr14'),
        ('Fr16', 'Fr16'),
        ('Fr18', 'Fr18'),
        ('Fr20', 'Fr20'),
        ('Fr22', 'Fr22'),
        ('Fr24', 'Fr24'),
    ]
    TUBE_TYPE_CHOICES = [
        ('圆管', '圆管'),
        ('十字管', '十字管'),
        ('双腔管', '双腔管'),
    ]
    DRAINAGE_BALL_CHOICES = [
        ('100ml引流球', '100ml引流球'),
        ('200ml引流球', '200ml引流球'),
    ]
    DRAINAGE_BAG_CHOICES = [
        ('无引流袋', '无引流袋'),
        ('700ml引流袋', '700ml引流袋'),
    ]
    PUNCTURE_NEEDLE_CHOICES = [
        ('无穿刺针', '无穿刺针'),
        ('配穿刺针', '配穿刺针'),
        ('配可折弫穿刺针', '配可折弫穿刺针'),
    ]

    specification = models.CharField(
        max_length=10, 
        choices=SPECIFICATION_CHOICES, 
        verbose_name="规格"
    )
    tube_type = models.CharField(
        max_length=10, 
        choices=TUBE_TYPE_CHOICES, 
        verbose_name="管型"
    )
    drainage_ball = models.CharField(
        max_length=20, 
        choices=DRAINAGE_BALL_CHOICES, 
        verbose_name="引流球"
    )
    drainage_bag = models.CharField(
        max_length=20, 
        choices=DRAINAGE_BAG_CHOICES, 
        verbose_name="引流袋"
    )
    puncture_needle = models.CharField(
        max_length=20, 
        choices=PUNCTURE_NEEDLE_CHOICES, 
        verbose_name="穿刺针"
    )

    full_name = models.CharField(max_length=300, unique=True, verbose_name="完整SKU名称", blank=True, editable=False)
    sku_code = models.CharField(max_length=80, unique=True, verbose_name="SKU编码", blank=True, editable=False)

    class Meta:
        verbose_name = "SKU数据库"
        verbose_name_plural = "SKU数据库管理"
        ordering = ['specification', 'tube_type', 'drainage_ball']

    def save(self, *args, **kwargs):
        # 自动生成完整名称
        self.full_name = (
            f"{self.PRODUCT_TYPE}{self.MODEL_TYPE}{self.specification}{self.tube_type}"
            f"{self.drainage_ball}{self.drainage_bag}{self.puncture_needle}"
        )
        # 简短SKU编码（可读性强）
        if not self.sku_code:
            ball_short = self.drainage_ball.replace('引流球', '')
            bag_short = self.drainage_bag.replace('引流袋', '').replace('无', 'W')
            needle_short = self.puncture_needle.replace('穿刺针', '').replace('配', 'P').replace('可折弫', 'FB')
            self.sku_code = f"DIII-{self.specification}-{self.tube_type[:2]}-{ball_short}-{bag_short}-{needle_short}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
