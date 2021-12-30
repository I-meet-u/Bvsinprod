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
    rfq_status=models.CharField(max_length=80,null=True,blank=True,default='Pending')
    rfq_type=models.CharField(max_length=80)
    publish_date=models.CharField(max_length=100)
    deadline_date=models.CharField(max_length=100)
    closing_date=models.CharField(max_length=100,null=True, blank=True)
    department=models.CharField(max_length=280,null=True, blank=True)
    currency=models.CharField(max_length=250,null=True, blank=True)
    category=models.CharField(max_length=250)
    bill_address=models.TextField(null=True, blank=True)
    ship_address=models.TextField(null=True, blank=True)
    scope_of_supply=models.TextField(null=True, blank=True)
    scope_of_work=models.TextField(null=True, blank=True)
    additional_info=models.TextField(null=True, blank=True)
    document_1=models.FileField(upload_to='OpenLeadsDocuments',null=True, blank=True)
    document_name_1=models.CharField(max_length=500,null=True, blank=True)
    document_2=models.FileField(upload_to='OpenLeadsDocuments',null=True, blank=True)
    document_name_2 = models.CharField(max_length=500,null=True, blank=True)
    document_3=models.FileField(upload_to='OpenLeadsDocuments',null=True, blank=True)
    document_name_3 = models.CharField(max_length=500,null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE)
    buyer_company_code = models.CharField(max_length=100, null=True, blank=True)
    buyer_company_name = models.CharField(max_length=500,null=True,blank=True)
    maincore = models.CharField(max_length=300, null=True, blank=True)
    subcategory = models.CharField(max_length=300, null=True, blank=True)
    rfq_title=models.TextField(null=True,blank=True)
    buyer_pk=models.ForeignKey(CreateBuyer,on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        db_table='OpenLeadsRfq'

class OpenLeadsItems(models.Model):
    item_code=models.CharField(max_length=100)
    item_name=models.CharField(max_length=300)
    item_description=models.TextField()
    item_type = models.CharField(max_length=80, null=True, blank=True)
    uom=models.CharField(max_length=100)
    quantity=models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE)
    open_leads_pk = models.ForeignKey(OpenLeadsRfq, on_delete=models.CASCADE, null=True, blank=True)
    buyer_company_code = models.CharField(max_length=100, null=True, blank=True)
    buyer_company_name = models.CharField(max_length=500,null=True,blank=True)
    buyer_pk = models.ForeignKey(CreateBuyer, on_delete=models.CASCADE, null=True, blank=True)
    dcouments=models.FileField(default='OpenLeadsItemsFiles',null=True,blank=True)
    rfq_number = models.CharField(max_length=50, null=True, blank=True)
    class Meta:
        db_table='OpenLeadsItems'



