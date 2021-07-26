from django.http import request

from .models import *
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

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        subcategoryobj = SubCategoryMaster.objects.count()
        if subcategoryobj == 0:
            sub_category_code = '60001'
        else:
            subcategoryobj = SubCategoryMaster.objects.last()
            print(subcategoryobj.sub_category_code)
            sub_category_code = int(subcategoryobj.sub_category_code) + 1
        values = SubCategoryMaster.objects.create(sub_category_code=sub_category_code, **validate_data)
        return values

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

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        uomobj = UOMMaster.objects.count()
        if uomobj == 0:
            uom_code = '7001'
        else:
            uomobj = UOMMaster.objects.last()
            uom_code = int(uomobj.uom_code) + 1
        values = UOMMaster.objects.create(uom_code=uom_code, **validate_data)
        return values


class DepartmentMasterSerializer(serializers.ModelSerializer):
    # department master serializer
    class Meta:
        model=DepartmentMaster
        fields='__all__'


    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        departmentobj = DepartmentMaster.objects.count()
        if departmentobj == 0:
            department_code = '2201'
        else:
            departmentobj = DepartmentMaster.objects.last()
            department_code = int(departmentobj.department_code) + 1
        values = DepartmentMaster.objects.create(department_code=department_code, **validate_data)
        return values


class DesignationMasterSerializer(serializers.ModelSerializer):
    # designation master serializer
    class Meta:
        model=DesignationMaster
        fields='__all__'

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        designationobj = DesignationMaster.objects.count()
        if designationobj == 0:
            designation_code = '2101'
        else:
            designationobj = DesignationMaster.objects.last()
            designation_code = int(designationobj.designation_code) + 1
        values = DesignationMaster.objects.create(designation_code=designation_code, **validate_data)
        return values

class TaxMasterSerializer(serializers.ModelSerializer):
    # tax master serializer
    class Meta:
        model=TaxMaster
        fields='__all__'

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        taxobj = TaxMaster.objects.count()
        if taxobj == 0:
            tax_code = '4201'
        else:
            taxobj = TaxMaster.objects.last()
            tax_code = int(taxobj.tax_code) + 1
        values = TaxMaster.objects.create(tax_code=tax_code, **validate_data)
        return values


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

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        pfchargeobj = PFChargesMaster.objects.count()
        if pfchargeobj == 0:
            pf_charge_code = '1901'
        else:
            pfchargeobj = PFChargesMaster.objects.last()
            pf_charge_code = int(pfchargeobj.pf_charge_code) + 1
        values = PFChargesMaster.objects.create(pf_charge_code=pf_charge_code, **validate_data)
        return values


class FrieghtChargesMasterSerializer(serializers.ModelSerializer):
    # frieght master serializer
    class Meta:
        model=FrieghtChargesMaster
        fields='__all__'


    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        freightobj = FrieghtChargesMaster.objects.count()
        if freightobj == 0:
            frieght_code = '1801'
        else:
            freightobj = FrieghtChargesMaster.objects.last()
            frieght_code = int(freightobj.frieght_code) + 1
        values = FrieghtChargesMaster.objects.create(frieght_code=frieght_code, **validate_data)
        return values

class WarrantyMasterSerializer(serializers.ModelSerializer):
    # warranty master serializer
    class Meta:
        model=WarrantyMaster
        fields='__all__'

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        warrantyobj = WarrantyMaster.objects.count()
        if warrantyobj == 0:
            warranty_code = '9500'
        else:
            warrantyobj = WarrantyMaster.objects.last()
            warranty_code = int(warrantyobj.warranty_code) + 1
        values = WarrantyMaster.objects.create(warranty_code=warranty_code, **validate_data)
        return values

