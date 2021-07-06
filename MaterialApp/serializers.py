from rest_framework import  serializers
from rest_framework.exceptions import ValidationError

from .models import VendorProduct_BasicDetails, VendorProduct_GeneralDetails, VendorProduct_TechnicalSpecifications, \
    VendorProduct_ProductFeatures, VendorProduct_Documents, BuyerProductDetails, ItemCodeSettings


class VendorProduct_BasicDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model=VendorProduct_BasicDetails
        fields='__all__'


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

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        buyerproductobj = BuyerProductDetails.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by('buyer_product_id')
        if buyerproductobj:
            return buyerproductobj
        raise  ValidationError({'message':"Buyer Product Details not exist",'status':204})

class ItemCodeSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model=ItemCodeSettings
        fields='__all__'