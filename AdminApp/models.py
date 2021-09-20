from django.contrib.postgres.fields import ArrayField
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
    super_admin_key=models.CharField(max_length=60,unique=True,null=True,blank=True)

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

    class Meta:
        db_table = "AdminInvite"


class CreateUser(models.Model):
    user_code = models.CharField(max_length=30, unique=True,null=True,blank=True)
    numeric = models.CharField(max_length=20)
    # user_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50, null=True, blank=True)
    user_type = models.CharField(max_length=50, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    # working_location=models.CharField(max_length=100,null=True,blank=True)
    # address = models.TextField(null=True, blank=True)
    # city = models.CharField(max_length=30, null=True, blank=True)
    # state = models.CharField(max_length=30, null=True, blank=True)
    # location = models.CharField(max_length=200, null=True, blank=True)
    # postal_code = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    # land_mark = models.CharField(max_length=200, null=True, blank=True)
    # organization = models.CharField(max_length=100, null=True, blank=True)
    # business_unit = models.CharField(max_length=100)
    # company_name = models.CharField(max_length=100)
    # employee_id = models.CharField(max_length=20)
    # company_unit = models.CharField(max_length=100)
    # company_code = models.CharField(max_length=20)
    # reporting_manager = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    business_to_serve = models.CharField(max_length=100, null=True,blank=True)
    nature_of_business = ArrayField(models.CharField(max_length=500),null=True)
    # emergency_contact = models.CharField(max_length=15, null=True, blank=True)
    # alternate_email = models.CharField(max_length=30, null=True, blank=True)
    # alternate_mobile = models.CharField(max_length=15, null=True, blank=True)
    contact_name = models.CharField(max_length=30, null=True, blank=True)
    # pan_number = models.CharField(max_length=20, unique=True)
    # aadhar_number = models.CharField(max_length=20, unique=True)
    # relationship = models.CharField(max_length=50, null=True, blank=True)
    # driving_license = models.CharField(max_length=30, null=True, blank=True, unique=True)
    # passport = models.CharField(max_length=50, null=True, blank=True, unique=True)
    # any_other = models.CharField(max_length=100, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)
    status = models.CharField(max_length=50, default='Active')
    admins=models.ForeignKey(AdminRegister,on_delete=models.CASCADE)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "CreateUser"



class CreateBuyer(models.Model):
    company_code=models.CharField(max_length=100,null=True,blank=True)
    company_name=models.CharField(max_length=500)
    gst_no=models.CharField(max_length=50)
    company_type=models.CharField(max_length=280)
    currency=models.CharField(max_length=300)
    pan_number=models.CharField(max_length=80)
    tax_payer_type=models.CharField(max_length=150)
    msme_registered=models.CharField(max_length=50)
    established_year=models.CharField(max_length=100)
    website=models.CharField(max_length=200,null=True,blank=True)
    industrial_scale=models.CharField(max_length=100)
    email_id=models.CharField(max_length=250,unique=True)
    phone_no=models.CharField(max_length=30)
    emergency_no=models.CharField(max_length=50)
    designation=models.CharField(max_length=150)
    department=models.CharField(max_length=150)
    alternate_email=models.CharField(max_length=100)
    bill_company_name=models.CharField(max_length=300)
    bill_address=models.TextField()
    bill_city=models.CharField(max_length=400)
    bill_state=models.CharField(max_length=400)
    bill_country=models.CharField(max_length=300)
    bill_pincode=models.IntegerField()
    bill_landmark=models.CharField(max_length=600,null=True,blank=True)
    bill_location = models.CharField(max_length=300, null=True, blank=True)
    ship_company_name = models.CharField(max_length=300)
    ship_address = models.TextField()
    ship_city = models.CharField(max_length=400)
    ship_state = models.CharField(max_length=400)
    ship_country = models.CharField(max_length=300)
    ship_pincode = models.IntegerField()
    ship_landmark = models.CharField(max_length=600, null=True, blank=True)
    ship_location = models.CharField(max_length=300, null=True, blank=True)
    numeric=models.IntegerField(null=True,blank=True)
    admins=models.ForeignKey(AdminRegister,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by = models.CharField(max_length=100,null=True,blank=True)
    user_image=models.FileField(upload_to="AdminImages",null=True,blank=True)

    class Meta:
        db_table = "CreateBuyer"


class OpenLeadsRfq(models.Model):
    buyer=models.CharField(max_length=200)
    rfq_number=models.CharField(max_length=50,null=True,blank=True)
    numeric=models.IntegerField(null=True,blank=True)
    rfq_status=models.CharField(max_length=80)
    rfq_type=models.CharField(max_length=80)
    publish_date=models.CharField(max_length=100)
    deadline_date=models.CharField(max_length=100)
    closing_date=models.CharField(max_length=100)
    department=models.CharField(max_length=280)
    currency=models.CharField(max_length=250)
    category=models.CharField(max_length=250)
    bill_address=models.TextField()
    ship_address=models.TextField()
    scope_of_supply=models.TextField()
    scope_of_work=models.TextField()
    additional_info=models.TextField()
    document_1=models.FileField(upload_to='OpenLeadsDocuments')
    document_name_1=models.CharField(max_length=500)
    document_2=models.FileField(upload_to='OpenLeadsDocuments')
    document_name_2 = models.CharField(max_length=500)
    document_3=models.FileField(upload_to='OpenLeadsDocuments')
    document_name_3 = models.CharField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE)

    class Meta:
        db_table='OpenLeadsRfq'

class OpenLeadsItems(models.Model):
    item_code=models.CharField(max_length=100)
    item_name=models.CharField(max_length=300)
    item_description=models.TextField()
    uom=models.CharField(max_length=100)
    quantity=models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE)

    class Meta:
        db_table='OpenLeadsItems'
