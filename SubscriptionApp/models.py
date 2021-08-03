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
    email_id=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=20)
    updated_by = models.ForeignKey(SelfRegistration, null=True, blank=True, on_delete=models.CASCADE)
    history=HistoricalRecords()

    class Meta:
        db_table = 'PlanModel'


class CustomBooleanField(models.BooleanField):

    def from_db_value(self, value, expression, connection, context=None):
        if value is None:
            return value
        return int(value) # return 0/1

class SubscriptionModel(models.Model):
    subscription_id=models.CharField(max_length=100,unique=True)
    entity=models.CharField(max_length=100,null=True,blank=True)
    plan_id=models.CharField(max_length=100,unique=True)
    status = models.CharField(null=True, blank=True, max_length=100)
    current_start=models.BigIntegerField(null=True, blank=True)
    current_end=models.BigIntegerField(null=True, blank=True)
    ended_at=models.BigIntegerField(null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    notes = models.JSONField(null=True,blank=True)
    customer_id=models.CharField(max_length=100,unique=True,null=True,blank=True)
    charge_at=models.BigIntegerField(null=True, blank=True)
    start_at = models.BigIntegerField(null=True, blank=True)
    end_at = models.BigIntegerField(null=True, blank=True)
    auth_attempts=models.IntegerField(null=True, blank=True)
    total_count=models.IntegerField()
    paid_count=models.IntegerField(null=True, blank=True)
    customer_notify=CustomBooleanField(default=1,null=True,blank=True)
    created_at=models.BigIntegerField(null=True, blank=True)
    expire_by=models.BigIntegerField(null=True,blank=True)
    short_url=models.CharField(max_length=100,null=True,blank=True)
    has_scheduled_changes=models.BooleanField(null=True,blank=True)
    change_scheduled_at=models.CharField(max_length=100,default='now',null=True,blank=True)
    offer_id = models.CharField(max_length=100, unique=True,null=True,blank=True)
    remaining_count=models.IntegerField(null=True, blank=True)
    notify_email=models.CharField(max_length=100,null=True,blank=True)
    notify_phone= models.CharField(max_length=100, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.ForeignKey(SelfRegistration, null=True, blank=True, on_delete=models.CASCADE)


    class Meta:
        db_table = 'SubscriptionModel'


# class RazorpayModel(models.Model):
#
#     subscription_id=models.CharField(max_length=100,unique=True)
#     plan_id=models.CharField(max_length=100,unique=True)
#     payment_id=models.CharField(max_length=100,unique=True)
#     period = models.CharField(max_length=100)
#     interval = models.CharField(max_length=100)
#     name=models.CharField(max_length=100)
#     email_id=models.CharField(max_length=100)
#     phone_number=models.CharField(max_length=20)
#     status=models.CharField(max_length=100)
#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)
#     created_by = models.BigIntegerField(null=True, blank=True)
#     updated_by=models.ForeignKey(SelfRegistration,null=True,blank=True,on_delete=models.CASCADE)
#     entity = models.CharField(max_length=100, null=True, blank=True)
#     short_url = models.CharField(max_length=100, null=True, blank=True)
#
#     class Meta:
#         db_table='RazorpayModel'
