from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError

from RegistrationApp.models import SelfRegistration
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

    def create(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        phone = request.data.get('phone', None)
        try:
            regobj = SelfRegistration.objects.filter().values()
            for i in range(0, len(regobj)):
                if regobj[i].get('username') == email and regobj[i].get('phone_number') == phone:
                    return Response(
                        {'status': 202, 'message': 'User Already Registered with this email and phone number'},
                        status=202)
            if email!="":
                mailchimp = MailchimpTransactional.Client('14kMF-44pCPZu8XbNkAzFA')
                message = {
                    "from_email": "admin@vendorsin.com",
                    "subject": "Invitation Mail",
                    "text":"You are invited",
                    "to": [
                        {
                            "email": email,
                            "type": "to"
                        }
                    ]
                }
                response = mailchimp.messages.send({"message": message})
                print(response)
                return super().create(request, *args, **kwargs)
            else:
                return Response({'status': 202, 'message': 'Email should not be empty'}, status=202)

        except ApiClientError as error:
            return Response({'status': 500, 'error': error}, status=500)
        # except Exception as e:
        #     return Response({'status': 500, 'error': str(e)}, status=500)


class CreateUserView(viewsets.ModelViewSet):
    queryset = CreateUser.objects.all()
    serializer_class = CreateUserSerializer



class PermissionsView(viewsets.ModelViewSet):
    queryset = Permissions.objects.all()
    serializer_class=PermissionsSerializer