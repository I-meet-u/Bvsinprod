
import math
import random
from base64 import b64encode
from datetime import datetime, date
from itertools import chain
from pprint import pprint

import sib_api_v3_sdk
from django.contrib.auth.hashers import make_password,check_password
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Q
from sib_api_v3_sdk.rest import ApiException

from MastersApp.models import CategoryMaster, SubCategoryMaster
from .serializers import *
from RegistrationApp.models import SelfRegistration, BasicCompanyDetails, IndustrialInfo, IndustrialHierarchy, \
    BankDetails, LegalDocuments, Employee_CompanyDetails, Employee_IndustryInfo, BillingAddress
from .models import *
from AdminApp.serializers import AdminInviteSerializer, CreateUserSerializer, AdminRegisterSerializer, \
    CreateBuyerSerializer, OpenLeadsRfqSerializer, OpenLeadsItemsSerializer, \
    BuyerProductDetailsAdminSerializer



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
    try:
        admin_obj = AdminRegister.objects.get(admin_email=admin_email)
        if admin_obj:
            if check_password(password, admin_obj.password) and admin_obj.admin_email == admin_email:
                admin_user_data = {
                    'adminemail': admin_obj.admin_email,
                    'super_admin_key':admin_obj.super_admin_key
                }
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
    super_admin_key=data['super_admin_key']
    email_otp=data['email_otp']
    admin_email=data['admin_email']
    try:
        adminobjverify=AdminRegister.objects.get(admin_email=admin_email)
        if adminobjverify.super_admin_key==super_admin_key:
            if adminobjverify.email_otp==email_otp:
                admin_data={
                    'admin_id':adminobjverify.admin_id
                }

                return Response({'status':200,'message':"Email OTP is verified","data":admin_data},status=200)
            else:
                return Response({'status': 204, 'message': "Email OTP is not correct"}, status=204)
        else:
            return Response({'status': 401, 'message': "Invalid Token or Authentication not Provided"}, status=401)
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


    def get_queryset(self):
        createuserobj=CreateUser.objects.filter(admins=self.request.GET.get('admins'))
        if not createuserobj:
            raise ValidationError({'message': 'Create User Details are not found', 'status': 204})
        return  createuserobj


@api_view(['put'])
def create_user_status_update(request):
    data=request.data
    id=data['id']
    super_admin_key=data['super_admin_key']
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


@api_view(['post'])
@permission_classes([AllowAny])
def registration_list(request):
    data=request.data
    super_admin_key=data['super_admin_key']
    emptydata=[]
    try:
        adminobj=AdminRegister.objects.filter().values()
        if adminobj[0].get('super_admin_key')==super_admin_key:
            # regobj=SelfRegistration.objects.filter(Q(user_type='Vendor') |Q(user_type='Buyer') | Q(user_type='Both')).values()
            regobj = SelfRegistration.objects.filter().values().order_by('id')
            for i in range(0, len(regobj)):
                x = regobj[i].get('id')
                basicobj = BasicCompanyDetails.objects.filter(updated_by=x).values()
                if basicobj:
                    industry_info = IndustrialInfo.objects.filter(updated_by=x).values()
                    if industry_info:
                        industry_hierarchy = IndustrialHierarchy.objects.filter(updated_by=x).values()
                        if industry_hierarchy:
                            legalobj = LegalDocuments.objects.filter(updated_by=x).values()
                            if legalobj:
                                emptydata.append({"id": x,
                                                  "company_code": basicobj[0].get('company_code'),
                                                  "company_name": basicobj[0].get('company_name'),
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
        else:
            return Response({'status': 401, 'message': 'Invalid Token or Authentication Not Provided'}, status=401)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['put'])
@permission_classes([AllowAny])
def admin_approval_from_pending(request):
    data=request.data
    super_admin_key = data['super_admin_key']
    adminid = data['adminid']
    userid = data['userid']
    try:
        adminobj=AdminRegister.objects.get(admin_id=adminid)
        if adminobj.super_admin_key==super_admin_key:
            if adminobj:
                regobjdata=SelfRegistration.objects.filter(Q(user_type='Vendor') |Q(user_type='Buyer') | Q(user_type='Both'),id=userid).values()
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
        else:
            return Response({'status': 401, 'message': 'Invalid Token or Authentication Not Provided'}, status=401)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['put'])
@permission_classes([AllowAny])
def admin_verify_from_pending(request):
    data=request.data
    super_admin_key = data['super_admin_key']
    adminid = data['adminid']
    userid = data['userid']
    try:
        adminobj=AdminRegister.objects.get(admin_id=adminid)
        if adminobj.super_admin_key==super_admin_key:
            if adminobj:
                regobjdata=SelfRegistration.objects.filter(Q(user_type='Vendor') |Q(user_type='Buyer') | Q(user_type='Both'),id=userid).values()
                legaldoc = LegalDocuments.objects.filter(updated_by_id=userid).values()
                if len(regobjdata)>0 and len(legaldoc)>0:
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
        else:
            return Response({'status': 401, 'message': 'Invalid Token or Authentication Not Provided'},status=401)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['put'])
@permission_classes([AllowAny])
def admin_approved_from_verify(request):
    data=request.data
    super_admin_key = data['super_admin_key']
    adminid = data['adminid']
    userid = data['userid']
    try:
        adminobj=AdminRegister.objects.get(admin_id=adminid)
        if adminobj.super_admin_key==super_admin_key:
            if adminobj:
                regobjdata=SelfRegistration.objects.filter(Q(user_type='Vendor') |Q(user_type='Buyer') | Q(user_type='Both'),id=userid).values()
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
        else:
            return Response({'status': 401, 'message': 'Invalid Token or Authentication Not Provided'}, status=401)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes([AllowAny])
def admin_pending_list(request):
    super_admin_key = request.data['super_admin_key']
    adminid=request.data['adminid']
    adminarray=[]
    try:
        adminobj=AdminRegister.objects.filter(admin_id=adminid).values()
        if adminobj[0].get('super_admin_key')==super_admin_key:
            regobj=SelfRegistration.objects.filter(Q(user_type='Vendor') |Q(user_type='Buyer') | Q(user_type='Both'),admin_approve='Pending').values().order_by('id')
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
                            "dateofreg":regobj[i].get('created_on'),
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
                            "dateofreg": regobj[i].get('created_on'),
                            "userid": regobj[i].get('id'),
                            "status": regobj[i].get('admin_approve')
                        })

                return Response({'status': 200, 'message':'Pending List','data':adminarray}, status=200)
            else:
                return Response({'status': 204, 'message': 'data not present'}, status=204)
        else:
            return Response({'status': 401, 'message': 'Invalid Token or Authentication Not Provided'}, status=401)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes([AllowAny])
def admin_approved_list(request):
    super_admin_key = request.data['super_admin_key']
    adminid = request.data['adminid']
    adminarray=[]
    try:
        adminobj = AdminRegister.objects.filter(admin_id=adminid).values()
        if adminobj[0].get('super_admin_key') == super_admin_key:
            regobj = SelfRegistration.objects.filter(Q(user_type='Vendor') |Q(user_type='Buyer') | Q(user_type='Both'),admin_approve='Approved').values().order_by('id')
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
                            "status": regobj[i].get('admin_approve'),
                            "setupstatus":regobj[i].get('setupstatus'),
                            "subscriptionflag":regobj[i].get('subscriptionflag')

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
                            "status": regobj[i].get('admin_approve'),
                            "setupstatus": regobj[i].get('setupstatus'),
                            "subscriptionflag": regobj[i].get('subscriptionflag')
                        })
                return Response({'status': 200, 'message': 'Approved List', 'data': adminarray}, status=200)
            else:
                return Response({'status': 204,'message': 'No data is approved by admin', 'data': adminarray}, status=204)
        else:
            return Response({'status': 401, 'message': 'Invalid Token or Authentication Not Provided'}, status=401)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes([AllowAny])
def admin_verified_list(request):
    super_admin_key=request.data['super_admin_key']
    adminid = request.data['adminid']
    adminarray=[]
    try:
        adminobj = AdminRegister.objects.filter(admin_id=adminid).values()
        if adminobj[0].get('super_admin_key') == super_admin_key:
            regobj = SelfRegistration.objects.filter(Q(user_type='Vendor') |Q(user_type='Buyer') | Q(user_type='Both'),admin_approve='Verified').values().order_by('id')
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
                return Response({'status': 204, 'message': 'No data is verified by admin', 'data': adminarray}, status=204)
        else:
            return Response({'status': 401, 'message': 'Invalid Token or Authentication Not Provided'}, status=401)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes([AllowAny])
def employee_all_list(request):
    data=request.data
    super_admin_key = data['super_admin_key']
    emptydata=[]
    try:
        adminobj = AdminRegister.objects.filter().values()
        if adminobj[0].get('super_admin_key') == super_admin_key:
            regobj=SelfRegistration.objects.filter(Q(user_type='Employee') |Q(user_type='Employer')).values().order_by('id')
            print(len(regobj))
            if len(regobj)>0:
                for i in range(0,len(regobj)):
                    userval=regobj[i].get('id')
                    print(userval)
                    empbasicobj = Employee_CompanyDetails.objects.filter(emp_updated_by_id=userval).values()
                    if empbasicobj:
                        industry_info = Employee_IndustryInfo.objects.filter(emp_updated_by_id=userval).values()
                        if industry_info:
                            emptydata.append({"id": userval,
                                              "user_type": regobj[i].get('user_type'),
                                              "username":regobj[i].get('contact_person'),
                                              "emp_company_code": empbasicobj[0].get('emp_company_code'),
                                              "emp_company_name": empbasicobj[0].get('emp_company_name'),
                                              "email": regobj[i].get('username'),
                                              "phone_number": regobj[i].get('phone_number'),
                                              "department": regobj[i].get('department'),
                                              "designation": regobj[i].get('designation'),
                                              "registration_status": "Registration Completed"})

                        else:
                            emptydata.append({"id":userval,
                                              "user_type": regobj[i].get('user_type'),
                                              "username": regobj[i].get('contact_person'),
                                              "emp_company_code": empbasicobj[0].get('emp_company_code'),
                                              "emp_company_name": empbasicobj[0].get('emp_company_name'),
                                              "email": regobj[i].get('username'),
                                              "phone_number": regobj[i].get('phone_number'),
                                              "department": regobj[i].get('department'),
                                              "designation": regobj[i].get('designation'),
                                              "registration_status": "Basic Info Details Completed"})

                    else:
                        emptydata.append({"id": userval,
                                          "user_type":regobj[i].get('user_type'),
                                          "username": regobj[i].get('contact_person'),
                                          "emp_company_code": "",
                                          "emp_company_name": "",
                                          "email": regobj[i].get('username'),
                                          "phone_number": regobj[i].get('phone_number'),
                                          "department": regobj[i].get('department'),
                                          "designation": regobj[i].get('designation'),
                                          "registration_status": "Upto Registration or Only in Registration"
                                          })
                return Response({'status': 200, 'message':'Employee and Employer Details','data':emptydata}, status=200)
            else:
                return Response({'status': 204, 'message': 'No data with this id'}, status=204)
        else:
            return Response({'status': 401, 'message': 'Invalid Token or Authentication Not Provided'}, status=401)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['post'])
@permission_classes([AllowAny])
def employee_pending_list(request):
    super_admin_key=request.data['super_admin_key']
    emp_pending_array=[]
    try:
        adminobj = AdminRegister.objects.filter().values()
        if adminobj[0].get('super_admin_key') == super_admin_key:
            regobj=SelfRegistration.objects.filter(Q(user_type='Employee')|Q(user_type='Employer'),admin_approve='Pending').values().order_by('id')
            print(len(regobj))
            if len(regobj)>0:
                for i in range(0,len(regobj)):
                    empbasicobj=Employee_CompanyDetails.objects.filter(emp_updated_by_id=regobj[i].get('id')).values()
                    if len(empbasicobj)>0:
                        emp_pending_array.append({
                            "emp_company_code":empbasicobj[0].get('emp_company_code'),
                            "emp_company_name":empbasicobj[0].get('emp_company_name'),
                            "username":regobj[i].get('contact_person'),
                            "user_type": regobj[i].get('user_type'),
                            "email": regobj[i].get('username'),
                            "phone_number": regobj[i].get('phone_number'),
                            "department": regobj[i].get('department'),
                            "designation": regobj[i].get('designation'),
                            "userid": regobj[i].get('id'),
                            "status":regobj[i].get('admin_approve')

                                           })
                    else:
                        emp_pending_array.append({
                            "emp_company_code": "",
                            "emp_company_name":"",
                            "username": regobj[i].get('contact_person'),
                            "user_type": regobj[i].get('user_type'),
                            "email": regobj[i].get('username'),
                            "phone_number": regobj[i].get('phone_number'),
                            "department": regobj[i].get('department'),
                            "designation": regobj[i].get('designation'),
                            "userid": regobj[i].get('id'),
                            "status": regobj[i].get('admin_approve')
                        })

                return Response({'status': 200, 'message':'Employee Pending List','data':emp_pending_array}, status=200)
            else:
                return Response({'status': 204, 'message': 'No Pending data for Employee or Employer'}, status=204)
        else:
            return Response({'status': 401, 'message': 'Invalid Token or Authentication Not Provided'},status=401)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes([AllowAny])
