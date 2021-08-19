from django.db import models

# Create your models here.
from AdminApp.models import AdminRegister, CreateUser
from RegistrationApp.models import SelfRegistration
# from simple_history.models import HistoricalRecords


# -----------------------------------------INDUSTRY_TO_SERVE MASTER-------------------------------------------------------------

class IndustryToServeMaster(models.Model):
    # industry to serve masters model and fields
    industry_id = models.BigAutoField(primary_key=True)
    industry_name = models.CharField(max_length=200, unique=True)
    industry_code = models.CharField(max_length=200, unique=True,null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    admins = models.ForeignKey(AdminRegister,on_delete=models.CASCADE,null=True,blank=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE,null=True,blank=True)
    created_by = models.BigIntegerField(null=True)
    updated_by_name = models.CharField(null=True, blank=True,max_length=100)
    created_by_name=models.CharField(null=True,blank=True,max_length=100)
    status = models.CharField(max_length=100, default='Active')
    csv_industry=models.FileField(upload_to='MasterFile',null=True,blank=True)
    # history = HistoricalRecords()

    class Meta:
        db_table = "IndustryToServeMaster"


#-----------------------------------------NATURE_OF_BUSINESS MASTER-------------------------------------------------------------

class NatureOfBusinessMaster(models.Model):
    # nature of business master model and fields
    nature_of_business_id = models.BigAutoField(primary_key=True)
    nature_of_business_code=models.CharField(max_length=80,null=True,unique=True,blank=True)
    nature_of_business_name = models.CharField(max_length=200)
    nature_of_business_description = models.TextField(null=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100, default='Active')
    csv_nature = models.FileField(upload_to='MasterFile', null=True, blank=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)
    # history = HistoricalRecords()

    class Meta:
        db_table = "NatureOfBusinessMaster"


# -----------------------------------------SUPPLY CAPABILITIES MASTER-------------------------------------------------------------

class SupplyCapabilitiesMaster(models.Model):
    # supply capability master model and fields
    supply_capability_id = models.BigAutoField(primary_key=True)
    supply_capability_name = models.CharField(max_length=50,null=True,blank=True)
    supply_capability_code = models.CharField(max_length=50,unique=True,null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    csv_supply = models.FileField(upload_to='MasterFile', null=True, blank=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)
    # history = HistoricalRecords()

    class Meta:
        db_table = "SupplyCapabilitiesMaster"


# -----------------------------------------MAINCORE MASTER-------------------------------------------------------------

class MaincoreMaster(models.Model):
    # maincore master model and fields
    maincore_id = models.BigAutoField(primary_key=True)
    maincore_code=models.CharField(max_length=40,null=True,blank=True)
    maincore_name = models.CharField(max_length=50, unique=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    admin_order = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=30, default='Active',null=True)
    csv_maincore= models.FileField(upload_to='MasterFile', null=True, blank=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    uupdated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)
    # history = HistoricalRecords()

    class Meta:
        db_table = "MaincoreMaster"


# -----------------------------------------CATEGORY MASTER-------------------------------------------------------------
class CategoryMaster(models.Model):
    # category master model and fields
    category_id = models.BigAutoField(primary_key=True)
    category_code = models.CharField(max_length=40, null=True, blank=True)
    category_name = models.CharField(max_length=100, unique=True, blank=True)
    is_verified = models.BooleanField(default=False)
    maincore = models.ForeignKey(MaincoreMaster, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    admin_order = models.CharField(max_length=50, null=True)
    csv_category= models.FileField(upload_to='MasterFile', null=True, blank=True)
    status = models.CharField(max_length=30, default='Active', null=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)
    # history = HistoricalRecords()

    class Meta:
        db_table = "CategoryMaster"


# -----------------------------------------SUB-CATEGORY MASTER-------------------------------------------------------------
class SubCategoryMaster(models.Model):
    # sub-category master model and fields
    sub_category_id = models.BigAutoField(primary_key=True)
    sub_category_code = models.CharField(max_length=40, null=True, blank=True)
    sub_category_name = models.CharField(max_length=100, unique=True, blank=True)
    is_verified = models.BooleanField(default=False)
    category = models.ForeignKey(CategoryMaster, on_delete=models.CASCADE)
    maincore = models.ForeignKey(MaincoreMaster, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    admin_order = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=30, default='Active',null=True)
    csv_subcategory = models.FileField(upload_to='MasterFile', null=True, blank=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)
    # history = HistoricalRecords()

    class Meta:
        db_table = "SubCategoryMaster"


# -----------------------------------------PINCODE MASTER-------------------------------------------------------------
class PincodeMaster(models.Model):
    # pincode master model and fields
    pincode_id = models.BigAutoField(primary_key=True)
    pincode = models.BigIntegerField(unique=True)
    pincode_area = models.CharField(max_length=300, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)
    # history = HistoricalRecords()

    class Meta:
        db_table = "PincodeMaster"


class UOMMaster(models.Model):
    # uom master models and fields
    uom_id = models.BigAutoField(primary_key=True)
    uom_short_text = models.CharField(max_length=30,null=True,unique=True)
    uom_code = models.CharField(max_length=30, null=True,unique=True)
    uom_description = models.CharField(max_length=300)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)
    # history = HistoricalRecords()

    class Meta:
        db_table = "UOMMaster"


class DepartmentMaster(models.Model):
    # department master models and fields
    department_id = models.BigAutoField(primary_key=True)
    department_code = models.CharField(max_length=30, null=True, blank=True)
    department_short_text = models.CharField(max_length=30, unique=True)
    department_name = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)
    # history = HistoricalRecords()

    class Meta:
        db_table = "DepartmentMaster"


class DesignationMaster(models.Model):
    # designation master models and fields
    designation_id = models.BigAutoField(primary_key=True)
    designation_code = models.CharField(max_length=30, null=True, blank=True)
    designation_short_text = models.CharField(max_length=70, null=True, blank=True, unique=True)
    designation_name = models.CharField(max_length=200)
    designation_level = models.CharField(max_length=30,null=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)
    # history = HistoricalRecords()

    class Meta:
        db_table = "DesignationMaster"



class TaxMaster(models.Model):
    # tax_master models and fields
    tax_id = models.BigAutoField(primary_key=True)
    tax_code = models.CharField(max_length=30,null=True,blank=True,unique=True)
    tax_slab_name = models.CharField(max_length=200,null=True)
    CGST=models.CharField(max_length=80,null=True,blank=True)
    SGST = models.CharField(max_length=80, null=True, blank=True)
    IGST= models.CharField(max_length=80, null=True, blank=True)
    tax_percent = models.CharField(max_length=30,null=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)
    # history = HistoricalRecords()

    class Meta:
        db_table = "TaxMaster"


class HSNMaster(models.Model):
    # hsn_master models and fields
    hsn_id = models.BigAutoField(primary_key=True)
    hsn_code = models.CharField(max_length=30,unique=True)
    gst_rate_percentage = models.CharField(max_length=200)
    description_of_goods = models.TextField(null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)
    # history = HistoricalRecords()

    class Meta:
        db_table = "HSNMaster"


class SACMaster(models.Model):
    # sac_master models and fields
    sac_id = models.BigAutoField(primary_key=True)
    sac_code = models.CharField(max_length=30, null=True, blank=True,unique=True)
    gst_rate_percentage = models.CharField(max_length=200)
    description_of_goods = models.TextField(null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE,null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)
    # history = HistoricalRecords()

    class Meta:
        db_table = "SACMaster"


class CurrencyMaster(models.Model):
    # currency_master models and fields
    currency_id = models.BigAutoField(primary_key=True)
    currency_code = models.CharField(max_length=30,unique=True)
    currency = models.CharField(max_length=200, unique=True)
    currency_name = models.CharField(max_length=500, unique=True)
    currency_symbol= models.CharField(max_length=500,null=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)
    # history = HistoricalRecords()

    class Meta:
        db_table = "CurrencyMaster"

class PFChargesMaster(models.Model):
    # pf_charge models and fields
    pf_charge_id = models.BigAutoField(primary_key=True)
    pf_charge_code = models.CharField(max_length=30,unique=True,null=True,blank=True)
    pf_charge_description = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)
    # history = HistoricalRecords()

    class Meta:
        db_table = "PFChargesMaster"

