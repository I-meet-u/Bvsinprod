# Generated by Django 3.2.9 on 2022-03-08 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MaterialApp', '0051_auto_20220221_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyerproduct_requirements',
            name='landing_page_pk',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='landingpagebidding',
            name='buyer_requirement_pk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='MaterialApp.buyerproduct_requirements'),
        ),
    ]
