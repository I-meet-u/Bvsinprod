from django.http import request

from .models import MaincoreMaster, CategoryMaster, SubCategoryMaster, \
    IndustryToServeMaster, NatureOfBusinessMaster, SupplyCapabilitiesMaster, PincodeMaster, UOMMaster, DepartmentMaster, \
    DesignationMaster, TaxMaster, HSNMaster, SACMaster, CurrencyMaster, PFChargesMaster
from rest_framework import serializers

class IndustryToServeMasterSerializer(serializers.ModelSerializer):
    # industry_serve master serializer
    class Meta:
        model=IndustryToServeMaster
        fields="__all__"

class NatureOfBusinessMasterSerializer(serializers.ModelSerializer):
    # nature_of_business master serializer
    class Meta:
        model=NatureOfBusinessMaster
        fields="__all__"

class SupplyCapabilitiesMasterSerializer(serializers.ModelSerializer):
    # supply_capabilities master serializer
    class Meta:
        model=SupplyCapabilitiesMaster
        fields="__all__"


class MainCoreMasterSerializer(serializers.ModelSerializer):
    # industry_serve master serializer
    class Meta:
        model = MaincoreMaster
        fields ="__all__"


class CategoryMasterSerializer(serializers.ModelSerializer):
    # category_master master serializer
    class Meta:
        model=CategoryMaster
        fields='__all__'

class SubcategoryMasterSerializer(serializers.ModelSerializer):
    # sub_category master serializer
    class Meta:
        model=SubCategoryMaster
        fields='__all__'

class PincodeMasterSerializer(serializers.ModelSerializer):
    # pin_code master serializer
    class Meta:
        model=PincodeMaster
        fields='__all__'


class UOMMasterSerializer(serializers.ModelSerializer):
    # pin_code master serializer
    class Meta:
        model=UOMMaster
        fields='__all__'

class DepartmentMasterSerializer(serializers.ModelSerializer):
    # pin_code master serializer
    class Meta:
        model=DepartmentMaster
        fields='__all__'


class DesignationMasterSerializer(serializers.ModelSerializer):
    # pin_code master serializer
    class Meta:
        model=DesignationMaster
        fields='__all__'

class TaxMasterSerializer(serializers.ModelSerializer):
    # pin_code master serializer
    class Meta:
        model=TaxMaster
        fields='__all__'

class HSNMasterSerializer(serializers.ModelSerializer):
    # pin_code master serializer
    class Meta:
        model=HSNMaster
        fields='__all__'

class SACMasterSerializer(serializers.ModelSerializer):
    # pin_code master serializer
    class Meta:
        model=SACMaster
        fields='__all__'

class CurrencyMasterSerializer(serializers.ModelSerializer):
    # pin_code master serializer
    class Meta:
        model=CurrencyMaster
        fields='__all__'

class PFChargesMasterSerializer(serializers.ModelSerializer):
    # pin_code master serializer
    class Meta:
        model=PFChargesMaster
        fields='__all__'