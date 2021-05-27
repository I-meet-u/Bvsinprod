from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import *
from AdminApp.serializers import AdminInviteSerializer, CreateUserSerializer, AdminRegisterSerializer, \
    PermissionsSerializer


class AdminRegisterView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = AdminRegister.objects.all()
    serializer_class = AdminRegisterSerializer

    def perform_create(self, serializer):
        # Hash password but passwords are not required
        if ('password' in self.request.data):
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()

    def perform_update(self, serializer):
        if ('password' in self.request.data):
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()

@api_view(['post'])
@permission_classes([AllowAny])
def admin_login(request):
    data = request.data
    password = data['password']
    admin_email = data['admin_email']
    try:
        admin_obj = AdminRegister.objects.get(admin_email=admin_email)
        if check_password(password, admin_obj.password) and admin_obj.admin_email == admin_email:
            admin_user_data = {
                'adminemail':admin_obj.admin_email,
                'Phoneno':admin_obj.admin_phone
            }
            return Response({'status': 200, 'message': 'Login Success', 'data': admin_user_data}, status=200)
        else:
            return Response({'status': 424, 'message': 'Password entered is not correct,Please Check Once'},
                                status=424)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

class AdminInviteView(viewsets.ModelViewSet):
    queryset = AdminInvite.objects.all()
    serializer_class = AdminInviteSerializer

class CreateUserView(viewsets.ModelViewSet):
    queryset = CreateUser.objects.all()
    serializer_class = CreateUserSerializer

class PermissionsView(viewsets.ModelViewSet):
    queryset = Permissions.objects.all()
    serializer_class=PermissionsSerializer