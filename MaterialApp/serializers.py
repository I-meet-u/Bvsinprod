from rest_framework import  serializers
from rest_framework.exceptions import ValidationError

from .models import VendorProductsDetail

class VendorProductsDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model=VendorProductsDetail
        fields='__all__'







