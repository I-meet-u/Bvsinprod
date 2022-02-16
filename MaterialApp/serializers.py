from rest_framework import  serializers
from rest_framework.exceptions import ValidationError

from .models import *


class VendorProduct_BasicDetailsSerializer(serializers.ModelSerializer):
    item_code = serializers.SerializerMethodField()

    def get_item_code(self, obj):
        return obj.item_code

    class Meta:
        model=VendorProduct_BasicDetails
        fields='__all__'

    def create(self, validate_data):
        # to add any extra details into the object before saving
        vendorobj = VendorProduct_BasicDetails.objects.count()
        if vendorobj == 0:
            item_code = '100001'
        else:
            vendorobj = VendorProduct_BasicDetails.objects.values_list('item_code', flat=True).last()
            item_code = int(vendorobj) + 1
        values = VendorProduct_BasicDetails.objects.create(item_code=item_code, **validate_data)
        return values

    def update(self, instance, validated_data):
        print(validated_data['add_image1'])
        if validated_data['add_image1'] == None:
            print('do nothing')

        else:
            instance.add_image1 = validated_data.get('add_image1', instance.add_image1)
            instance.save()
        if validated_data['add_image2']==None:
                pass
        else:
            instance.add_image2 = validated_data.get('add_image2', instance.add_image2)
            instance.save()
        if validated_data['add_image3']==None:
            pass
        else:
            instance.add_image3 = validated_data.get('add_image3', instance.add_image3)
            instance.save()
        if validated_data['add_image4']==None:
            pass
        else:
            instance.add_image4 = validated_data.get('add_image4', instance.add_image4)
            instance.save()
        instance.core_sector=validated_data.get('core_sector',instance.core_sector)
        instance.category = validated_data.get('category', instance.category)
        instance.sub_category = validated_data.get('sub_category', instance.sub_category)
        instance.item_type = validated_data.get('item_type', instance.item_type)
        instance.item_group = validated_data.get('item_group', instance.item_group)
        instance.item_code = validated_data.get('item_code', instance.item_code)
        instance.item_code_manual = validated_data.get('item_code_manual', instance.item_code_manual)
        instance.product_category = validated_data.get('product_category', instance.product_category)
        instance.final_selling_price = validated_data.get('final_selling_price', instance.final_selling_price)
        instance.item_name = validated_data.get('item_name', instance.item_name)
        instance.item_description = validated_data.get('item_description', instance.item_description)
        instance.unit_price = validated_data.get('unit_price', instance.unit_price)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.brand_make = validated_data.get('brand_make', instance.brand_make)
        instance.pricing = validated_data.get('pricing', instance.pricing)
        instance.uom = validated_data.get('uom', instance.uom)
        instance.country_of_origin = validated_data.get('country_of_origin', instance.country_of_origin)
        instance.request_on_quote = validated_data.get('request_on_quote', instance.request_on_quote)
        instance.tax = validated_data.get('tax', instance.tax)
        instance.hsn_sac = validated_data.get('hsn_sac', instance.hsn_sac)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.status = validated_data.get('status', instance.status)
        instance.price_range_from = validated_data.get('price_range_from', instance.price_range_from)
        instance.price_range_to = validated_data.get('price_range_to', instance.price_range_to)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.sku_id = validated_data.get('sku_id', instance.sku_id)
        instance.numeric = validated_data.get('numeric', instance.numeric)
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.admin_create = validated_data.get('admin_create', instance.admin_create)
        instance.company_code = validated_data.get('company_code', instance.company_code)
        instance.save()
        return instance



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

class VendorProduct_RequirementsSerializer(serializers.ModelSerializer):

    class Meta:
        model=VendorProduct_Requirements
        fields='__all__'


class BuyerProductDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model=BuyerProductDetails
        fields='__all__'

class BuyerServiceDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model=BuyerServiceDetails
        fields='__all__'


class BuyerMachinaryDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model=BuyerMachinaryDetails
        fields='__all__'


class ItemCodeSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model=ItemCodeSettings
        fields='__all__'

class LandingPageBidding_PublishSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPageBidding_Publish
        fields = '__all__'


class LandingPageBiddingRFQAwardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = awardpostedRFQ
        fields = '__all__'

class LandingPageBiddingRFQ_SelectVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = landingpagelistingleadsselectvendors
        fields = '__all__'


class LandingPageListingLeadsPurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPageListingLeadsPurchaseOrder
        fields = "__all__"