class GuaranteeMasterSerializer(serializers.ModelSerializer):
    # guarentee master serializer
    class Meta:
        model=GuaranteeMaster
        fields='__all__'

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        guaranteeobj = GuaranteeMaster.objects.count()
        if guaranteeobj == 0:
            guarantee_code = '2001'
        else:
            guaranteeobj = GuaranteeMaster.objects.last()
            guarantee_code = int(guaranteeobj.guarantee_code) + 1
        values = GuaranteeMaster.objects.create(guarantee_code=guarantee_code, **validate_data)
        return values

class DeliveryMasterSerializer(serializers.ModelSerializer):
    # delivery master serializer
    class Meta:
        model=DeliveryMaster
        fields='__all__'

    def create(self, validate_data):
        # to add any extra details into the object before saving
        deliveryobj = DeliveryMaster.objects.count()
        if deliveryobj == 0:
            delivery_code = '3000'
        else:
            deliveryobj = DeliveryMaster.objects.last()
            print(deliveryobj.delivery_code)
            delivery_code = int(deliveryobj.delivery_code) + 1
        values = DeliveryMaster.objects.create(delivery_code=delivery_code, **validate_data)
        return values

class CountryMasterSerializer(serializers.ModelSerializer):
    # country master serializer
    class Meta:
        model=CountryMaster
        fields='__all__'

class ItemGroupMasterSerializer(serializers.ModelSerializer):
    # item_group master serializer
    class Meta:
        model=ItemGroupMaster
        fields='__all__'

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        itemgroupobj = ItemGroupMaster.objects.count()
        if itemgroupobj == 0:
            item_group_code = '1601'
        else:
            itemgroupobj = ItemGroupMaster.objects.last()
            print(itemgroupobj.item_group_code)
            item_group_code = int(itemgroupobj.item_group_code) + 1
        values = ItemGroupMaster.objects.create(item_group_code=item_group_code, **validate_data)
        return values

class TransitInsuranceMasterSerializer(serializers.ModelSerializer):
    # transit insurance master serializer
    class Meta:
        model=TransitInsuranceMaster
        fields='__all__'

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        transitobj = TransitInsuranceMaster.objects.count()
        if transitobj == 0:
            transit_code = '1701'
        else:
            transitobj = TransitInsuranceMaster.objects.last()
            print(transitobj.transit_code)
            transit_code = int(transitobj.transit_code) + 1
        values = TransitInsuranceMaster.objects.create(transit_code=transit_code, **validate_data)
        return values



class PaymentMasterSerializer(serializers.ModelSerializer):
    # payment master serializer
    class Meta:
        model=PaymentMaster
        fields='__all__'

    def create(self, validate_data):
        # to add any extra details into the object before saving
        paymentobj = PaymentMaster.objects.count()
        if paymentobj == 0:
            payment_code = '1801'
        else:
            paymentobj = PaymentMaster.objects.last()
            print(paymentobj.payment_code)
            payment_code = int(paymentobj.payment_code) + 1
        values = PaymentMaster.objects.create(payment_code=payment_code, **validate_data)
        return values


class ValidityMasterSerializer(serializers.ModelSerializer):
    # validity master serializer
    class Meta:
        model=ValidityMaster
        fields='__all__'

    def create(self, validate_data):
        # to add any extra details into the object before saving
        validityobj = ValidityMaster.objects.count()
        if validityobj == 0:
            validity_code = '1901'
        else:
            validityobj = ValidityMaster.objects.last()
            print(validityobj.validity_code)
            validity_code = int(validityobj.validity_code) + 1
        values = ValidityMaster.objects.create(validity_code=validity_code, **validate_data)
        return values


class RfqCategoryMasterSerializer(serializers.ModelSerializer):
    # rfq_category master serializer
    class Meta:
        model=RfqCategoryMaster
        fields='__all__'

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        rfqcategoryobj = RfqCategoryMaster.objects.count()
        if rfqcategoryobj == 0:
            rfq_category_code = '3201'
        else:
            rfqcategoryobj = RfqCategoryMaster.objects.last()
            print(rfqcategoryobj.rfq_category_code)
            rfq_category_code = int(rfqcategoryobj.rfq_category_code) + 1
        values = RfqCategoryMaster.objects.create(rfq_category_code=rfq_category_code, **validate_data)
        return values