def employee_approved_list(request):
    super_admin_key = request.data['super_admin_key']
    employeeapprovedlist=[]
    try:
        adminobj = AdminRegister.objects.filter().values()
        if adminobj[0].get('super_admin_key') == super_admin_key:
            regobj = SelfRegistration.objects.filter(Q(user_type='Employee')|Q(user_type='Employer'),admin_approve='Approved').values().order_by('id')
            print(len(regobj))
            if len(regobj) > 0:
                for i in range(0, len(regobj)):
                    empbasicobj = Employee_CompanyDetails.objects.filter(emp_updated_by_id=regobj[i].get('id')).values()
                    if len(empbasicobj) > 0:
                        employeeapprovedlist.append({
                            "emp_company_code": empbasicobj[0].get('emp_company_code'),
                            "emp_company_name": empbasicobj[0].get('emp_company_name'),
                            "username": regobj[i].get('contact_person'),
                            "user_type": regobj[i].get('user_type'),
                            "email": regobj[i].get('username'),
                            "phone_number": regobj[i].get('phone_number'),
                            "department": regobj[i].get('department'),
                            "designation": regobj[i].get('designation'),
                            "userid":regobj[i].get('id'),
                            "status": regobj[i].get('admin_approve')
                        })
                    else:
                        employeeapprovedlist.append({
                            "emp_company_code": "",
                            "emp_company_name": "",
                            "username": regobj[i].get('contact_person'),
                            "user_type": regobj[i].get('user_type'),
                            "email": regobj[i].get('username'),
                            "phone_number": regobj[i].get('phone_number'),
                            "department": regobj[i].get('department'),
                            "designation": regobj[i].get('designation'),
                            "userid": regobj[i].get('id'),
                            "status": regobj[i].get('admin_approve')
                        })
                return Response({'status': 200, 'message': 'Employee Approved List', 'data': employeeapprovedlist}, status=200)
            else:
                return Response({'status': 204, 'message': 'No approved data for Employee or Employer', 'data': employeeapprovedlist}, status=204)
        else:
            return Response({'status': 401, 'message': 'Invalid Token or Authentication Not Provided'}, status=401)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes([AllowAny])
def employee_verified_list(request):
    super_admin_key = request.data['super_admin_key']
    adminarray=[]
    try:
        adminobj = AdminRegister.objects.filter().values()
        if adminobj[0].get('super_admin_key') == super_admin_key:
            regobj = SelfRegistration.objects.filter(Q(user_type='Employee')|Q(user_type='Employer'),admin_approve='Verified').values().order_by('id')
            print(len(regobj))
            if len(regobj) > 0:
                for i in range(0, len(regobj)):
                    empbasicobj = Employee_CompanyDetails.objects.filter(emp_updated_by_id=regobj[i].get('id')).values()
                    if len(empbasicobj) > 0:
                        adminarray.append({
                            "emp_company_code": empbasicobj[0].get('emp_company_code'),
                            "emp_company_name": empbasicobj[0].get('emp_company_name'),
                            "username": regobj[i].get('contact_person'),
                            "user_type": regobj[i].get('user_type'),
                            "email": regobj[i].get('username'),
                            "phone_number": regobj[i].get('phone_number'),
                            "department": regobj[i].get('department'),
                            "designation": regobj[i].get('designation'),
                            "userid": regobj[i].get('id'),
                            "status": regobj[i].get('admin_approve')
                        })
                    else:
                        adminarray.append({
                            "emp_company_code": "",
                            "emp_company_name": "",
                            "username": regobj[i].get('contact_person'),
                            "user_type": regobj[i].get('user_type'),
                            "email": regobj[i].get('username'),
                            "phone_number": regobj[i].get('phone_number'),
                             "department": regobj[i].get('department'),
                            "designation": regobj[i].get('designation'),
                            "userid": regobj[i].get('id'),
                            "status": regobj[i].get('admin_approve')
                        })
                return Response({'status': 200, 'message': 'Employee Verified List', 'data': adminarray}, status=200)
            else:
                return Response({'status': 200, 'message': 'No verified data for Employee or Employer', 'data': adminarray}, status=200)
        else:
            return Response({'status': 401, 'message': 'Invalid Token or Authentication Not Provided'}, status=401)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['put'])
@permission_classes([AllowAny])
def employee_status_update_from_pending_to_approved(request):
    data=request.data
    super_admin_key = request.data['super_admin_key']
    adminid = data['adminid']
    userid = data['userid']
    try:
        adminval=AdminRegister.objects.filter().values()
        if adminval[0].get('super_admin_key') == super_admin_key:
            adminobj = AdminRegister.objects.get(admin_id=adminid)
            if adminobj:
                regobjdata=SelfRegistration.objects.filter(Q(user_type='Employee')|Q(user_type='Employer'),id=userid).values()
                employeeobj=Employee_IndustryInfo.objects.filter(emp_updated_by_id=userid).values()
                if regobjdata and employeeobj:
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
                    return Response({'status': 200, 'message': 'user is not present or not registered or not present in industry info'}, status=200)
            else:
                return Response({'status':204,'message':'Admin Data Not Present for this Id'},status=204)
        else:
            return Response({'status': 401, 'message': 'Invalid Token or Authentication Not Provided'}, status=401)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['put'])
@permission_classes([AllowAny])
def employee_status_update_from_pending_to_verified(request):
    data=request.data
    super_admin_key=data['super_admin_key']
    adminid = data['adminid']
    userid = data['userid']
    try:
        adminobj = AdminRegister.objects.filter().values()
        if adminobj[0].get('super_admin_key') == super_admin_key:
            adminobj=AdminRegister.objects.get(admin_id=adminid)
            if adminobj.super_admin_key == super_admin_key:
                regobjdata=SelfRegistration.objects.filter(Q(user_type='Employee')|Q(user_type='Employer'),id=userid).values()
                employeeobj=Employee_IndustryInfo.objects.filter(emp_updated_by_id=userid).values()
                if regobjdata and employeeobj:
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
                    return Response({'status': 200, 'message': 'user is not present or not registered or not present in pending info'}, status=200)
            else:
                return Response({'status':204,'message':'Not present for this particular admin id'},status=204)
        else:
            return Response({'status': 401, 'message': 'Invalid Token or Authentication Not Provided'}, status=401)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['put'])
@permission_classes([AllowAny])
def employee_status_update_from_verify_to_approved(request):
    data=request.data
    super_admin_key=data['super_admin_key']
    adminid = data['adminid']
    userid = data['userid']
    try:
        adminobj = AdminRegister.objects.filter().values()
        if adminobj[0].get('super_admin_key') == super_admin_key:
            adminobj=AdminRegister.objects.get(admin_id=adminid)
            if adminobj.super_admin_key==super_admin_key:
                regobjdata=SelfRegistration.objects.filter(Q(user_type='Employee')|Q(user_type='Employer'),id=userid).values()
                employeeobj=Employee_IndustryInfo.objects.filter(emp_updated_by_id=userid).values()
                if regobjdata and employeeobj:
                    regobj=SelfRegistration.objects.get(id=userid)
                    if regobj.admin_approve=='Verified':
                        regobj.admin_approve='Approved'
                        regobj.save()
                        return Response({'status': 200, 'message': 'Admin Approved'}, status=200)
                    else:
                        if regobj.admin_approve == 'Approved':
                            return Response({'status': 202, 'message': 'Admin Already Approved'}, status=202)
                        elif regobj.admin_approve == 'Verified':
                            return Response({'status': 202, 'message': 'Admin Already Verified'}, status=202)
                else:
                    return Response({'status': 200, 'message': 'user is not present or not registered or not present in industry info'}, status=200)
            else:
                return Response({'status':204,'message':'Not present for this particular admin id'},status=204)
        else:
            return Response({'status': 401, 'message': 'Invalid Token or Authentication Not Provided'}, status=401)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)





@api_view(['post'])
@permission_classes([AllowAny])
def company_registration_list(request):
    data=request.data
    super_admin_key=data['super_admin_key']
    emptydata=[]
    try:
        adminobj = AdminRegister.objects.filter().values()
        if adminobj[0].get('super_admin_key') == super_admin_key:
            regobj=SelfRegistration.objects.filter(Q(user_type='Vendor') |Q(user_type='Buyer') | Q(user_type='Both')).values().order_by('id')
            for i in range(0, len(regobj)):
                x = regobj[i].get('id')
                basicobj = BasicCompanyDetails.objects.filter(updated_by=x).values()
                if basicobj:
                    industry_info = IndustrialInfo.objects.filter(updated_by=x).values()
                    if industry_info:
                        industry_hierarchy = IndustrialHierarchy.objects.filter(updated_by=x).values()
                        if industry_hierarchy:
                            legalobj = LegalDocuments.objects.filter(updated_by=x).values()
                            if legalobj:
                                emptydata.append({"id": x,
                                                  "company_code": basicobj[0].get('company_code'),
                                                  "company_name": basicobj[0].get('company_name'),
                                                  "username": regobj[i].get('contact_person'),
                                                  "user_type": regobj[i].get('user_type'),
                                                  "email": regobj[i].get('username'),
                                                  "phone_number": regobj[i].get('phone_number'),
                                                  "nature_of_business": regobj[i].get('nature_of_business'),
                                                  "business_type": regobj[i].get('business_to_serve'),
                                                  "setupstatus":regobj[i].get('setupstatus'),
                                                  "setupdate":regobj[i].get('setupdate'),
                                                  "subcriptionstatus":regobj[i].get('subscriptionflag'),
                                                  "adminapprove": regobj[i].get('admin_approve'),
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
                                                  "setupstatus": regobj[i].get('setupstatus'),
                                                  "setupdate": regobj[i].get('setupdate'),
                                                  "subcriptionstatus": regobj[i].get('subscriptionflag'),
                                                  "adminapprove": regobj[i].get('admin_approve'),
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
                                              "setupstatus": regobj[i].get('setupstatus'),
                                              "setupdate": regobj[i].get('setupdate'),
                                              "subcriptionstatus": regobj[i].get('subscriptionflag'),
                                              "adminapprove":regobj[i].get('admin_approve'),
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
                                          "setupstatus": regobj[i].get('setupstatus'),
                                          "setupdate": regobj[i].get('setupdate'),
                                          "subcriptionstatus": regobj[i].get('subscriptionflag'),
                                          "adminapprove": regobj[i].get('admin_approve'),
                                          "registration_status": "company details"})

            return Response({'status': 200, 'message': 'ok', 'data': emptydata}, status=200)
        else:
            return Response({'status': 401, 'message': 'Invalid Token or Authentication Not Provided'},
                                    status=401)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['put'])
@permission_classes([AllowAny])
def employee_status_update_from_pending_to_reject(request):
    data=request.data
    super_admin_key=data['super_admin_key']
    adminid = data['adminid']
    userid = data['userid']
    try:
        adminobj = AdminRegister.objects.filter().values()
        if adminobj[0].get('super_admin_key') == super_admin_key:
            adminobj=AdminRegister.objects.get(admin_id=adminid)
            if adminobj.super_admin_key==super_admin_key:
                regobjdata=SelfRegistration.objects.filter(Q(user_type='Employee')|Q(user_type='Employer'),id=userid).values()
                if regobjdata:
                    regobj=SelfRegistration.objects.get(id=userid)
                    if regobj.admin_approve=='Pending':
                        regobj.admin_approve='Reject'
                        regobj.save()
                        return Response({'status': 200, 'message': 'Admin Rejected'}, status=200)
                    else:
                        if regobj.admin_approve == 'Reject':
                            return Response({'status': 202, 'message': 'Admin Already Rejected'}, status=202)
                        elif regobj.admin_approve!='Pending':
                            return Response({'status': 202, 'message': 'Pending Data Not Present'}, status=202)
                else:
                    return Response({'status': 200, 'message': 'user is not present or not registered or not present'}, status=200)
            else:
                return Response({'status':204,'message':'Admin Data Not Present for this Id'},status=204)
        else:
            return Response({'status': 401, 'message': 'Invalid Token or Authentication Not Provided'}, status=401)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['put'])
