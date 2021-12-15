from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.

from RegistrationApp.models import SelfRegistration, BasicCompanyDetails


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
    type_user=models.CharField(max_length=80,null=True,blank=True)
    created_by = models.BigIntegerField()
    updated_by_invites = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        db_table="InviteVendor"


class BusinessRequest(models.Model):
    company_code=models.CharField(max_length=50)
    company_name=models.CharField(max_length=200)
    gst_number=models.CharField(max_length=70,null=True,blank=True)
    city=models.CharField(max_length=100,null=True,blank=True)
    state=models.CharField(max_length=200,null=True,blank=True)
    email_id=models.CharField(max_length=100,null=True,blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    nature_of_business=ArrayField(models.CharField(max_length=200),null=True,blank=True)
    supply_capabilites =ArrayField(models.CharField(max_length=500),null=True,blank=True)
    industry_to_serve =ArrayField(models.CharField(max_length=500),null=True,blank=True)
    maincore=ArrayField(models.CharField(max_length=500),null=True,blank=True)
    category = ArrayField(models.CharField(max_length=500),null=True,blank=True)
    sub_category = ArrayField(models.CharField(max_length=500),null=True,blank=True)
    send_status=models.CharField(max_length=200,default='Pending')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table="BusinessRequest"



class InternalVendor(models.Model):
    internal_vendor_id=models.BigAutoField(primary_key=True)
    company_code=models.CharField(max_length=50)
    company_name=models.CharField(max_length=500)
    city=models.CharField(max_length=500,null=True,blank=True)
    state=models.CharField(max_length=500,null=True,blank=True)
    nature_of_business=ArrayField(models.CharField(max_length=500),null=True,blank=True)
    email_id=models.CharField(max_length=500)
    phone_number=models.CharField(max_length=20)
    maincore=ArrayField(models.CharField(max_length=500),null=True,blank=True)
    category = ArrayField(models.CharField(max_length=500),null=True,blank=True)
    sub_category = ArrayField(models.CharField(max_length=500),null=True,blank=True)
    groups=models.CharField(max_length=500,null=True,blank=True)
    registration_status=models.CharField(max_length=500,default='Not Registered')
    approval_status=models.CharField(max_length=500,default='Pending')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table="InternalVendor"


class InternalBuyer(models.Model):
    internal_buyer_id=models.BigAutoField(primary_key=True)
    company_code=models.CharField(max_length=50)
    company_name=models.CharField(max_length=200)
    city=models.CharField(max_length=100,null=True,blank=True)
    state=models.CharField(max_length=200,null=True,blank=True)
    nature_of_business=ArrayField(models.CharField(max_length=500),null=True,blank=True)
    industry_to_serve = ArrayField(models.CharField(max_length=500), null=True, blank=True)
    email_id = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=20)
    # maincore = ArrayField(models.CharField(max_length=500), null=True, blank=True)
    # category = ArrayField(models.CharField(max_length=500), null=True, blank=True)
    # sub_category = ArrayField(models.CharField(max_length=500), null=True, blank=True)
    groups=models.CharField(max_length=200,null=True,blank=True)
    registration_status=models.CharField(max_length=200,default='Not Registered')
    approval_status=models.CharField(max_length=500,default='Pending')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table="InternalBuyer"

class TrailVendors(models.Model):
    company_code = models.ForeignKey(BasicCompanyDetails,on_delete=models.CASCADE,null=True,blank=True)
    status = models.CharField(max_length=80, default= 'Pending')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "TrailVendors"


class QuoteModel(models.Model):
    post_requirements=models.CharField(max_length=1000)
    messages=models.TextField(null=True,blank=True)
    quantity=models.CharField(max_length=50)
    uom=models.CharField(max_length=100)
    budget=models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    company_code=models.ForeignKey(BasicCompanyDetails,on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        db_table = "QuoteModel"


