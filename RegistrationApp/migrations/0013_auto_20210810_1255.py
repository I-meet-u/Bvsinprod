# Generated by Django 3.2 on 2021-08-10 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RegistrationApp', '0012_auto_20210809_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selfregistration',
            name='email_otp',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='selfregistration',
            name='phone_otp',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