@permission_classes([AllowAny])
def admin_update_from_pending_to_reject(request):
    data=request.data
    super_admin_key = data['super_admin_key']
    adminid = data['adminid']
    userid = data['userid']
    try:
        adminobj=AdminRegister.objects.get(admin_id=adminid)
        if adminobj.super_admin_key==super_admin_key:
            regobjdata=SelfRegistration.objects.filter(Q(user_type='Vendor') |Q(user_type='Buyer') | Q(user_type='Both'),id=userid).values()
            if regobjdata:
                regobj=SelfRegistration.objects.get(id=userid)
                if regobj.admin_approve=='Pending':
                    regobj.admin_approve='Reject'
                    regobj.save()
                    return Response({'status': 200, 'message': 'Admin Rejected'}, status=200)
                else:
                    if regobj.admin_approve=='Reject':
                        return Response({'status': 202, 'message': 'Admin Already Rejected'}, status=202)
                    elif regobj.admin_approve!="Pending":
                        return Response({'status': 202, 'message': 'Pending data is not present'}, status=202)
            else:
                return Response({'status': 200, 'message': 'user is not present or not registered'}, status=200)
        else:
            return Response({'status':204,'message':'Not present for this particular admin id'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['post'])
@permission_classes([AllowAny])
def admin_rejected_list(request):
    # adminid = request.data['adminid']
    super_admin_key =request.data['super_admin_key']
    adminarray=[]
    try:
        adminval = AdminRegister.objects.filter().values()
        if adminval[0].get('super_admin_key') == super_admin_key:
            regobj = SelfRegistration.objects.filter(Q(user_type='Vendor') |Q(user_type='Buyer') | Q(user_type='Both'),admin_approve='Reject').values().order_by('id')
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
                return Response({'status': 200, 'message': 'Rejected List', 'data': adminarray}, status=200)
            else:
                return Response({'status': 204, 'message': 'No data is rejected by admin', 'data': adminarray}, status=204)
        else:
            return Response({'status': 401, 'message': 'Invalid Token or Authentication Not Provided'}, status=401)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes([AllowAny])
def employee_rejected_list(request):
    super_admin_key = request.data['super_admin_key']
    # adminid = request.data['adminid']
    adminarray=[]
    try:
        adminobj = AdminRegister.objects.filter().values()
        if adminobj[0].get('super_admin_key') == super_admin_key:
            regobj = SelfRegistration.objects.filter(Q(user_type='Employee')|Q(user_type='Employer'),admin_approve='Reject').values().order_by('id')
            print(len(regobj))
            if len(regobj) > 0:
                for i in range(0, len(regobj)):
                    empbasicobj = Employee_CompanyDetails.objects.filter(emp_updated_by_id=regobj[i].get('id')).values()
                    if len(empbasicobj) > 0:
                        adminarray.append({
                            "emp_company_code": empbasicobj[0].get('emp_company_code'),
                            "emp_company_name": empbasicobj[0].get('emp_company_name'),
                            "username": regobj[i].get('contact_person'),
                            "user_type": regobj[i].get('user_type'),
                            "email": regobj[i].get('username'),
                            "phone_number": regobj[i].get('phone_number'),
                            "department": regobj[i].get('department'),
                            "designation": regobj[i].get('designation'),
                            "userid": regobj[i].get('id'),
                            "status": regobj[i].get('admin_approve')
                        })
                    else:
                        adminarray.append({
                            "emp_company_code": "",
                            "emp_company_name": "",
                            "username": regobj[i].get('contact_person'),
                            "user_type": regobj[i].get('user_type'),
                            "email": regobj[i].get('username'),
                            "phone_number": regobj[i].get('phone_number'),
                             "department": regobj[i].get('department'),
                            "designation": regobj[i].get('designation'),
                            "userid": regobj[i].get('id'),
                            "status": regobj[i].get('admin_approve')
                        })
                return Response({'status': 200, 'message': 'Rejected List', 'data': adminarray}, status=200)
            else:
                return Response({'status': 200, 'message': 'No rejected data for Employee or Employer', 'data': adminarray}, status=200)
        else:
            return Response({'status': 401, 'message': 'Invalid Token or Authentication Not Provided'}, status=401)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def add_data_based_on_user_type_to_create_user(request):
    data=request.data
    super_admin_key=data['super_admin_key']
    userid=data['userid']
    try:
        adminobj = AdminRegister.objects.filter().values()
        if adminobj[0].get('super_admin_key') == super_admin_key:
            regobjdata = SelfRegistration.objects.filter(id=userid,admin_approve='Approved').values()
            if len(regobjdata)>0:
                if regobjdata[0].get('user_type')=='Vendor':
                    regvalue=SelfRegistration.objects.get(user_type='Vendor',id=userid)
                    if regvalue:
                        CreateUser.objects.create(contact_name=regvalue.contact_person,
                                                  user_type=regvalue.user_type,
                                                  country=regvalue.country,
                                                  business_to_serve=regvalue.business_to_serve,
                                                  nature_of_business=regvalue.nature_of_business,
                                                  mobile=regvalue.phone_number,
                                                  email=regvalue.username,
                                                  admins=AdminRegister.objects.get(admin_id=1),
                                                  created_by=userid,
                                                  updated_by=SelfRegistration.objects.get(id=userid)



                                                  )
                        return Response({'status': 200, 'message': 'Vendor Data added to create user'}, status=200)
                elif regobjdata[0].get('user_type')=='Buyer':
                    regvalue=SelfRegistration.objects.get(user_type='Buyer',id=userid)
                    if regvalue:
                        CreateUser.objects.create(contact_name=regvalue.contact_person,
                                                  user_type=regvalue.user_type,
                                                  country=regvalue.country,
                                                  business_to_serve=regvalue.business_to_serve,
                                                  nature_of_business=regvalue.nature_of_business,
                                                  mobile=regvalue.phone_number,
                                                  email=regvalue.username,
                                                  admins=AdminRegister.objects.get(admin_id=1),
                                                  created_by=userid,
                                                  updated_by=SelfRegistration.objects.get(id=userid)




                                                  )
                    return Response({'status': 200, 'message': 'Buyer Data added to create user'}, status=200)
                elif regobjdata[0].get('user_type') == 'Both':
                    regvalue = SelfRegistration.objects.get(user_type='Both', id=userid)
                    if regvalue:
                        CreateUser.objects.create(contact_name=regvalue.contact_person,
                                                  user_type=regvalue.user_type,
                                                  country=regvalue.country,
                                                  business_to_serve=regvalue.business_to_serve,
                                                  nature_of_business=regvalue.nature_of_business,
                                                  mobile=regvalue.phone_number,
                                                  email=regvalue.username,
                                                  admins=AdminRegister.objects.get(admin_id=1),
                                                  created_by=userid,
                                                  updated_by=SelfRegistration.objects.get(id=userid)

                                                  )
                    return Response({'status': 200, 'message': 'Both Data added to create user'}, status=200)
                else:
                    return Response({'status': 202, 'message': 'user type not present'}, status=204)
            else:
                return Response({'status':204,'message':'Not Present'},status=204)
        else:
            return Response({'status': 401, 'message': 'Invalid Token or Authentication Not Provided'}, status=401)



    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



class CreateBuyerView(viewsets.ModelViewSet):
    queryset = CreateBuyer.objects.all()
    serializer_class = CreateBuyerSerializer
    permission_classes = (AllowAny,)


    # def create(self, request, *args, **kwargs):
    #     token = request.data.get('token', None)
    #     if token == "4aoedpde123Vyeyweuo2":
    #         return super().create(request, *args, **kwargs)
    #     else:
    #         return Response({'status': 401, 'message': 'UnAuthorized'}, status=401)

    def get_queryset(self):
        createbuyerobj=CreateBuyer.objects.filter(admins=self.request.GET.get('admins'))
        if not createbuyerobj:
            raise ValidationError({'message': 'Create Buyer Details are not found', 'status': 204})
        return  createbuyerobj


class OpenLeadsRfqViewSet(viewsets.ModelViewSet):
    permission_classes = ((AllowAny,))
    queryset = OpenLeadsRfq.objects.all()
    serializer_class = OpenLeadsRfqSerializer

    def create(self, request, *args, **kwargs):
        token = request.data.get('token', None)
        if token == "4aoedpde123Vyeyweuo2":
            return super().create(request, *args, **kwargs)
        else:
            return Response({'status': 401, 'message': 'UnAuthorized'}, status=401)

    def get_queryset(self):
        openleadsobj=OpenLeadsRfq.objects.filter(admins=self.request.GET.get('admins')).order_by('id')
        if not openleadsobj:
            raise ValidationError({'message': 'Create Open Leads Details are not found', 'status': 204})
        return openleadsobj

class OpenLeadsItemsViewSet(viewsets.ModelViewSet):
    queryset = OpenLeadsItems.objects.all()
    serializer_class = OpenLeadsItemsSerializer
    permission_classes = ((AllowAny,))

    def create(self, request, *args, **kwargs):
        itemsarray=request.data['itemsarray']
        admins=request.data.get('admins',None)
        open_leads_pk=request.data.get('open_leads_pk',None)
        buyer_company_code =request.data.get('buyer_company_code',None)
        buyer_company_name = request.data.get('buyer_company_name',None)
        token = request.data.get('token', None)
        rfq_number=request.data.get('rfq_number',None)
        # buyer_pk =request.data.get('buyer_pk',None)
        try:
            if token == "4aoedpde123Vyeyweuo2":
                for i in range(0,len(itemsarray)):
                    openleadsitemsobj=OpenLeadsItems.objects.create(item_code=itemsarray[i].get('item_code'),
                                                                    item_name=itemsarray[i].get('item_name'),
                                                                    item_description=itemsarray[i].get('item_description'),
                                                                    item_type=itemsarray[i].get('item_type'),
                                                                    uom=itemsarray[i].get('uom'),
                                                                    quantity=itemsarray[i].get('quantity'),
                                                                    dcouments=itemsarray[i].get('documents'),
                                                                    admins=AdminRegister.objects.get(admin_id=admins),
                                                                    open_leads_pk=OpenLeadsRfq.objects.get(id=open_leads_pk),
                                                                    buyer_company_code=buyer_company_code,
                                                                    buyer_company_name=buyer_company_name,
                                                                    rfq_number=rfq_number
                                                                    )
                return Response({'status': 201, 'message': 'Open Leads Items are created'}, status=201)
            else:
                return Response({'status': 401, 'message': 'UnAuthorized'}, status=401)
        except Exception as e:
            return Response({'status':500,'error':str(e)},status=500)


class OpenLeadsTermsDescriptionViewSet(viewsets.ModelViewSet):
    queryset = OpenLeadsTermsDescription.objects.all()
    serializer_class = OpenLeadsTermsDescriptionSerializer
    permission_classes = ((AllowAny,))

    def create(self, request, *args, **kwargs):
        rfq_number = request.data['rfq_number']
        termsqueries = request.data['termsqueries']
        print(type(termsqueries))
        open_leads_pk = request.data.get('open_leads_pk', None)
        rfq_type = request.data.get('rfq_type', None)
        admins = request.data.get('admins', None)
        buyer_company_code = request.data.get('buyer_company_code', None)
        buyer_company_name = request.data.get('buyer_company_name', None)
        buyer_pk = request.data.get('buyer_pk', None)
        token = request.data.get('token', None)
        try:
            if token == "4aoedpde123Vyeyweuo2":
                for i in range(0, len(termsqueries)):
                    for keys in termsqueries[i]:
                        OpenLeadsTermsDescription.objects.create(rfq_number=rfq_number,
                                                                 terms=keys,
                                                                 description=termsqueries[i][keys],
                                                                 open_leads_pk=OpenLeadsRfq.objects.get(id=open_leads_pk),
                                                                 admins=AdminRegister.objects.get(admin_id=admins),
                                                                 rfq_type=rfq_type,
                                                                 buyer_company_code=buyer_company_code,
                                                                 buyer_company_name=buyer_company_name,
                                                                 buyer_pk=CreateBuyer.objects.get(id=buyer_pk)

                                                                 )

                return Response({'status': 201, 'message': 'Open Leads Terms and Descriptions are created'}, status=201)
            else:
                return Response({'status': 401, 'message': 'UnAuthorized'}, status=401)
        except Exception as e:
            return Response({'status': 500, 'message': str(e)}, status=500)


# class OpenLeadsPublishViewSet(viewsets.ModelViewSet):
#     queryset = OpenLeadsPublish.objects.all()
#     serializer_class = OpenLeadsPublishSerializer
#     permission_classes = ((AllowAny,))
#
#     def create(self, request, *args, **kwargs):
#         token=request.data.get('token',None)
#         if token=="4aoedpde123Vyeyweuo2":
#             return super().create(request, *args, **kwargs)
#         else:
#             return Response({'status':401,'message':'UnAuthorized'},status=401)


@api_view(['get'])
def get_all_open_bids_vendors(request):
    try:
        openobj=OpenLeadsRfq.objects.filter().values()
        if len(openobj)>0:
            return Response({'status': 200, 'message': 'ok','data':openobj}, status=200)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=204)

    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def get_all_buyers(request):
    data=request.data
    token=data['token']
    try:
        if token == "4aoedpde123Vyeyweuo2":
            getbuyerobj=CreateBuyer.objects.filter().values().order_by('id')
            if len(getbuyerobj)>0:
                return Response({'status': 200, 'message': 'Buyers List', 'data': getbuyerobj}, status=200)
            else:
                return Response({'status': 204, 'message': 'Buyer Lists are not present'}, status=204)
        else:
            return Response({'status': 401, 'message': 'UnAuthorized'}, status=401)
    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)


class BuyerProductDetailsAdminViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = BuyerProductDetailsAdmin.objects.all()
    serializer_class = BuyerProductDetailsAdminSerializer

    def create(self, request, *args, **kwargs):
        token=request.data.get('token',None)
        item_type=request.data.get('item_type',None)
        item_name=request.data.get('item_name',None)
        item_description=request.data.get('item_description',None)
        uom=request.data.get('uom',None)
        hsn_sac = request.data.get('hsn_sac',None)
        unit_price = request.data.get('unit_price',None)
        category = request.data.get('category',None)
        department = request.data.get('department',None)
        item_group = request.data.get('item_group',None)
        safety_stock=request.data.get('safety_stock',None)
        # annual_consumption = request.data.get('annual_consumption',None)
        # safety_stock = request.data.get('safety_stock',None)
        # model_no = request.data.get('model_no',None)
        document1 = request.data.get('document1',None)
        document2 = request.data.get('document2', None)
        document3 = request.data.get('document3', None)
        additional_specifications = request.data.get('additional_specifications',None)
        # add_product_supplies = request.data.get('buyer_add_product_supplies',None)
        admins = request.data.get('admins',None)
        try:
            if token=="4aoedpde123Vyeyweuo2":
                buyerproductobj = BuyerProductDetailsAdmin.objects.filter(admins=admins).order_by('-numeric').values()
                if len(buyerproductobj)==0:
                    print("data not exist")
                    buyerobj = BuyerProductDetailsAdmin.objects.create(item_type=item_type,
                                                                  prefix="MAT",
                                                                  suffix="",
                                                                  numeric=5101102,
                                                                  item_code="MAT"+""+str(5101101),
                                                                  item_name=item_name,
                                                                  item_description=item_description,
                                                                  uom=uom,
                                                                  hsn_sac=hsn_sac,
                                                                  unit_price=unit_price,
                                                                  category=category,
                                                                  department=department,
                                                                  item_group=item_group,
                                                                  safety_stock=safety_stock,
                                                                  document1=document1,
                                                                  document2=document2,
                                                                  document3=document3,
                                                                  admins=AdminRegister.objects.get(admin_id=admins),
                                                                  additional_specifications=additional_specifications)
                else:
                    print('already present')
                    print(buyerproductobj[0].get('prefix'))
                    print(int(buyerproductobj[0].get('numeric'))+1,'pl')
                    print(buyerproductobj[0].get('numeric'))
                    buyerobj = BuyerProductDetailsAdmin.objects.create(item_type=item_type,
                                                                       prefix=buyerproductobj[0].get('prefix'),
                                                                       suffix=buyerproductobj[0].get('suffix'),
                                                                       numeric=int(buyerproductobj[0].get('numeric'))+1,
                                                                       item_code=buyerproductobj[0].get('prefix') + buyerproductobj[0].get('suffix')+buyerproductobj[0].get('numeric'),
                                                                       item_name=item_name,
                                                                       item_description=item_description,
                                                                       uom=uom,
                                                                       hsn_sac=hsn_sac,
                                                                       unit_price=unit_price,
                                                                       category=category,
                                                                       department=department,
                                                                       item_group=item_group,
                                                                       document1=document1,
                                                                       document2=document2,
                                                                       document3=document3,
                                                                       admins=AdminRegister.objects.get(admin_id=admins),
                                                                       safety_stock=safety_stock,
                                                                       additional_specifications=additional_specifications)


                return Response({'status':201,'message':'Buyer Product Created'},status=201)
            else:
                return Response({'status': 401, 'message': 'UnAuthorized'}, status=401)
        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes([AllowAny,])
def getbuyeraddedadminbyccode(request):
    data=request.data
    key=data['key']
    try:
        if key=="vsinadmindb":
            CreateBuyerobj=CreateBuyer.objects.filter(company_code=data['companycode']).values()
            return Response({'status': 200, 'message': 'ok','data':CreateBuyerobj}, status=200)
        else:
            return Response({'status': 400, 'message': 'bad request'}, status=400)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def fetch_all_buyer_product_details(request):
    key = request.data['key']
    try:
        if key == "vsinadmindb":
            getbuyerproductobj=BuyerProductDetailsAdmin.objects.filter().values().order_by('product_id')
            if len(getbuyerproductobj)>0:
                return Response({'status': 200, 'message': 'Buyer Product Details List', 'data': getbuyerproductobj}, status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)

        else:
            return Response({'status': 400, 'message': 'bad request'}, status=400)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['post'])
@permission_classes((AllowAny,))
def fetch_all_buyer_product_details_by_pk(request):
    data=request.data
    key = data['key']
    buyerid=data['buyerid']
    try:
        if key == "vsinadmindb":
            getbuyerproductobj=BuyerProductDetailsAdmin.objects.filter(product_id__in=buyerid).values().order_by('product_id')
            if len(getbuyerproductobj)>0:
                return Response({'status': 200, 'message': 'Buyer Product Details List', 'data': getbuyerproductobj}, status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)

        else:
            return Response({'status': 400, 'message': 'bad request'}, status=400)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)
    #hello

@api_view(['post'])
@permission_classes((AllowAny,))
def fetch_open_leads_rfq(request):
    key = request.data['key']
    try:
        if key == "vsinadmindb":
            openleadsobj=OpenLeadsRfq.objects.filter().values().order_by('id')
            if len(openleadsobj)>0:
                return Response({'status': 200, 'message': 'Buyer Product Details List', 'data': openleadsobj}, status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)

        else:
            return Response({'status': 400, 'message': 'bad request'}, status=400)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def get_all_open_leads_by_pk(request):
    key = request.data['key']
    userpk=request.data['userpk']

    try:
        if key == "vsinadmindb":
            openleadsobj=OpenLeadsRfq.objects.filter(id=userpk).values().order_by('id')
            openleadsitemsobj=OpenLeadsItems.objects.filter(open_leads_pk_id=userpk).values().order_by('id')
            for i in range(0,len(openleadsitemsobj)):
                if len(openleadsitemsobj)>0:
                    print(openleadsitemsobj[i].get('item_code'))
                    buyerobj=BuyerProductDetailsAdmin.objects.filter(item_code=openleadsitemsobj[i].get('item_code')).values().order_by('product_id')
                    if len(buyerobj)>0:
                        if not buyerobj[0].get('document1'):
                            openleadsitemsobj[i].__setitem__('buyer_doc1',"")
                        else:
                            openleadsitemsobj[i].__setitem__('buyer_doc1',buyerobj[0].get('document1'))

                        if not buyerobj[0].get('document2'):
                            openleadsitemsobj[i].__setitem__('buyer_doc2', "")
                        else:
                            openleadsitemsobj[i].__setitem__('buyer_doc2', buyerobj[0].get('document2'))

                        if not buyerobj[0].get('document3'):
                            openleadsitemsobj[i].__setitem__('buyer_doc3', "")
                        else:
                            openleadsitemsobj[i].__setitem__('buyer_doc3', buyerobj[0].get('document2'))
                    else:
                        pass

            openleadsterms=OpenLeadsTermsDescription.objects.filter(open_leads_pk_id=userpk).values().order_by('id')
            if len(openleadsobj)>0 or len(openleadsitemsobj)>0 or len(openleadsterms)>0:
                return Response({'status': 200, 'message': 'Open Bids Rfq List', 'data':openleadsobj,'data1':openleadsitemsobj,'data3':openleadsterms}, status=200)

            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)
        else:
            return Response({'status': 400, 'message': 'bad request'}, status=400)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes((AllowAny,))
def fetch_open_leads_rfq(request):
    key = request.data['key']
    itemlist=[]
    newarray=[]
    quantityval=0
    count = 0
    try:
        if key == "vsinadmindb":
            openleadsobj=OpenLeadsRfq.objects.filter().values().order_by('-id')
            if len(openleadsobj)>0:
                for i in range(0, len(openleadsobj)):
                    deadline = openleadsobj[i].get('deadline_date')
                    datevalue = datetime.strptime(deadline, '%Y-%m-%d').strftime('%d-%m-%Y')
                    datevalue1=datetime.strptime(datevalue,'%d-%m-%Y')
                    conveteddeadlinedate = datetime.date(datevalue1)
                    todaydate = date.today()
                    if conveteddeadlinedate > todaydate:
                        print('Not Expired')
                        openleads=OpenLeadsRfq.objects.filter(rfq_number=openleadsobj[i].get('rfq_number')).values()
                        print(openleads[0].get('deadline_date'),'lk')
                        openobj=OpenLeadsItems.objects.filter(open_leads_pk=openleadsobj[i].get('id')).values().order_by('quantity')
                        for j in range(len(openobj)):
                            if openobj[j].get('quantity') != "":
                                count = count + int(openobj[j].get('quantity'))
                        print("====j loop ended")
                        newarray.append({'id': openleads[0].get('id'),
                                         'buyer': openleads[0].get('buyer'),
                                         'rfq_number': openleads[0].get('rfq_number'),
                                         'numeric': openleads[0].get('numeric'),
                                         'rfq_status': openleads[0].get('rfq_status'),
                                         'rfq_type':openleads[0].get('rfq_type'),
                                         'publish_date': openleads[0].get('publish_date'),
                                         'deadline_date': openleads[0].get('deadline_date'),
                                         'closing_date': openleads[0].get('closing_date'),
                                         'department': openleads[0].get('department'),
                                         'currency': openleads[0].get('currency'),
                                         'category': openleads[0].get('category'),
                                         'bill_address': openleads[0].get('bill_address'),
                                         'ship_address': openleads[0].get('ship_address'),
                                         'scope_of_supply': openleads[0].get('scope_of_supply'),
                                         'scope_of_work': openleads[0].get('scope_of_work'),
                                         'additional_info': openleads[0].get('additional_info'),
                                         'document_1': openleads[0].get('document_1'),
                                         'document_name_1': openleads[0].get('document_name_1'),
                                         'document_2': openleads[0].get('document_2'),
                                         'document_name_2 ': openleads[0].get('document_name_2') ,
                                         'document_3': openleads[0].get('document_3'),
                                         'document_name_3':openleads[0].get('document_name_3'),
                                         'created_on': openleads[0].get('created_on'),
                                         'updated_on': openleads[0].get('updated_on'),
                                         'created_by': openleads[0].get('created_by'),
                                         'updated_by': openleads[0].get('updated_by'),
                                         'admins': openleads[0].get('admins_id'),
                                         'buyer_company_code': openleads[0].get('buyer_company_code'),
                                         'buyer_company_name': openleads[0].get('buyer_company_name'),
                                         'maincore': openleads[0].get('maincore'),
                                         'subcategory': openleads[0].get('subcategory'),
                                         'rfq_title': openleads[0].get('rfq_title'),
                                         'buyer_pk': openleads[0].get('buyer_pk_id'),
                                         'noi': len(openobj),
                                         'noq': count,

                                         })
                        count = 0

                return Response({'status': 200, 'message': 'Buyer Product Details List','data':newarray}, status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)

        else:
            return Response({'status': 400, 'message': 'bad request'}, status=400)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

class OpenLeadsVendorPublishRfqViewSet(viewsets.ModelViewSet):
    queryset = OpenLeadsVendorPublishRfq.objects.all()
    serializer_class =OpenLeadsVendorPublishRfqSerializer

    def get_queryset(self):
        openleadsvendorobj = OpenLeadsVendorPublishRfq.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by('id')
        if openleadsvendorobj:
            return openleadsvendorobj
        raise ValidationError(
            {'message': 'Vendor Bidding Open Leads Vendor Publish Rfq', 'status': 204})

class OpenLeadsVendorPublishItemsViewSet(viewsets.ModelViewSet):
    queryset = OpenLeadsVendorPublishItems.objects.all()
    serializer_class = OpenLeadsVendorPublishItemsSerializer

    def create(self, request, *args, **kwargs):
        itemsarray=request.data['itemsarray']
        updated_by=request.data.get('updated_by',None)
        vendor_open_leads_pk=request.data.get('vendor_open_leads_pk',None)
        vendor_code=request.data.get('vendor_code',None)
        try:

            for i in range(0,len(itemsarray)):
                openleadsitemsobj=OpenLeadsVendorPublishItems.objects.create(vendor_item_code=itemsarray[i].get('item_code'),
                                                                vendor_item_name=itemsarray[i].get('item_name'),
                                                                vendor_item_description=itemsarray[i].get('item_description'),
                                                                vendor_uom=itemsarray[i].get('uom'),
                                                                buyer_quantity=itemsarray[i].get('quantity'),
                                                                vendor_rate=itemsarray[i].get('rate'),
                                                                vendor_tax=itemsarray[i].get('tax'),
                                                                vendor_discount=itemsarray[i].get('discount'),
                                                                vendor_total_amount=itemsarray[i].get('total_amount'),
                                                                vendor_item_type=itemsarray[i].get('item_type'),
                                                                updated_by=SelfRegistration.objects.get(id=updated_by),
                                                                created_by=updated_by,
                                                                vendor_open_leads_pk=OpenLeadsVendorPublishRfq.objects.get(id=vendor_open_leads_pk),
                                                                vendor_code=vendor_code
                                                                )
            return Response({'status': 201, 'message': 'Open Leads Vendor Items are created'}, status=201)

        except Exception as e:
            return Response({'status':500,'error':str(e)},status=500)


class OpenLeadsVendorPublishTermsDescriptionViewSet(viewsets.ModelViewSet):
    queryset = OpenLeadsVendorPublishTermsDescription.objects.all()
    serializer_class = OpenLeadsVendorPublishTermsDescriptionSerializer

    def create(self, request, *args, **kwargs):
        vendor_rfq_number = request.data['vendor_rfq_number']
        dictsqueries = request.data['dictsqueries']
        vendor_open_leads_pk = request.data.get('open_leads_pk', None)
        updated_by=request.data.get('updated_by',None)
        vendor_rfq_type=request.data.get('vendor_rfq_type',None)
        vendor_code = request.data.get('vendor_code', None)
        try:
            for i in range(0, len(dictsqueries)):
                for keys in dictsqueries[i]:
                    OpenLeadsVendorPublishTermsDescription.objects.create(vendor_rfq_number=vendor_rfq_number,
                                                                   vendor_terms=keys,
                                                                  vendor_description=dictsqueries[i][keys][0],
                                                                  vendor_response=dictsqueries[i][keys][1],
                                                                  vendor_open_leads_pk=OpenLeadsVendorPublishRfq.objects.get(
                                                                     id=vendor_open_leads_pk),
                                                                  vendor_rfq_type=vendor_rfq_type,
                                                                  updated_by=SelfRegistration.objects.get(id=updated_by),
                                                                  created_by=updated_by,
                                                                  vendor_code=vendor_code
                                                                   )
            return Response({'status': 201, 'message': 'Open Leads Vendor Terms and Descriptions are created'}, status=201)

        except Exception as e:
            return Response({'status': 500, 'message': str(e)}, status=500)

