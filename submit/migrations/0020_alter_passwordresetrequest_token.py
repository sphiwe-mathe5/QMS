# Generated by Django 5.0.3 on 2024-11-16 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0019_alter_passwordresetrequest_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetrequest',
            name='token',
            field=models.CharField(default='ymoVfQ7B5VXgBvVsOYuwbpkP4DPu0mlm', editable=False, max_length=32, unique=True),
        ),
    ]