class FrieghtChargesMaster(models.Model):
    # frieght_models and fields
    frieght_id = models.BigAutoField(primary_key=True)
    frieght_code = models.CharField(max_length=30,unique=True)
    frieght_description = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)
    # history = HistoricalRecords()

    class Meta:
        db_table = "FrieghtChargesMaster"

class WarrantyMaster(models.Model):
    # warranty_master models and fields
    warranty_id = models.BigAutoField(primary_key=True)
    warranty_code = models.CharField(max_length=30,unique=True)
    warranty_description = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)
    # history = HistoricalRecords()

    class Meta:
        db_table = "WarrantyMaster"

class GuaranteeMaster(models.Model):
    # guarantee_master models and fields
    guarantee_id = models.BigAutoField(primary_key=True)
    guarantee_code = models.CharField(max_length=30,unique=True)
    guarantee_description = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)
    # history = HistoricalRecords()

    class Meta:
        db_table = "GuaranteeMaster"

class DeliveryMaster(models.Model):
    # delivery_master models and fields
    delivery_id = models.BigAutoField(primary_key=True)
    delivery_code = models.CharField(max_length=30,unique=True)
    delivery_description = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)
    # history = HistoricalRecords()
    class Meta:
        db_table = "DeliveryMaster"

class CountryMaster(models.Model):
    # country_master models and fields
    country_id = models.BigAutoField(primary_key=True)
    country_code = models.CharField(max_length=30,null=True)
    country_name = models.CharField(max_length=200, unique=True,null=True,blank=True)
    country_prefix = models.CharField(max_length=200, unique=True,null=True,blank=True)
    country_flag=models.FileField(upload_to='CountryFlags',null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True,blank=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)
    # history = HistoricalRecords()

    class Meta:
        db_table = "CountryMaster"


