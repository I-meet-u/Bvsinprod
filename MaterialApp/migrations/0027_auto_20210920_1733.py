# Generated by Django 3.1.5 on 2021-09-20 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MaterialApp', '0026_awardpostedrfq_po_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='awardpostedrfq',
            name='po_status',
            field=models.CharField(blank=True, default='Pending', max_length=50, null=True),
        ),
    ]