@api_view(['post'])
@permission_classes((AllowAny,))
def get_open_bids_list(request):
    data=request.data
    key=data['key']
    openleadsarray=[]
    idarray=[]
    count=0
    try:

        if key=="vsinadmindb":
            adminobj=AdminRegister.objects.filter().values()
            if len(adminobj):
                openrfqobj=OpenLeadsRfq.objects.filter(admins=adminobj[0].get('admin_id')).values().order_by('id')
                if len(openrfqobj):
                    for i in range(0,len(openrfqobj)):

                        openleadsitems = OpenLeadsItems.objects.filter(open_leads_pk=openrfqobj[i].get('id')).values().order_by('quantity')
                        if len(openleadsitems)>0:
                            for j in range(0,len(openleadsitems)):
                                if openleadsitems[j].get('quantity')!="":
                                    count=count+int(openleadsitems[j].get('quantity'))
                            print('count-------------------------------',count)
                        else:
                            print('items not present')


                        openleadspublish = OpenLeadsVendorPublishRfq.objects.filter(
                            vendor_rfq_number=openrfqobj[i].get('rfq_number')).values()
                        if len(openleadspublish) > 0:
                            print('-----------------------count-------------',count)
                            openleadsarray.append({'rfq_number': openrfqobj[i].get('rfq_number'),
                                                   'rfq_title': openrfqobj[i].get('rfq_title'),
                                                   'rfq_status': openrfqobj[i].get('rfq_status'),
                                                   'rfq_type': openrfqobj[i].get('rfq_type'),
                                                   'publish_date': openrfqobj[i].get('publish_date'),
                                                   'deadline_date': openrfqobj[i].get('deadline_date'),
                                                   'closing_date': openrfqobj[i].get('closing_date'),
                                                   'id':openrfqobj[i].get('id'),
                                                   'response_count': len(openleadspublish),
                                                   'quantity': count

                                                   })
                        else:
                            openleadsarray.append({'rfq_number': openrfqobj[i].get('rfq_number'),
                                                   'rfq_title': openrfqobj[i].get('rfq_title'),
                                                   'rfq_status': openrfqobj[i].get('rfq_status'),
                                                   'rfq_type': openrfqobj[i].get('rfq_type'),
                                                   'publish_date': openrfqobj[i].get('publish_date'),
                                                   'deadline_date': openrfqobj[i].get('deadline_date'),
                                                   'closing_date': openrfqobj[i].get('closing_date'),
                                                   'id': openrfqobj[i].get('id'),
                                                   'response_count': 0,
                                                   'quantity': count

                                                   })

                        count = 0
                    return Response({'status': 200, 'message': 'Open Leads Rfq List','data':openleadsarray},status=200)
                else:
                    return Response({'status': 204, 'message': 'Not Present'}, status=204)
            else:
                return Response({'status': 202, 'message': 'Admin id is not present'}, status=202)
        else:
            return Response({'status': 400, 'message': 'Bad Request'}, status=400)


    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def fetch_buyer_product_details_admin(request):
    data=request.data
    try:
        if data['token']=="4aoedpde123Vyeyweuo2":
            adminproductobj=BuyerProductDetailsAdmin.objects.filter(admins=data['adminid'],product_status='Active').values().order_by('product_id')
            if len(adminproductobj)>0:
                return Response({'status': 200, 'message': 'Admin Added Products List', 'data': adminproductobj}, status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)
        else:
            return Response({'status': 400, 'message': 'Bad Request'}, status=400)

    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)





@api_view(['post'])
@permission_classes((AllowAny,))
def fetch_all_open_leads_rfq(request):
    try:
        if request.data['key']=="vsinadmindb":
            openleadsobj=OpenLeadsRfq.objects.filter().values().order_by('id')
            if len(openleadsobj)>0:
                return Response({'status': 200, 'message': 'Open Leads Rfq List','data':openleadsobj},status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)
        else:
            return Response({'status': 400, 'message': 'Bad Request'}, status=400)

    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def fetch_vendor_open_leads(request):
    data=request.data
    rfqnumber=data['rfqnumber']
    openleadsarray=[]
    count=0
    try:
        if data['token'] == "4aoedpde123Vyeyweuo2":
            openleadsvendorobj=OpenLeadsVendorPublishRfq.objects.filter(vendor_rfq_number=rfqnumber).values().order_by('id')
            if len(openleadsvendorobj)>0:
                for i in range(0, len(openleadsvendorobj)):
                    basicobj=BasicCompanyDetails.objects.filter(updated_by_id=openleadsvendorobj[i].get('updated_by_id')).values()
                    vendorproductobj = OpenLeadsVendorPublishItems.objects.filter(vendor_open_leads_pk=openleadsvendorobj[i].get('id')).values().order_by('id')
                    if len(vendorproductobj)>0:
                        for j in range(0, len(vendorproductobj)):
                            print('s print')
                            if vendorproductobj[j].get('buyer_quantity') != "":
                                count = count + int(vendorproductobj[j].get('buyer_quantity'))
                            print('count-------------------------------', count)

                    else:
                        print('items not present')

                    openleadsarray.append({'company_name': basicobj[0].get('company_name'),
                                           'company_code': basicobj[0].get('company_code'),
                                           'vendor_rfq_number': openleadsvendorobj[i].get('vendor_rfq_number'),
                                           'final_amount': openleadsvendorobj[i].get('final_amount'),
                                           'buyer_quantity':count,
                                           'pk':openleadsvendorobj[i].get('id')

                                           })
                    count = 0




                return Response({'status': 200, 'message': 'Admin Added Products List', 'data': openleadsarray}, status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)
        else:
            return Response({'status': 400, 'message': 'Bad Request'}, status=400)

    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def fetch_vendor_open_leads_by_pk(request):
    data=request.data
    vendorpk=data['vendorpk']
    try:
        if data['token'] == "4aoedpde123Vyeyweuo2":
            openleadsvendorobj=OpenLeadsVendorPublishRfq.objects.filter(id=vendorpk).values().order_by('id')
            if len(openleadsvendorobj)>0:
                for i in range(0, len(openleadsvendorobj)):
                    vendorproductobj = OpenLeadsVendorPublishItems.objects.filter(vendor_open_leads_pk=openleadsvendorobj[i].get('id')).values().order_by('id')
                    for j in range(0,len(vendorproductobj)):
                        pass

                    vendorterms = OpenLeadsVendorPublishTermsDescription.objects.filter(vendor_open_leads_pk=vendorpk).values().order_by('id')
                    for k in range(0, len(vendorterms)):
                        print('correct')
                    openleadsvendorobj[i].__setitem__('product', vendorproductobj)
                    openleadsvendorobj[i].__setitem__('vendor_rfq_terms', vendorterms)

                return Response({'status': 200, 'message': 'Vendor Open Leads  List', 'data': openleadsvendorobj}, status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)
        else:
            return Response({'status': 400, 'message': 'Bad Request'}, status=400)

    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)



class OpenLeadsAwardsViewSet(viewsets.ModelViewSet):
    queryset = OpenLeadsAwards.objects.all()
    serializer_class = OpenLeadsAwardsSerializer
    permission_classes = ((AllowAny,))

    def create(self, request, *args, **kwargs):
        token=request.data.get('token',None)
        adminid=request.data.get('adminid',None)
        vendorpk=request.data.get('vendorpk',None)
        company_code=request.data.get('company_code',None)
        order_quantity=request.data.get('order_quantity',None)
        pcode=[]
        pname=[]
        pdesc=[]
        try:
            if token=="4aoedpde123Vyeyweuo2":
                vendorobj=OpenLeadsVendorPublishRfq.objects.filter(id=vendorpk).values()
                if len(vendorobj)>0:
                    openleadsitems=OpenLeadsVendorPublishItems.objects.filter(vendor_open_leads_pk=vendorobj[0].get('id')).values()
                    if len(openleadsitems)>0:
                        basicoj = BasicCompanyDetails.objects.filter(company_code=company_code).values()
                        if len(basicoj)>0:
                            for i in range(0,len(openleadsitems)):
                                print(vendorobj[0].get('vendor_rfq_number'),'ok')
                                print(openleadsitems[i].get('vendor_item_code'),'--------------------------------')
                                pcode.append(openleadsitems[i].get('vendor_item_code'))
                                pname.append(openleadsitems[i].get('vendor_item_name'))
                                pdesc.append(openleadsitems[i].get('vendor_item_description'))

                            awardobj=OpenLeadsAwards.objects.create(rfq_number=vendorobj[0].get('vendor_rfq_number'),
                                                                    company_code=[company_code],
                                                                    company_name=[basicoj[0].get('company_name')],
                                                                    buyer_bid_quantity=order_quantity,
                                                                    product_code=pcode,
                                                                    product_name=pname,
                                                                    product_description=pdesc,
                                                                    admins=AdminRegister.objects.get(admin_id=adminid)
                                                                    )
                            return Response({'status': 200, 'message': 'Open Leads Award Created'},
                                            status=200)
                        else:
                            pass


                    else:
                        return Response({'status': 204, 'message': 'Open Leads Items are not present'},
                                        status=204)
                else:
                    return Response({'status': 204, 'message': 'Rfq Published details are not present Present'}, status=204)
            else:
                return Response({'status': 400, 'message': 'Bad Request'}, status=400)


        except Exception as e:
            return Response({'status': 500, 'message': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def price_analysis_admin(request):
    data = request.data
    resarray = []
    token = data['token']
    rfq_number = data['rfq_number']
    buyerarray=[]
    vendor_code = data['vendor_code']
    try:
        if token=="4aoedpde123Vyeyweuo2":
            buyeropenleads=OpenLeadsItems.objects.filter(rfq_number=rfq_number).values().order_by('id')
            if len(buyeropenleads)>0:
                for i in range(0,len(buyeropenleads)):
                    buyerarray.append({'item_code':buyeropenleads[i].get('item_code'),
                                       'item_name':buyeropenleads[i].get('item_name'),
                                       'item_description':buyeropenleads[i].get('item_description'),
                                       'uom':buyeropenleads[i].get('uom'),
                                       'quantity':buyeropenleads[i].get('quantity'),
                                       'item_type':buyeropenleads[i].get('item_type')
                                       })
                    vpdetails = OpenLeadsVendorPublishItems.objects.filter(vendor_rfq_number=rfq_number,vendor_code__in=vendor_code,
                                                                           vendor_item_code=buyeropenleads[i].get('item_code')).values().order_by('vendor_code')
                    print(len(vpdetails))

                    for j in range(0, len(vpdetails)):
                        buyerarray[i].setdefault('ccode' + str(j), vpdetails[j].get('vendor_code'))
                        buyerarray[i].setdefault('rate' + str(j), vpdetails[j].get('vendor_rate'))
                        buyerarray[i].setdefault('tax' + str(j), vpdetails[j].get('vendor_tax'))
                        buyerarray[i].setdefault('discount' + str(j), vpdetails[j].get('vendor_discount'))
                        # resarray[i].setdefault('totalcost' + str(j), vpdetails[j].get('vendor_final_amount'))
                        buyerarray[i].setdefault('total_all_cost' + str(j), vpdetails[j].get('vendor_total_amount'))
                    print("---------------------------------")
                return Response({'status': 200, 'message': 'price analysis','data':buyerarray},status=200)
        else:
            return Response({'status': 400, 'message': 'bad request'}, status=400)
    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def get_buyer_name_by_ccode(request):
    data=request.data
    try:
        if data['token']=="vsinadmindb":
            buyerobj=CreateBuyer.objects.filter(company_code=data['buyercode']).values('company_name')
            if len(buyerobj)>0:
                return Response({'status': 200, 'message': 'Success', 'data': buyerobj}, status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)

@api_view(['post'])
@permission_classes((AllowAny,))
def get_create_buyer_list(request):
    data=request.data
    try:
        if data['token'] == "vsinadmindb":
            createbuyerobj=CreateBuyer.objects.filter(admins=data['aid']).values().order_by('id')
            if len(createbuyerobj)>0:
                return Response({'status': 200, 'message': 'Success', 'data': createbuyerobj}, status=200)
            else:
                return Response({'status': 204, 'message': ' Create Buyer details are Not Present'}, status=204)
        else:
            return Response({'status':400,'message':'Bad Request'},status=400)

    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)

@api_view(['post'])
@permission_classes((AllowAny,))
def get_create_buyer_list_companycode(request):
    data = request.data
    try:
        if data['token'] == "vsinadmindb":
            create_buyer = CreateBuyer.objects.filter(company_code = data['c_code']).values()
            if len(create_buyer)>0:
                return Response({'status': 200, 'message': 'Success', 'data': create_buyer}, status=200)
            else:
                return Response({'status': 204, 'message': ' Create Buyer details are Not Present'}, status=204)

        else:
            return Response({'status': 400, 'message': 'Bad Request'}, status=400)

    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)