class OpenLeadsTermsDescription(models.Model):
    rfq_number=models.CharField(max_length=200,null=True,blank=True)
    terms=models.CharField(max_length=500)
    description=models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE)
    open_leads_pk=models.ForeignKey(OpenLeadsRfq, on_delete=models.CASCADE,null=True,blank=True)
    rfq_type = models.CharField(max_length=150,null=True,blank=True)
    buyer_company_code = models.CharField(max_length=100, null=True, blank=True)
    buyer_company_name = models.CharField(max_length=500,null=True,blank=True)
    buyer_pk = models.ForeignKey(CreateBuyer, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "OpenLeadsTermsDescription"


# class OpenLeadsPublish(models.Model):
#     company_name=models.CharField(max_length=200)
#     vendor_code=models.CharField(max_length=70)
#     nature_of_busines=models.CharField(max_length=200)
#     supply_capability=models.CharField(max_length=200)
#     vendor_group=models.CharField(max_length=200,null=True,blank=True)
#     maincore=models.CharField(max_length=200)
#     category=models.CharField(max_length=300)
#     sub_category=models.CharField(max_length=300)
#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)
#     created_by = models.BigIntegerField(null=True, blank=True)
#     updated_by = models.BigIntegerField(null=True, blank=True)
#     admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE)
#     buyer_company_code = models.CharField(max_length=100, null=True, blank=True)
#     buyer_company_name = models.CharField(max_length=500,null=True,blank=True)
#     buyer_pk = models.ForeignKey(CreateBuyer, on_delete=models.CASCADE, null=True, blank=True)
#
#     class Meta:
#         db_table = "OpenLeadsPublish"


class BuyerProductDetailsAdmin(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    item_type = models.CharField(max_length=100, null=True)
    item_code = models.CharField(max_length=100, null=True, unique=True)
    item_name = models.CharField(max_length=100, null=True)
    item_description = models.TextField(null=True,blank=True)
    numeric = models.CharField(max_length=50,null=True,blank=True)
    uom = models.CharField(max_length=100, blank=True)
    hsn_sac = models.CharField(max_length=100, blank=True,null=True)
    unit_price = models.CharField(max_length=100, blank=True,null=True)
    prefix = models.CharField(max_length=50,null=True, blank=True)
    suffix = models.CharField(max_length=50,null=True, blank=True)
    category=models.CharField(max_length=500,null=True,blank=True)
    department=models.CharField(max_length=400,null=True,blank=True)
    item_group = models.CharField(max_length=500, blank=True,null=True)
    annual_consumption = models.CharField(max_length=500, null=True,blank=True)
    safety_stock = models.CharField(max_length=100, blank=True,null=True)
    model_no = models.CharField(max_length=500, blank=True,null=True)
    document1=models.FileField(upload_to='BuyerProductFilesAdmin',null=True,blank=True)
    document2 = models.FileField(upload_to='BuyerProductFilesAdmin', null=True, blank=True)
    document3 = models.FileField(upload_to='BuyerProductFilesAdmin', null=True, blank=True)
    additional_specifications=models.TextField(null=True,blank=True)
    add_product_supplies=models.CharField(max_length=200,null=True,blank=True)
    product_status=models.CharField(max_length=50,default='Active')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE)
    rfq_number=models.CharField(max_length=100,null=True,blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table = "BuyerProductDetailsAdmin"



class OpenLeadsVendorPublishRfq(models.Model):
    vendor_rfq_number = models.CharField(max_length=50, null=True, blank=True)
    vendor_code = models.CharField(max_length=70,null=True,blank=True)
    vendor_rfq_status = models.CharField(max_length=80, null=True, blank=True,default='Pending')
    vendor_rfq_type = models.CharField(max_length=80)
    buyer_publish_date = models.CharField(max_length=100, null=True, blank=True)
    vendor_publish_date = models.DateField(auto_now_add=True)
    vendor_deadline_date = models.CharField(max_length=100,null=True,blank=True)
    vendor_closing_date = models.CharField(max_length=100, null=True, blank=True)
    maincore = models.CharField(max_length=300, null=True, blank=True)
    category = models.CharField(max_length=250,null=True,blank=True)
    subcategory = models.CharField(max_length=300, null=True, blank=True)
    vendor_bill_address = models.TextField(null=True, blank=True)
    vendor_ship_address = models.TextField(null=True, blank=True)
    vendor_rfq_title = models.TextField(null=True, blank=True)
    final_amount=models.CharField(max_length=200,null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    open_rfq_buyer_pk = models.ForeignKey(OpenLeadsRfq, on_delete=models.CASCADE, null=True, blank=True)
    buyer_company_code = models.CharField(max_length=100, null=True, blank=True)
    buyer_company_name = models.CharField(max_length=500, null=True, blank=True)
    vendor_comments=models.TextField(null=True, blank=True)


    class Meta:
        db_table='OpenLeadsVendorPublishRfq'


class OpenLeadsVendorPublishItems(models.Model):
    vendor_item_type = models.CharField(max_length=100, null=True, blank=True)
    vendor_item_code= models.CharField(max_length=100,null=True,blank=True)
    vendor_item_name = models.CharField(max_length=300)
    vendor_item_description = models.TextField(null=True,blank=True)
    vendor_uom = models.CharField(max_length=100)
    buyer_quantity = models.CharField(max_length=100,null=True,blank=True)
    # vendor_quantity = models.CharField(max_length=100,null=True,blank=True)
    vendor_rate = models.CharField(max_length=100,null=True,blank=True)
    vendor_tax = models.CharField(max_length=100,null=True,blank=True)
    vendor_discount = models.CharField(max_length=100,null=True,blank=True)
    # vendor_final_amount = models.CharField(max_length=80,null=True,blank=True)
    vendor_total_amount= models.CharField(max_length=80,null=True,blank=True)
    # vendor_document=models.FileField(upload_to='OpenLeadsItemsFiles',null=True,blank=True)
    vendor_rfq_number = models.CharField(max_length=100, null=True, blank=True)
    # vendor_category = models.CharField(max_length=500, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    vendor_open_leads_pk = models.ForeignKey(OpenLeadsVendorPublishRfq, on_delete=models.CASCADE, null=True, blank=True)
    vendor_code = models.CharField(max_length=70, null=True, blank=True)
    buyer_company_code = models.CharField(max_length=100, null=True, blank=True)
    buyer_company_name = models.CharField(max_length=500, null=True, blank=True)


    class Meta:
        db_table='OpenLeadsVendorPublishItems'


class OpenLeadsVendorPublishTermsDescription(models.Model):
    vendor_rfq_number = models.CharField(max_length=200, null=True, blank=True)
    vendor_terms = models.CharField(max_length=500, null=True, blank=True)
    vendor_description = models.TextField(null=True, blank=True)
    vendor_response = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    vendor_open_leads_pk = models.ForeignKey(OpenLeadsVendorPublishRfq, on_delete=models.CASCADE, null=True, blank=True)
    vendor_rfq_type = models.CharField(max_length=150, null=True, blank=True)
    buyer_company_code = models.CharField(max_length=100, null=True, blank=True)
    buyer_company_name = models.CharField(max_length=500, null=True, blank=True)
    vendor_code = models.CharField(max_length=70, null=True, blank=True)

    class Meta:
        db_table = "OpenLeadsVendorPublishTermsDescription"


class OpenLeadsAwards(models.Model):
    rfq_number = models.CharField(max_length=50)
    company_code=ArrayField(models.CharField(max_length=200),null=True,blank=True)
    company_name=ArrayField(models.CharField(max_length=200),null=True,blank=True)
    buyer_bid_quantity = models.CharField(max_length=100, null=True, blank=True)
    totalamount=models.CharField(max_length=200, null=True, blank=True)
    rfq_title = models.CharField(max_length=100, null=True, blank=True)
    rfq_status = models.CharField(max_length=100, null=True, default="Pending", blank=True)
    product_code=ArrayField(models.CharField(max_length=200),null=True,blank=True)
    product_name = ArrayField(models.CharField(max_length=200),null=True,blank=True)
    daterange = models.DateField(null=True,blank=True)
    product_description = ArrayField(models.CharField(max_length=800),null=True,blank=True)
    awarded_date = models.DateField(auto_now=True, null=True, blank=True)
    publish_date=models.CharField(max_length=100,null=True, blank=True)
    deadline_date=models.CharField(max_length=100,null=True, blank=True)
    # awardstatus=models.CharField(max_length=100,null=True,blank=True,default='Pending')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE,null=True,blank=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE,null=True,blank=True)
    postatus=models.CharField(max_length=100,default='Pending',blank=True,null=True)
    rfq_type=models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        db_table = "OpenLeadsAwards"


class AdminSelectedCategories(models.Model):
    category_name=models.CharField(max_length=200,unique=True)
    category_id=models.CharField(max_length=100,null=True,blank=True)
    admins=models.ForeignKey(AdminRegister,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    category_image = models.FileField(upload_to='CategoryImage', null=True, blank=True)
    priority=models.CharField(max_length=150,null=True,blank=True)

    class Meta:
        db_table="AdminSelectedCategories"

class TrendingCategories(models.Model):
    trending_category_name=models.CharField(max_length=200,unique=True)
    trending_category_id=models.CharField(max_length=100,null=True,blank=True)
    admins=models.ForeignKey(AdminRegister,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    trending_category_image = models.FileField(upload_to='CategoryImage', null=True, blank=True)
    trending_priority=models.CharField(max_length=150,null=True,blank=True)

    class Meta:
        db_table="TrendingCategories"


class AdminSelectedSubCategories(models.Model):
    sub_category_name=models.CharField(max_length=200,unique=True)
    sub_category_id=models.CharField(max_length=100,null=True,blank=True)
    admins=models.ForeignKey(AdminRegister,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    sub_category_image = models.FileField(upload_to='CategoryImage', null=True, blank=True)
    sub_categories_priority=models.CharField(max_length=150,null=True,blank=True)

    class Meta:
        db_table="AdminSelectedSubCategories"

class TrendingSubCategories(models.Model):
    trending_sub_category_name=models.CharField(max_length=200,unique=True)
    trending_sub_category_id=models.CharField(max_length=100,null=True,blank=True)
    admins=models.ForeignKey(AdminRegister,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    trending_sub_category_image = models.FileField(upload_to='CategoryImage', null=True, blank=True)
    trending_sub_categories_priority=models.CharField(max_length=150,null=True,blank=True)

    class Meta:
        db_table="TrendingSubCategories"


class BrandRegistration(models.Model):
    # Brand Registration  Details model fields
    brand_name= models.TextField(max_length=500)
    trade_mark_certified=models.CharField(max_length=100)
    brand_code=models.CharField(max_length=100)
    maincore=models.CharField(max_length=100)
    category=models.CharField(max_length=200)
    sub_category=models.CharField(max_length=200)
    brand_registered_tm=models.CharField(max_length=100)
    registration_date=models.CharField(max_length=100)
    tm_certificate_no=models.CharField(max_length=150)
    oem_country_of_origin=models.CharField(max_length=200)
    copy_right_status=models.CharField(max_length=100)
    brand_patented=models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table="BrandRegistration"



class BrandCompanyDetails(models.Model):
    # Brand Company Details model fields
     company_name= models.TextField(max_length=500)
     address=models.TextField(max_length=500)
     country = models.CharField(max_length=200)
     state = models.CharField(max_length=200)
     city = models.CharField(max_length=200)
     pincode = models.BigIntegerField()
     landmark = models.CharField(max_length=50, blank=True,null=True)
     location = models.CharField(max_length=200, blank=True,null=True)
     created_on = models.DateTimeField(auto_now_add=True)
     updated_on = models.DateTimeField(auto_now=True)
     created_by = models.BigIntegerField()
     brand = models.ForeignKey(BrandRegistration, on_delete=models.CASCADE,null=True,blank=True)
     admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True, blank=True)
     class Meta:
         db_table = "BrandCompanyDetails"

class BasicSellerOrDistributerDetails(models.Model):
    # Basic Seller Or Distributer Details model fields
    company_name = models.TextField(max_length=500)
    address = models.TextField(max_length=500)
    country = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    pincode = models.BigIntegerField()
    landmark = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    brand = models.ForeignKey(BrandRegistration, on_delete=models.CASCADE, null=True, blank=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "BasicSellerOrDistributerDetails"

class BrandCompanyCommunicationDetails(models.Model):
    # Brand Company Communication Details model fields
    contact_name = models.TextField(max_length=500)
    country = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    email = models.CharField(max_length=60)
    department = models.CharField(max_length=50, blank=True,null=True)
    telephone = models.IntegerField(blank=True,null=True)
    mobile_number= models.IntegerField(blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    brand_cmp_details = models.ForeignKey(BrandCompanyDetails, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey(BrandRegistration, on_delete=models.CASCADE, null=True, blank=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "BrandCompanyCommunicationDetails"


class SellerOrDistributerCommunicationDetails(models.Model):
    # Basic Seller Or Distributer Communication Details model fields
    contact_name = models.TextField(max_length=500)
    country = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    email = models.CharField(max_length=60)
    department = models.CharField(max_length=50, blank=True,null=True)
    telephone = models.IntegerField(blank=True,null=True)
    mobile_number = models.IntegerField(blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    seller_distributer_details = models.ForeignKey(BrandCompanyCommunicationDetails, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey(BrandRegistration, on_delete=models.CASCADE,null=True,blank=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "SellerOrDistributerCommunicationDetails"


class BrandLegalDocuments(models.Model):
    legal_docs=models.FileField(upload_to='BrandFiles')
    description=models.TextField(null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    brand = models.ForeignKey(BrandRegistration, on_delete=models.CASCADE, null=True, blank=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "BrandLegalDocuments"
