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

class VendorRfqTermsDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=VendorRfqTermsDescription
        fields='__all__'