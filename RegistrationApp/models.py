from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here.


class SelfRegistration(AbstractUser):
    # registration model create
    first_name = None
    last_name = None
    contact_person = models.CharField(max_length=200)
    business_to_serve = models.CharField(max_length=50,null=True)
    country = models.CharField(max_length=100)
    nature_of_business = ArrayField(models.CharField(max_length=500),null=True)
    user_type = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    admin_approve = models.CharField(max_length=50, default='Pending')
    email_otp = models.CharField(max_length=20, blank=True)
    phone_otp = models.CharField(max_length=20, blank=True)
    department=models.CharField(max_length=100,null=True,blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    profile_cover_photo = models.FileField(upload_to='coverphoto',null=True)
    # registration_status = models.CharField(max_length=80, default='Not Registered')

    class Meta:
        db_table = 'SelfRegistration'


class SelfRegistration_Sample(models.Model):
    contact_person = models.CharField(max_length=200)
    business_to_serve = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    nature_of_business = ArrayField(models.CharField(max_length=800))
    user_type = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    email_otp = models.CharField(max_length=20, blank=True)
    phone_otp = models.CharField(max_length=20, blank=True)
    profile_cover_photo = models.FileField(upload_to='static/coverphoto',null=True)

    class Meta:
        db_table = 'SelfRegistration_Sample'


class BasicCompanyDetails(models.Model):
    # basic details model fields
    company_code = models.CharField(max_length=200, primary_key=True)
    gst_number = models.CharField(max_length=30)
    company_name = models.CharField(max_length=200)
    company_type = models.CharField(max_length=200)
    listing_date = models.CharField(blank=True, max_length=200)
    pan_number = models.CharField(max_length=30)
    tax_payer_type = models.CharField(max_length=200)
    msme_registered = models.CharField(max_length=20)
    company_established = models.CharField(max_length=200)
    registered_iec = models.CharField(max_length=400)
    industrial_scale = models.CharField(max_length=150)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.OneToOneField(SelfRegistration, on_delete=models.CASCADE)

    class Meta:
        db_table = "BasicCompanyDetails"




class IndustrialInfo(models.Model):
    # industry info model fields
    nature_of_business = ArrayField(models.CharField(max_length=1000))
    geographical_area = ArrayField(models.CharField(max_length=1000))
    supply_capabilites = ArrayField(models.CharField(max_length=1000))
    industry_to_serve = ArrayField(models.CharField(max_length=1000))
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.OneToOneField(SelfRegistration, on_delete=models.CASCADE)
    company_code = models.OneToOneField(BasicCompanyDetails, on_delete=models.CASCADE,null=True)

    class Meta:
        db_table = "IndustrialInfo"


class IndustrialHierarchy(models.Model):
    # industrial hierarchy model fields
    maincore = ArrayField(models.CharField(max_length=500))
    category = ArrayField(models.CharField(max_length=500))
    subcategory = ArrayField(models.CharField(max_length=500))
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.OneToOneField(SelfRegistration, on_delete=models.CASCADE)
    company_code = models.OneToOneField(BasicCompanyDetails, on_delete=models.CASCADE)

    class Meta:
        db_table = "IndustrialHierarchy"


class BankDetails(models.Model):
    # bank details model fields
    ifsc_code = models.CharField(max_length=40)
    account_number = models.CharField(max_length=40, unique=True)
    iban_number=models.CharField(max_length=50,null=True,blank=True)
    swift_code=models.CharField(max_length=50,null=True,blank=True)
    micr_number=models.CharField(max_length=50,null=True,blank=True)
    account_type = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=200)
    branch = models.CharField(max_length=50)
    bank_city = models.CharField(max_length=100)
    bank_district = models.CharField(max_length=100)
    bank_state = models.CharField(max_length=100)
    bank_address = models.TextField()
    account_holder_name = models.CharField(max_length=300)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    company_code = models.ForeignKey(BasicCompanyDetails, on_delete=models.CASCADE)

    class Meta:
        db_table = "BankDetails"

