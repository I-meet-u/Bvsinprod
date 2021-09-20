from rest_framework import  serializers
from rest_framework.exceptions import ValidationError
from .models import *


class AdminRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminRegister
        fields = ('admin_id','full_name','company_name','admin_email','admin_phone','password')

class AdminInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model=AdminInvite
        fields = '__all__'

class CreateUserSerializer(serializers.ModelSerializer):
    user_code = serializers.SerializerMethodField()
    numeric = serializers.SerializerMethodField()

    def get_numeric(self, obj):
        return obj.numeric

    def get_user_code(self, obj):
        return obj.user_code

    class Meta:
        model=CreateUser
        fields = '__all__'

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        createobj = CreateUser.objects.count()
        if createobj == 0:
            numeric = 100001
        else:
            createobj = CreateUser.objects.values_list('numeric', flat=True).last()
            print(createobj)
            numeric = int(createobj) + 1
            print(numeric)
        values = CreateUser.objects.create(numeric=numeric,user_code="USR"+str(numeric), **validate_data)
        return values


class CreateBuyerSerializer(serializers.ModelSerializer):
    company_code = serializers.SerializerMethodField()
    numeric = serializers.SerializerMethodField()

    def get_numeric(self, obj):
        return obj.numeric

    def get_company_code(self, obj):
        return obj.company_code

    class Meta:
        model=CreateBuyer
        fields = '__all__'

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        createbuyer = CreateBuyer.objects.count()
        if createbuyer == 0:
            numeric = 1011001
        else:
            createbuyer = CreateBuyer.objects.values_list('numeric', flat=True).last()
            print(createbuyer)
            numeric = int(createbuyer) + 1
            print(numeric)
        values = CreateBuyer.objects.create(numeric=numeric,company_code=str(numeric), **validate_data)
        return values



class OpenLeadsRfqSerializer(serializers.ModelSerializer):
    rfq_number = serializers.SerializerMethodField()
    numeric = serializers.SerializerMethodField()

    def get_numeric(self, obj):
        return obj.numeric

    def get_rfq_number(self, obj):
        return obj.rfq_number

    class Meta:
        model=OpenLeadsRfq
        fields = '__all__'

    def create(self, validate_data):
        # to add any extra details into the object before saving
        print(validate_data)
        openleadsrfq = OpenLeadsRfq.objects.count()
        if openleadsrfq == 0:
            numeric = 3000001
        else:
            openleadsrfq = OpenLeadsRfq.objects.values_list('numeric', flat=True).last()
            print(openleadsrfq)
            numeric = int(openleadsrfq) + 1
            print(numeric)
        values = OpenLeadsRfq.objects.create(numeric=numeric,rfq_number="RFX"+str(numeric), **validate_data)
        return values

class OpenLeadsItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model=OpenLeadsItems
        fields = '__all__'