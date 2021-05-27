from django.db import models

# Create your models here.
from simple_history.models import HistoricalRecords


class AdminRegister(models.Model):

    admin_id=models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=70)
    company_name = models.CharField(max_length=100)
    admin_email=models.CharField(max_length=150,unique=True)
    admin_phone = models.CharField(max_length=15, unique=True)
    email_otp=models.CharField(max_length=6,null=True,blank=True)
    phone_otp=models.CharField(max_length=6,null=True,blank=True)
    password=models.CharField(max_length=200)

    class Meta:
        db_table = "AdminRegister"


class AdminInvite(models.Model):

    user_name=models.CharField(max_length=100)
    user_type=models.CharField(max_length=100)
    invite_date=models.DateField()
    email=models.CharField(max_length=50)
    phone=models.CharField(max_length=100)
    user_add_to=models.CharField(max_length=100)
    status=models.CharField(max_length=100, default='Pending')
    history = HistoricalRecords()

    class Meta:
        db_table="AdminInvite"

class CreateUser(models.Model):
    user_code=models.CharField(max_length=30)
    user_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    status=models.CharField(max_length=50, default='Pending')
    user_type=models.CharField(max_length=50, null=True, blank=True)
    designation=models.CharField(max_length=100, null=True, blank=True)
    grander=models.CharField(max_length=100, null=True, blank=True)
    department=models.CharField(max_length=100, null=True, blank=True)
    organization = models.CharField(max_length=100, null=True, blank=True)
    company_name = models.CharField(max_length=100)
    company_code = models.CharField(max_length=20)
    employee_id = models.CharField(max_length=20)
    business_unit=models.CharField(max_length=100)
    company_unit = models.CharField(max_length=100)
    reporting_manager=models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=15, null=True, blank=True)
    alternate_email = models.CharField(max_length=30, null=True, blank=True)
    alternate_mobile = models.CharField(max_length=15, null=True, blank=True)
    contact_name = models.CharField(max_length=30, null=True, blank=True)
    pan_number = models.CharField(max_length=20)
    adhar_number = models.CharField(max_length=20)
    relationship = models.CharField(max_length=50, null=True, blank=True)
    driving_license = models.CharField(max_length=30, null=True, blank=True)
    passport = models.CharField(max_length=50, null=True, blank=True)
    any_other = models.CharField(max_length=100, null=True, blank=True)
    address=models.TextField(null=True,blank=True)
    city=models.CharField(max_length=30, null=True, blank=True)
    state=models.CharField(max_length=30, null=True, blank=True)
    location=models.CharField(max_length=200,null=True,blank=True)
    postal_code=models.CharField(max_length=100, null=True, blank=True)
    country=models.CharField(max_length=100, null=True, blank=True)
    land_mark=models.CharField(max_length=200, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table="CreateUser"

class Permissions(models.Model):
    modules=models.CharField(max_length=400,unique=True)
    full_access=models.BooleanField(null=True,blank=True)
    read=models.BooleanField(null=True,blank=True)
    create = models.BooleanField(null=True,blank=True)
    modify = models.BooleanField(null=True,blank=True)
    delete = models.BooleanField(null=True,blank=True)
    disable = models.BooleanField(null=True,blank=True)
    Active = models.BooleanField(null=True,blank=True)

    class Meta:
        db_table="Permissions"