class LegalDocuments(models.Model):
    # legal documents model fields
    document_name = models.CharField(max_length=100)
    document = models.FileField(upload_to='static/legalfiles')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)


    class Meta:
        db_table = "LegalDocuments"


class BasicCompanyDetails_Others(models.Model):
    # basic details model fields
    company_name = models.CharField(max_length=200)
    company_code = models.CharField(max_length=20,primary_key=True)
    company_established = models.CharField(max_length=200)
    industrial_scale = models.CharField(max_length=150)
    market_location= models.CharField(max_length=150)
    company_type = models.CharField(max_length=200)
    tax_id_or_vat = models.CharField(max_length=200)
    currency = models.CharField(max_length=30)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.OneToOneField(SelfRegistration, on_delete=models.CASCADE)

    class Meta:
        db_table = "BasicCompanyDetails_Others"


class BillingAddress_Others(models.Model):
    # billing address model fields
    bill_address_others = models.TextField(max_length=500)
    bill_country_others = models.CharField(max_length=200)
    bill_state_others=models.CharField(max_length=200)
    bill_city_others = models.CharField(max_length=200)
    bill_pincode_others = models.IntegerField()
    bill_landmark_others = models.CharField(max_length=50, blank=True)
    bill_location_others = models.CharField(max_length=200, blank=True)
    created_on_others = models.DateTimeField(auto_now_add=True)
    updated_on_others = models.DateTimeField(auto_now=True)
    created_by_others = models.BigIntegerField()
    updated_by_others = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    company_code_others = models.ForeignKey(BasicCompanyDetails_Others,on_delete=models.CASCADE)

    class Meta:
        db_table = "BillingAddress_Others"


class ShippingAddress_Others(models.Model):
    # shipping address model fields
    ship_address_others = models.TextField(max_length=500)
    ship_country_others = models.CharField(max_length=200)
    ship_state_others = models.CharField(max_length=200)
    ship_city_others = models.CharField(max_length=200)
    ship_pincode_others = models.BigIntegerField()
    ship_landmark_others = models.CharField(max_length=50, blank=True)
    ship_location_others = models.CharField(max_length=200, blank=True)
    created_on_others = models.DateTimeField(auto_now_add=True)
    updated_on_others = models.DateTimeField(auto_now=True)
    created_by_others = models.BigIntegerField()
    updated_by_others = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    company_code_others = models.ForeignKey(BasicCompanyDetails_Others,on_delete=models.CASCADE)

    class Meta:
        db_table = "ShippingAddress_Others"


# class EmployeeRegistration(models.Model):
#     emp_id=models.BigAutoField(primary_key=True)
#     username=models.CharField(max_length=100)
#     employee_user_type=models.CharField(max_length=100,null=True,blank=True)
#     country=models.CharField(max_length=100)
#     department=models.CharField(max_length=100)
#     designation=models.CharField(max_length=100)
#     email_id=models.CharField(max_length=100,unique=True)
#     phone_no=models.CharField(max_length=20,unique=True)
#     employee_usertype=models.CharField(max_length=70,null=True)
#     password=models.CharField(max_length=300)
#     created_on_others = models.DateTimeField(auto_now_add=True)
#     updated_on_others = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         db_table="EmployeeRegistration"

class Employee_CompanyDetails(models.Model):
    # basic details model fields
    emp_company_id=models.BigAutoField(primary_key=True)
    emp_company_name = models.CharField(max_length=200)
    emp_company_code = models.CharField(max_length=20,unique=True)
    emp_tax_id_or_vat = models.CharField(max_length=200)
    emp_company_established = models.CharField(max_length=200)
    emp_industrial_scale = models.CharField(max_length=150)
    emp_market_location= models.CharField(max_length=150)
    emp_company_type = models.CharField(max_length=200)
    emp_currency = models.CharField(max_length=30)
    emp_bill_address = models.TextField(max_length=500)
    emp_bill_country = models.CharField(max_length=200)
    emp_bill_state = models.CharField(max_length=200)
    emp_bill_city = models.CharField(max_length=200)
    emp_bill_pincode = models.IntegerField()
    emp_bill_landmark = models.CharField(max_length=50, blank=True)
    emp_bill_location = models.CharField(max_length=200, blank=True)
    emp_ship_address = models.TextField(max_length=500)
    emp_ship_country = models.CharField(max_length=200)
    emp_ship_state = models.CharField(max_length=200)
    emp_ship_city = models.CharField(max_length=200)
    emp_ship_pincode = models.BigIntegerField()
    emp_ship_landmark = models.CharField(max_length=50, blank=True)
    emp_ship_location = models.CharField(max_length=200, blank=True)
    emp_created_on = models.DateTimeField(auto_now_add=True)
    emp_updated_on = models.DateTimeField(auto_now=True)
    emp_created_by = models.BigIntegerField()
    emp_updated_by = models.OneToOneField(SelfRegistration, on_delete=models.CASCADE)

    class Meta:
        db_table = "Employee_CompanyDetails"


