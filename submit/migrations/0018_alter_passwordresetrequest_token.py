# Generated by Django 5.0.3 on 2024-11-16 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0017_alter_passwordresetrequest_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetrequest',
            name='token',
            field=models.CharField(default='tl6B62lMR0H2ivSfSH7Sw846tpuIrxi0', editable=False, max_length=32, unique=True),
        ),
    ]