class ItemGroupMaster(models.Model):
    # item_group_master models and fields
    item_group_id = models.BigAutoField(primary_key=True)
    item_group_code = models.CharField(max_length=30,unique=True,null=True,blank=True)
    item_groups = models.CharField(max_length=200,null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by_name=models.CharField(max_length=100,null=True,blank=True)
    updated_by_name = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True,blank=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    # history = HistoricalRecords()

    class Meta:
        db_table = "ItemGroupMaster"




class TransitInsuranceMaster(models.Model):
    # transit_insurance models and fields
    transit_id = models.BigAutoField(primary_key=True)
    transit_code = models.CharField(max_length=30,unique=True,null=True,blank=True)
    transit_name = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by_name=models.CharField(max_length=100,null=True,blank=True)
    updated_by_name = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True,blank=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    # history = HistoricalRecords()

    class Meta:
        db_table = "TransitInsuranceMaster"


class ValidityMaster(models.Model):
    # validity_master models and fields
    validity_id = models.BigAutoField(primary_key=True)
    validity_code = models.CharField(max_length=30,unique=True,null=True,blank=True)
    validity_name = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by_name=models.CharField(max_length=100,null=True,blank=True)
    updated_by_name = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True,blank=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    # history = HistoricalRecords()

    class Meta:
        db_table = "ValidityMaster"



class PaymentMaster(models.Model):
    # payment_master models and fields
    payment_id = models.BigAutoField(primary_key=True)
    payment_code = models.CharField(max_length=30,unique=True,null=True,blank=True)
    payment_terms = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by_name=models.CharField(max_length=100,null=True,blank=True)
    updated_by_name = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True,blank=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    # history = HistoricalRecords()

    class Meta:
        db_table = "PaymentMaster"


class RfqCategoryMaster(models.Model):
    # rfq category master model and fields
    rfq_category_id = models.BigAutoField(primary_key=True)
    rfq_category_code = models.CharField(max_length=40,unique=True,null=True,blank=True)
    rfq_category_name = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    admin_order = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=30, default='Active', null=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)

    class Meta:
        db_table = "RfqCategoryMaster"


class PriceBasisMaster(models.Model):
    # price basis master model and fields
    price_basis_id = models.BigAutoField(primary_key=True)
    price_basis_code = models.CharField(max_length=40, unique=True,null=True,blank=True)
    price_basis_name = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    admin_order = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=30, default='Active', null=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)

    class Meta:
        db_table = "PriceBasisMaster"


class InspectionMaster(models.Model):
    # inspection master model and fields
    inspection_id = models.BigAutoField(primary_key=True)
    inspection_code = models.CharField(max_length=40,unique=True,null=True,blank=True)
    inspection_name = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    admin_order = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=30, default='Active', null=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)

    class Meta:
        db_table = "InspectionMaster"


class LiquidatedDamageMaster(models.Model):
    #  liquidated master model and fields
    liquidated_id = models.BigAutoField(primary_key=True)
    liquidated_code = models.CharField(max_length=40, null=True, blank=True,unique=True)
    liquidated_name = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    admin_order = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=30, default='Active', null=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)

    class Meta:
        db_table = "LiquidatedDamageMaster"



class TaxesAndDutiesMaster(models.Model):
    #  taxes and duties master model and fields
    tax_duties_id = models.BigAutoField(primary_key=True)
    tax_duties_code = models.CharField(max_length=40,unique=True,null=True, blank=True)
    tax_duties_name = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    admin_order = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=30, default='Active', null=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)

    class Meta:
        db_table = "TaxesAndDutiesMaster"



class TestAndQapMaster(models.Model):
    #  test and qap master model and fields
    test_qap_id = models.BigAutoField(primary_key=True)
    test_qap_code = models.CharField(max_length=40, unique=True,null=True, blank=True)
    test_qap_name = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    admin_order = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=30, default='Active', null=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)

    class Meta:
        db_table = "TestAndQapMaster"


class PerformanceGuaranteesMaster(models.Model):
    #  peroformance guarantee master model and fields
    performance_id = models.BigAutoField(primary_key=True)
    performance_code = models.CharField(max_length=40, unique=True, null=True, blank=True)
    performance_name = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    admin_order = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=30, default='Active', null=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)

    class Meta:
        db_table = "PerformanceGuaranteesMaster"

class DivisionMaster(models.Model):
    #  division master model and fields
    division_id = models.BigAutoField(primary_key=True)
    division_code = models.CharField(max_length=40, unique=True,null=True, blank=True)
    division_name = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    admin_order = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=30, default='Active', null=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by_name = models.CharField(null=True, blank=True, max_length=100)
    created_by_name = models.CharField(null=True, blank=True, max_length=100)

    class Meta:
        db_table = "DivisionMaster"