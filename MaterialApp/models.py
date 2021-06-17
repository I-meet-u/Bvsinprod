from django.db import models

# Create your models here.

from django.db import models

from RegistrationApp.models import SelfRegistration

class VendorProductsDetail(models.Model):

    core_sector=models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    sub_category = models.CharField(max_length=100, blank=True)
    product_category=models.CharField(max_length=100, blank=True)
    product_subcategory=models.CharField(max_length=100, blank=True)
    product_type=models.CharField(max_length=100, null=True)
    type_of_product=models.CharField(max_length=100,null=True)
    product_code=models.CharField(max_length=100,null=True,unique=True)
    product_name=models.CharField(max_length=100, null=True)
    product_description=models.CharField(max_length=100, null=True)
    product_document=models.FileField(upload_to='ProductsFile',blank=True)
    numeric=models.BigIntegerField(null=True)
    add_image1 = models.FileField(upload_to='vendorproductimage', null=True, blank=True)
    add_image2 = models.FileField(upload_to='vendorproductimage', null=True, blank=True)
    add_image3 = models.FileField(upload_to='vendorproductimage', null=True, blank=True)
    add_image4 = models.FileField(upload_to='vendorproductimage', null=True, blank=True)
    uom=models.CharField(max_length=100, blank=True)
    quantity=models.CharField(max_length=100, blank=True)
    hsn_sac=models.CharField(max_length=100, blank=True)
    unit_price=models.CharField(max_length=100, blank=True)
    discount=models.CharField(max_length=50, blank=True)
    tax=models.CharField(max_length=100, blank=True)
    sku_id=models.CharField(max_length=100, blank=True)
    country_of_origin=models.CharField(max_length=50, blank=True)
    currency=models.CharField(max_length=50, blank=True)
    p_andf_charges=models.CharField(max_length=100, blank=True)
    fright_charges=models.CharField(max_length=100, blank=True)
    warrenty_or_guarantee=models.CharField(max_length=100, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)

    class Meta:
        db_table = "VendorProductsDetail"


# class GeneralProductsDetails(models.Model):
#
#     warrenty=models.CharField(max_length=100, blank=True)
#     guarantee=models.CharField(max_length=100, blank=True)
#     after_sale_service=models.CharField(max_length=100, blank=True)
#     not_covered_WorG=models.CharField(max_length=100, blank=True)
#     industry_to_use=models.CharField(max_length=100, blank=True)
#     brand_make=models.CharField(max_length=100, blank=True)
#     model_no=models.CharField(max_length=100, blank=True)
#     part_no=models.CharField(max_length=100, blank=True)
#     alternate_parts=models.CharField(max_length=100, blank=True)
#     usage_application=models.CharField(max_length=100, blank=True)
#     department=models.CharField(max_length=100, blank=True)
#     min_order_quantity=models.CharField(max_length=100, blank=True)
#     packing_type=models.CharField(max_length=100, blank=True)
#     delievery_days=models.CharField(max_length=100, blank=True)
#     industries_sectors=models.CharField(max_length=100, blank=True)
#     standard_measures=models.CharField(max_length=100, blank=True)
#     item_weight=models.CharField(max_length=100, blank=True)
#     after_packing_weight=models.CharField(max_length=100, blank=True)
#     product_length=models.CharField(max_length=100, blank=True)
#     product_width=models.CharField(max_length=100, blank=True)
#     product_height=models.CharField(max_length=100, blank=True)
#     shipping_uom=models.CharField(max_length=100, blank=True)
#     shipping_weight=models.CharField(max_length=100, blank=True)
#     ship_via=models.CharField(max_length=100, blank=True)
#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)
#     created_by = models.BigIntegerField()
#     updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table="ProductGeneralDetails"
#
# class PricingOffer(models.Model):
#
#     base_price=models.CharField(max_length=100, blank=True)
#     discount=models.CharField(max_length=50, blank=True)
#     final_price=models.CharField(max_length=100, blank=True)
#     tax=models.CharField(max_length=50, blank=True)
#     total_amount=models.CharField(max_length=100, blank=True)
#     manufacturer_mrp=models.CharField(max_length=100, blank=True)
#     net_price=models.CharField(max_length=100, blank=True)
#     offering_quantity=models.CharField(max_length=50, blank=True)
#     start_date=models.DateField(auto_now=False)
#     end_date=models.DateField(auto_now=False)
#     offering_days=models.CharField(max_length=50, blank=True)
#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)
#     created_by = models.BigIntegerField()
#     updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table="PricingOffer"
#
#
# class TechnicalDetails(models.Model):
#
#     item = models.CharField(max_length=100, blank=True)
#     description = models.CharField(max_length=100, blank=True)
#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)
#     created_by = models.BigIntegerField()
#     updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table="TechnicalDetails"
#
# class ProductFeatures(models.Model):
#
#     item = models.CharField(max_length=100, blank=True)
#     description = models.CharField(max_length=100, blank=True)
#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)
#     created_by = models.BigIntegerField()
#     updated_by = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table="ProductFeatures"
