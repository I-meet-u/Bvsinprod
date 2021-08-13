from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.

from django.db import models
from simple_history.models import HistoricalRecords

from RegistrationApp.models import SelfRegistration, BasicCompanyDetails


class VendorProduct_BasicDetails(models.Model):
    vendor_product_id=models.BigAutoField(primary_key=True)
    core_sector=models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    sub_category = models.CharField(max_length=100, blank=True)
    item_type = models.CharField(max_length=100, null=True)
    item_group = models.CharField(max_length=100, null=True)
    item_code = models.CharField(max_length=100, null=True, unique=True)
    item_code_manual=models.CharField(max_length=100,null=True,blank=True)
    product_category=models.CharField(max_length=100, null=True,blank=True)
    final_selling_price = models.CharField(max_length=80, null=True,blank=True)
    item_name = models.CharField(max_length=100, null=True,blank=True)
    add_image1 = models.FileField(upload_to='vendorproductimage', null=True, blank=True)
    add_image2 = models.FileField(upload_to='vendorproductimage', null=True, blank=True)
    add_image3 = models.FileField(upload_to='vendorproductimage', null=True, blank=True)
    add_image4 = models.FileField(upload_to='vendorproductimage', null=True, blank=True)
    item_description=models.TextField(null=True,blank=True)
    unit_price = models.CharField(max_length=100, null=True, blank=True)
    discount = models.CharField(max_length=50, null=True, blank=True)
    brand_make = models.CharField(max_length=150, null=True, blank=True)
    pricing = models.CharField(max_length=300, null=True, blank=True)
    uom=models.CharField(max_length=100, null=True,blank=True)
    country_of_origin = models.CharField(max_length=50, blank=True)
    request_on_quote = models.CharField(max_length=400, null=True, blank=True)
    tax = models.CharField(max_length=100, null=True, blank=True)
    hsn_sac = models.CharField(max_length=100, null=True, blank=True)
    currency = models.CharField(max_length=50, blank=True,null=True)
    status = models.CharField(max_length=200, null=True, blank=True,default='Pending')
    price_range_from = models.CharField(max_length=200, null=True, blank=True)
    price_range_to = models.CharField(max_length=200, null=True, blank=True)
    quantity=models.CharField(max_length=100,null=True, blank=True)
    sku_id=models.CharField(max_length=100, blank=True)
    numeric = models.BigIntegerField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    company_code=models.CharField(max_length=100,null=True,blank=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        db_table = "VendorProduct_BasicDetails"

class VendorProduct_GeneralDetails(models.Model):

    p_f_charges=models.CharField(max_length=400,null=True,blank=True)
    frieght_charges=models.CharField(max_length=400,null=True,blank=True)
    delivery = models.CharField(max_length=400, null=True, blank=True)
    warranty=models.CharField(max_length=400, blank=True)
    insurance = models.CharField(max_length=400, blank=True)
    department = models.CharField(max_length=400, blank=True)
    guarantee=models.CharField(max_length=400, blank=True)
    not_covered_w_g = models.CharField(max_length=400, blank=True)
    # min_order_quantity = models.CharField(max_length=400, blank=True)
    after_sale_service=models.CharField(max_length=400, blank=True)
    available_stock = models.CharField(max_length=100, blank=True)
    packing_type = models.CharField(max_length=400, blank=True)
    # standard_measures = models.CharField(max_length=100, blank=True)
    # product_length = models.CharField(max_length=100, blank=True)
    # shipping_uom = models.CharField(max_length=100, blank=True)
    # item_weight = models.CharField(max_length=100, blank=True)
    # product_width = models.CharField(max_length=100, blank=True)
    # shipping_weight = models.CharField(max_length=100, blank=True)
    # packed_weight = models.CharField(max_length=100, blank=True)
    # product_height = models.CharField(max_length=100, blank=True)
    # ship_via = models.CharField(max_length=100, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    vendor_products=models.ForeignKey(VendorProduct_BasicDetails,on_delete=models.CASCADE,null=True,blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table="VendorProduct_GeneralDetails"

class VendorProduct_TechnicalSpecifications(models.Model):

    item_specification = models.CharField(max_length=100, blank=True)
    item_description = models.TextField(null=True,blank=True)
    # description = models.TextField(null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    vendor_products=models.ForeignKey(VendorProduct_BasicDetails,on_delete=models.CASCADE,null=True,blank=True)
    history = HistoricalRecords()


    class Meta:
        db_table="VendorProduct_TechnicalSpecifications"

class VendorProduct_ProductFeatures(models.Model):
    product_item_specification = models.CharField(max_length=100, blank=True)
    product_item_description = models.TextField(null=True, blank=True)
    # description = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    vendor_products=models.ForeignKey(VendorProduct_BasicDetails,on_delete=models.CASCADE,null=True,blank=True)
    history = HistoricalRecords()


    class Meta:
        db_table="VendorProduct_ProductFeatures"


class VendorProduct_Documents(models.Model):
    document1=models.FileField(upload_to='vendorproductimage',null=True,blank=True)
    document_description1=models.TextField(null=True,blank=True)
    document2 = models.FileField(upload_to='vendorproductimage', null=True, blank=True)
    document_description2 = models.TextField(null=True, blank=True)
    document3 = models.FileField(upload_to='vendorproductimage', null=True, blank=True)
    document_description3 = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    vendor_products=models.ForeignKey(VendorProduct_BasicDetails,on_delete=models.CASCADE,null=True,blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table="VendorProduct_Documents"

class BuyerProductDetails(models.Model):
    buyer_product_id = models.BigAutoField(primary_key=True)
    buyer_item_type = models.CharField(max_length=100, null=True)
    buyer_item_code = models.CharField(max_length=100, null=True, unique=True)
    buyer_item_name = models.CharField(max_length=100, null=True)
    buyer_item_description = models.TextField(null=True)
    buyer_numeric = models.CharField(max_length=50,null=True,blank=True)
    buyer_uom = models.CharField(max_length=100, blank=True)
    buyer_hsn_sac = models.CharField(max_length=100, blank=True,null=True)
    buyer_unit_price = models.CharField(max_length=100, blank=True,null=True)
    buyer_prefix = models.CharField(max_length=50,null=True, blank=True)
    buyer_suffix = models.CharField(max_length=50,null=True, blank=True)
    # buyer_country_of_origin = models.CharField(max_length=50, blank=True)
    buyer_category=models.CharField(max_length=500,null=True,blank=True)
    buyer_department=models.CharField(max_length=400,null=True,blank=True)
    buyer_item_group = models.CharField(max_length=500, blank=True,null=True)
    buyer_annual_consumption = models.CharField(max_length=500, null=True,blank=True)
    buyer_safety_stock = models.CharField(max_length=100, blank=True,null=True)
    buyer_model_no = models.CharField(max_length=500, blank=True,null=True)
    buyer_document=models.FileField(upload_to='BuyerProductFiles',null=True,blank=True)
    buyer_additional_specifications=models.TextField(null=True,blank=True)
    buyer_add_product_supplies=models.CharField(max_length=200,null=True,blank=True)
    buyer_product_status=models.CharField(max_length=50,default='Active')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        db_table = "BuyerProductDetails"


class BuyerServiceDetails(models.Model):
    buyer_service_id = models.BigAutoField(primary_key=True)
    buyer_service_item_type = models.CharField(max_length=100, null=True)
    buyer_service_item_code = models.CharField(max_length=100, null=True, unique=True)
    buyer_service_item_name = models.CharField(max_length=100, null=True)
    buyer_service_item_description = models.TextField(null=True)
    buyer_service_numeric = models.CharField(max_length=50,null=True,blank=True)
    buyer_service_uom = models.CharField(max_length=100, blank=True,null=True)
    buyer_service_hsn_sac = models.CharField(max_length=100, blank=True,null=True)
    buyer_service_unit_price = models.CharField(max_length=100, blank=True,null=True)
    buyer_service_prefix = models.CharField(max_length=50,null=True,blank=True)
    buyer_service_suffix = models.CharField(max_length=50,null=True,blank=True)
    # buyer_country_of_origin = models.CharField(max_length=50, blank=True)
    buyer_service_category=models.CharField(max_length=500,null=True,blank=True)
    buyer_service_department=models.CharField(max_length=400,null=True,blank=True)
    buyer_service_item_group = models.CharField(max_length=500, blank=True,null=True)
    buyer_service_annual_consumption = models.CharField(max_length=500,blank=True,null=True)
    buyer_service_safety_stock = models.CharField(max_length=100, blank=True,null=True)
    buyer_service_model_no = models.CharField(max_length=500,blank=True,null=True)
    buyer_service_document=models.FileField(upload_to='BuyerServiceFiles',null=True,blank=True)
    buyer_service_additional_specifications=models.TextField(null=True,blank=True)
    buyer_service_add_product_supplies=models.CharField(max_length=200,null=True,blank=True)
    buyer_service_status=models.CharField(max_length=50,default='Active')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        db_table = "BuyerServiceDetails"


class BuyerMachinaryDetails(models.Model):
    buyer_machinary_id = models.BigAutoField(primary_key=True)
    buyer_machinary_item_type = models.CharField(max_length=100,null=True)
    buyer_machinary_item_code = models.CharField(max_length=100,null=True, unique=True)
    buyer_machinary_item_name = models.CharField(max_length=100,null=True)
    buyer_machinary_item_description = models.TextField(null=True)
    buyer_machinary_numeric = models.CharField(max_length=50,null=True,blank=True)
    buyer_machinary_uom = models.CharField(max_length=100, blank=True,null=True)
    buyer_machinary_hsn_sac = models.CharField(max_length=100, blank=True,null=True)
    buyer_machinary_unit_price = models.CharField(max_length=100, blank=True,null=True)
    buyer_machinary_prefix = models.CharField(max_length=50,null=True, blank=True)
    buyer_machinary_suffix = models.CharField(max_length=50,null=True, blank=True)
    # buyer_country_of_origin = models.CharField(max_length=50, blank=True)
    buyer_machinary_category=models.CharField(max_length=500,null=True,blank=True)
    buyer_machinary_department=models.CharField(max_length=400,null=True,blank=True)
    buyer_machinary_item_group = models.CharField(max_length=500, blank=True,null=True)
    buyer_machinary_annual_consumption = models.CharField(max_length=500, blank=True,null=True)
    buyer_machinary_safety_stock = models.CharField(max_length=100,blank=True,null=True)
    buyer_machinary_model_no = models.CharField(max_length=500, blank=True,null=True)
    buyer_machinary_document=models.FileField(upload_to='BuyerMachinaryFiles',null=True,blank=True)
    buyer_machinary_additional_specifications=models.TextField(null=True,blank=True)
    buyer_machinary_add_product_supplies=models.CharField(max_length=200,null=True,blank=True)
    buyer_machinary_product_status=models.CharField(max_length=50,default='Active')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration,on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        db_table = "BuyerMachinaryDetails"



class ItemCodeSettings(models.Model):
    item_type=models.CharField(max_length=200)
    prefix=models.CharField(max_length=70,null=True,blank=True)
    numeric=models.CharField(max_length=30)
    suffix=models.CharField(max_length=70,null=True,blank=True)
    code_format=models.CharField(max_length=120,null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)

    class Meta:
        db_table = "ItemCodeSettings"
