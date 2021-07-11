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