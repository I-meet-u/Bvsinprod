# Generated by Django 3.2 on 2021-08-09 09:29

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0004_auto_20210806_1111'),
    ]

    operations = [
        migrations.RenameField(
            model_name='createuser',
            old_name='any_other',
            new_name='business_to_serve',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='aadhar_number',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='address',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='alternate_email',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='alternate_mobile',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='business_unit',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='city',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='company_code',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='company_name',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='company_unit',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='driving_license',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='emergency_contact',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='employee_id',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='land_mark',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='location',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='pan_number',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='passport',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='postal_code',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='relationship',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='reporting_manager',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='state',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='user_name',
        ),
        migrations.RemoveField(
            model_name='createuser',
            name='working_location',
        ),
        migrations.AddField(
            model_name='createuser',
            name='nature_of_business',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), null=True, size=None),
        ),
    ]
