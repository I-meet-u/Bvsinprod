# Generated by Django 3.2 on 2021-08-07 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MaterialApp', '0006_auto_20210807_1003'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalvendorproduct_basicdetails',
            old_name='price_range',
            new_name='price_range_from',
        ),
        migrations.RenameField(
            model_name='vendorproduct_basicdetails',
            old_name='price_range',
            new_name='price_range_from',
        ),
        migrations.AddField(
            model_name='historicalvendorproduct_basicdetails',
            name='price_range_to',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='vendorproduct_basicdetails',
            name='price_range_to',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
