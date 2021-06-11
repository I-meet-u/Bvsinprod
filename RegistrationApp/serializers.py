from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import SelfRegistration, SelfRegistration_Sample, BasicCompanyDetails, BillingAddress, ShippingAddress, \
    IndustrialInfo, IndustrialHierarchy, BankDetails, LegalDocuments, BasicCompanyDetails_Others, EmployeeRegistration


class SelfRegistrationSerializer(serializers.ModelSerializer):
    # registration serializer
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(max_length=150, required=True,
                                     validators=[UniqueValidator(queryset=SelfRegistration.objects.all())])
    phone_number=serializers.CharField(max_length=15,required=True,validators=[UniqueValidator(queryset=SelfRegistration.objects.all())])

    class Meta:
        model = SelfRegistration
        fields = ('id','username', 'password', 'confirm_password', 'last_login', 'contact_person', 'business_to_serve', 'country',
        'nature_of_business','user_type','phone_number', 'admin_approve', 'registration_status')

    def validate(self, obj):
        # validation of password and confirm_password
        if obj['password'] != obj['confirm_password']:
            raise serializers.ValidationError({'password': 'Passwords did not match', 'status': 400})
        return obj



    def create(self, validated_data):
        registerobj = SelfRegistration.objects.create(
            username=validated_data['username'],
            password=validated_data['password'],
            contact_person=validated_data['contact_person'],
            business_to_serve=validated_data['business_to_serve'],
            country=validated_data['country'],
            nature_of_business=validated_data['nature_of_business'],
            user_type=validated_data['user_type'],
            phone_number=validated_data['phone_number'],
            last_login=timezone.now()
        )
        registerobj.set_password(validated_data['password'])
        registerobj.save()
        return registerobj

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

class SelfRegistrationSerializerSample(serializers.ModelSerializer):
    # registraion serializer sample
    class Meta:
        model=SelfRegistration_Sample
        fields='__all__'


class BasicCompanyDetailsSerializers(serializers.ModelSerializer):
    # basic info details serializers
    company_code = serializers.SerializerMethodField()

    def get_company_code(self, obj):
        return obj.company_code


    class Meta:
        model=BasicCompanyDetails
        fields=('company_code','gst_number','company_name','company_type','listing_date','pan_number','tax_payer_type',
               'msme_registered','company_established','registered_iec','industrial_scale','created_on','updated_on',
                'created_by','updated_by')

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        basic = BasicCompanyDetails.objects.count()
        if basic == 0:
            company_code = '100001'
        else:
            basic = BasicCompanyDetails.objects.values_list('company_code', flat=True).last()
            print(basic)
            company_code = int(basic) + 1
            print(company_code)
        values = BasicCompanyDetails.objects.create(company_code=company_code,**validate_data)
        return values

class BillingAddressSerializer(serializers.ModelSerializer):
    # billing address serializer
    class Meta:
        model=BillingAddress
        fields='__all__'

class ShippingAddressSerializer(serializers.ModelSerializer):
    # shipping address serializer
    class Meta:
        model=ShippingAddress
        fields='__all__'

class IndustrialInfoSerializer(serializers.ModelSerializer):
    # industrial info serializer
    class Meta:
        model=IndustrialInfo
        fields="__all__"

class IndustrialHierarchySerializer(serializers.ModelSerializer):
    # industrial hierarchy serializer
    class Meta:
        model=IndustrialHierarchy
        fields="__all__"

class BankDetailsSerializer(serializers.ModelSerializer):
    # bank details serializer
    class Meta:
        model=BankDetails
        fields="__all__"

class LegalDocumentsSerializers(serializers.ModelSerializer):
    # legal documents serializer
    class Meta:
        model=LegalDocuments
        fields="__all__"


class BasicCompanyDetailsOthersSerializers(serializers.ModelSerializer):
    # basic info details serializers
    company_code = serializers.SerializerMethodField()

    def get_company_code(self, obj):
        return obj.company_code


    class Meta:
        model=BasicCompanyDetails_Others
        fields=('company_code','company_name','company_established','industrial_scale','market_location','company_type',
               'tax_id_or_vat','currency','created_on','updated_on',
                'created_by','updated_by')

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        basic = BasicCompanyDetails_Others.objects.count()
        if basic == 0:
            company_code = '100001'
        else:
            basic = BasicCompanyDetails_Others.objects.values_list('company_code', flat=True).last()
            print(basic)
            company_code = int(basic) + 1
            print(company_code)
        values = BasicCompanyDetails_Others.objects.create(company_code=company_code,**validate_data)
        return values


class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeRegistration
        fields = '__all__'