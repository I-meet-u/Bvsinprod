# Generated by Django 3.2 on 2021-10-04 06:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0017_openleadspublish'),
    ]

    operations = [
        migrations.AddField(
            model_name='openleadsitems',
            name='buyer_company_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='openleadsitems',
            name='buyer_pk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AdminApp.createbuyer'),
        ),
        migrations.AddField(
            model_name='openleadspublish',
            name='buyer_company_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='openleadspublish',
            name='buyer_pk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AdminApp.createbuyer'),
        ),
        migrations.AddField(
            model_name='openleadsrfq',
            name='buyer_company_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='openleadsrfq',
            name='buyer_pk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AdminApp.createbuyer'),
        ),
        migrations.AddField(
            model_name='openleadstermsdescription',
            name='buyer_company_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='openleadstermsdescription',
            name='buyer_pk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AdminApp.createbuyer'),
        ),
    ]
