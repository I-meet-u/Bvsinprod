from rest_framework import  serializers
from rest_framework.exceptions import ValidationError

from .models import VendorProduct_BasicDetails, VendorProduct_GeneralDetails,VendorProduct_TechnicalSpecifications,VendorProduct_ProductFeatures,VendorProduct_Documents


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




