# Generated by Django 3.2.9 on 2022-03-03 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MastersApp', '0025_alter_frieghtchargesmaster_frieght_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverymaster',
            name='delivery_code',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='paymentmaster',
            name='payment_code',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='transitinsurancemaster',
            name='transit_code',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='validitymaster',
            name='validity_code',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
