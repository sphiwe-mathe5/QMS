# Generated by Django 5.0.3 on 2024-11-27 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
