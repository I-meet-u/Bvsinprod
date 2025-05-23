# Generated by Django 3.2.9 on 2022-02-11 10:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('BiddingApp', '0051_auto_20220205_1351'),
    ]

    operations = [
        migrations.CreateModel(
            name='SourcePurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_code', models.CharField(blank=True, max_length=100, null=True)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('awarded_date', models.DateTimeField(auto_now_add=True)),
                ('po_date', models.CharField(blank=True, max_length=100, null=True)),
                ('po_number', models.CharField(blank=True, max_length=100, null=True)),
                ('delivery_date', models.CharField(blank=True, max_length=100, null=True)),
                ('remind_date', models.CharField(blank=True, max_length=100, null=True)),
                ('delivery_days', models.CharField(blank=True, max_length=100, null=True)),
                ('item_name', models.CharField(blank=True, max_length=200, null=True)),
                ('item_description', models.TextField(blank=True, null=True)),
                ('uom', models.CharField(blank=True, max_length=100, null=True)),
                ('quantity', models.CharField(blank=True, max_length=100, null=True)),
                ('unit_rate', models.CharField(blank=True, max_length=100, null=True)),
                ('discount', models.CharField(blank=True, max_length=100, null=True)),
                ('tax', models.CharField(blank=True, max_length=100, null=True)),
                ('total_amount', models.CharField(blank=True, max_length=100, null=True)),
                ('subject', models.CharField(blank=True, max_length=1000, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('attachment_1', models.FileField(blank=True, null=True, upload_to='SourcePOFiles')),
                ('attachment_2', models.FileField(blank=True, null=True, upload_to='SourcePOFiles')),
                ('attachment_3', models.FileField(blank=True, null=True, upload_to='SourcePOFiles')),
                ('createdon', models.DateTimeField(auto_now_add=True, null=True)),
                ('updatedon', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('source_code', models.CharField(blank=True, max_length=100, null=True)),
                ('source_type', models.CharField(blank=True, max_length=100, null=True)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'SourcePurchaseOrder',
            },
        ),
    ]
