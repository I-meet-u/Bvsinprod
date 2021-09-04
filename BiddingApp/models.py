from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
from simple_history.models import HistoricalRecords

from RegistrationApp.models import SelfRegistration


class BuyerProductBidding(models.Model):
    product_bidding_id=models.BigAutoField(primary_key=True)
    product_rfq_number=models.CharField(max_length=40,unique=True,null=True,blank=True)
    user_rfq_number=models.CharField(max_length=50,null=True,blank=True)
    user_bidding_numeric = models.CharField(max_length=30,null=True)
    user_prefix=models.CharField(max_length=50,null=True,blank=True)
    product_rfq_type=models.CharField(max_length=400)
    product_rfq_status=models.CharField(max_length=50,default='Pending')
    product_publish_date=models.CharField(max_length=100)
    product_deadline_date=models.DateField(max_length=100,null=True,blank=True)
    product_delivery_date = models.CharField(max_length=100)
    product_rfq_currency = models.CharField(max_length=100,null=True,blank=True)
    product_rfq_category = models.CharField(max_length=100, null=True, blank=True)
    product_department=models.CharField(max_length=300)
    product_bill_address=models.TextField()
    product_ship_address=models.TextField()
    product_rfq_title = models.CharField(max_length=600)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    from_registration=models.CharField(max_length=100,null=True,blank=True,default='False')
    history=HistoricalRecords()

    class Meta:
        db_table='BuyerProductBidding'



class BiddingBuyerProductDetails(models.Model):
    buyer_item_type = models.CharField(max_length=100, null=True,blank=True)
    buyer_item_code= models.CharField(max_length=100,null=True,blank=True)
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
    from_registration = models.CharField(max_length=100, null=True, blank=True, default='False')
    auto_rfq_number = models.CharField(max_length=40, null=True, blank=True)
    history = HistoricalRecords()


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

