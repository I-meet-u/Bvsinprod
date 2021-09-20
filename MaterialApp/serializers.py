from rest_framework import  serializers
from rest_framework.exceptions import ValidationError

from .models import *


class VendorProduct_BasicDetailsSerializer(serializers.ModelSerializer):
    item_code = serializers.SerializerMethodField()

    def get_item_code(self, obj):
        return obj.item_code

    class Meta:
        model=VendorProduct_BasicDetails
        fields='__all__'
    def create(self, validate_data):
        # to add any extra details into the object before saving
        vendorobj = VendorProduct_BasicDetails.objects.count()
        if vendorobj == 0:
            item_code = '100001'
        else:
            vendorobj = VendorProduct_BasicDetails.objects.values_list('item_code', flat=True).last()
            item_code = int(vendorobj) + 1
        values = VendorProduct_BasicDetails.objects.create(item_code=item_code, **validate_data)
        return values



class VendorProduct_GeneralDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model=VendorProduct_GeneralDetails
        fields='__all__'

class VendorProduct_TechnicalSpecificationsSerialzer(serializers.ModelSerializer):

    class Meta:
        model=VendorProduct_TechnicalSpecifications
        fields='__all__'

class VendorProduct_ProductFeaturesSerializer(serializers.ModelSerializer):

    class Meta:
        model=VendorProduct_ProductFeatures
        fields='__all__'

class VendorProduct_DocumentsSerializer(serializers.ModelSerializer):

    class Meta:
        model=VendorProduct_Documents
        fields='__all__'


class BuyerProductDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model=BuyerProductDetails
        fields='__all__'
    #
    # def get_queryset(self):
    #     # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
    #     buyerproductobj = BuyerProductDetails.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by('buyer_product_id')
    #     if buyerproductobj:
    #         return buyerproductobj
    #     raise  ValidationError({'message':"Buyer Product Details not exist",'status':204})
class BuyerServiceDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model=BuyerServiceDetails
        fields='__all__'


class BuyerMachinaryDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model=BuyerMachinaryDetails
        fields='__all__'


class ItemCodeSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model=ItemCodeSettings
        fields='__all__'

class LandingPageBidding_PublishSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPageBidding_Publish
        fields = '__all__'


class LandingPageBiddingRFQAwardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = awardpostedRFQ
        fields = '__all__'