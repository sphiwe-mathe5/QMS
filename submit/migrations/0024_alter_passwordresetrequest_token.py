# Generated by Django 4.2.11 on 2024-11-18 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0023_alter_passwordresetrequest_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetrequest',
            name='token',
            field=models.CharField(default='XGNNtixzAs3fHxy1UySHYBuN415aQnPs', editable=False, max_length=32, unique=True),
        ),
    ]
