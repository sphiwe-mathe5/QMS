# Generated by Django 4.2.11 on 2024-07-21 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0004_profile_category_profile_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]