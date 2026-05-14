from django.db import migrations


def populate_sku_database(apps, schema_editor):
    SkuDatabase = apps.get_model('inventory', 'SkuDatabase')

    specs = ['Fr10', 'Fr12', 'Fr14', 'Fr16', 'Fr18', 'Fr20', 'Fr22', 'Fr24']
    tubes = ['圆管', '十字管', '双腔管']
    balls = ['100ml引流球', '200ml引流球']
    bags = ['无引流袋', '700ml引流袋']
    needles = ['无穿刺针', '配穿刺针', '配可折弯穿刺针']

    for spec in specs:
        for tube in tubes:
            for ball in balls:
                for bag in bags:
                    for needle in needles:
                        SkuDatabase.objects.get_or_create(
                            specification=spec,
                            tube_type=tube,
                            drainage_ball=ball,
                            drainage_bag=bag,
                            puncture_needle=needle
                        )


class Migration(migrations.Migration):
    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_sku_database),
    ]
