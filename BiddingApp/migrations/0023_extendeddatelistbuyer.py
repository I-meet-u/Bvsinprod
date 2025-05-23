# Generated by Django 3.2 on 2021-09-05 08:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('BiddingApp', '0022_auto_20210904_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendedDateListBuyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_rfq_number', models.CharField(blank=True, max_length=100, null=True)),
                ('vendor_code', models.CharField(blank=True, max_length=100, null=True)),
                ('product_bidding_id', models.CharField(blank=True, max_length=100, null=True)),
                ('product_rfq_status', models.CharField(blank=True, max_length=100, null=True)),
                ('rfq_type', models.CharField(blank=True, max_length=100, null=True)),
                ('product_publish_date', models.CharField(blank=True, max_length=200, null=True)),
                ('product_department', models.CharField(blank=True, max_length=100, null=True)),
                ('product_deadline_date', models.DateField(blank=True, null=True)),
                ('product_rfq_title', models.CharField(blank=True, max_length=100, null=True)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.BigIntegerField()),
                ('userid', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ExtendedDateListBuyer',
            },
        ),
    ]