class RfqTermsDescription(models.Model):
    rfq_number=models.CharField(max_length=200,null=True,blank=True)
    terms=models.CharField(max_length=500)
    description=models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    product_biddings=models.ForeignKey(BuyerProductBidding, on_delete=models.CASCADE,null=True,blank=True)
    rfq_type = models.CharField(max_length=150,null=True,blank=True)
    from_registration = models.CharField(max_length=100, null=True, blank=True, default='False')
    auto_rfq_number = models.CharField(max_length=40, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table = "RfqTermsDescription"


class SelectVendorsForBiddingProduct(models.Model):
    rfq_number = models.CharField(max_length=50,null=True,blank=True)
    vendor_code=models.CharField(max_length=80)
    vendor_status=models.CharField(max_length=50,default='Pending')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    auto_rfq_number=models.CharField(max_length=100,null=True,blank=True)
    rfq_type=models.CharField(max_length=100,null=True,blank=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    from_registration = models.CharField(max_length=100, null=True, blank=True, default='False')

    class Meta:
        db_table = "SelectVendorsForBiddingProduct"

class BiddingTermMasterSettings(models.Model):
    terms_name=models.CharField(max_length=80)
    terms_description=models.CharField(max_length=800,null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)

    class Meta:
        db_table = "BiddingTermMasterSettings"


class VendorProductBidding(models.Model):
    vendor_product_bidding_id=models.BigAutoField(primary_key=True)
    vendor_product_rfq_number=models.CharField(max_length=40,null=True,blank=True)
    vendor_user_rfq_number=models.CharField(max_length=50,null=True,blank=True)
    vendor_product_rfq_type=models.CharField(max_length=400)
    vendor_product_rfq_status=models.CharField(max_length=50,default='Pending')
    vendor_product_publish_date=models.CharField(max_length=100)
    vendor_product_deadline_date=models.CharField(max_length=100)
    vendor_product_delivery_date = models.CharField(max_length=100)
    vendor_product_rfq_currency = models.CharField(max_length=100,null=True,blank=True)
    vendor_product_rfq_category = models.CharField(max_length=100, null=True, blank=True)
    vendor_product_department=models.CharField(max_length=300)
    vendor_product_bill_address=models.TextField()
    vendor_product_ship_address=models.TextField()
    vendor_product_rfq_title = models.CharField(max_length=600)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    vendor_code=models.CharField(max_length=100,null=True,blank=True)
    # from_registration = models.CharField(max_length=100, null=True, blank=True, default='False')
    # auto_rfq_number = models.CharField(max_length=40, null=True, blank=True)
    history=HistoricalRecords()

    class Meta:
        db_table='VendorProductBidding'


class VendorBiddingBuyerProductDetails(models.Model):
    vendor_item_type = models.CharField(max_length=100, null=True, blank=True)
    vendor_item_code= models.CharField(max_length=100,null=True,blank=True)
    vendor_item_name = models.CharField(max_length=100)
    vendor_item_description = models.TextField(null=True,blank=True)
    vendor_uom = models.CharField(max_length=100, null=True,blank=True)
    vendor_category = models.CharField(max_length=500,null=True,blank=True)
    buyer_quantity = models.CharField(max_length=100,null=True,blank=True)
    vendor_quantity = models.CharField(max_length=100,null=True,blank=True)
    vendor_rate = models.CharField(max_length=100,null=True,blank=True)
    vendor_tax = models.CharField(max_length=100,null=True,blank=True)
    vendor_discount = models.CharField(max_length=100,null=True,blank=True)
    vendor_final_amount = models.CharField(max_length=80,null=True,blank=True)
    vendor_total_amount= models.CharField(max_length=80,null=True,blank=True)
    vendor_document=models.FileField(upload_to='BuyerProductFiles',null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    vendor_rfq_number=models.CharField(max_length=100,null=True,blank=True)
    vendor_code=models.CharField(max_length=200,null=True,blank=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    # from_registration = models.CharField(max_length=100, null=True, blank=True, default='False')
    # auto_rfq_number = models.CharField(max_length=40, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table='VendorBiddingBuyerProductDetails'


class VendorRfqTermsDescription(models.Model):
    vendor_rfq_number=models.CharField(max_length=200)
    vendor_terms=models.CharField(max_length=500,null=True,blank=True)
    vendor_description=models.TextField(null=True,blank=True)
    vendor_response=models.TextField(null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    vendor_product_biddings=models.ForeignKey(VendorProductBidding, on_delete=models.CASCADE,null=True,blank=True)
    rfq_type = models.CharField(max_length=100, null=True, blank=True)
    # from_registration = models.CharField(max_length=100, null=True, blank=True, default='False')
    # auto_rfq_number = models.CharField(max_length=40, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table = "VendorRfqTermsDescription"




class Awards(models.Model):
    rfq_number = models.CharField(max_length=50)
    company_code =models.CharField(max_length=100,null=True,blank=True)
    company_name=models.CharField(max_length=200,null=True,blank=True)
    # order_quantity=models.CharField(max_length=100,null=True,blank=True)
    buyer_bid_quantity = models.CharField(max_length=100, null=True, blank=True)
    vendor_bid_quantity = models.CharField(max_length=100, null=True, blank=True)
    # frieght_cost=models.CharField(max_length=500, null=True, blank=True)
    # p_f_charge=models.CharField(max_length=500, null=True, blank=True)
    totalamount=models.CharField(max_length=200, null=True, blank=True)
    rfq_title = models.CharField(max_length=100, null=True, blank=True)
    rfq_status = models.CharField(max_length=100, null=True, default="Pending", blank=True)
    product_code=ArrayField(models.CharField(max_length=200),null=True,blank=True)
    product_name = ArrayField(models.CharField(max_length=200),null=True,blank=True)
    daterange = models.DateField(null=True,blank=True)
    product_description = ArrayField(models.CharField(max_length=200),null=True,blank=True)
    awarded_date = models.DateField(auto_now=True, null=True, blank=True)
    publish_date=models.CharField(max_length=100,null=True, blank=True)
    deadline_date=models.CharField(max_length=100,null=True, blank=True)
    awardstatus=models.CharField(max_length=100,null=True,blank=True,default='Pending')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    postatus=models.CharField(max_length=100,default='Pending',blank=True,null=True)
    rfq_type=models.CharField(max_length=100,null=True,blank=True)
    # from_registration = models.CharField(max_length=100, null=True, blank=True, default='False')
    # auto_rfq_number = models.CharField(max_length=40, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table = "Awards"

class ServiceAwards(models.Model):
    service_rfq_number = models.CharField(max_length=50)
    service_company_code =models.CharField(max_length=100,null=True,blank=True)
    service_company_name=models.CharField(max_length=200,null=True,blank=True)
    # order_quantity=models.CharField(max_length=100,null=True,blank=True)
    service_buyer_bid_quantity = models.CharField(max_length=100, null=True, blank=True)
    service_vendor_bid_quantity = models.CharField(max_length=100, null=True, blank=True)
    # frieght_cost=models.CharField(max_length=500, null=True, blank=True)
    # p_f_charge=models.CharField(max_length=500, null=True, blank=True)
    service_totalamount=models.CharField(max_length=200, null=True, blank=True)
    service_rfq_title = models.CharField(max_length=100, null=True, blank=True)
    service_rfq_status = models.CharField(max_length=100, null=True, default="Pending", blank=True)
    service_code=ArrayField(models.CharField(max_length=200),null=True,blank=True)
    service_name = ArrayField(models.CharField(max_length=200),null=True,blank=True)
    service_daterange = models.DateField(null=True,blank=True)
    service_description =ArrayField(models.CharField(max_length=200),null=True,blank=True)
    service_awarded_date = models.DateField(auto_now=True, null=True, blank=True)
    service_publish_date=models.CharField(max_length=100,null=True, blank=True)
    service_deadline_date=models.CharField(max_length=100,null=True, blank=True)
    service_award_status=models.CharField(max_length=100,null=True,blank=True,default='Pending')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    service_po_status=models.CharField(max_length=100,default='Pending',blank=True,null=True)
    rfq_type = models.CharField(max_length=100, null=True, blank=True)
    # from_registration = models.CharField(max_length=100, null=True, blank=True, default='False')
    # auto_rfq_number = models.CharField(max_length=40, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table = "ServiceAwards"


class MachinaryAwards(models.Model):
    machinary_rfq_number = models.CharField(max_length=50)
    machinary_company_code =models.CharField(max_length=100,null=True,blank=True)
    machinary_company_name=models.CharField(max_length=200,null=True,blank=True)
    # order_quantity=models.CharField(max_length=100,null=True,blank=True)
    machinary_buyer_bid_quantity = models.CharField(max_length=100, null=True, blank=True)
    machinary_vendor_bid_quantity = models.CharField(max_length=100, null=True, blank=True)
    # frieght_cost=models.CharField(max_length=500, null=True, blank=True)
    # p_f_charge=models.CharField(max_length=500, null=True, blank=True)
    machinary_totalamount=models.CharField(max_length=200, null=True, blank=True)
    machinary_rfq_title = models.CharField(max_length=100, null=True, blank=True)
    machinary_rfq_status = models.CharField(max_length=100, null=True, default="Pending", blank=True)
    machinary_code=ArrayField(models.CharField(max_length=200),null=True,blank=True)
    machinary_name = ArrayField(models.CharField(max_length=200),null=True,blank=True)
    machinary_date_range = models.DateField(null=True,blank=True)
    machinary_description = ArrayField(models.CharField(max_length=200),null=True,blank=True)
    machinary_awarded_date = models.DateField(auto_now=True, null=True, blank=True)
    machinary_publish_date=models.CharField(max_length=100,null=True, blank=True)
    machinary_deadline_date=models.CharField(max_length=100,null=True, blank=True)
    machinary_award_status=models.CharField(max_length=100,null=True,blank=True,default='Pending')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    machinary_po_status=models.CharField(max_length=100,default='Pending',blank=True,null=True)
    rfq_type = models.CharField(max_length=100, null=True, blank=True)
    # from_registration = models.CharField(max_length=100, null=True, blank=True, default='False')
    # auto_rfq_number = models.CharField(max_length=40, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table = "MachinaryAwards"
# ------------------------------------------------------------SERVICE BIDDING--------------------------------------------------------------------------------------------



class BiddingBuyerServiceDetails(models.Model):
    service_item_type = models.CharField(max_length=100, null=True,blank=True)
    service_buyer_item_code= models.CharField(max_length=100,null=True,blank=True)
    service_buyer_item_name = models.CharField(max_length=100)
    service_buyer_item_description = models.TextField(null=True,blank=True)
    service_buyer_uom = models.CharField(max_length=100, null=True,blank=True)
    service_buyer_category = models.CharField(max_length=500,null=True)
    service_buyer_quantity = models.CharField(max_length=100)
    service_buyer_document=models.FileField(upload_to='BuyerServiceFiles',null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    service_buyer_rfq_number=models.CharField(max_length=100)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    from_registration = models.CharField(max_length=100, null=True, blank=True, default='False')
    auto_rfq_number = models.CharField(max_length=40, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table='BiddingBuyerServiceDetails'


class BiddingBuyerMachinaryDetails(models.Model):
    machinary_item_type = models.CharField(max_length=100, null=True,blank=True)
    machinary_buyer_item_code= models.CharField(max_length=100,null=True,blank=True)
    machinary_buyer_item_name = models.CharField(max_length=100)
    machinary_buyer_item_description = models.TextField(null=True,blank=True)
    machinary_buyer_uom = models.CharField(max_length=100, null=True,blank=True)
    machinary_buyer_category = models.CharField(max_length=500,null=True)
    machinary_buyer_quantity = models.CharField(max_length=100)
    machinary_buyer_document=models.FileField(upload_to='BuyerMachinaryFiles',null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    machinary_buyer_rfq_number=models.CharField(max_length=100)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    from_registration = models.CharField(max_length=100, null=True, blank=True, default='False')
    auto_rfq_number = models.CharField(max_length=40, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table='BiddingBuyerMachinaryDetails'



class VendorBiddingBuyerServiceDetails(models.Model):
    vendor_service_item_type = models.CharField(max_length=100, null=True, blank=True)
    vendor_service_item_code= models.CharField(max_length=100,null=True,blank=True)
    vendor_service_item_name = models.CharField(max_length=100)
    vendor_service_item_description = models.TextField(null=True,blank=True)
    vendor_service_uom = models.CharField(max_length=100, null=True,blank=True)
    vendor_service_category = models.CharField(max_length=500,null=True,blank=True)
    buyer_service_quantity = models.CharField(max_length=100,null=True,blank=True)
    vendor_service_quantity = models.CharField(max_length=100,null=True,blank=True)
    vendor_service_rate = models.CharField(max_length=100,null=True,blank=True)
    vendor_service_tax = models.CharField(max_length=100,null=True,blank=True)
    vendor_service_discount = models.CharField(max_length=100,null=True,blank=True)
    vendor_service_final_amount = models.CharField(max_length=80,null=True,blank=True)
    vendor_service_total_amount= models.CharField(max_length=80,null=True,blank=True)
    vendor_service_document=models.FileField(upload_to='BuyerProductFiles',null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    vendor_service_rfq_number=models.CharField(max_length=100,null=True,blank=True)
    vendor_code=models.CharField(max_length=200,null=True,blank=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    # from_registration = models.CharField(max_length=100, null=True, blank=True, default='False')
    # auto_rfq_number = models.CharField(max_length=40, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table='VendorBiddingBuyerServiceDetails'


class VendorBiddingBuyerMachinaryDetails(models.Model):
    vendor_machinary_item_type = models.CharField(max_length=100, null=True, blank=True)
    vendor_machinary_item_code= models.CharField(max_length=100,null=True,blank=True)
    vendor_machinary_item_name = models.CharField(max_length=100)
    vendor_machinary_item_description = models.TextField(null=True,blank=True)
    vendor_machinary_uom = models.CharField(max_length=100, null=True,blank=True)
    vendor_machinary_category = models.CharField(max_length=500,null=True,blank=True)
    buyer_machinary_quantity = models.CharField(max_length=100,null=True,blank=True)
    vendor_machinary_quantity = models.CharField(max_length=100,null=True,blank=True)
    vendor_machinary_rate = models.CharField(max_length=100,null=True,blank=True)
    vendor_machinary_tax = models.CharField(max_length=100,null=True,blank=True)
    vendor_machinary_discount = models.CharField(max_length=100,null=True,blank=True)
    vendor_machinary_final_amount = models.CharField(max_length=80,null=True,blank=True)
    vendor_machinary_total_amount= models.CharField(max_length=80,null=True,blank=True)
    vendor_machinary_document=models.FileField(upload_to='BuyerProductFiles',null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField(null=True,blank=True)
    vendor_machinary_rfq_number=models.CharField(max_length=100,null=True,blank=True)
    vendor_code=models.CharField(max_length=200,null=True,blank=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
    # from_registration = models.CharField(max_length=100, null=True, blank=True, default='False')
    # auto_rfq_number = models.CharField(max_length=40, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table='VendorBiddingBuyerMachinaryDetails'


class PurchaseOrder(models.Model):

    rfq_number = models.CharField(max_length=50, null=True, blank=True)
    rfq_title = models.CharField(max_length=100, null=True, blank=True)
    PO_date = models.CharField(max_length=400,null=True,blank=True)
    PO_expirydate = models.CharField(max_length=400,null=True,blank=True)
    subject = models.TextField(null=True,blank=True)
    attachment1 = models.FileField(upload_to='POfile', null=True, blank=True)
    attachment2 = models.FileField(upload_to='POfile', null=True, blank=True)
    attachment3 = models.FileField(upload_to='POfile', null=True, blank=True)
    PO_num = models.CharField(max_length=50, null=True, blank=True)
    delivery_date = models.CharField(max_length=400,null=True,blank=True)
    remind_date = models.CharField(max_length=400,null=True,blank=True)
    delivery_days = models.CharField(max_length=100,null=True,blank=True)
    vendorcode = models.CharField(max_length=30)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    createdon = models.DateTimeField(null=True, auto_now_add=True, blank=True)
    updatedon = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by=models.BigIntegerField(null=True,blank=True)
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, null=True, blank=True)
    history = HistoricalRecords()
    po_numeric=models.CharField(max_length=100,null=True,blank=True)
    rfq_type=models.CharField(max_length=120,null=True,blank=True)
    # from_registration = models.CharField(max_length=100, null=True, blank=True, default='False')
    # auto_rfq_number = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        db_table = "PurchaseOrder"


#------------------------------------SOURCE-------------------------------------------


class SourceList_CreateItems(models.Model):
    item_type=models.CharField(max_length=80)
    source_code=models.CharField(unique=True,max_length=100,null=True,blank=True)
    source=models.CharField(max_length=200)
    item_name=models.CharField(max_length=200)
    item_code=models.CharField(max_length=60,null=True,blank=True)
    item_description=models.TextField()
    uom=models.CharField(max_length=80)
    department=models.CharField(max_length=100)
    quantity=models.CharField(max_length=80)

    deadline_date=models.CharField(max_length=100,null=True,blank=True)
    publish_date = models.CharField(max_length=100,null=True,blank=True)

    # present_cost=models.CharField(max_length=50,null=True,blank=True)
    # target_cost=models.CharField(max_length=50,null=True,blank=True)

    product_category=models.CharField(max_length=100)
    p_f_charges=models.CharField(max_length=200)
    frieght_charges=models.CharField(max_length=200)
    delivery=models.CharField(max_length=200)
    priority=models.CharField(max_length=200)
    annual_consumption=models.CharField(max_length=200)
    source_required_city=models.CharField(max_length=200)
    source_vendors = ArrayField(models.CharField(max_length=800),null=True,blank=True)
    document_name1 = models.CharField(max_length=200, null=True, blank=True)
    document_name2 = models.CharField(max_length=200, null=True, blank=True)
    document_name3 = models.CharField(max_length=200, null=True, blank=True)

    document_1=models.FileField(upload_to='SourceListFiles',null=True,blank=True)
    document_2 = models.FileField(upload_to='SourceListFiles',null=True,blank=True)
    document_3= models.FileField(upload_to='SourceListFiles',null=True,blank=True)
    # status=models.CharField(max_length=40,default='Pending')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)

    class Meta:
        db_table="SourceList_CreateItems"

class SourcePublish(models.Model):
    source_item_type=models.CharField(max_length=100,null=True,blank=True)
    source_code = models.CharField(max_length=100, null=True, blank=True)
    source_type = models.CharField(max_length=100, null=True, blank=True)
    source_department=models.CharField(max_length=150,null=True,blank=True)
    source_present_cost = models.CharField(max_length=70, null=True, blank=True)
    source_target_cost = models.CharField(max_length=70, null=True, blank=True)
    source_pf_charges=models.CharField(max_length=200,null=True,blank=True)
    source_frieght_charges = models.CharField(max_length=200, null=True, blank=True)
    source_delivery_charges = models.CharField(max_length=200, null=True, blank=True)
    source_item_code = models.CharField(max_length=100, null=True, blank=True)
    source_item_name = models.CharField(max_length=100, null=True, blank=True)
    source_item_description=models.TextField(null=True,blank=True)
    source_uom=models.CharField(max_length=70,null=True,blank=True)
    source_product_category = models.CharField(max_length=200, null=True, blank=True)
    source_priority = models.CharField(max_length=50, null=True, blank=True)
    source_quantity=models.CharField(max_length=50,null=True,blank=True)
    source_unit_rate = models.CharField(max_length=50, null=True, blank=True)
    source_tax = models.CharField(max_length=50, null=True, blank=True)
    source_discount = models.CharField(max_length=50, null=True, blank=True)
    source_total_amount=models.CharField(max_length=50,null=True,blank=True)
    source=models.ForeignKey(SourceList_CreateItems,models.CASCADE, null=True,blank=True)
    source_user_id = models.CharField(max_length=40)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)

    class Meta:
        db_table="SourcePublish"