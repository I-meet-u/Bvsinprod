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
    class Meta:
        model=CreateUser
        fields = '__all__'


class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Permissions
        fields='__all__'
