# Generated by Django 3.2 on 2021-08-08 09:22

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('BiddingApp', '0007_auto_20210807_1521'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalAwards',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('rfq_number', models.CharField(max_length=50)),
                ('company_code', models.CharField(blank=True, max_length=100, null=True)),
                ('company_name', models.CharField(blank=True, max_length=200, null=True)),
                ('order_quantity', models.CharField(blank=True, max_length=100, null=True)),
                ('bid_quantity', models.CharField(blank=True, max_length=100, null=True)),
                ('frieght_cost', models.CharField(blank=True, max_length=500, null=True)),
                ('p_f_charge', models.CharField(blank=True, max_length=500, null=True)),
                ('totalamount', models.CharField(blank=True, max_length=200, null=True)),
                ('rfq_title', models.CharField(blank=True, max_length=100, null=True)),
                ('rfq_status', models.CharField(blank=True, default='Pending', max_length=100, null=True)),
                ('product_code', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None)),
                ('product_name', models.CharField(blank=True, max_length=100, null=True)),
                ('daterange', models.DateField(blank=True, null=True)),
                ('product_description', models.CharField(blank=True, max_length=200, null=True)),
                ('awarded_date', models.DateField(blank=True, editable=False, null=True)),
                ('publish_date', models.DateField(blank=True, null=True)),
                ('deadline_date', models.DateField(blank=True, null=True)),
                ('awardstatus', models.CharField(blank=True, default='Pending', max_length=100, null=True)),
                ('createdon', models.DateTimeField(blank=True, editable=False, null=True)),
                ('updatedon', models.DateTimeField(blank=True, editable=False, null=True)),
                ('postatus', models.CharField(blank=True, default='Pending', max_length=100, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updatedby', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical awards',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Awards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rfq_number', models.CharField(max_length=50)),
                ('company_code', models.CharField(blank=True, max_length=100, null=True)),
                ('company_name', models.CharField(blank=True, max_length=200, null=True)),
                ('order_quantity', models.CharField(blank=True, max_length=100, null=True)),
                ('bid_quantity', models.CharField(blank=True, max_length=100, null=True)),
                ('frieght_cost', models.CharField(blank=True, max_length=500, null=True)),
                ('p_f_charge', models.CharField(blank=True, max_length=500, null=True)),
                ('totalamount', models.CharField(blank=True, max_length=200, null=True)),
                ('rfq_title', models.CharField(blank=True, max_length=100, null=True)),
                ('rfq_status', models.CharField(blank=True, default='Pending', max_length=100, null=True)),
                ('product_code', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None)),
                ('product_name', models.CharField(blank=True, max_length=100, null=True)),
                ('daterange', models.DateField(blank=True, null=True)),
                ('product_description', models.CharField(blank=True, max_length=200, null=True)),
                ('awarded_date', models.DateField(auto_now=True, null=True)),
                ('publish_date', models.DateField(blank=True, null=True)),
                ('deadline_date', models.DateField(blank=True, null=True)),
                ('awardstatus', models.CharField(blank=True, default='Pending', max_length=100, null=True)),
                ('createdon', models.DateTimeField(auto_now_add=True, null=True)),
                ('updatedon', models.DateTimeField(auto_now=True, null=True)),
                ('postatus', models.CharField(blank=True, default='Pending', max_length=100, null=True)),
                ('updatedby', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Awards',
            },
        ),
    ]
