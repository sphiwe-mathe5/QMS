# Generated by Django 4.2.11 on 2025-01-02 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0051_alter_passwordresetrequest_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetrequest',
            name='token',
            field=models.CharField(default='7fsFFYKnyHThGyEK5MoIVbUooJ8D0eqI', editable=False, max_length=32, unique=True),
        ),
    ]