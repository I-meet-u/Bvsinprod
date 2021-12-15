from rest_framework import  serializers

from .models import *


class InviteVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=InviteVendor
        fields="__all__"


class BusinessRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=BusinessRequest
        fields="__all__"

class InternalVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=InternalVendor
        fields="__all__"


class InternalBuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model=InternalBuyer
        fields="__all__"

class TrailVendorsSerializer(serializers.ModelSerializer):
    class Meta:
        model=TrailVendors
        fields="__all__"

class QuoteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=QuoteModel
        fields="__all__"