import math
import random
from base64 import b64encode

from django.contrib.auth.hashers import make_password,check_password
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from RegistrationApp.models import SelfRegistration, BasicCompanyDetails, IndustrialInfo, IndustrialHierarchy, \
    BankDetails, LegalDocuments
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
@permission_classes((AllowAny,))
def admin_login(request):
    data = request.data
    password = data['password']
    admin_email = data['admin_email']
    digits = '0123456789'
    OTP = ""
    try:
        admin_obj = AdminRegister.objects.get(admin_email=admin_email)
        if admin_obj:
            if check_password(password, admin_obj.password) and admin_obj.admin_email == admin_email:
                admin_user_data = {
                    'adminemail': admin_obj.admin_email,
                    'OTP':OTP
                }
                admin_obj.email_otp=OTP
                admin_obj.save()
                return Response({'status': 200, 'message': 'Email sent successfully','data': admin_user_data}, status=200)
            else:
                return Response({'status': 424, 'message': 'Password entered is not correct,Please Check Once'},
                            status=424)

    except ObjectDoesNotExist as e:
        return Response({'status': 404, 'error': "Email not exist"}, status=404)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def admin_email_otp_verify(request):
    data=request.data
    email_otp=data['email_otp']
    admin_email=data['admin_email']
    try:
        adminobjverify=AdminRegister.objects.get(admin_email=admin_email)
        if adminobjverify and adminobjverify.email_otp==email_otp:
            admin_data={
                'admin_id':adminobjverify.admin_id
            }

            return Response({'status':200,'message':"Email OTP is verified","data":admin_data},status=200)
        else:
            return Response({'status': 204, 'message': "Email OTP is not correct"}, status=204)
    except ObjectDoesNotExist as e:
        return Response({'status': 404, 'error': "Email not exist"}, status=404)
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
        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)


class CreateUserView(viewsets.ModelViewSet):
    queryset = CreateUser.objects.all()
    serializer_class = CreateUserSerializer
    # permission_classes = [permissions.AllowAny]


    def get_queryset(self):
        createuserobj=CreateUser.objects.filter(admins=self.request.GET.get('admins'))
        if not createuserobj:
            raise ValidationError({'message': 'Create User Details are not found', 'status': 204})
        return  createuserobj



class PermissionsView(viewsets.ModelViewSet):
    queryset = Permissions.objects.all()
    serializer_class=PermissionsSerializer


@api_view(['put'])
def create_user_status_update(request):
    data=request.data
    id=data['id']
    try:
        createuserobj=CreateUser.objects.filter(id__in=id).values()
        if len(createuserobj)>0:
            for i in range(0,len(createuserobj)):
                userobj=CreateUser.objects.get(id=createuserobj[i].get('id'))
                if userobj.status=='Active':
                    userobj.status='Disabled'
                    userobj.save()
                else:
                    return Response({'status': 202, 'message': 'Already status disabled'}, status=202)
            return Response({'status': 200, 'message': 'User status changed to disabled'}, status=200)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['get'])
@permission_classes([AllowAny])
def registration_list(request):
    data=request.data
    emptydata=list()
    try:
        regobj=SelfRegistration.objects.filter().values()
        for i in range(0, len(regobj)):
            x = regobj[i].get('id')
            basicobj = BasicCompanyDetails.objects.filter(updated_by=x).values()
            if basicobj:
                print('basic', x)
                industry_info = IndustrialInfo.objects.filter(updated_by=x).values()
                if industry_info:
                    industry_hierarchy = IndustrialHierarchy.objects.filter(updated_by=x).values()
                    if industry_hierarchy:
                        bankdetails = BankDetails.objects.filter(updated_by=x).values()
                        if bankdetails:
                            legalobj = LegalDocuments.objects.filter(updated_by=x).values()
                            if legalobj:
                                emptydata.append({"id":x ,
                                        "company_code":basicobj[0].get('company_code'),
                                        "company_name":basicobj[0].get('company_name'),
                                        "username": regobj[i].get('contact_person'),
                                        "user_type": regobj[i].get('user_type'),
                                        "email": regobj[i].get('username'),
                                        "phone_number": regobj[i].get('phone_number'),
                                        "nature_of_business": regobj[i].get('nature_of_business'),
                                        "business_type": regobj[i].get('business_to_serve'),
                                        "registration_status": "Registration completed"})
                            else:
                                emptydata.append({"id": x,
                                                  "company_code": basicobj[0].get('company_code'),
                                                  "company_name": basicobj[0].get('company_name'),
                                                  "username": regobj[i].get('contact_person'),
                                                  "user_type": regobj[i].get('user_type'),
                                                  "email": regobj[i].get('username'),
                                                  "phone_number": regobj[i].get('phone_number'),
                                                  "nature_of_business": regobj[i].get('nature_of_business'),
                                                  "business_type": regobj[i].get('business_to_serve'),
                                                  "registration_status": "Bank Details"})

                        else:
                            emptydata.append({"id": x,
                                              "company_code": basicobj[0].get('company_code'),
                                              "company_name": basicobj[0].get('company_name'),
                                              "username": regobj[i].get('contact_person'),
                                              "user_type": regobj[i].get('user_type'),
                                              "email": regobj[i].get('username'),
                                              "phone_number": regobj[i].get('phone_number'),
                                              "nature_of_business": regobj[i].get('nature_of_business'),
                                              "business_type": regobj[i].get('business_to_serve'),
                                              "registration_status": "Industry hierarchy"})

                    else:
                        emptydata.append({"id": x,
                                          "company_code": basicobj[0].get('company_code'),
                                          "company_name": basicobj[0].get('company_name'),
                                          "username": regobj[i].get('contact_person'),
                                          "user_type": regobj[i].get('user_type'),
                                          "email": regobj[i].get('username'),
                                          "phone_number": regobj[i].get('phone_number'),
                                          "nature_of_business": regobj[i].get('nature_of_business'),
                                          "business_type": regobj[i].get('business_to_serve'),
                                          "registration_status": "Seller info"})




                else:
                    emptydata.append({"id": x,
                                      "company_code": basicobj[0].get('company_code'),
                                      "company_name": basicobj[0].get('company_name'),
                                      "username": regobj[i].get('contact_person'),
                                      "user_type": regobj[i].get('user_type'),
                                      "email": regobj[i].get('username'),
                                      "phone_number": regobj[i].get('phone_number'),
                                      "nature_of_business": regobj[i].get('nature_of_business'),
                                      "business_type": regobj[i].get('business_to_serve'),
                                      "registration_status": "company details"})

        return Response({'status': 200, 'message': 'ok', 'data': emptydata}, status=200)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['put'])