@api_view(['post'])
def open_leads_vendor_publish_rfq(request):
    data = request.data
    user_id = data['user_id']
    open_leads_vendor_publish_rfq_data=[]
    try:

        vendor_publish_rfq_data=OpenLeadsVendorPublishRfq.objects.filter( updated_by=user_id).values()
        for i in range(0,len(vendor_publish_rfq_data)):
            print(vendor_publish_rfq_data[i].get('buyer_company_code'))
            create_buyer_data =CreateBuyer.objects.filter(company_code=vendor_publish_rfq_data[i].get('buyer_company_code')).values()
            open_leads_vendor_publish_rfq_data.append({'id':vendor_publish_rfq_data[i].get('id'),
                                                       'ccode': vendor_publish_rfq_data[i].get('buyer_company_code'),
                                                       'cname':create_buyer_data[0].get('company_name'),
                                                       'city':create_buyer_data[0].get('bill_city'),
                                                       'rfq_number': vendor_publish_rfq_data[i].get('vendor_rfq_number'),
                                                       'rfq_title': vendor_publish_rfq_data[i].get('vendor_rfq_title'),
                                                       'rfq_type': vendor_publish_rfq_data[i].get('vendor_rfq_type'),
                                                       'final_amount':vendor_publish_rfq_data[i].get('final_amount'),
                                                       'publish_date': vendor_publish_rfq_data[i].get('vendor_publish_date'),
                                                       'deadline_date': vendor_publish_rfq_data[i].get('vendor_deadline_date')

            })
        return Response({'status': 200, 'message': 'ok','opnleadsvendorpublishrfg':open_leads_vendor_publish_rfq_data,}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def open_leads_vendor_publishrfq_view(request):
    data = request.data
    pk = data['pk']
    try:
        open_leads_vendor_publish_rfq_view = OpenLeadsVendorPublishRfq.objects.filter(id=pk).values()
        open_leads_vendor_publish_rfq_items =OpenLeadsVendorPublishItems.objects.filter( vendor_open_leads_pk =pk).values()
        open_leads_vendor_publish_rfq_terms =OpenLeadsVendorPublishTermsDescription.objects.filter( vendor_open_leads_pk=pk).values()
        return Response({'status': 200, 'message': 'ok', 'OpenLeadsVendorPublishRfqView': open_leads_vendor_publish_rfq_view, 'OpenLeadsVendorPublishRfqItems':open_leads_vendor_publish_rfq_items,'OpenLeadsVendorPublishRfqTerms':open_leads_vendor_publish_rfq_terms,},status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def channel_leads_closed_leads_deadline_date(request):
    data = request.data
    user_id = data['user_id']
    key_array =[]
    resarr=[]
    try:
        ChannelLeads_ClosedLeads_DeadlineDate_Data = OpenLeadsVendorPublishRfq.objects.filter(updated_by=user_id).values()
        for i in range(0, len(ChannelLeads_ClosedLeads_DeadlineDate_Data)):
            key_array.append(ChannelLeads_ClosedLeads_DeadlineDate_Data[i].get('open_rfq_buyer_pk_id'))
        id_data=OpenLeadsRfq.objects.filter(~Q(id__in=key_array)).values()
        for j in range(0,len(id_data)):
            date2=datetime.strptime(id_data[j].get('deadline_date'),'%Y-%m-%d')
            if date2.date() < date.today():
                resarr.append(id_data[j])

        return Response({'status': 200, 'message': 'ok', 'ChannelLeadsClosedLeadsDeadlineDateData':resarr,}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def create_admin_selected_categories(request):
    data = request.data
    key = data['key']
    category_name = data['category_name']
    admins = data['admins']
    try:
        if key == 'vsinadmin':
            for i in range(0, len(category_name)):
                catobjname = AdminSelectedCategories.objects.filter(category_name=category_name[i].get('catname')).values()
                for k in range(0, len(catobjname)):
                    catobjr = AdminSelectedCategories.objects.get(category_name=catobjname[k].get('category_name'))
                    catobjr.delete()
                adminselectedcategory = AdminSelectedCategories.objects.create(
                    category_name=category_name[i].get('catname'),
                    category_id=category_name[i].get('id'),
                    admins=AdminRegister.objects.get(admin_id=admins),
                    priority=category_name[i].get('priority'))
            return Response({'status': 201, 'message': 'Admin Selected Categories are Created'}, status=201)
        else:
            return Response({'status': 401, 'message': 'Unauthorized'}, status=401)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def create_admin_selected_trending_categories(request):
    data = request.data
    key = data['key']
    category_name = data['category_name']
    admins = data['admins']
    try:
        if key == 'vsinadmin':
            for i in range(0, len(category_name)):
                catobjname = TrendingCategories.objects.filter(trending_category_name=category_name[i].get('catname')).values()
                for k in range(0, len(catobjname)):
                    catobjr = TrendingCategories.objects.get(trending_category_name=catobjname[k].get('trending_category_name'))
                    catobjr.delete()
                adminselectedcategory = TrendingCategories.objects.create(
                    trending_category_name=category_name[i].get('catname'),
                    trending_category_id=category_name[i].get('id'),
                    admins=AdminRegister.objects.get(admin_id=admins),
                    trending_priority=category_name[i].get('priority'))
            return Response({'status': 201, 'message': 'Trending Categories are Created'}, status=201)
        else:
            return Response({'status': 401, 'message': 'Unauthorized'}, status=401)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes((AllowAny,))
def create_admin_selected_sub_categories(request):
    data = request.data
    key = data['key']
    sub_category_data = data['sub_category_data']
    admins = data['admins']
    try:
        if key == 'vsinadmin':
            for i in range(0, len(sub_category_data)):
                catobjname = AdminSelectedSubCategories.objects.filter(sub_category_name=sub_category_data[i].get('subcatname')).values()
                for k in range(0, len(catobjname)):
                    catobjr = AdminSelectedSubCategories.objects.get(sub_category_name=catobjname[k].get('sub_category_name'))
                    catobjr.delete()
                adminselectedsubcategory = AdminSelectedSubCategories.objects.create(
                    sub_category_name=sub_category_data[i].get('subcatname'),
                    sub_category_id=sub_category_data[i].get('id'),
                    admins=AdminRegister.objects.get(admin_id=admins),
                    sub_categories_priority=sub_category_data[i].get('priority'))
            return Response({'status': 201, 'message': 'Admin selected Sub Categories are Created'}, status=201)
        else:
            return Response({'status': 401, 'message': 'Unauthorized'}, status=401)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def create_admin_trending_sub_categories(request):
    data = request.data
    key = data['key']
    sub_category_data = data['sub_category_data']
    admins = data['admins']
    try:
        if key == 'vsinadmin':
            for i in range(0, len(sub_category_data)):
                catobjname = TrendingSubCategories.objects.filter(trending_sub_category_name=sub_category_data[i].get('subcatname')).values()
                for k in range(0, len(catobjname)):
                    catobjr = TrendingSubCategories.objects.get(trending_sub_category_name=catobjname[k].get('trending_sub_category_name'))
                    catobjr.delete()
                adminselectedcategory = TrendingSubCategories.objects.create(
                    trending_sub_category_name=sub_category_data[i].get('subcatname'),
                    trending_sub_category_id=sub_category_data[i].get('id'),
                    admins=AdminRegister.objects.get(admin_id=admins),
                    trending_sub_categories_priority=sub_category_data[i].get('priority'))
            return Response({'status': 201, 'message': 'Admin Trending Sub Categories are Created'}, status=201)
        else:
            return Response({'status': 401, 'message': 'Unauthorized'}, status=401)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


# @api_view(['post'])
# @permission_classes((AllowAny,))
# def fetch_admin_selected_categories(request):
#     key=request.data['key']
#     catarray=[]
#     rearay=[]
#     try:
#         if key=='vsinadmin':
#             adminselectedcategoryobj=AdminSelectedCategories.objects.filter().values()
#             for i in range(0,len(adminselectedcategoryobj)):
#                 catarray.append(int(adminselectedcategoryobj[i].get('priority')))
#             print(catarray)
#             print("sorted ",sorted(catarray))
#             catarray=sorted(catarray)
#             if len(catarray)>0:
#                 for i in range(0,len(catarray)):
#                     adminselectedcategoryobj = AdminSelectedCategories.objects.filter(priority=catarray[i]).values()
#                     print("yes or no ",adminselectedcategoryobj)
#                     catobj=CategoryMaster.objects.filter(category_name=adminselectedcategoryobj[0].get('category_name')).values()
#                     rearay.append({'category_name':adminselectedcategoryobj[0].get('category_name'),
#                                      'category_id':adminselectedcategoryobj[0].get('category_id'),
#                                      'admins':adminselectedcategoryobj[0].get('admins'),
#                                      'created_on':adminselectedcategoryobj[0].get('created_on'),
#                                      'updated_on':adminselectedcategoryobj[0].get('updated_on'),
#                                      'priority':adminselectedcategoryobj[0].get('priority'),
#                                      'category_code':catobj[0].get('category_code'),
#                                      'category_status':catobj[0].get('status')
#                                      })
#                 return Response({'status':200,'message':'Admin Selected Categories List','data':rearay},status=200)
#             else:
#                 return Response({'status': 204, 'message': 'Admin Selected Categories Not Present'}, status=204)
#         else:
#             return Response({'status': 401, 'message': 'Unauthorized'}, status=401)
#
#     except Exception as e:
#         return Response({'status':500,'error':str(e)},status=500)
#

# @api_view(['post'])
# @permission_classes((AllowAny,))
# def fetch_admin_selected_categories(request):
#     key = request.data['key']
#     rearay = []
#     catarray=[]
#     try:
#         if key == 'vsinadmin':
#             allselecteddata = AdminSelectedCategories.objects.filter().values()
#             for i in range(0, len(allselecteddata)):
#                 catarray.append(int(allselecteddata[i].get('priority')))
#             print(catarray)
#             values=sorted(catarray)
#             print("sorted ", sorted(catarray))
#             if len(allselecteddata)>0:
#                 for i in range(0, len(values)):
#                     allselecteddata = AdminSelectedCategories.objects.filter(priority=values[i]).values()
#                     catobj = CategoryMaster.objects.filter(category_name=allselecteddata[0].get('category_name')).values()
#                     rearay.append({'category_name': allselecteddata[0].get('category_name'),
#                                    'category_id': allselecteddata[0].get('category_id'),
#                                    'admins': allselecteddata[0].get('admins'),
#                                    'created_on': allselecteddata[0].get('created_on'),
#                                    'updated_on': allselecteddata[0].get('updated_on'),
#                                    'priority': allselecteddata[0].get('priority'),
#                                    'category_code': catobj[0].get('category_code'),
#                                    'category_status': catobj[0].get('status')
#                                    })
#                 return Response({'status': 200, 'message': 'Admin Selected Categories List', 'data': rearay}, status=200)
#             else:
#                 return Response({'status': 204, 'message': 'Admin Selected Categories Not Present'}, status=204)
#
#         else:
#             return Response({'status': 401, 'message': 'Unauthorized'}, status=401)
#     except Exception as e:
#         return Response({'status': 500, 'error': str(e)}, status=500)
#
#
# @api_view(['post'])
# @permission_classes((AllowAny,))
# def fetch_admin_trending_categories(request):
#     key=request.data['key']
#     catarray=[]
#     arrayval=[]
#     try:
#         if key=='vsinadmin':
#             trendingcategoryobj=TrendingCategories.objects.filter().values()
#             for i in range(0, len(trendingcategoryobj)):
#                 arrayval.append(int(trendingcategoryobj[i].get('trending_priority')))
#             print(arrayval)
#             values=sorted(arrayval)
#             print("sorted ", sorted(arrayval))
#             if len(trendingcategoryobj)>0:
#                 for i in range(0, len(values)):
#                     trendingcategoryobj=TrendingCategories.objects.filter(trending_priority=values[i]).values()
#
#                     catobj=CategoryMaster.objects.filter(category_name=trendingcategoryobj[0].get('trending_category_name')).values()
#                     catarray.append({'trending_category_name':trendingcategoryobj[0].get('trending_category_name'),
#                                      'trending_category_id':trendingcategoryobj[0].get('trending_category_id'),
#                                      'admins':trendingcategoryobj[0].get('admins'),
#                                      'created_on':trendingcategoryobj[0].get('created_on'),
#                                      'updated_on':trendingcategoryobj[0].get('updated_on'),
#                                      'trending_priority':trendingcategoryobj[0].get('trending_priority'),
#                                      'category_code':catobj[0].get('category_code'),
#                                      'category_status':catobj[0].get('status')
#
#
#                                      })
#                 return Response({'status':200,'message':'Admin Trending Categories List','data':catarray},status=200)
#             else:
#                 return Response({'status': 204, 'message': 'Admin Trending Categories Not Present'}, status=204)
#         else:
#             return Response({'status': 401, 'message': 'Unauthorized'}, status=401)
#
#     except Exception as e:
#         return Response({'status':500,'error':str(e)},status=500)





# @api_view(['post'])
# @permission_classes((AllowAny,))
# def fetch_admin_trending_sub_categories(request):
#     key = request.data['key']
#     subcatarray = []
#     arrayval=[]
#     try:
#         if key == 'vsinadmin':
#             trendingsubcategoryobj = TrendingSubCategories.objects.filter().values()
#             for i in range(0, len(trendingsubcategoryobj)):
#                 arrayval.append(int(trendingsubcategoryobj[i].get('trending_sub_categories_priority')))
#             print(arrayval)
#             values=sorted(arrayval)
#             print("sorted ", sorted(arrayval))
#
#             if len(trendingsubcategoryobj)>0:
#                 for i in range(0, len(values)):
#                     trendingsubcategoryobj2=TrendingSubCategories.objects.filter(trending_sub_categories_priority=values[i]).values()
#                     subcatobj = SubCategoryMaster.objects.filter(sub_category_name=trendingsubcategoryobj2[0].get('trending_sub_category_name')).values()
#                     subcatarray.append({'trending_sub_category_name': trendingsubcategoryobj2[i].get('trending_sub_category_name'),
#                          'trending_sub_category_id': trendingsubcategoryobj2[i].get('trending_sub_category_id'),
#                          'admins': trendingsubcategoryobj2[i].get('admins'),
#                          'created_on': trendingsubcategoryobj2[i].get('created_on'),
#                          'updated_on': trendingsubcategoryobj2[i].get('updated_on'),
#                          'trending_sub_categories_priority': trendingsubcategoryobj2[i].get('trending_sub_categories_priority'),
#                          'sub_category_code': subcatobj[0].get('sub_category_code'),
#                          'sub_category_status': subcatobj[0].get('status')
#                          })
#                 return Response({'status': 200, 'message': 'Admin Trending SubCategories List', 'data': subcatarray},
#                                 status=200)
#             else:
#                 return Response({'status': 204, 'message': 'Admin Trending SubCategories Not Present'}, status=204)
#
#         else:
#             return Response({'status': 401, 'message': 'Unauthorized'}, status=401)
#     except Exception as e:
#         return Response({'status': 500, 'error': str(e)}, status=500)


# @api_view(['post'])
# @permission_classes((AllowAny,))
# def fetch_admin_selected_sub_categories(request):
#     key=request.data['key']
#     subcatarray=[]
#     valarray=[]
#     try:
#         if key=='vsinadmin':
#             selectedsubcategoryobj=AdminSelectedSubCategories.objects.filter().values()
#             for i in range(0, len(selectedsubcategoryobj)):
#                 valarray.append(int(selectedsubcategoryobj[i].get('sub_categories_priority')))
#             print(valarray)
#             datas=sorted(valarray)
#             print("sorted ", datas)
#             if len(selectedsubcategoryobj)>0:
#
#
#                 for i in range(0,len(datas)):
#                     selectedsubcategoryobj = AdminSelectedSubCategories.objects.filter(sub_categories_priority=datas[i]).values()
#                     subcatobj=SubCategoryMaster.objects.filter(sub_category_name=selectedsubcategoryobj[0].get('sub_category_name')).values()
#                     subcatarray.append({'sub_category_name':selectedsubcategoryobj[0].get('sub_category_name'),
#                                         'sub_category_id':selectedsubcategoryobj[0].get('sub_category_id'),
#                                         'admins':selectedsubcategoryobj[0].get('admins'),
#                                         'created_on':selectedsubcategoryobj[0].get('created_on'),
#                                         'updated_on':selectedsubcategoryobj[0].get('updated_on'),
#                                         'sub_categories_priority':selectedsubcategoryobj[0].get('sub_categories_priority'),
#                                         'sub_category_code':subcatobj[0].get('sub_category_code'),
#                                         'sub_category_status':subcatobj[0].get('status')
#                                         })
#                 return Response({'status':200,'message':'Admin Selected SubCategories List','data':subcatarray},status=200)
#             else:
#                 return Response({'status': 204, 'message': 'Admin Selected SubCategories Not Present'}, status=204)
#         else:
#             return Response({'status': 401, 'message': 'Unauthorized'}, status=401)
#
#     except Exception as e:
#         return Response({'status':500,'error':str(e)},status=500)

@api_view(['post'])
@permission_classes((AllowAny,))
def fetch_admin_selected_sub_categories(request):
    key=request.data['key']
    subcatarray=[]
    valarray=[]
    try:
        if key=='vsinadmin':
            selectedsubcategoryobj1 = AdminSelectedSubCategories.objects.filter(sub_categories_priority='0').values()
            selectedsubcategoryobj=AdminSelectedSubCategories.objects.filter(~Q(sub_categories_priority='0')).values()
            for i in range(0, len(selectedsubcategoryobj)):
                valarray.append(int(selectedsubcategoryobj[i].get('sub_categories_priority')))
            print(valarray)
            datas=sorted(valarray)
            print("sorted ", datas)

            if selectedsubcategoryobj1:
                for j in range(0, len(selectedsubcategoryobj1)):
                    subcatobj = SubCategoryMaster.objects.filter(
                        sub_category_name=selectedsubcategoryobj1[j].get('sub_category_name')).values()
                    subcatarray.append({'sub_category_name': selectedsubcategoryobj1[j].get('sub_category_name'),
                                        'sub_category_id': selectedsubcategoryobj1[j].get('sub_category_id'),
                                        'admins': selectedsubcategoryobj1[j].get('admins'),
                                        'created_on': selectedsubcategoryobj1[j].get('created_on'),
                                        'updated_on': selectedsubcategoryobj1[j].get('updated_on'),
                                        'sub_categories_priority': selectedsubcategoryobj1[j].get(
                                            'sub_categories_priority'),
                                        'sub_category_code': subcatobj[0].get('sub_category_code'),
                                        'sub_category_status': subcatobj[0].get('status')
                                        })


                for i in range(0,len(datas)):
                    selectedsubcategoryobj2 = AdminSelectedSubCategories.objects.filter(sub_categories_priority=datas[i]).values()


                    for j in range(0,len(selectedsubcategoryobj2)):
                        subcatobj=SubCategoryMaster.objects.filter(sub_category_name=selectedsubcategoryobj2[j].get('sub_category_name')).values()
                        subcatarray.append({'sub_category_name':selectedsubcategoryobj2[j].get('sub_category_name'),
                                        'sub_category_id':selectedsubcategoryobj2[j].get('sub_category_id'),
                                        'admins':selectedsubcategoryobj2[j].get('admins'),
                                        'created_on':selectedsubcategoryobj2[j].get('created_on'),
                                        'updated_on':selectedsubcategoryobj2[j].get('updated_on'),
                                        'sub_categories_priority':selectedsubcategoryobj2[j].get('sub_categories_priority'),
                                        'sub_category_code':subcatobj[0].get('sub_category_code'),
                                        'sub_category_status':subcatobj[0].get('status')
                                        })
                return Response({'status':200,'message':'Admin Selected SubCategories List','data':subcatarray},status=200)
        else:
            return Response({'status': 401, 'message': 'Unauthorized'}, status=401)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)
#
# @api_view(['post'])
# @permission_classes((AllowAny,))
# def fetch_admin_trending_sub_categories(request):
#     key=request.data['key']
#     subcatarray = []
#     valarray=[]
#     try:
#         if key=='vsinadmin':
#             trendingsubcategoryobj=TrendingSubCategories.objects.filter().values()
#             if len(trendingsubcategoryobj)>0:
#                 for i in range(0,len(trendingsubcategoryobj)):
#                     valarray.append(int(trendingsubcategoryobj[i].get('trending_sub_categories_priority')))
#                 sortvalue=sorted(valarray)
#                 if len(sortvalue)>0:
#                     for i in range(0,len(sortvalue)):
#                         trendingsubcategoryobj = TrendingSubCategories.objects.filter(trending_sub_categories_priority=sortvalue[i]).values()
#
#                         subcatobj=SubCategoryMaster.objects.filter(sub_category_name=trendingsubcategoryobj[0].get('trending_sub_category_name')).values()
#                         subcatarray.append({'trending_sub_category_name':trendingsubcategoryobj[0].get('trending_sub_category_name'),
#                                             'trending_sub_category_id':trendingsubcategoryobj[0].get('trending_sub_category_id'),
#                                             'admins':trendingsubcategoryobj[0].get('admins'),
#                                             'created_on':trendingsubcategoryobj[0].get('created_on'),
#                                             'updated_on':trendingsubcategoryobj[0].get('updated_on'),
#                                             'trending_sub_categories_priority':trendingsubcategoryobj[0].get('trending_sub_categories_priority'),
#                                             'sub_category_code':subcatobj[0].get('sub_category_code'),
#                                             'sub_category_status':subcatobj[0].get('status')
#                                             })
#                 return Response({'status':200,'message':'Admin Trending SubCategories List','data':subcatarray},status=200)
#             else:
#                 return Response({'status': 204, 'message': 'Admin Trending SubCategories Not Present'}, status=204)
#         else:
#             return Response({'status': 401, 'message': 'Unauthorized'}, status=401)
#
#     except Exception as e:
#         return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['post'])
@permission_classes((AllowAny,))
def fetch_admin_selected_categories(request):
    key = request.data['key']
    rearay = []
    catarray=[]
    try:
        if key == 'vsinadmin':
            selectedcategoryobj1 = AdminSelectedCategories.objects.filter(priority='0').values()
            selectedcategoryobj=AdminSelectedCategories.objects.filter(~Q(priority='0')).values()
            for i in range(0, len(selectedcategoryobj)):
                catarray.append(int(selectedcategoryobj[i].get('priority')))
            print(catarray)
            datas=sorted(catarray)
            print("sorted ",datas )
            if selectedcategoryobj1:
                for j in range(0, len(selectedcategoryobj1)):
                    catobj = CategoryMaster.objects.filter(category_name=selectedcategoryobj1[j].get('category_name')).values()
                    rearay.append({'category_name': selectedcategoryobj1[j].get('category_name'),
                                           'category_id': selectedcategoryobj1[j].get('category_id'),
                                           'admins': selectedcategoryobj1[j].get('admins'),
                                           'created_on': selectedcategoryobj1[j].get('created_on'),
                                           'updated_on': selectedcategoryobj1[j].get('updated_on'),
                                           'priority': selectedcategoryobj1[j].get('priority'),
                                           'category_code': catobj[0].get('category_code'),
                                           'category_status': catobj[0].get('status')
                                           })

            if len(selectedcategoryobj)>0:
                for i in range(0, len(datas)):
                    selectedcategoryobj2 = AdminSelectedCategories.objects.filter(priority=datas[i]).values()
                    for j in range(0, len(selectedcategoryobj2)):
                        catobj = CategoryMaster.objects.filter(category_name=selectedcategoryobj2[j].get('category_name')).values()
                        rearay.append({'category_name': selectedcategoryobj2[j].get('category_name'),
                                   'category_id': selectedcategoryobj2[j].get('category_id'),
                                   'admins': selectedcategoryobj2[j].get('admins'),
                                   'created_on': selectedcategoryobj2[j].get('created_on'),
                                   'updated_on': selectedcategoryobj2[j].get('updated_on'),
                                   'priority': selectedcategoryobj2[j].get('priority'),
                                   'category_code': catobj[0].get('category_code'),
                                   'category_status': catobj[0].get('status')
                                   })
                return Response({'status': 200, 'message': 'Admin Selected Categories List', 'data': rearay}, status=200)
            else:
                return Response({'status': 204, 'message': 'Admin Selected Categories Not Present'}, status=204)

        else:
            return Response({'status': 401, 'message': 'Unauthorized'}, status=401)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
@permission_classes((AllowAny,))
def fetch_admin_trending_categories(request):
    key=request.data['key']
    catarray=[]
    arrayval=[]
    try:
        if key=='vsinadmin':
            trendingcategoryobj1=TrendingCategories.objects.filter(trending_priority='0').values()
            trendingcategoryobj=TrendingCategories.objects.filter(~Q(trending_priority='0')).values()
            for i in range(0, len(trendingcategoryobj)):
                arrayval.append(int(trendingcategoryobj[i].get('trending_priority')))
            print(arrayval)
            datas=sorted(arrayval)
            print("sorted ", sorted(arrayval))
            if trendingcategoryobj1:
                for j in range(0, len(trendingcategoryobj1)):
                    catobj = CategoryMaster.objects.filter(category_name=trendingcategoryobj1[j].get('trending_category_name')).values()
                    catarray.append({'trending_category_name': trendingcategoryobj1[j].get('trending_category_name'),
                                             'trending_category_id':trendingcategoryobj1[j].get('trending_category_id'),
                                             'admins':trendingcategoryobj1[j].get('admins'),
                                             'created_on':trendingcategoryobj1[j].get('created_on'),
                                             'updated_on':trendingcategoryobj1[j].get('updated_on'),
                                             'trending_priority':trendingcategoryobj1[j].get('trending_priority'),
                                             'category_code':catobj[0].get('category_code'),
                                             'category_status':catobj[0].get('status')
                                             })
                if len(trendingcategoryobj) > 0:
                    for i in range(0, len(datas)):
                        trendingcategoryobj2 = TrendingCategories.objects.filter(trending_priority=datas[i]).values()
                        for j in range(0, len(trendingcategoryobj2)):
                            catobj=CategoryMaster.objects.filter(category_name=trendingcategoryobj2[j].get('trending_category_name')).values()
                            catarray.append({'trending_category_name':trendingcategoryobj2[j].get('trending_category_name'),
                                     'trending_category_id':trendingcategoryobj2[j].get('trending_category_id'),
                                     'admins':trendingcategoryobj2[j].get('admins'),
                                     'created_on':trendingcategoryobj2[j].get('created_on'),
                                     'updated_on':trendingcategoryobj2[j].get('updated_on'),
                                     'trending_priority':trendingcategoryobj2[j].get('trending_priority'),
                                     'category_code':catobj[0].get('category_code'),
                                     'category_status':catobj[0].get('status')
                                     })
                return Response({'status':200,'message':'Admin Trending Categories List','data':catarray},status=200)
            else:
                return Response({'status': 204, 'message': 'Admin Trending Categories Not Present'}, status=204)
        else:
            return Response({'status': 401, 'message': 'Unauthorized'}, status=401)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)



@api_view(['post'])
@permission_classes((AllowAny,))
def fetch_admin_trending_sub_categories(request):
    key = request.data['key']
    subcatarray = []
    valarray=[]
    try:
        if key == 'vsinadmin':
            trendingsubcategoryobj1 =TrendingSubCategories.objects.filter(trending_sub_categories_priority='0').values()
            trendingsubcategoryobj=TrendingSubCategories.objects.filter(~Q(trending_sub_categories_priority='0')).values()
            for i in range(0, len(trendingsubcategoryobj)):
                valarray.append(int(trendingsubcategoryobj[i].get('trending_sub_categories_priority')))
            print(valarray)
            datas=sorted(valarray)
            print("sorted ", sorted(valarray))
            if trendingsubcategoryobj1:
                for j in range(0, len(trendingsubcategoryobj1)):
                    subcatobj = SubCategoryMaster.objects.filter(sub_category_name=trendingsubcategoryobj1[j].get('trending_sub_category_name')).values()
                    subcatarray.append({'trending_sub_category_name': trendingsubcategoryobj1[j].get('trending_sub_category_name'),
                         'trending_sub_category_id': trendingsubcategoryobj1[j].get('trending_sub_category_id'),
                         'admins': trendingsubcategoryobj1[j].get('admins'),
                         'created_on': trendingsubcategoryobj1[j].get('created_on'),
                         'updated_on': trendingsubcategoryobj1[j].get('updated_on'),
                         'trending_sub_categories_priority': trendingsubcategoryobj1[j].get('trending_sub_categories_priority'),
                         'sub_category_code': subcatobj[0].get('sub_category_code'),
                         'sub_category_status': subcatobj[0].get('status')
                         })

                    for i in range(0, len(datas)):
                        trendingsubcategoryobj2 = TrendingSubCategories.objects.filter(trending_sub_categories_priority=datas[i]).values()
                        for j in range(0, len(trendingsubcategoryobj2)):
                            subcatobj = SubCategoryMaster.objects.filter(sub_category_name=trendingsubcategoryobj2[j].get('trending_sub_category_name')).values()
                            subcatarray.append({'trending_sub_category_name': trendingsubcategoryobj2[j].get('trending_sub_category_name'),
                                                'trending_sub_category_id': trendingsubcategoryobj2[j].get('trending_sub_category_id'),
                                                'admins': trendingsubcategoryobj2[j].get('admins'),
                                                'created_on': trendingsubcategoryobj2[j].get('created_on'),
                                                'updated_on': trendingsubcategoryobj2[j].get('updated_on'),
                                                'trending_sub_categories_priority': trendingsubcategoryobj2[0].get('trending_sub_categories_priority'),
                                                'sub_category_code': subcatobj[0].get('sub_category_code'),
                                                'sub_category_status': subcatobj[0].get('status')
                                                })
                    return Response({'status': 200, 'message': 'Trending SubCategories List', 'data': subcatarray},
                                status=200)
        else:
            return Response({'status': 401, 'message': 'Unauthorized'}, status=401)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
@permission_classes((AllowAny,))
def delete_trending_category(request):
    data=request.data
    key=data['key']
    trending_pk=data['trending_pk']
    try:
        if key=='vsinadmin':
            trendingobj=TrendingCategories.objects.filter(trending_category_id__in=trending_pk).values()
            print(len(trendingobj))
            if len(trendingobj)>0:
                for i in range(0,len(trendingobj)):
                    print(trendingobj[i].get('id'))
                    trendingval=TrendingCategories.objects.get(id=trendingobj[i].get('id'))
                    print(trendingval.id)
                    if trendingval:
                        trendingval.delete()
                return  Response({'status':204,'message':'Trending Categories are Deleted'},status=204)
            else:
                return Response({'status':200,'message':'Trending Categoires data are not present or already deleted'},status=200)
        else:
            return Response({'status': 401, 'message': 'Unauthorized'}, status=401)



    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def delete_admin_selected_category(request):
    data = request.data
    key = data['key']
    admin_select_cat_id = data['admin_select_cat_id']
    try:
        if key == 'vsinadmin':
            adminselectcatobj = AdminSelectedCategories.objects.filter(category_id__in=admin_select_cat_id).values()
            print(len(adminselectcatobj))
            if len(adminselectcatobj) > 0:
                for i in range(0, len(adminselectcatobj)):
                    print(adminselectcatobj[i].get('id'))
                    adminselcetcatval = AdminSelectedCategories.objects.get(id=adminselectcatobj[i].get('id'))
                    print(adminselcetcatval.id)
                    if adminselcetcatval:
                        adminselcetcatval.delete()
                return Response({'status': 204, 'message': 'Admin Selected Categories are Deleted'}, status=204)
            else:
                return Response(
                    {'status': 200, 'message': 'Admin Selected Categoires data are not present or already deleted'},
                    status=200)
        else:
            return Response({'status': 401, 'message': 'Unauthorized'}, status=401)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def delete_admin_selected_sub_category(request):
    data=request.data
    key=data['key']
    admin_subcat_id=data['admin_subcat_id']
    try:
        if key=='vsinadmin':
            adminsubcatobj=AdminSelectedSubCategories.objects.filter(sub_category_id__in=admin_subcat_id).values()
            print(len(adminsubcatobj))
            if len(adminsubcatobj)>0:
                for i in range(0,len(adminsubcatobj)):
                    print(adminsubcatobj[i].get('id'))
                    adminsubcatval=AdminSelectedSubCategories.objects.get(id=adminsubcatobj[i].get('id'))
                    print(adminsubcatval.id)
                    if adminsubcatval:
                        adminsubcatval.delete()
                return  Response({'status':204,'message':'Admin Selected Sub Categories are Deleted'},status=204)
            else:
                return Response({'status':200,'message':'Admin Selected Sub Categoires data are not present or already deleted'},status=200)
        else:
            return Response({'status': 401, 'message': 'Unauthorized'}, status=401)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
@permission_classes((AllowAny,))
def delete_trending_sub_category(request):
    data=request.data
    key=data['key']
    trending_subcat_id=data['trending_subcat_id']
    try:
        if key=='vsinadmin':
            trendingsubcatobj=TrendingSubCategories.objects.filter(trending_sub_category_id__in=trending_subcat_id).values()
            print(len(trendingsubcatobj))
            if len(trendingsubcatobj)>0:
                for i in range(0,len(trendingsubcatobj)):
                    print(trendingsubcatobj[i].get('id'))
                    trendingsucatval=TrendingSubCategories.objects.get(id=trendingsubcatobj[i].get('id'))
                    print(trendingsucatval.id)
                    if trendingsucatval:
                        trendingsucatval.delete()
                return  Response({'status':204,'message':'Trending Sub Categories are Deleted'},status=204)
            else:
                return Response({'status':200,'message':'Trending Sub Categoires data are not present or already deleted'},status=200)
        else:
            return Response({'status': 401, 'message': 'Unauthorized'}, status=401)



    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['put'])
