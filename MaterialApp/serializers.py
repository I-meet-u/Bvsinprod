from rest_framework import  serializers


from .models import VendorProductsDetail, GeneralProductsDetails, PricingOffer, TechnicalDetails, ProductFeatures

class VendorProductsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=VendorProductsDetail
        fields='__all__'

class GeneralProductsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=GeneralProductsDetails
        fields='__all__'

class PricingOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model=PricingOffer
        fields='__all__'

class ProductFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductFeatures
        fields='__all__'

class TechnicalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=TechnicalDetails
        fields='__all__'
