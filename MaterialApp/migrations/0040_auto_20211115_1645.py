# Generated by Django 3.2.3 on 2021-11-15 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MaterialApp', '0039_auto_20211115_1619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='landingpagelistingleadspurchaseorder',
            name='po_numeric',
        ),
        migrations.RemoveField(
            model_name='landingpagelistingleadspurchaseorder',
            name='rfq_type',
        ),
        migrations.AddField(
            model_name='landingpagelistingleadspurchaseorder',
            name='award_pk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='MaterialApp.awardpostedrfq'),
        ),
        migrations.AddField(
            model_name='landingpagelistingleadspurchaseorder',
            name='landing_page_publish_pk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='MaterialApp.landingpagebidding_publish'),
        ),
    ]
