# Generated by Django 3.2 on 2021-09-23 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SubscriptionApp', '0008_auto_20210920_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='razorpaymodel',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