@permission_classes([AllowAny])
def admin_approval_from_pending(request):
    data=request.data
    adminid = data['adminid']
    userid = data['userid']
    try:
        adminobj=AdminRegister.objects.get(admin_id=adminid)
        if adminobj:
            regobjdata=SelfRegistration.objects.filter(id=userid).values()
            legaldoc=LegalDocuments.objects.filter(updated_by_id=userid).values()
            if regobjdata and legaldoc:
                regobj=SelfRegistration.objects.get(id=userid)
                if regobj.admin_approve=='Pending':
                    regobj.admin_approve='Approved'
                    regobj.save()
                    return Response({'status': 200, 'message': 'Admin Approved'}, status=200)
                else:
                    if regobj.admin_approve == 'Approved':
                        return Response({'status': 202, 'message': 'Admin Already Approved'}, status=202)
                    if regobj.admin_approve == 'Verified':
                        return Response({'status': 202, 'message': 'Admin Already Verified'}, status=202)
            else:
                return Response({'status': 200, 'message': 'user is not present or not registered or not present in legal info'}, status=200)
        else:
            return Response({'status':204,'message':'Admin Data Not Present for this Id'},status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['put'])
@permission_classes([AllowAny])
def admin_verify_from_approve(request):
    data=request.data
    adminid = data['adminid']
    userid = data['userid']
    try:
        adminobj=AdminRegister.objects.get(admin_id=adminid)
        if adminobj:
            regobjdata=SelfRegistration.objects.filter(id=userid).values()
            legaldoc = LegalDocuments.objects.filter(updated_by_id=userid).values()
            if regobjdata and legaldoc:
                regobj=SelfRegistration.objects.get(id=userid)
                if regobj.admin_approve=='Pending':
                    regobj.admin_approve='Verified'
                    regobj.save()
                    return Response({'status': 200, 'message': 'Admin Verified'}, status=200)
                else:
                    if regobj.admin_approve == 'Verified':
                        return Response({'status': 202, 'message': 'Admin Already Verified'}, status=202)
                    elif regobj.admin_approve=='Approved':
                        return Response({'status': 202, 'message': 'Admin Already Approved'}, status=202)
            else:
                return Response({'status': 200, 'message': 'user is not present or not registered or not present in legal info'}, status=200)
        else:
            return Response({'status':204,'message':'Not present for this particular admin id'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['put'])
@permission_classes([AllowAny])
def admin_approved_from_verify(request):
    data=request.data
    adminid = data['adminid']
    userid = data['userid']
    try:
        adminobj=AdminRegister.objects.get(admin_id=adminid)
        if adminobj:
            regobjdata=SelfRegistration.objects.filter(id=userid).values()
            legaldoc = LegalDocuments.objects.filter(updated_by_id=userid).values()
            if regobjdata and legaldoc:
                regobj=SelfRegistration.objects.get(id=userid)
                if regobj.admin_approve=='Verified':
                    regobj.admin_approve='Approved'
                    regobj.save()
                    return Response({'status': 200, 'message': 'Admin verify changes to approved'}, status=200)
                else:
                    if regobj.admin_approve == 'Approved':
                        return Response({'status': 202, 'message': 'Admin Already Approved'}, status=202)
            else:
                return Response({'status': 200, 'message': 'user is not present or not registered or not present in legal info'}, status=200)
        else:
            return Response({'status':204,'message':'Not present for this particular admin id'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes([AllowAny])
def admin_pending_list(request):
    adminid=request.data['adminid']
    adminarray=[]
    try:
        regobj=SelfRegistration.objects.filter(admin_approve='Pending').values()
        print(len(regobj))
        if len(regobj)>0:
            for i in range(0,len(regobj)):
                basicobj=BasicCompanyDetails.objects.filter(updated_by_id=regobj[i].get('id')).values()
                if len(basicobj)>0:
                    adminarray.append({
                        "company_code":basicobj[0].get('company_code'),
                        "company_name":basicobj[0].get('company_name'),
                        "username":regobj[i].get('contact_person'),
                        "user_type": regobj[i].get('user_type'),
                        "email": regobj[i].get('username'),
                        "phone_number": regobj[i].get('phone_number'),
                        "nature_of_business": regobj[i].get('nature_of_business'),
                        "business_type": regobj[i].get('business_to_serve'),
                        "userid": regobj[i].get('id'),
                        "status":regobj[i].get('admin_approve')

                                       })
                else:
                    adminarray.append({
                        "company_code": "",
                        "company_name":"",
                        "username": regobj[i].get('contact_person'),
                        "user_type": regobj[i].get('user_type'),
                        "email": regobj[i].get('username'),
                        "phone_number": regobj[i].get('phone_number'),
                        "nature_of_business": regobj[i].get('nature_of_business'),
                        "business_type": regobj[i].get('business_to_serve'),
                        "userid": regobj[i].get('id'),
                        "status": regobj[i].get('admin_approve')
                    })

            return Response({'status': 200, 'message':'Pending List','data':adminarray}, status=200)
        else:
            return Response({'status': 204, 'message': 'data not present'}, status=204)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes([AllowAny])
def admin_approved_list(request):
    adminid = request.data['adminid']
    adminarray=[]
    try:
        regobj = SelfRegistration.objects.filter(admin_approve='Approved').values()
        print(len(regobj))
        if len(regobj) > 0:
            for i in range(0, len(regobj)):
                basicobj = BasicCompanyDetails.objects.filter(updated_by_id=regobj[i].get('id')).values()
                if len(basicobj) > 0:
                    adminarray.append({
                        "company_code": basicobj[0].get('company_code'),
                        "company_name": basicobj[0].get('company_name'),
                        "username": regobj[i].get('contact_person'),
                        "user_type": regobj[i].get('user_type'),
                        "email": regobj[i].get('username'),
                        "phone_number": regobj[i].get('phone_number'),
                        "nature_of_business": regobj[i].get('nature_of_business'),
                        "business_type": regobj[i].get('business_to_serve'),
                        "userid":regobj[i].get('id'),
                        "status": regobj[i].get('admin_approve')
                    })
                else:
                    adminarray.append({
                        "company_code": "",
                        "company_name": "",
                        "username": regobj[i].get('contact_person'),
                        "user_type": regobj[i].get('user_type'),
                        "email": regobj[i].get('username'),
                        "phone_number": regobj[i].get('phone_number'),
                        "nature_of_business": regobj[i].get('nature_of_business'),
                        "business_type": regobj[i].get('business_to_serve'),
                        "userid": regobj[i].get('id'),
                        "status": regobj[i].get('admin_approve')
                    })
            return Response({'status': 200, 'message': 'Approved List', 'data': adminarray}, status=200)
        else:
            return Response({'status': 200, 'message': 'No data is approved by admin', 'data': adminarray}, status=200)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes([AllowAny])
def admin_verified_list(request):
    adminid = request.data['adminid']
    adminarray=[]
    try:
        regobj = SelfRegistration.objects.filter(admin_approve='Verified').values()
        print(len(regobj))
        if len(regobj) > 0:
            for i in range(0, len(regobj)):
                basicobj = BasicCompanyDetails.objects.filter(updated_by_id=regobj[i].get('id')).values()
                if len(basicobj) > 0:
                    adminarray.append({
                        "company_code": basicobj[0].get('company_code'),
                        "company_name": basicobj[0].get('company_name'),
                        "username": regobj[i].get('contact_person'),
                        "user_type": regobj[i].get('user_type'),
                        "email": regobj[i].get('username'),
                        "phone_number": regobj[i].get('phone_number'),
                        "nature_of_business": regobj[i].get('nature_of_business'),
                        "business_type": regobj[i].get('business_to_serve'),
                        "userid": regobj[i].get('id'),
                        "status": regobj[i].get('admin_approve')
                    })
                else:
                    adminarray.append({
                        "company_code": "",
                        "company_name": "",
                        "username": regobj[i].get('contact_person'),
                        "user_type": regobj[i].get('user_type'),
                        "email": regobj[i].get('username'),
                        "phone_number": regobj[i].get('phone_number'),
                        "nature_of_business": regobj[i].get('nature_of_business'),
                        "business_type": regobj[i].get('business_to_serve'),
                        "userid": regobj[i].get('id'),
                        "status": regobj[i].get('admin_approve')
                    })
            return Response({'status': 200, 'message': 'Verified List', 'data': adminarray}, status=200)
        else:
            return Response({'status': 200, 'message': 'No data is verified by admin', 'data': adminarray}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)