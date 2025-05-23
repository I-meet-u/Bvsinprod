# Generated by Django 3.2 on 2021-08-11 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('BiddingApp', '0013_auto_20210811_1308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='biddingbuyerproductdetails',
            name='product_rfq_type',
        ),
        migrations.RemoveField(
            model_name='historicalbiddingbuyerproductdetails',
            name='product_rfq_type',
        ),
        migrations.RemoveField(
            model_name='historicalrfqtermsdescription',
            name='product_rfq_type',
        ),
        migrations.RemoveField(
            model_name='rfqtermsdescription',
            name='product_rfq_type',
        ),
        migrations.AddField(
            model_name='historicalrfqtermsdescription',
            name='rfq_type',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='rfqtermsdescription',
            name='rfq_type',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='historicalrfqtermsdescription',
            name='rfq_number',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='rfqtermsdescription',
            name='rfq_number',
            field=models.CharField(max_length=200),
        ),
        migrations.CreateModel(
            name='HistoricalBiddingBuyerMachinaryDetails',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('machinary_buyer_item_code', models.CharField(blank=True, max_length=100, null=True)),
                ('machinary_buyer_item_name', models.CharField(max_length=100)),
                ('machinary_buyer_item_description', models.TextField(blank=True, null=True)),
                ('machinary_buyer_uom', models.CharField(blank=True, max_length=100, null=True)),
                ('machinary_buyer_category', models.CharField(max_length=500, null=True)),
                ('machinary_buyer_quantity', models.CharField(max_length=100)),
                ('machinary_buyer_document', models.TextField(blank=True, max_length=100, null=True)),
                ('created_on', models.DateTimeField(blank=True, editable=False)),
                ('updated_on', models.DateTimeField(blank=True, editable=False)),
                ('created_by', models.BigIntegerField()),
                ('machinary_buyer_rfq_number', models.CharField(max_length=100)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical bidding buyer machinary details',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='BiddingBuyerMachinaryDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('machinary_buyer_item_code', models.CharField(blank=True, max_length=100, null=True)),
                ('machinary_buyer_item_name', models.CharField(max_length=100)),
                ('machinary_buyer_item_description', models.TextField(blank=True, null=True)),
                ('machinary_buyer_uom', models.CharField(blank=True, max_length=100, null=True)),
                ('machinary_buyer_category', models.CharField(max_length=500, null=True)),
                ('machinary_buyer_quantity', models.CharField(max_length=100)),
                ('machinary_buyer_document', models.FileField(blank=True, null=True, upload_to='BuyerMachinaryFiles')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField()),
                ('machinary_buyer_rfq_number', models.CharField(max_length=100)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'BiddingBuyerMachinaryDetails',
            },
        ),
    ]
