# Generated by Django 3.2 on 2021-10-05 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0021_openleadsitems_dcouments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openleadsrfq',
            name='additional_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='openleadsrfq',
            name='bill_address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='openleadsrfq',
            name='closing_date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='openleadsrfq',
            name='currency',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='openleadsrfq',
            name='department',
            field=models.CharField(blank=True, max_length=280, null=True),
        ),
        migrations.AlterField(
            model_name='openleadsrfq',
            name='document_1',
            field=models.FileField(blank=True, null=True, upload_to='OpenLeadsDocuments'),
        ),
        migrations.AlterField(
            model_name='openleadsrfq',
            name='document_2',
            field=models.FileField(blank=True, null=True, upload_to='OpenLeadsDocuments'),
        ),
        migrations.AlterField(
            model_name='openleadsrfq',
            name='document_3',
            field=models.FileField(blank=True, null=True, upload_to='OpenLeadsDocuments'),
        ),
        migrations.AlterField(
            model_name='openleadsrfq',
            name='document_name_1',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='openleadsrfq',
            name='document_name_2',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='openleadsrfq',
            name='document_name_3',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='openleadsrfq',
            name='rfq_status',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='openleadsrfq',
            name='scope_of_supply',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='openleadsrfq',
            name='scope_of_work',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='openleadsrfq',
            name='ship_address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
