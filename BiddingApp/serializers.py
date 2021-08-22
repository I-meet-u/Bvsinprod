from rest_framework import serializers
from  .models import *

class BuyerProductBiddingSerializer(serializers.ModelSerializer):
    class Meta:
        model=BuyerProductBidding
        fields='__all__'

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        rfqobj = BuyerProductBidding.objects.count()
        if rfqobj == 0:
            product_rfq_number = '40001'
        else:
            rfqobj = BuyerProductBidding.objects.last()
            print(rfqobj.product_rfq_number)
            product_rfq_number = int(rfqobj.product_rfq_number) + 1
        values = BuyerProductBidding.objects.create(product_rfq_number=product_rfq_number, **validate_data)
        return values

class BiddingBuyerProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=BiddingBuyerProductDetails
        fields='__all__'


class RfqCodeSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model=RfqCodeSettings
        fields='__all__'

class RfqTermsDescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model=RfqTermsDescription
        fields='__all__'


class SelectVendorsForBiddingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectVendorsForBiddingProduct
        fields='__all__'

class BiddingTermMasterSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiddingTermMasterSettings
        fields='__all__'


class VendorProductBiddingSerializer(serializers.ModelSerializer):
    class Meta:
        model=VendorProductBidding
        fields='__all__'

class VendorBiddingBuyerProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=VendorBiddingBuyerProductDetails
        fields='__all__'

class VendorBiddingBuyerServiceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=VendorBiddingBuyerServiceDetails
        fields='__all__'


class VendorBiddingBuyerMachinaryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=VendorBiddingBuyerMachinaryDetails
        fields='__all__'


class VendorRfqTermsDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=VendorRfqTermsDescription
        fields='__all__'


class BiddingBuyerServiceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=BiddingBuyerServiceDetails
        fields='__all__'

class BiddingBuyerMachinaryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=BiddingBuyerMachinaryDetails
        fields='__all__'

class AwardsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Awards
        fields='__all__'

class ServiceAwardsSerializer(serializers.ModelSerializer):
    class Meta:
        model=ServiceAwards
        fields='__all__'

class MachinaryAwardsSerializer(serializers.ModelSerializer):
    class Meta:
        model=MachinaryAwards
        fields='__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"

    # def create(self, validate_data):
    #     # to add any extra details into the object before saving
    #     # print(validate_data)
    #     poobj = PurchaseOrder.objects.count()
    #     if poobj == 0:
    #         po_numeric = '720001'
    #     else:
    #         poobj = PurchaseOrder.objects.last()
    #         print(poobj.po_numeric,'came')
    #         po_numeric = int(poobj.po_numeric) + 1
    #     values = PurchaseOrder.objects.create(PO_num="PO_"+str(po_numeric),po_numeric=po_numeric, **validate_data)
    #     return values


class PurchaseOrderServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderService
        fields = "__all__"

    # def create(self, validate_data):
    #     # to add any extra details into the object before saving
    #     # print(validate_data)
    #     poobjservice = PurchaseOrderService.objects.count()
    #     if poobjservice == 0:
    #         service_po_numeric = '820001'
    #     else:
    #         poobjservice = PurchaseOrderService.objects.last()
    #         print(poobjservice.service_po_numeric,'came')
    #         service_po_numeric = int(poobjservice.service_po_numeric) + 1
    #     values = PurchaseOrderService.objects.create(service_PO_num="PO_"+str(service_po_numeric),service_po_numeric=service_po_numeric, **validate_data)
    #     return values

class PurchaseOrderMachinarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderMachinary
        fields = "__all__"

    # def create(self, validate_data):
    #     # to add any extra details into the object before saving
    #     # print(validate_data)
    #     poobjmachinary = PurchaseOrderMachinary.objects.count()
    #     if poobjmachinary == 0:
    #         machinary_po_numeric = '920001'
    #     else:
    #         poobjmachinary = PurchaseOrderMachinary.objects.last()
    #         print(poobjmachinary.machinary_po_numeric,'came')
    #         machinary_po_numeric = int(poobjmachinary.machinary_po_numeric) + 1
    #     values = PurchaseOrderMachinary.objects.create(machinary_PO_num="PO_"+str(machinary_po_numeric),machinary_po_numeric=machinary_po_numeric, **validate_data)
    #     return values

class SourceList_CreateItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model=SourceList_CreateItems
        fields='__all__'

    def create(self, validate_data):
        # to add any extra details into the object before saving
        sourceobj = SourceList_CreateItems.objects.count()
        if sourceobj == 0:
            source_code = '80001'
        else:
            sourceobj = SourceList_CreateItems.objects.last()
            source_code = int(sourceobj.source_code) + 1
        values = SourceList_CreateItems.objects.create(source_code=source_code, **validate_data)
        return values

class SourcePublishSerializer(serializers.ModelSerializer):
    class Meta:
        model=SourcePublish
        fields='__all__'