class PriceBasisMasterSerializer(serializers.ModelSerializer):
    # price basis master serializer
    class Meta:
        model=PriceBasisMaster
        fields='__all__'

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        pricebasisobj = PriceBasisMaster.objects.count()
        if pricebasisobj == 0:
            price_basis_code = '3301'
        else:
            pricebasisobj = PriceBasisMaster.objects.last()
            print(pricebasisobj.price_basis_code)
            price_basis_code = int(pricebasisobj.price_basis_code) + 1
        values = PriceBasisMaster.objects.create(price_basis_code=price_basis_code, **validate_data)
        return values


class InspectionMasterSerializer(serializers.ModelSerializer):
    # inspection  master serializer
    class Meta:
        model=InspectionMaster
        fields='__all__'

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        inspectionobj = InspectionMaster.objects.count()
        if inspectionobj == 0:
            inspection_code = '3401'
        else:
            inspectionobj = InspectionMaster.objects.last()
            print(inspectionobj.inspection_code)
            inspection_code = int(inspectionobj.inspection_code) + 1
        values = InspectionMaster.objects.create(inspection_code=inspection_code, **validate_data)
        return values


class LiquidatedDamageMasterSerializer(serializers.ModelSerializer):
    # liquidated  master serializer
    class Meta:
        model=LiquidatedDamageMaster
        fields='__all__'

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        liquidatedobj = LiquidatedDamageMaster.objects.count()
        if liquidatedobj == 0:
            liquidated_code = '3501'
        else:
            liquidatedobj = LiquidatedDamageMaster.objects.last()
            print(liquidatedobj.liquidated_code)
            liquidated_code = int(liquidatedobj.liquidated_code) + 1
        values = LiquidatedDamageMaster.objects.create(liquidated_code=liquidated_code, **validate_data)
        return values

class TaxesAndDutiesMasterSerializer(serializers.ModelSerializer):
    # taxes and duties  master serializer
    class Meta:
        model=TaxesAndDutiesMaster
        fields='__all__'

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        taxdutiesobj = TaxesAndDutiesMaster.objects.count()
        if taxdutiesobj == 0:
            tax_duties_code = '3601'
        else:
            taxdutiesobj = TaxesAndDutiesMaster.objects.last()
            print(taxdutiesobj.tax_duties_code)
            tax_duties_code = int(taxdutiesobj.tax_duties_code) + 1
        values = TaxesAndDutiesMaster.objects.create(tax_duties_code=tax_duties_code, **validate_data)
        return values


class TestAndQapMasterSerializer(serializers.ModelSerializer):
    # test and qap  master serializer
    class Meta:
        model=TestAndQapMaster
        fields='__all__'

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        testqapobj = TestAndQapMaster.objects.count()
        if testqapobj == 0:
            test_qap_code = '3701'
        else:
            testqapobj = TestAndQapMaster.objects.last()
            print(testqapobj.test_qap_code)
            test_qap_code = int(testqapobj.test_qap_code) + 1
        values = TestAndQapMaster.objects.create(test_qap_code=test_qap_code, **validate_data)
        return values

class PerformanceGuaranteesMasterSerializer(serializers.ModelSerializer):
    # performance and guarantee  master serializer
    class Meta:
        model=PerformanceGuaranteesMaster
        fields='__all__'

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        performanceobj = PerformanceGuaranteesMaster.objects.count()
        if performanceobj == 0:
            performance_code = '3801'
        else:
            performanceobj = PerformanceGuaranteesMaster.objects.last()
            print(performanceobj.performance_code)
            performance_code = int(performanceobj.performance_code) + 1
        values = PerformanceGuaranteesMaster.objects.create(performance_code=performance_code, **validate_data)
        return values