# Generated by Django 3.1.5 on 2021-08-19 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MaterialApp', '0013_auto_20210813_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalvendorproduct_documents',
            name='id',
            field=models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='historicalvendorproduct_generaldetails',
            name='id',
            field=models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='historicalvendorproduct_productfeatures',
            name='id',
            field=models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='historicalvendorproduct_technicalspecifications',
            name='id',
            field=models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='itemcodesettings',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='vendorproduct_documents',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='vendorproduct_generaldetails',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='vendorproduct_productfeatures',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='vendorproduct_technicalspecifications',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
