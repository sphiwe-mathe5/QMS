# Generated by Django 4.2.11 on 2025-01-02 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0050_alter_passwordresetrequest_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetrequest',
            name='token',
            field=models.CharField(default='1PLa8cp0kM1MafrLVm5xNtjGeH6gg4D7', editable=False, max_length=32, unique=True),
        ),
    ]
