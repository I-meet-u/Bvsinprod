# Generated by Django 3.2.9 on 2021-12-28 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BiddingApp', '0045_auto_20211122_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyerproductbidding',
            name='get_vendors',
            field=models.CharField(blank=True, default='False', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicalbuyerproductbidding',
            name='get_vendors',
            field=models.CharField(blank=True, default='False', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicalvendorproductbidding',
            name='get_vendors',
            field=models.CharField(blank=True, default='False', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='vendorproductbidding',
            name='get_vendors',
            field=models.CharField(blank=True, default='False', max_length=100, null=True),
        ),
    ]
