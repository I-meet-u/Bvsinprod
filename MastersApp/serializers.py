from django.http import request

from .models import MaincoreMaster, CategoryMaster, SubCategoryMaster, CountryMaster, StateMaster, CityMaster, \
    IndustryToServeMaster,NatureOfBusinessMaster,SupplyCapabilitiesMaster,PincodeMaster
from rest_framework import serializers

class IndustryToServeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=IndustryToServeMaster
        fields="__all__"

class NatureOfBusinessMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=NatureOfBusinessMaster
        fields="__all__"

class SupplyCapabilitiesMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=SupplyCapabilitiesMaster
        fields="__all__"


class MainCoreMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaincoreMaster
        fields ="__all__"


class CategoryMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=CategoryMaster
        fields='__all__'

class SubcategoryMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubCategoryMaster
        fields='__all__'

class CountryMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=CountryMaster
        fields='__all__'

class StateMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=StateMaster
        fields='__all__'

class CityMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=CityMaster
        fields='__all__'



class PincodeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=PincodeMaster
        fields='__all__'