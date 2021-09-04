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