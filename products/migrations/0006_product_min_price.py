# Generated by Django 3.2.22 on 2023-10-14 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20231012_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='min_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
