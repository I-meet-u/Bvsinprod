# Generated by Django 3.2.9 on 2021-12-10 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0043_alter_adminselectedcategories_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminselectedcategories',
            name='priority',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
