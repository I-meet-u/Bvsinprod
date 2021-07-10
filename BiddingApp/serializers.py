from rest_framework import serializers
from  .models import *

class BuyerProductBiddingSerializer(serializers.ModelSerializer):
    class Meta:
        model=BuyerProductBidding
        fields='__all__'


class BiddingBuyerProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=BiddingBuyerProductDetails
        fields='__all__'


class RfqCodeSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model=RfqCodeSettings
        fields='__all__'