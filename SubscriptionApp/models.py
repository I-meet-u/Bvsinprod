from django.db import models
from simple_history.models import HistoricalRecords

from RegistrationApp.models import SelfRegistration

# Create your models here.

class RazorpayModel(models.Model):

    subscription_id=models.CharField(max_length=100,unique=True)
    plan_id=models.CharField(max_length=100,unique=True)
    payment_id=models.CharField(max_length=100,unique=True)
    period = models.CharField(max_length=100)
    interval = models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    email_id=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=20)
    status=models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by=models.ForeignKey(SelfRegistration,null=True,blank=True,on_delete=models.CASCADE)
    entity = models.CharField(max_length=100, null=True, blank=True)
    short_url = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table='RazorpayModel'
