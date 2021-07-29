from django.db import models
from simple_history.models import HistoricalRecords

from RegistrationApp.models import SelfRegistration

# Create your models here.
class PlanModel(models.Model):
    plan_id=models.CharField(max_length=100,unique=True)
    entity=models.CharField(max_length=50,null=True,blank=True)
    period = models.CharField(max_length=100)
    interval=models.CharField(max_length=100)
    item=models.JSONField(null=True,blank=True,default=list)
    item_id=models.CharField(max_length=100,unique=True)
    item_name=models.CharField(max_length=100)
    item_description=models.CharField(max_length=200,null=True,blank=True)
    amount=models.BigIntegerField()
    currency=models.CharField(max_length=100)
    type=models.CharField(max_length=100,null=True,blank=True)
    item_created_at=models.IntegerField(null=True,blank=True)
    item_updated_at=models.IntegerField(null=True,blank=True)
    plan_created_at=models.IntegerField(null=True,blank=True)
    notes = models.JSONField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by=models.ForeignKey(SelfRegistration,on_delete=models.CASCADE)
    email_id=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=20)
    history=HistoricalRecords()

    class Meta:
        db_table = 'PlanModel'
