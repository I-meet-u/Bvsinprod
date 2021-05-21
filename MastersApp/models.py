from django.db import models


# Create your models here.
from RegistrationApp.models import SelfRegistration
from simple_history.models import HistoricalRecords
#-----------------------------------------INDUSTRY_TO_SERVE MASTER-------------------------------------------------------------

class IndustryToServeMaster(models.Model):
    industry_id = models.BigAutoField(primary_key=True)
    industry_name = models.CharField(max_length=50, unique=True)
    industry_code= models.CharField(max_length=50, unique=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=30,default='Active')
    # created_by_name = models.CharField(max_length=100, blank=True, null=True)
    # updated_by_name = models.CharField(max_length=100, blank=True, null=True)
    # created_by = models.BigIntegerField()
    # updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        db_table = "IndustryToServeMaster"

#-----------------------------------------NATURE_OF_BUSINESS MASTER-------------------------------------------------------------

class NatureOfBusinessMaster(models.Model):
    nature_of_business_id = models.BigAutoField(primary_key=True)
    nature_of_business_name = models.CharField(max_length=50, unique=True)
    nature_of_business_description=models.TextField(unique=True,null=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    # created_by_name = models.CharField(max_length=100, blank=True, null=True)
    # updated_by_name = models.CharField(max_length=100, blank=True, null=True)
    # created_by = models.BigIntegerField()
    # updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        db_table = "NatureOfBusinessMaster"

#-----------------------------------------SUPPLY CAPABILITIES MASTER-------------------------------------------------------------

class SupplyCapabilitiesMaster(models.Model):
    supply_capability_id = models.BigAutoField(primary_key=True)
    supply_capability_name = models.CharField(max_length=50, unique=True)
    supply_capability_code = models.CharField(max_length=50, unique=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    # created_by_name = models.CharField(max_length=100, blank=True, null=True)
    # updated_by_name = models.CharField(max_length=100, blank=True, null=True)
    # created_by = models.BigIntegerField()
    # updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        db_table = "SupplyCapabilitiesMaster"


#-----------------------------------------MAINCORE MASTER-------------------------------------------------------------

class MaincoreMaster(models.Model):
    maincore_id = models.BigAutoField(primary_key=True)
    maincore_name = models.CharField(max_length=50,unique=True,blank=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # created_by_name = models.CharField(max_length=100, blank=True, null=True)
    # updated_by_name = models.CharField(max_length=100, blank=True, null=True)
    # created_by = models.BigIntegerField()
    # updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    history = HistoricalRecords()
    class Meta:
        db_table = "MaincoreMaster"


#-----------------------------------------CATEGORY MASTER-------------------------------------------------------------
class CategoryMaster(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    category_name =models.CharField(max_length=100,unique=True,blank=True)
    is_verified = models.BooleanField(default=False)
    maincore = models.ForeignKey(MaincoreMaster, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # created_by_name = models.CharField(max_length=100, blank=True, null=True)
    # updated_by_name = models.CharField(max_length=100, blank=True, null=True)
    # created_by = models.BigIntegerField()
    # updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        db_table = "CategoryMaster"


#-----------------------------------------SUB-CATEGORY MASTER-------------------------------------------------------------
class SubCategoryMaster(models.Model):
    sub_category_id = models.BigAutoField(primary_key=True)
    sub_category_name =models.CharField(max_length=100,unique=True,blank=True)
    is_verified = models.BooleanField(default=False)
    category = models.ForeignKey(CategoryMaster, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # created_by_name = models.CharField(max_length=100, blank=True, null=True)
    # updated_by_name = models.CharField(max_length=100, blank=True, null=True)
    # created_by = models.BigIntegerField()
    # updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        db_table = "SubCategoryMaster"



#-----------------------------------------PINCODE MASTER-------------------------------------------------------------
class PincodeMaster(models.Model):
    pincode_id = models.BigAutoField(primary_key=True)
    pincode = models.BigIntegerField(unique=True)
    pincode_area = models.CharField(max_length=300,blank=True,null=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Active')
    # created_by_name = models.CharField(max_length=100, blank=True, null=True)
    # updated_by_name = models.CharField(max_length=100, blank=True, null=True)
    # created_by = models.BigIntegerField()
    # updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        db_table = "PincodeMaster"