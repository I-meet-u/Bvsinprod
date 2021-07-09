from django.db import models

# Create your models here.
from simple_history.models import HistoricalRecords

from RegistrationApp.models import SelfRegistration


class InviteVendor(models.Model):
    invite_id=models.BigAutoField(primary_key=True)
    company_name=models.CharField(max_length=200,null=True,blank=True)
    contact_name=models.CharField(max_length=100,null=True,blank=True)
    email_id=models.CharField(max_length=200)
    phone_number=models.CharField(max_length=20)
    registration_status=models.CharField(max_length=200,default='Not Registered')
    approval_status=models.CharField(max_length=500,default='Pending')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by_invites = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE,null=True,blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table="InviteVendor"


class BusinessRequest(models.Model):
    company_code=models.CharField(max_length=50)
    company_name=models.CharField(max_length=200)
    city=models.CharField(max_length=100,null=True,blank=True)
    state=models.CharField(max_length=200,null=True,blank=True)
    nature_of_business=models.CharField(max_length=500,null=True,blank=True)
    supply_capabilites = models.CharField(max_length=500,null=True,blank=True)
    industry_to_serve =models.CharField(max_length=500,null=True,blank=True)
    maincore=models.CharField(max_length=200,null=True,blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    sub_category = models.CharField(max_length=200, null=True, blank=True)
    send_status=models.CharField(max_length=200,default='Pending')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table="BusinessRequest"


class InternalVendor(models.Model):
    internal_vendor_id=models.BigAutoField(primary_key=True)
    company_code=models.CharField(max_length=50)
    company_name=models.CharField(max_length=200)
    city=models.CharField(max_length=100,null=True,blank=True)
    state=models.CharField(max_length=200,null=True,blank=True)
    nature_of_business=models.CharField(max_length=200,null=True,blank=True)
    email_id=models.CharField(max_length=200)
    phone_number=models.CharField(max_length=20)
    maincore=models.CharField(max_length=200,null=True,blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    sub_category = models.CharField(max_length=200, null=True, blank=True)
    groups=models.CharField(max_length=200,null=True,blank=True)
    registration_status=models.CharField(max_length=200,default='Not Registered')
    approval_status=models.CharField(max_length=500,default='Pending')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table="InternalVendor"


class InternalBuyer(models.Model):
    internal_buyer_id=models.BigAutoField(primary_key=True)
    company_code=models.CharField(max_length=50)
    company_name=models.CharField(max_length=200)
    city=models.CharField(max_length=100,null=True,blank=True)
    state=models.CharField(max_length=200,null=True,blank=True)
    nature_of_business=models.CharField(max_length=200,null=True,blank=True)
    email_id=models.CharField(max_length=200)
    phone_number=models.CharField(max_length=20)
    maincore=models.CharField(max_length=200,null=True,blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    sub_category = models.CharField(max_length=200, null=True, blank=True)
    groups=models.CharField(max_length=200,null=True,blank=True)
    registration_status=models.CharField(max_length=200,default='Not Registered')
    approval_status=models.CharField(max_length=500,default='Pending')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table="InternalBuyer"