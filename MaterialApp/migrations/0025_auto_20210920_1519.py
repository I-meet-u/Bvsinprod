# Generated by Django 3.1.5 on 2021-09-20 09:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MaterialApp', '0024_auto_20210920_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='awardpostedrfq',
            name='created_by',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='awardpostedrfq',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='awardpostedrfq',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='awardpostedrfq',
            name='updated_on',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
