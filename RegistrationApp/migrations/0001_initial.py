# Generated by Django 3.2 on 2021-08-03 10:31

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    # dependencies = [
    #     ('auth','0012_alter_user_first_name_max_length')
    # ]

    operations = [
        migrations.CreateModel(
            name='BasicCompanyDetails',
            fields=[
                ('company_code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('gst_number', models.CharField(max_length=30)),
                ('company_name', models.CharField(max_length=200)),
                ('company_type', models.CharField(max_length=200)),
                ('listing_date', models.CharField(blank=True, max_length=200)),
                ('pan_number', models.CharField(max_length=30)),
                ('tax_payer_type', models.CharField(max_length=200)),
                ('msme_registered', models.CharField(max_length=20)),
                ('company_established', models.CharField(max_length=200)),
                ('registered_iec', models.CharField(max_length=400)),
                ('industrial_scale', models.CharField(max_length=150)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField()),
            ],
            options={
                'db_table': 'BasicCompanyDetails',
            },
        ),
        migrations.CreateModel(
            name='BasicCompanyDetails_Others',
            fields=[
                ('company_name', models.CharField(max_length=200)),
                ('company_code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('company_established', models.CharField(max_length=200)),
                ('industrial_scale', models.CharField(max_length=150)),
                ('market_location', models.CharField(max_length=150)),
                ('company_type', models.CharField(max_length=200)),
                ('tax_id_or_vat', models.CharField(max_length=200)),
                ('currency', models.CharField(max_length=30)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField()),
            ],
            options={
                'db_table': 'BasicCompanyDetails_Others',
            },
        ),
        migrations.CreateModel(
            name='Employee_CompanyDetails',
            fields=[
                ('emp_company_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('emp_company_name', models.CharField(max_length=200)),
                ('emp_company_code', models.CharField(max_length=20, unique=True)),
                ('emp_tax_id_or_vat', models.CharField(max_length=200)),
                ('emp_company_established', models.CharField(max_length=200)),
                ('emp_industrial_scale', models.CharField(max_length=150)),
                ('emp_market_location', models.CharField(max_length=150)),
                ('emp_company_type', models.CharField(max_length=200)),
                ('emp_currency', models.CharField(max_length=30)),
                ('emp_bill_address', models.TextField(max_length=500)),
                ('emp_bill_country', models.CharField(max_length=200)),
                ('emp_bill_state', models.CharField(max_length=200)),
                ('emp_bill_city', models.CharField(max_length=200)),
                ('emp_bill_pincode', models.IntegerField()),
                ('emp_bill_landmark', models.CharField(blank=True, max_length=50)),
                ('emp_bill_location', models.CharField(blank=True, max_length=200)),
                ('emp_ship_address', models.TextField(max_length=500)),
                ('emp_ship_country', models.CharField(max_length=200)),
                ('emp_ship_state', models.CharField(max_length=200)),
                ('emp_ship_city', models.CharField(max_length=200)),
                ('emp_ship_pincode', models.BigIntegerField()),
                ('emp_ship_landmark', models.CharField(blank=True, max_length=50)),
                ('emp_ship_location', models.CharField(blank=True, max_length=200)),
                ('emp_created_on', models.DateTimeField(auto_now_add=True)),
                ('emp_updated_on', models.DateTimeField(auto_now=True)),
                ('emp_created_by', models.BigIntegerField()),
            ],
            options={
                'db_table': 'Employee_CompanyDetails',
            },
        ),
        migrations.CreateModel(
            name='SelfRegistration_Sample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_person', models.CharField(max_length=200)),
                ('business_to_serve', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=100)),
                ('nature_of_business', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=800), size=None)),
                ('user_type', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('email_otp', models.CharField(blank=True, max_length=20)),
                ('phone_otp', models.CharField(blank=True, max_length=20)),
                ('profile_cover_photo', models.FileField(null=True, upload_to='static/coverphoto')),
            ],
            options={
                'db_table': 'SelfRegistration_Sample',
            },
        ),
        migrations.CreateModel(
            name='SelfRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('contact_person', models.CharField(max_length=200)),
                ('business_to_serve', models.CharField(max_length=50, null=True)),
                ('country', models.CharField(max_length=100)),
                ('nature_of_business', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), null=True, size=None)),
                ('user_type', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('admin_approve', models.CharField(default='Pending', max_length=50)),
                ('email_otp', models.CharField(blank=True, max_length=20)),
                ('phone_otp', models.CharField(blank=True, max_length=20)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('designation', models.CharField(blank=True, max_length=100, null=True)),
                ('profile_cover_photo', models.FileField(null=True, upload_to='coverphoto')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'SelfRegistration',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress_Others',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ship_address_others', models.TextField(max_length=500)),
                ('ship_country_others', models.CharField(max_length=200)),
                ('ship_state_others', models.CharField(max_length=200)),
                ('ship_city_others', models.CharField(max_length=200)),
                ('ship_pincode_others', models.BigIntegerField()),
                ('ship_landmark_others', models.CharField(blank=True, max_length=50)),
                ('ship_location_others', models.CharField(blank=True, max_length=200)),
                ('created_on_others', models.DateTimeField(auto_now_add=True)),
                ('updated_on_others', models.DateTimeField(auto_now=True)),
                ('created_by_others', models.BigIntegerField()),
                ('company_code_others', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RegistrationApp.basiccompanydetails_others')),
                ('updated_by_others', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ShippingAddress_Others',
            },
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ship_address', models.TextField(max_length=500)),
                ('ship_country', models.CharField(max_length=200)),
                ('ship_state', models.CharField(max_length=200)),
                ('ship_city', models.CharField(max_length=200)),
                ('ship_pincode', models.BigIntegerField()),
                ('ship_landmark', models.CharField(blank=True, max_length=50)),
                ('ship_location', models.CharField(blank=True, max_length=200)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField()),
                ('company_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='RegistrationApp.basiccompanydetails')),
                ('emp_company_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='RegistrationApp.employee_companydetails')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ShippingAddress',
            },
        ),
        migrations.CreateModel(
            name='LegalDocuments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_name', models.CharField(max_length=100)),
                ('document', models.FileField(upload_to='static/legalfiles')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField()),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'LegalDocuments',
            },
        ),
        migrations.CreateModel(
            name='IndustrialInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nature_of_business', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=800), size=None)),
                ('geographical_area', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=None)),
                ('supply_capabilites', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=800), size=None)),
                ('industry_to_serve', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=800), size=None)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField()),
                ('company_code', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='RegistrationApp.basiccompanydetails')),
                ('updated_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'IndustrialInfo',
            },
        ),
        migrations.CreateModel(
            name='IndustrialHierarchy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maincore', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), size=None)),
                ('category', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), size=None)),
                ('subcategory', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), size=None)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField()),
                ('company_code', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='RegistrationApp.basiccompanydetails')),
                ('updated_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'IndustrialHierarchy',
            },
        ),
        migrations.CreateModel(
            name='Employee_IndustryInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_nature_of_business', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=800), size=None)),
                ('emp_supply_capabilites', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=800), size=None)),
                ('emp_industry_to_serve', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=800), size=None)),
                ('emp_created_on', models.DateTimeField(auto_now_add=True)),
                ('emp_updated_on', models.DateTimeField(auto_now=True)),
                ('emp_created_by', models.BigIntegerField()),
                ('emp_company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='RegistrationApp.employee_companydetails')),
                ('emp_updated_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Employee_IndustryInfo',
            },
        ),
        migrations.AddField(
            model_name='employee_companydetails',
            name='emp_updated_by',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ContactDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('currency', models.CharField(blank=True, max_length=100, null=True)),
                ('department', models.CharField(blank=True, max_length=200, null=True)),
                ('designation', models.CharField(blank=True, max_length=200, null=True)),
                ('region', models.CharField(blank=True, max_length=200, null=True)),
                ('email_id', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField()),
                ('updated_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ContactDetails',
            },
        ),
        migrations.CreateModel(
            name='CommunicationDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('currency', models.CharField(blank=True, max_length=100, null=True)),
                ('department', models.CharField(blank=True, max_length=200, null=True)),
                ('designation', models.CharField(blank=True, max_length=200, null=True)),
                ('region', models.CharField(blank=True, max_length=200, null=True)),
                ('email_id', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('unit_address', models.TextField(blank=True, null=True)),
                ('unit_name', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(blank=True, max_length=80, null=True)),
                ('pincode', models.CharField(blank=True, max_length=12, null=True)),
                ('landmark', models.CharField(blank=True, max_length=150, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField()),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'CommunicationDetails',
            },
        ),
        migrations.CreateModel(
            name='BillingAddress_Others',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_address_others', models.TextField(max_length=500)),
                ('bill_country_others', models.CharField(max_length=200)),
                ('bill_state_others', models.CharField(max_length=200)),
                ('bill_city_others', models.CharField(max_length=200)),
                ('bill_pincode_others', models.IntegerField()),
                ('bill_landmark_others', models.CharField(blank=True, max_length=50)),
                ('bill_location_others', models.CharField(blank=True, max_length=200)),
                ('created_on_others', models.DateTimeField(auto_now_add=True)),
                ('updated_on_others', models.DateTimeField(auto_now=True)),
                ('created_by_others', models.BigIntegerField()),
                ('company_code_others', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RegistrationApp.basiccompanydetails_others')),
                ('updated_by_others', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'BillingAddress_Others',
            },
        ),
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_address', models.TextField(max_length=500)),
                ('bill_country', models.CharField(max_length=200)),
                ('bill_state', models.CharField(max_length=200)),
                ('bill_city', models.CharField(max_length=200)),
                ('bill_pincode', models.IntegerField()),
                ('bill_landmark', models.CharField(blank=True, max_length=50)),
                ('bill_location', models.CharField(blank=True, max_length=200)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField()),
                ('company_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='RegistrationApp.basiccompanydetails')),
                ('emp_company_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='RegistrationApp.employee_companydetails')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'BillingAddress',
            },
        ),
        migrations.AddField(
            model_name='basiccompanydetails_others',
            name='updated_by',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='basiccompanydetails',
            name='updated_by',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='BankDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ifsc_code', models.CharField(max_length=40)),
                ('account_number', models.CharField(max_length=40, unique=True)),
                ('iban_number', models.CharField(blank=True, max_length=50, null=True)),
                ('swift_code', models.CharField(blank=True, max_length=50, null=True)),
                ('micr_number', models.CharField(blank=True, max_length=50, null=True)),
                ('account_type', models.CharField(max_length=50)),
                ('bank_name', models.CharField(max_length=200)),
                ('branch', models.CharField(max_length=50)),
                ('bank_city', models.CharField(max_length=100)),
                ('bank_district', models.CharField(max_length=100)),
                ('bank_state', models.CharField(max_length=100)),
                ('bank_address', models.TextField()),
                ('account_holder_name', models.CharField(max_length=300)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField()),
                ('company_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RegistrationApp.basiccompanydetails')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'BankDetails',
            },
        ),
    ]
