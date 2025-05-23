# Generated by Django 3.2 on 2021-08-03 10:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('AdminApp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='permissions',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='createuser',
            name='admins',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdminApp.adminregister'),
        ),
        migrations.AddField(
            model_name='admininvite',
            name='admins',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdminApp.adminregister'),
        ),
    ]
