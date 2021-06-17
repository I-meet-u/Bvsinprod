from rest_framework import  serializers
from rest_framework.exceptions import ValidationError

from .models import VendorProductsDetail


class ManualProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorProductsDetail
        fields = '__all__'


    def create(self, validated_data):
        productofuser = VendorProductsDetail.objects.filter().order_by('-numeric')
        if len(productofuser) == 0 or productofuser == " ":
            raise ValidationError({'message': 'No Products present ,Add Products'})
        else:
            numerics = productofuser[0].numeric
        value1 = VendorProductsDetail.objects.create(numeric=numerics, **validated_data)
        print(value1)
        return value1

class VendorProductsDetailSerializer(serializers.ModelSerializer):
    # productselect=contec

    # def __init__(self, *args, **kwargs):
    #     self.productselect=kwargs.pop('productselect')
    #     super().__init__(*args, **kwargs)

    class Meta:
        model=VendorProductsDetail
        fields='__all__'

    def create(self, validated_data):
        updated_by=validated_data['updated_by']
        productselect=self.context['request'].productselect
        if productselect=='auto':
            print('yes')
            # productobj = VendorProductsDetail.objects.filter(updated_by=updated_by).order_by('-numeric').values()
            # if productselect == 'auto':
            #     if len(productobj) == 0:
            #         print('data not there')
            #         numeric = 100002
            #         product_code = 100001
            #     else:
            #         existvalue = productobj[0].get('numeric')
            #         numeric = existvalue + 1
            #         product_code=existvalue
            #     value = VendorProductsDetail.objects.create(product_code=product_code, numeric=numeric, **validated_data)
            #     return value
            # if producttype=='manual':
            #     numeric = productobj[0].get('numeric')
            #     print(numeric)
            value1 = VendorProductsDetail.objects.create(numeric=numeric,**validated_data)
            return value1