@permission_classes((AllowAny,))
def edit_admin_selected_categories(request):
    data=request.data
    key=data['key']
    category_array=data['category_array']
    admin_id=data['admin_id']
    try:
        if key=='vsinadmin':
            for i in range(0,len(category_array)):
                adminobj=AdminSelectedCategories.objects.filter(category_id=category_array[i].get('id'),admins=admin_id).values()
                if len(adminobj)>0:
                    adminvalue = AdminSelectedCategories.objects.get(id=adminobj[0].get('id'))
                    if adminvalue.priority!=category_array[i].get('priority'):
                        adminvalue.priority=category_array[i].get('priority')
                        adminvalue.save()
            return  Response({'status':200,'message':'Top Categories Are Updated'},status=200)

        else:
            return Response({'status': 401, 'message': 'Unauthorized'}, status=401)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['put'])
@permission_classes((AllowAny,))
def edit_admin_trending_categories(request):
    data=request.data
    key=data['key']
    category_array=data['category_array']
    admin_id=data['admin_id']
    try:
        if key=='vsinadmin':
            for i in range(0,len(category_array)):
                adminobj=TrendingCategories.objects.filter(trending_category_id=category_array[i].get('id'),admins=admin_id).values()
                if len(adminobj)>0:
                    adminvalue = TrendingCategories.objects.get(id=adminobj[0].get('id'))
                    if adminvalue.trending_priority!=category_array[i].get('priority'):
                        adminvalue.trending_priority=category_array[i].get('priority')
                        adminvalue.save()

            return  Response({'status':200,'message':'Trending Categories Are Updated'},status=200)

        else:
            return Response({'status': 401, 'message': 'Unauthorized'}, status=401)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['put'])
