# Generated by Django 3.2 on 2021-10-11 12:15

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0027_openleadsawards'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='openleadsawards',
            name='vendor_bid_quantity',
        ),
        migrations.AlterField(
            model_name='openleadsawards',
            name='product_description',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=800), blank=True, null=True, size=None),
        ),
    ]
