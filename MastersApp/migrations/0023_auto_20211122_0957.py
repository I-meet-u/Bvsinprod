# Generated by Django 3.2.3 on 2021-11-22 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MastersApp', '0022_delete_termmasterssettingsdescription'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorymaster',
            name='category_image',
            field=models.FileField(blank=True, null=True, upload_to='CategoryImage'),
        ),
        migrations.AddField(
            model_name='maincoremaster',
            name='maincore_image',
            field=models.FileField(blank=True, null=True, upload_to='MaincoreImage'),
        ),
        migrations.AddField(
            model_name='subcategorymaster',
            name='sub_category_image',
            field=models.FileField(blank=True, null=True, upload_to='SubCategoryImage'),
        ),
    ]
