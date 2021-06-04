from django.db import models

# Create your models here.
from simple_history.models import HistoricalRecords

from RegistrationApp.models import SelfRegistration


class AdminRegister(models.Model):
    admin_id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=70)
    company_name = models.CharField(max_length=100)
    admin_email = models.CharField(max_length=150, unique=True)
    admin_phone = models.CharField(max_length=15, unique=True)
    email_otp = models.CharField(max_length=6, null=True, blank=True)
    phone_otp = models.CharField(max_length=6, null=True, blank=True)
    password = models.CharField(max_length=200)

    class Meta:
        db_table = "AdminRegister"


class AdminInvite(models.Model):
    user_name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=100)
    invite_date = models.CharField(max_length=50)
    register_date = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=100, unique=True)
    user_add_to = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default='Pending')
    history = HistoricalRecords()

    class Meta:
        db_table = "AdminInvite"


class CreateUser(models.Model):
    user_code = models.CharField(max_length=30, unique=True)
    numeric = models.CharField(max_length=20)
    user_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    user_type = models.CharField(max_length=50, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    grander = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    organization = models.CharField(max_length=100, null=True, blank=True)
    company_name = models.CharField(max_length=100)
    company_code = models.CharField(max_length=20)
    employee_id = models.CharField(max_length=20)
    business_unit = models.CharField(max_length=100)
    company_unit = models.CharField(max_length=100)
    reporting_manager = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    emergency_contact = models.CharField(max_length=15, null=True, blank=True)
    alternate_email = models.CharField(max_length=30, null=True, blank=True)
    alternate_mobile = models.CharField(max_length=15, null=True, blank=True)
    contact_name = models.CharField(max_length=30, null=True, blank=True)
    pan_number = models.CharField(max_length=20, unique=True)
    aadhar_number = models.CharField(max_length=20, unique=True)
    relationship = models.CharField(max_length=50, null=True, blank=True)
    driving_license = models.CharField(max_length=30, null=True, blank=True, unique=True)
    passport = models.CharField(max_length=50, null=True, blank=True, unique=True)
    any_other = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    postal_code = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    land_mark = models.CharField(max_length=200, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)
    status = models.CharField(max_length=50, default='Active')
    history = HistoricalRecords()

    class Meta:
        db_table = "CreateUser"


class Permissions(models.Model):
    modules = models.CharField(max_length=400, unique=True)
    full_access = models.BooleanField(null=True, blank=True)
    read = models.BooleanField(null=True, blank=True)
    create = models.BooleanField(null=True, blank=True)
    modify = models.BooleanField(null=True, blank=True)
    delete = models.BooleanField(null=True, blank=True)
    disable = models.BooleanField(null=True, blank=True)
    active = models.BooleanField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "Permissions"
