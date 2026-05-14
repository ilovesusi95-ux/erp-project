from django.db import migrations


def populate_sku_database(apps, schema_editor):
    SkuDatabase = apps.get_model('inventory', 'SkuDatabase')

    specs = ['Fr10', 'Fr12', 'Fr14', 'Fr16', 'Fr18', 'Fr20', 'Fr22', 'Fr24']
    tubes = ['圆管', '十字管', '双腔管']
    balls = ['100ml引流球', '200ml引流球']
    bags = ['无引流袋', '700ml引流袋']
    needles = ['无穿刺针', '配穿刺针', '配可折弫穿刺针']

    created = 0
    for spec in specs:
        for tube in tubes:
            for ball in balls:
                for bag in bags:
                    for needle in needles:
                        full_name = f"一次性使用术后引流管套件III型{spec}{tube}{ball}{bag}{needle}"
                        if not SkuDatabase.objects.filter(full_name=full_name).exists():
                            SkuDatabase.objects.create(
                                specification=spec,
                                tube_type=tube,
                                drainage_ball=ball,
                                drainage_bag=bag,
                                puncture_needle=needle,
                            )
                            created += 1
    print(f"\n自动生成了 {created} 条 SKU数据\n")


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_skudatabase_delete_sku'),
    ]

    operations = [
        migrations.RunPython(populate_sku_database),
    ]
