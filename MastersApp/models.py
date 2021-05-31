from django.db import models

# Create your models here.
from AdminApp.models import AdminRegister
from RegistrationApp.models import SelfRegistration
from simple_history.models import HistoricalRecords


# -----------------------------------------INDUSTRY_TO_SERVE MASTER-------------------------------------------------------------

class IndustryToServeMaster(models.Model):
    # industry to serve masters model and fields
    industry_id = models.BigAutoField(primary_key=True)
    industry_name = models.CharField(max_length=50, unique=True)
    industry_code = models.CharField(max_length=50, unique=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default='Active')
    history = HistoricalRecords()

    class Meta:
        db_table = "IndustryToServeMaster"


#-----------------------------------------NATURE_OF_BUSINESS MASTER-------------------------------------------------------------

class NatureOfBusinessMaster(models.Model):
    # nature of business master model and fields
    nature_of_business_id = models.BigAutoField(primary_key=True)
    nature_of_business_name = models.CharField(max_length=50, unique=True)
    nature_of_business_description = models.TextField(unique=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        db_table = "NatureOfBusinessMaster"


# -----------------------------------------SUPPLY CAPABILITIES MASTER-------------------------------------------------------------

class SupplyCapabilitiesMaster(models.Model):
    # supply capability master model and fields
    supply_capability_id = models.BigAutoField(primary_key=True)
    supply_capability_name = models.CharField(max_length=50, unique=True)
    supply_capability_code = models.CharField(max_length=50, unique=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        db_table = "SupplyCapabilitiesMaster"


# -----------------------------------------MAINCORE MASTER-------------------------------------------------------------

class MaincoreMaster(models.Model):
    # maincore master model and fields
    maincore_id = models.BigAutoField(primary_key=True)
    maincore_name = models.CharField(max_length=50, unique=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    admin_order = models.CharField(max_length=50, null=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE)

    class Meta:
        db_table = "MaincoreMaster"


# -----------------------------------------CATEGORY MASTER-------------------------------------------------------------
class CategoryMaster(models.Model):
    # category master model and fields
    category_id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=100, unique=True, blank=True)
    is_verified = models.BooleanField(default=False)
    maincore = models.ForeignKey(MaincoreMaster, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    admin_order = models.CharField(max_length=50, null=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        db_table = "CategoryMaster"


# -----------------------------------------SUB-CATEGORY MASTER-------------------------------------------------------------
class SubCategoryMaster(models.Model):
    # sub-category master model and fields
    sub_category_id = models.BigAutoField(primary_key=True)
    sub_category_name = models.CharField(max_length=100, unique=True, blank=True)
    is_verified = models.BooleanField(default=False)
    category = models.ForeignKey(CategoryMaster, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    admin_order = models.CharField(max_length=50, null=True)
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE)
    history = HistoricalRecords()

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
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        db_table = "PincodeMaster"


class UOMMaster(models.Model):
    # uom master models and fields
    uom_id = models.BigAutoField(primary_key=True)
    uom_code = models.CharField(max_length=30)
    uom_description = models.CharField(max_length=300, unique=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        db_table = "UOMMaster"


class DepartmentMaster(models.Model):
    # department master models and fields
    department_id = models.BigAutoField(primary_key=True)
    department_code = models.CharField(max_length=30, null=True, blank=True)
    department_short_text = models.CharField(max_length=30, unique=True)
    department_name = models.CharField(max_length=200, unique=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        db_table = "DepartmentMaster"


class DesignationMaster(models.Model):
    # designation master models and fields
    designation_id = models.BigAutoField(primary_key=True)
    designation_code = models.CharField(max_length=30, null=True, blank=True)
    designation_name = models.CharField(max_length=200, unique=True)
    designation_level = models.CharField(max_length=30, unique=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        db_table = "DesignationMaster"



class TaxMaster(models.Model):
    # tax_master models and fields
    tax_id = models.BigAutoField(primary_key=True)
    tax_group = models.CharField(max_length=30,null=True,blank=True)
    tax_slab_name = models.CharField(max_length=200,null=True)
    tax_percent = models.CharField(max_length=30,null=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        db_table = "TaxMaster"


class HSNMaster(models.Model):
    # hsn_master models and fields
    hsn_id = models.BigAutoField(primary_key=True)
    hsn_code = models.CharField(max_length=30, null=True, blank=True)
    gst_rate_percentage = models.CharField(max_length=200)
    description_of_goods = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        db_table = "HSNMaster"


class SACMaster(models.Model):
    # sac_master models and fields
    sac_id = models.BigAutoField(primary_key=True)
    sac_code = models.CharField(max_length=30, null=True, blank=True)
    gst_rate_percentage = models.CharField(max_length=200)
    description_of_goods = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        db_table = "SACMaster"


class CurrencyMaster(models.Model):
    # currency_master models and fields
    currency_id = models.BigAutoField(primary_key=True)
    currency_code = models.CharField(max_length=30,unique=True)
    currency = models.CharField(max_length=200, unique=True)
    currency_name = models.CharField(max_length=500, unique=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        db_table = "CurrencyMaster"

class PFChargesMaster(models.Model):
    # pf_charge models and fields
    currency_id = models.BigAutoField(primary_key=True)
    currency_code = models.CharField(max_length=30,unique=True)
    currency = models.CharField(max_length=200, unique=True)
    currency_name = models.CharField(max_length=30, unique=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    admins = models.ForeignKey(AdminRegister, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        db_table = "PFChargesMaster"

