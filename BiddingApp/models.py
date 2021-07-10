from django.db import models

# Create your models here.
from RegistrationApp.models import SelfRegistration


class BuyerProductBidding(models.Model):
    product_bidding_id=models.BigAutoField(primary_key=True)
    product_rfq_number=models.CharField(max_length=40,unique=True)
    product_rfq_type=models.CharField(max_length=400)
    product_rfq_status=models.CharField(max_length=50,default='Pending')
    product_publish_date=models.CharField(max_length=100)
    product_deadline_date=models.CharField(max_length=100)
    product_delivery_date = models.CharField(max_length=100)
    product_rfq_currency = models.CharField(max_length=100,null=True,blank=True)
    product_rfq_category = models.CharField(max_length=100, null=True, blank=True)
    product_department=models.CharField(max_length=300)
    product_bill_address=models.TextField()
    product_ship_address=models.TextField()
    product_rfq_title = models.CharField(max_length=600)
    bidding_numeric=models.CharField(max_length=30)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)

    class Meta:
        db_table='BuyerProductBidding'



class BiddingBuyerProductDetails(models.Model):
    buyer_item_code= models.CharField(max_length=100,unique=True)
    buyer_item_name = models.CharField(max_length=100)
    buyer_item_description = models.TextField(null=True,blank=True)
    buyer_uom = models.CharField(max_length=100, null=True,blank=True)
    buyer_category = models.CharField(max_length=500,null=True)
    buyer_quantity = models.CharField(max_length=100)
    buyer_document=models.FileField(upload_to='BuyerProductFiles',null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    buyer_rfq_number=models.CharField(max_length=100)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    product_biddings = models.ForeignKey(BuyerProductBidding, on_delete=models.CASCADE)

    class Meta:
        db_table='BiddingBuyerProductDetails'


class RfqCodeSettings(models.Model):
    rfq_number=models.CharField(max_length=200)
    prefix=models.CharField(max_length=70,null=True,blank=True)
    numeric=models.CharField(max_length=30)
    suffix=models.CharField(max_length=70,null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)

    class Meta:
        db_table = "RfqCodeSettings"
