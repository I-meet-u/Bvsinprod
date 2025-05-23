# Generated by Django 3.2.3 on 2021-12-30 10:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AdminApp', '0049_auto_20211229_1417'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrandCompanyCommunicationDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_name', models.TextField(max_length=500)),
                ('country', models.CharField(max_length=200)),
                ('region', models.CharField(max_length=200)),
                ('designation', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=60)),
                ('department', models.CharField(blank=True, max_length=50, null=True)),
                ('telephone', models.IntegerField(blank=True, null=True)),
                ('mobile_number', models.IntegerField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField()),
                ('admins', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AdminApp.adminregister')),
            ],
            options={
                'db_table': 'BrandCompanyCommunicationDetails',
            },
        ),
        migrations.AlterField(
            model_name='admininvite',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='adminselectedcategories',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='adminselectedsubcategories',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='createbuyer',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='createuser',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='openleadsawards',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='openleadsitems',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='openleadsrfq',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='openleadstermsdescription',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='openleadsvendorpublishitems',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='openleadsvendorpublishrfq',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='openleadsvendorpublishtermsdescription',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='trendingcategories',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='trendingsubcategories',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='SellerOrDistributerCommunicationDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_name', models.TextField(max_length=500)),
                ('country', models.CharField(max_length=200)),
                ('region', models.CharField(max_length=200)),
                ('designation', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=60)),
                ('department', models.CharField(blank=True, max_length=50, null=True)),
                ('telephone', models.IntegerField(blank=True, null=True)),
                ('mobile_number', models.IntegerField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField()),
                ('admins', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AdminApp.adminregister')),
                ('seller_distributer_details', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AdminApp.brandcompanycommunicationdetails')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'SellerOrDistributerCommunicationDetails',
            },
        ),
        migrations.CreateModel(
            name='BrandRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.TextField(max_length=500)),
                ('trade_mark_certified', models.CharField(max_length=100)),
                ('brand_code', models.CharField(max_length=100)),
                ('maincore', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=200)),
                ('sub_category', models.CharField(max_length=200)),
                ('brand_registered_tm', models.CharField(max_length=100)),
                ('registration_date', models.CharField(max_length=100)),
                ('tm_certificate_no', models.CharField(max_length=150)),
                ('oem_country_of_origin', models.CharField(max_length=200)),
                ('copy_right_status', models.CharField(max_length=100)),
                ('brand_patented', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField()),
                ('admins', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AdminApp.adminregister')),
            ],
            options={
                'db_table': 'BrandRegistration',
            },
        ),
        migrations.CreateModel(
            name='BrandCompanyDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.TextField(max_length=500)),
                ('address', models.TextField(max_length=500)),
                ('country', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('pincode', models.BigIntegerField()),
                ('landmark', models.CharField(blank=True, max_length=50, null=True)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField()),
                ('admins', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AdminApp.adminregister')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'BrandCompanyDetails',
            },
        ),
        migrations.AddField(
            model_name='brandcompanycommunicationdetails',
            name='brand_cmp_details',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AdminApp.brandcompanydetails'),
        ),
        migrations.CreateModel(
            name='BasicSellerOrDistributerDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.TextField(max_length=500)),
                ('address', models.TextField(max_length=500)),
                ('country', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('pincode', models.BigIntegerField()),
                ('landmark', models.CharField(blank=True, max_length=50, null=True)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField()),
                ('admins', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AdminApp.adminregister')),
            ],
            options={
                'db_table': 'BasicSellerOrDistributerDetails',
            },
        ),
    ]
