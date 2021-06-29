from django.http import request

from .models import MaincoreMaster, CategoryMaster, SubCategoryMaster, \
    IndustryToServeMaster, NatureOfBusinessMaster, SupplyCapabilitiesMaster, PincodeMaster, UOMMaster, DepartmentMaster, \
    DesignationMaster, TaxMaster, HSNMaster, SACMaster, CurrencyMaster, PFChargesMaster, FrieghtChargesMaster, \
    DeliveryMaster, CountryMaster, WarrantyMaster, GuaranteeMaster
from rest_framework import serializers

class IndustryToServeMasterSerializer(serializers.ModelSerializer):
    industry_code = serializers.SerializerMethodField()

    def get_industry_code(self, obj):
        return obj.industry_code

    # industry_serve master serializer
    class Meta:
        model=IndustryToServeMaster
        fields = ('industry_id','industry_name','industry_code','is_verified','admins','created_by','updated_by','status')

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        industryobj = IndustryToServeMaster.objects.count()
        if industryobj == 0:
            industry_code = '3001'
        else:
            industryobj = IndustryToServeMaster.objects.last()
            print(industryobj.industry_code)
            industry_code = int(industryobj.industry_code) + 1
        values = IndustryToServeMaster.objects.create(industry_code=industry_code, **validate_data)
        return values

class NatureOfBusinessMasterSerializer(serializers.ModelSerializer):
    # nature_of_business master serializer
    class Meta:
        model=NatureOfBusinessMaster
        fields="__all__"

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        natureobj = NatureOfBusinessMaster.objects.count()
        if natureobj == 0:
            nature_of_business_code = '1001'
        else:
            natureobj = NatureOfBusinessMaster.objects.last()
            print(natureobj.nature_of_business_code)
            nature_of_business_code = int(natureobj.nature_of_business_code) + 1
        values = NatureOfBusinessMaster.objects.create(nature_of_business_code=nature_of_business_code, **validate_data)
        return values


class SupplyCapabilitiesMasterSerializer(serializers.ModelSerializer):
    # supply_capabilities master serializer
    class Meta:
        model=SupplyCapabilitiesMaster
        fields="__all__"

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        supplyobj = SupplyCapabilitiesMaster.objects.count()
        if supplyobj == 0:
            supply_capability_code = '2001'
        else:
            supplyobj = SupplyCapabilitiesMaster.objects.last()
            print(supplyobj.supply_capability_code)
            supply_capability_code = int(supplyobj.supply_capability_code) + 1
        values = SupplyCapabilitiesMaster.objects.create(supply_capability_code=supply_capability_code, **validate_data)
        return values


class MainCoreMasterSerializer(serializers.ModelSerializer):
    # industry_serve master serializer
    class Meta:
        model = MaincoreMaster
        fields ="__all__"

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        maincoreobj = MaincoreMaster.objects.count()
        if maincoreobj == 0:
            maincore_code = '4001'
        else:
            maincoreobj = MaincoreMaster.objects.last()
            print(maincoreobj.maincore_code)
            maincore_code = int(maincoreobj.maincore_code) + 1
        values = MaincoreMaster.objects.create(maincore_code=maincore_code, **validate_data)
        return values


class CategoryMasterSerializer(serializers.ModelSerializer):
    # category_master master serializer
    class Meta:
        model=CategoryMaster
        fields='__all__'

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        categoryobj = CategoryMaster.objects.count()
        if categoryobj == 0:
            category_code = '5001'
        else:
            categoryobj = CategoryMaster.objects.last()
            print(categoryobj.category_code)
            category_code = int(categoryobj.category_code) + 1
        values = CategoryMaster.objects.create(category_code=category_code, **validate_data)
        return values


class SubcategoryMasterSerializer(serializers.ModelSerializer):
    # sub_category master serializer
    class Meta:
        model=SubCategoryMaster
        fields='__all__'

    # def create(self, validate_data):
    #     # to add any extra details into the object before saving
    #     print(validate_data)
    #     subcategoryobj = SubCategoryMaster.objects.count()
    #     if subcategoryobj == 0:
    #         sub_category_code = '60001'
    #     else:
    #         subcategoryobj = SubCategoryMaster.objects.last()
    #         print(subcategoryobj.sub_category_code)
    #         sub_category_code = int(subcategoryobj.sub_category_code) + 1
    #     values = SubCategoryMaster.objects.create(sub_category_code=sub_category_code, **validate_data)
    #     return values

class PincodeMasterSerializer(serializers.ModelSerializer):
    # pin_code master serializer
    class Meta:
        model=PincodeMaster
        fields='__all__'


class UOMMasterSerializer(serializers.ModelSerializer):
    # uom master serializer
    class Meta:
        model=UOMMaster
        fields='__all__'

class DepartmentMasterSerializer(serializers.ModelSerializer):
    # department master serializer
    class Meta:
        model=DepartmentMaster
        fields='__all__'


class DesignationMasterSerializer(serializers.ModelSerializer):
    # designation master serializer
    class Meta:
        model=DesignationMaster
        fields='__all__'

class TaxMasterSerializer(serializers.ModelSerializer):
    # tax master serializer
    class Meta:
        model=TaxMaster
        fields='__all__'

class HSNMasterSerializer(serializers.ModelSerializer):
    # hsn_master  serializer
    class Meta:
        model=HSNMaster
        fields='__all__'

class SACMasterSerializer(serializers.ModelSerializer):
    # sac_master serializer
    class Meta:
        model=SACMaster
        fields='__all__'

class CurrencyMasterSerializer(serializers.ModelSerializer):
    # currency master serializer
    class Meta:
        model=CurrencyMaster
        fields='__all__'

class PFChargesMasterSerializer(serializers.ModelSerializer):
    # pf_charges master serializer
    class Meta:
        model=PFChargesMaster
        fields='__all__'

class FrieghtChargesMasterSerializer(serializers.ModelSerializer):
    # frieght master serializer
    class Meta:
        model=FrieghtChargesMaster
        fields='__all__'

class WarrantyMasterSerializer(serializers.ModelSerializer):
    # warranty master serializer
    class Meta:
        model=WarrantyMaster
        fields='__all__'

class GuaranteeMasterSerializer(serializers.ModelSerializer):
    # guarentee master serializer
    class Meta:
        model=GuaranteeMaster
        fields='__all__'

class DeliveryMasterSerializer(serializers.ModelSerializer):
    # delivery master serializer
    class Meta:
        model=DeliveryMaster
        fields='__all__'

class CountryMasterSerializer(serializers.ModelSerializer):
    # country master serializer
    class Meta:
        model=CountryMaster
        fields='__all__'