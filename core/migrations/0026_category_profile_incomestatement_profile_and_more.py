# Generated by Django 4.2.11 on 2024-11-02 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0015_alter_passwordresetrequest_token'),
        ('core', '0025_remove_incomestatement_operating_expenses_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='submit.profile'),
        ),
        migrations.AddField(
            model_name='incomestatement',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='submit.profile'),
        ),
        migrations.AddField(
            model_name='product',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='submit.profile'),
        ),
    ]