@permission_classes((AllowAny,))
def edit_admin_sub_categories(request):
    data = request.data
    key = data['key']
    sub_category_array = data['sub_category_array']
    admin_id = data['admin_id']
    try:
        if key == 'vsinadmin':
            for i in range(0, len(sub_category_array)):
                adminsubobj = AdminSelectedSubCategories.objects.filter(sub_category_id=sub_category_array[i].get('id'),
                                                                        admins=admin_id).values()
                if len(adminsubobj) > 0:
                    adminsubvalue = AdminSelectedSubCategories.objects.get(id=adminsubobj[0].get('id'))
                    if adminsubvalue.sub_categories_priority != sub_category_array[i].get('priority'):
                        adminsubvalue.sub_categories_priority = sub_category_array[i].get('priority')
                        adminsubvalue.save()

            return Response({'status': 200, 'message': 'Admin Sub Categories Are Updated'}, status=200)

        else:
            return Response({'status': 401, 'message': 'Unauthorized'}, status=401)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['put'])
@permission_classes((AllowAny,))
def edit_admin_trending_sub_categories(request):
    data = request.data
    key = data['key']
    sub_category_array = data['sub_category_array']
    admin_id = data['admin_id']
    try:
        if key == 'vsinadmin':
            for i in range(0, len(sub_category_array)):
                adminsubobj = TrendingSubCategories.objects.filter(trending_sub_category_id=sub_category_array[i].get('id'),
                                                                   admins=admin_id).values()
                if len(adminsubobj) > 0:
                    adminsubvalue = TrendingSubCategories.objects.get(id=adminsubobj[0].get('id'))
                    if adminsubvalue.trending_sub_categories_priority != sub_category_array[i].get('priority'):
                        adminsubvalue.trending_sub_categories_priority = sub_category_array[i].get('priority')
                        adminsubvalue.save()
            return Response({'status': 200, 'message': 'Trending Sub Categories Are Updated'}, status=200)
        else:
            return Response({'status': 401, 'message': 'Unauthorized'}, status=401)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes((AllowAny,))
def contact_us_send_mail(request):
    data=request.data
    key=data['key']
    name=data['name']
    phone=data['phone']
    email=data['email']
    title=data['title']
    message=data['message']
    company_name=data['company_name']
    city=data['city']
    try:
        if key=='vsinadmin':
            basicobj=BasicCompanyDetails.objects.filter(company_name=company_name).values().order_by('company_code')
            if len(basicobj)>0:
                regobj=SelfRegistration.objects.filter(id=basicobj[0].get('updated_by_id')).values()
                # Configure API key authorization: api-key
                configuration = sib_api_v3_sdk.Configuration()
                configuration.api_key[
                    'api-key'] = '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'

                # create an instance of the API class
                configuration = sib_api_v3_sdk.Configuration()
                configuration.api_key[
                    'api-key'] = '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'

                api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
                subject = title
                text_content = "Dear " + company_name+"," +"\n\n" + message + "\n\n" + "Regards , "+"\n" + name + "\n"+phone+ "\n" +email +"\n"+city+"\n\n" + "Note: Please Don't Share this email with anyone"
                sender = {"name": name, "email":email}
                to = [{"email": regobj[0].get('username'), "name": regobj[0].get('contact_person')}]
                send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to,text_content=text_content,
                                                               sender=sender, subject=subject)
                print(send_smtp_email)
                try:
                    # Send a transactional email
                    api_response = api_instance.send_transac_email(send_smtp_email)
                    pprint(api_response)
                except ApiException as e:
                    print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
                return Response({'status': 200, 'message': 'Contact Us Mail Sent'}, status=200)
            else:
                return Response({'status': 204, 'message': 'Data not present for this particular company'}, status=204)
        else:
            return Response({'status': 401, 'message': 'Unauthorized'}, status=401)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

class BrandRegistrationView(viewsets.ModelViewSet):
    # Brand Registration information
    queryset = BrandRegistration.objects.all()
    serializer_class = BrandRegistrationSerializer
    permission_classes = (AllowAny,)


class BrandCompanyDetailsView(viewsets.ModelViewSet):
    # Brand Company Details
    queryset = BrandCompanyDetails.objects.all()
    serializer_class = BrandCompanyDetailsSerializer
    permission_classes = (AllowAny,)

class BasicSellerOrDistributerDetailsView(viewsets.ModelViewSet):
    # Basic Seller Or Distributer Details
    queryset = BasicSellerOrDistributerDetails.objects.all()
    serializer_class = BasicSellerOrDistributerDetailsSerializer
    permission_classes = (AllowAny,)

class BrandCompanyCommunicationDetailsView(viewsets.ModelViewSet):
    # Brand Company Communication Details
    queryset = BrandCompanyCommunicationDetails.objects.all()
    serializer_class = BrandCompanyCommunicationDetailsSerializer
    permission_classes = (AllowAny,)

class SellerOrDistributerCommunicationDetailsView(viewsets.ModelViewSet):
    # SellerOrDistributerCommunicationDetails
    queryset = SellerOrDistributerCommunicationDetails.objects.all()
    serializer_class = SellerOrDistributerCommunicationDetailsSerializer
    permission_classes = (AllowAny,)


class BrandLegalDocumentsViewSet(viewsets.ModelViewSet):
    # brand legal documents viewsets
    queryset = BrandLegalDocuments.objects.all()
    serializer_class = BrandLegalDocumentsSerializer
    permission_classes = (AllowAny,)