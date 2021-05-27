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
            user_code = 100001
        else:
            createobj = CreateUser.objects.values_list('user_code', flat=True).last()
            print(createobj)
            user_code = int(createobj) + 1
            print(user_code)
        values = CreateUser.objects.create(user_code=user_code, **validate_data)
        return values


class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Permissions
        fields='__all__'
