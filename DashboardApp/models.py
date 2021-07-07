from django.db import models

# Create your models here.
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

    class Meta:
        db_table="InviteVendor"


# class InternalVendor(models.Model):
#     company_code=models.CharField(max_length=50)
#     company_name=models.CharField(max_length=200)
#     contact_name=models.CharField(max_length=100,null=True,blank=True)
#     email_id=models.CharField(max_length=200)
#     phone_number=models.CharField(max_length=20)
#     registration_status=models.CharField(max_length=200,default='Not Registered')
#     approval_status=models.CharField(max_length=500,default='Pending')
#
#     class Meta:
#         db_table="InternalVendor"
