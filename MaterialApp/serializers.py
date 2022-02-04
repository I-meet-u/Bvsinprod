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