from rest_framework import  serializers
from rest_framework.exceptions import ValidationError

from .models import VendorProductsDetail, IndustrialDetails_SearchCategory


class VendorProductsDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model=VendorProductsDetail
        fields='__all__'


class IndustrialDetails_SearchCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model=IndustrialDetails_SearchCategory
        fields='__all__'




