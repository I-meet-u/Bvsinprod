# Generated by Django 3.2.9 on 2021-12-10 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0047_adminselectedsubcategories_trendingsubcategories'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trendingsubcategories',
            old_name='trending_sub_priority',
            new_name='trending_sub_categories_priority',
        ),
    ]