class Employee_IndustryInfo(models.Model):
    emp_nature_of_business = ArrayField(models.CharField(max_length=800))
    emp_supply_capabilites = ArrayField(models.CharField(max_length=800))
    emp_industry_to_serve = ArrayField(models.CharField(max_length=800))
    emp_created_on = models.DateTimeField(auto_now_add=True)
    emp_updated_on = models.DateTimeField(auto_now=True)
    emp_created_by = models.BigIntegerField()
    emp_updated_by = models.OneToOneField(SelfRegistration, on_delete=models.CASCADE)
    emp_company = models.OneToOneField(Employee_CompanyDetails, on_delete=models.CASCADE)

    class Meta:
        db_table = "Employee_IndustryInfo"


class ContactDetails(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    currency=models.CharField(max_length=100,null=True,blank=True)
    department = models.CharField(max_length=200, null=True, blank=True)
    designation = models.CharField(max_length=200, null=True, blank=True)
    region = models.CharField(max_length=200, null=True, blank=True)
    email_id = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.OneToOneField(SelfRegistration, on_delete=models.CASCADE)

    class Meta:
        db_table = "ContactDetails"


class CommunicationDetails(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    currency=models.CharField(max_length=100,null=True,blank=True)
    department = models.CharField(max_length=200, null=True, blank=True)
    designation = models.CharField(max_length=200, null=True, blank=True)
    region = models.CharField(max_length=200, null=True, blank=True)
    email_id = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    unit_address=models.TextField(null=True,blank=True)
    unit_name= models.CharField(max_length=100, null=True, blank=True)
    address=models.TextField(null=True,blank=True)
    state=models.CharField(max_length=50, null=True, blank=True)
    city=models.CharField(max_length=80, null=True, blank=True)
    pincode=models.CharField(max_length=12, null=True, blank=True)
    landmark=models.CharField(max_length=150,null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)

    class Meta:
        db_table = "CommunicationDetails"




class BillingAddress(models.Model):
    # billing address model fields
    bill_address = models.TextField(max_length=500)
    bill_country = models.CharField(max_length=200)
    bill_state=models.CharField(max_length=200)
    bill_city = models.CharField(max_length=200)
    bill_pincode = models.IntegerField()
    bill_landmark = models.CharField(max_length=50, blank=True)
    bill_location = models.CharField(max_length=200, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE,null=True,blank=True)
    company_code = models.ForeignKey(BasicCompanyDetails,on_delete=models.CASCADE,null=True,blank=True)
    emp_company_code = models.ForeignKey(Employee_CompanyDetails, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "BillingAddress"


class ShippingAddress(models.Model):
    # shipping address model fields
    ship_address = models.TextField(max_length=500)
    ship_country = models.CharField(max_length=200)
    ship_state = models.CharField(max_length=200)
    ship_city = models.CharField(max_length=200)
    ship_pincode = models.BigIntegerField()
    ship_landmark = models.CharField(max_length=50, blank=True)
    ship_location = models.CharField(max_length=200, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE,null=True,blank=True)
    company_code = models.ForeignKey(BasicCompanyDetails,on_delete=models.CASCADE,null=True,blank=True)
    emp_company_code = models.ForeignKey(Employee_CompanyDetails, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "ShippingAddress"