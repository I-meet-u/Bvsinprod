from __future__ import print_function
import time
import urllib
from pprint import pprint
import itertools
import json
import math
import random

from django.contrib.auth.hashers import make_password, check_password

import requests
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import SelfRegistration, SelfRegistration_Sample, BasicCompanyDetails, BillingAddress, ShippingAddress, \
    IndustrialInfo, IndustrialHierarchy, BankDetails, LegalDocuments, BasicCompanyDetails_Others, BillingAddress_Others, \
    ShippingAddress_Others, Employee_CompanyDetails, Employee_IndustryInfo, ContactDetails, \
    CommunicationDetails
from .serializers import SelfRegistrationSerializer, SelfRegistrationSerializerSample, BasicCompanyDetailsSerializers, \
    BillingAddressSerializer, ShippingAddressSerializer, IndustrialInfoSerializer, IndustrialHierarchySerializer, \
    BankDetailsSerializer, LegalDocumentsSerializers, BasicCompanyDetailsOthersSerializers,Employee_CompanyDetailsSerializers, Employee_IndustryInfoSerializer, \
    ContactDetailsSerializer, CommunicationDetailsSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

class SelfRegisterView(viewsets.ModelViewSet):
    # Register user information
    queryset = SelfRegistration.objects.all()
    serializer_class = SelfRegistrationSerializer
    permission_classes = (AllowAny,)
    ordering_fields = ['id']
    ordering = ['id']

class SelfRegistrationSampleView(viewsets.ModelViewSet):
    # registration user information sample view
    queryset= SelfRegistration_Sample.objects.all()
    serializer_class = SelfRegistrationSerializerSample
    permission_classes = (AllowAny,)
    ordering_fields = ['id']
    ordering = ['id']

    def perform_create(self, serializer):
        # Hash password but passwords are not required
        if ('password' in self.request.data):
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()

class LegalDocumentsView(viewsets.ModelViewSet):
    # legal document view
    # permission_classes = (AllowAny,)
    queryset = LegalDocuments.objects.all()
    serializer_class = LegalDocumentsSerializers
    parser_classes = [MultiPartParser]
    ordering_fields = ['id']
    ordering = ['id']

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        legalobj = LegalDocuments.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if not legalobj:
            raise ValidationError({'message': 'Legal Documents details not exist', 'status': 204})
        return legalobj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status':status.HTTP_204_NO_CONTENT, 'data':"Legal Documnent is deleted"})


class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)




@api_view(['post'])
# @permission_classes([AllowAny])
def get_token_key_by_userid(request):
    # geting token by userid
    data = request.data
    try:
        auth_token=Token.objects.filter(user_id=data['userid']).values('key')
        token=auth_token[0].get('key')
        return Response({'status': 200,'data':token}, status=200)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
# @permission_classes([AllowAny])
def get_userid_by_token(request):
    # get user_id by passing token
    data = request.data
    try:
        auth_token_userid=Token.objects.filter(key=data['token']).values('user_id')
        return Response({'status': 202,'data':auth_token_userid}, status=202)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
# @permission_classes((AllowAny,))
def change_email(request):
    # passing userid and already presented email and changing email to another email
    data=request.data
    email=data['email']
    userid=data['userid']
    try:
        user=SelfRegistration.objects.get(id=userid)
        user.username=email
        user.save()
        email_info = {'email': user.username}
        return Response({'status': 200, 'message': 'Email changed successfully','data': email_info}, status=200)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
# @permission_classes((AllowAny,))
def change_phonenumber(request):
    # change phone number by using userid and already presented phone and changed to new phone number
    data=request.data
    phonenumber=data['phonenumber']
    userid=data['userid']
    try:
        user=SelfRegistration.objects.get(id=userid)
        user.phone_number=phonenumber
        user.save()
        user_info={'phone_num':user.phone_number}
        return Response({'status': 200, 'message': 'Phone number changed successfully',
                         'data': user_info}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
# @permission_classes((AllowAny,))
def change_password_with_phone_number(request):
    # change password by using phone_number
    data = request.data
    phonenumber=data['phonenumber']
    try:
        user = SelfRegistration.objects.get(phone_number=phonenumber)
        if user:
            user.set_password(data['password'])
            user.save()
            return Response({'status': 200, 'message': 'Password changed successfully with phone number'}, status=200)
        else:
            return Response({'status': 424, 'message': 'OTP not match'}, status=424)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
# @permission_classes((AllowAny,))
def change_password_with_email(request):
    # change password by using email_id
    data = request.data
    password=data['password']
    email=data['email']
    name="hari"
    try:
        user = SelfRegistration.objects.get(username=email)
        if user:

            user.set_password(password)
            user.save()

            headers = {
                'accept': 'application/json',
                'api-key': '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',
                'content-type': 'application/json',
            }
            data = '{ "sender":{ "name":"VENDORSIN COMMERCE PVT LTD", "email":"admin@vendorsin.com" }, "to":[ { "email":"' + email + '' \
                                                                                                                                     '", "name":"Harish" } ], "subject":"Vendorsin Portal password was changed", "templateId":15 ''}'



            # data = '{ "sender":{ "name":"VENDORSIN COMMERCE PVT LTD", "email":"admin@vendorsin.com" },"subject":"This is my default subject line","templateId":96,"to":[ { "email":"harishshetty7459@gmail.com", "name":"harish" } ]'

            response = requests.post('https://api.sendinblue.com/v3/smtp/email', headers=headers, data=data)
            print("----")
            print(response)
            print("----")



            return Response({'status': 200, 'message': 'Password changed successfully'}, status=200)
        else:
            return Response({'status': 424, 'message': "Email not exist"}, status=424)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['post'])
# @permission_classes((AllowAny,))
def otp_session_time_out_of_phone_and_email(request):
    #otp session time out for both phone and email by using user_id
    data=request.data

    try:
        sessionobj=SelfRegistration.objects.get(id=data['user_id'])
        if sessionobj:
            sessionobj.phone_otp=''
            sessionobj.email_otp=''
            sessionobj.save()
            return Response({'status':200,'message':"OTP session timeout"},status=200)
        else:
            return Response({'status':202,'message':"Not Found"},status=202)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['post'])
# @permission_classes((AllowAny,))
def phone_otp_session_out(request):
    # otp session time out for both phone  by using user_id
    data=request.data

    try:
        phonesessionobj=SelfRegistration.objects.get(id=data['user_id'])
        if phonesessionobj:
            phonesessionobj.phone_otp=''
            phonesessionobj.save()
            return Response({'status':200,'message':"Phone OTP session timeout"},status=200)
        else:
            return Response({'status':202,'message':"Not Found"},status=202)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
# @permission_classes((AllowAny,))
def email_otp_session_out(request):
    # otp session time out for both email by using user_id
    data = request.data
    try:
        emailsessionobj = SelfRegistration.objects.get(id=data['user_id'])
        if emailsessionobj:
            emailsessionobj.email_otp = ''
            emailsessionobj.save()
            return Response({'status': 200, 'message': "Email OTP session timeout"}, status=200)
        else:
            return Response({'status': 202, 'message': "Not Found"}, status=202)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


class BasicCompanyDetailsView(viewsets.ModelViewSet):
    # basic company info viewset
    permission_classes = [permissions.AllowAny]
    queryset = BasicCompanyDetails.objects.all()
    serializer_class = BasicCompanyDetailsSerializers
    ordering_fields = ['id']
    ordering = ['id']

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        basicobj = BasicCompanyDetails.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if not basicobj:
            raise ValidationError({'message': 'Basic Details not exist','status':204})
        return basicobj


class BillingAddressView(viewsets.ModelViewSet):
    # billing address viewsets
    # permission_classes = (AllowAny,)
    queryset = BillingAddress.objects.all()
    serializer_class = BillingAddressSerializer
    ordering_fields = ['id']
    ordering = ['id']

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        basicobj = BillingAddress.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if not basicobj:
            raise ValidationError({'message': 'Billing Address not exist', 'status': 204})
        return basicobj



class ShippingAddressView(viewsets.ModelViewSet):
    # shipping address viewsets
    # permission_classes = (AllowAny,)
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer
    ordering_fields = ['id']
    ordering = ['id']

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        basicobj = ShippingAddress.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if not basicobj:
            raise ValidationError({'message': 'Shipping Address not exist', 'status': 204})
        return basicobj


class IndustrialInfoView(viewsets.ModelViewSet):
    # industrail info viewsets
    # permission_classes = (AllowAny,)
    queryset =IndustrialInfo.objects.all()
    serializer_class=IndustrialInfoSerializer
    ordering_fields = ['id']
    ordering = ['id']

    def create(self,request,*args, **kwargs):
        updated_by = request.data.get('updated_by', None)
        created_by=request.data.get('created_by',None)
        nature_of_business=request.data.get('nature_of_business',None)
        geographical_area=request.data.get('geographical_area',None)
        supply_capabilites=request.data.get('supply_capabilites',None)
        industry_to_serve=request.data.get('industry_to_serve',None)
        company_code=request.data.get('company_code',None)
        try:
            industryobj=IndustrialInfo.objects.update_or_create(nature_of_business=nature_of_business,
                                                      geographical_area=geographical_area,
                                                      supply_capabilites=supply_capabilites,
                                                      industry_to_serve=industry_to_serve,
                                                      updated_by=SelfRegistration.objects.get(id=updated_by),
                                                      created_by=created_by,
                                                      company_code=BasicCompanyDetails.objects.get(company_code=company_code))

            # print(industryobj.)
            # industryobj.company_code=company_code
            # industryobj.save()
            regobj = SelfRegistration.objects.get(id=updated_by)
            regobj.nature_of_business = nature_of_business
            regobj.save()
            return Response({'status': 201, 'message': 'Industry Info Created'}, status=201)


        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)


    def get_queryset(self):
        # it determines the list of objects that you want to display by passing userid(updated_by)
        industryinfoobj = IndustrialInfo.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if not industryinfoobj:
            raise ValidationError({'message': 'Industry info details not exist','status':204})
        return industryinfoobj



class IndustrialHierarchyView(viewsets.ModelViewSet):
    # industrial hierarchy viewsets
    # permission_classes = (AllowAny,)
    queryset =IndustrialHierarchy.objects.all()
    serializer_class=IndustrialHierarchySerializer
    ordering_fields = ['id']
    ordering = ['id']

    def get_queryset(self):
        # it determines the list of objects that you want to display by passing userid(updated_by)
        industryhierarchyobj = IndustrialHierarchy.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if not industryhierarchyobj:
            raise ValidationError({'message': 'Industry hierarchy  details not exist','status':204})
        return industryhierarchyobj

class BankDetailsView(viewsets.ModelViewSet):
    # bank details viewsets
    # permission_classes = (AllowAny,)
    queryset =BankDetails.objects.all()
    serializer_class=BankDetailsSerializer
    ordering_fields = ['id']
    ordering = ['id']

    def get_queryset(self):
        # it determines the list of objects that you want to display by passing userid(updated_by)
        bankobj = BankDetails.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if not bankobj:
            raise ValidationError({'message': 'Bank Details not exist','status':204})
        return bankobj

@api_view(['post'])
# @permission_classes((AllowAny,))
def list_documents_user(request):
    data = request.data
    msme = data['msme']
    msmeexist = False
    cancelledcheck = False
    panexist = False
    docarray = []
    try:
        userdoc = list(LegalDocuments.objects.filter(updated_by=data['userid']).values())

        print(len(userdoc))
        if len(userdoc) > 0:
            print("inside")
            if msme == "Yes":
                print("yes inside")
                for i in range(len(userdoc)):
                    if userdoc[i].get('document_name') == "msmecertificate":
                        docarray.append('msmecertificate')
                    if userdoc[i].get('document_name') == "cancelledcheque":
                        docarray.append('cancelledcheque')
                    if userdoc[i].get('document_name') == "pancard":
                        docarray.append('pancard')
                    if userdoc[i].get('document_name') == "registerediec":
                        docarray.append('registerediec')
            else:
                for i in range(len(userdoc)):
                    if userdoc[i].get('document_name') == "cancelledcheque":
                        docarray.append('cancelledcheque')
                    if userdoc[i].get('document_name') == "pancard":
                        docarray.append('pancard')

        return Response({'status': 200, 'message': "Success", 'data': docarray}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


class BasicCompanyDetailsOthersView(viewsets.ModelViewSet):
    # basic company info viewset
    # permission_classes = (AllowAny,)
    queryset = BasicCompanyDetails_Others.objects.all()
    serializer_class = BasicCompanyDetailsOthersSerializers
    ordering_fields = ['id']
    ordering = ['id']

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        basicobj = BasicCompanyDetails_Others.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if not basicobj:
            raise ValidationError({'message': 'Basic Details not exist','status':204})
        return basicobj

@api_view(['post'])
# @permission_classes((AllowAny,))
def all_basic_data(request):
    data=request.data
    user_id=data['user_id']
    try:
        basic_obj=BasicCompanyDetails_Others.objects.count()
        if basic_obj==0:
            company_code='100001'
        else:
            basic_obj=BasicCompanyDetails_Others.objects.values_list('company_code', flat=True).last()
            company_code=int(basic_obj)+1
            print(company_code)
        basicobject=BasicCompanyDetails_Others.objects.filter(updated_by=user_id).values()
        if len(basicobject)==0:
            basicobjcode = BasicCompanyDetails_Others.objects.create(company_code=company_code,
                                                                     company_name=data['company_name'],
                                                                     company_established=data['company_established'],
                                                                     industrial_scale=data['industrial_scale'],
                                                                     market_location=data['market_location'],
                                                                     company_type=data['company_type'],
                                                                     tax_id_or_vat=data['tax_id_or_vat'],
                                                                     currency=data['currency'],
                                                                     created_by=data['created_by'],
                                                                     updated_by=SelfRegistration.objects.get(id=user_id)
                                                                     )
            BillingAddress_Others.objects.create(company_code_others=BasicCompanyDetails_Others.objects.get(company_code=basicobjcode.company_code),
                                        updated_by_others=SelfRegistration.objects.get(id=user_id),
                                        bill_address_others=data['bill_address_others'],
                                        bill_country_others=data['bill_country_others'],
                                        bill_state_others=data['bill_state_others'],
                                        bill_city_others=data['bill_city_others'],
                                        bill_pincode_others=data['bill_pincode_others'],
                                        bill_landmark_others=data['bill_landmark_others'],
                                        bill_location_others=data['bill_location_others'],
                                        created_by_others=data['created_by'])

            ShippingAddress_Others.objects.create(company_code_others=BasicCompanyDetails_Others.objects.get(company_code=basicobjcode.company_code),
                                           updated_by_others=SelfRegistration.objects.get(id=user_id),
                                           ship_address_others=data['ship_address_others'],
                                           ship_country_others=data['ship_country_others'],
                                           ship_state_others=data['ship_state_others'],
                                           ship_city_others=data['ship_city_others'],
                                           ship_pincode_others=data['ship_pincode_others'],
                                           ship_landmark_others=data['ship_landmark_others'],
                                           ship_location_others=data['ship_location_others'],
                                           created_by_others=data['created_by']
                                           )

            return Response({'status':200,'message':'Basic Details Created','data':basicobjcode.company_code},status=200)
        else:
            return Response({'status': 202, 'message': 'Basic Details Already present','data':basicobject[0].get('company_code')}, status=202)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


# class EmployeeRegistrationView(viewsets.ModelViewSet):
#     permission_classes = (AllowAny,)
#     queryset = EmployeeRegistration.objects.all()
#     serializer_class = EmployeeRegistrationSerializer
#     ordering_fields = ['emp_id']
#     ordering = ['emp_id']
#
#     def perform_create(self, serializer):
#         # Hash password but passwords are not required
#         if ('password' in self.request.data):
#             password = make_password(self.request.data['password'])
#             serializer.save(password=password)
#         else:
#             serializer.save()
#
#     def perform_update(self, serializer):
#         if ('password' in self.request.data):
#             password = make_password(self.request.data['password'])
#             serializer.save(password=password)
#         else:
#             serializer.save()


class Employee_CompanyDetailsView(viewsets.ModelViewSet):
    # employee company info viewset
    # permission_classes = (AllowAny,)
    queryset = Employee_CompanyDetails.objects.all()
    serializer_class = Employee_CompanyDetailsSerializers

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        employeeobj = Employee_CompanyDetails.objects.filter(emp_updated_by=self.request.GET.get('emp_updated_by'))
        if not employeeobj:
            raise ValidationError({'message': 'Employee Basic Details not exist','status':204})
        return employeeobj

class EmployeeIndustrialInfoView(viewsets.ModelViewSet):
    # industrail info viewsets
    # permission_classes = (AllowAny,)
    queryset =Employee_IndustryInfo.objects.all()
    serializer_class=Employee_IndustryInfoSerializer

    def get_queryset(self):
        # it determines the list of objects that you want to display by passing userid(updated_by)
        employee_industry = Employee_IndustryInfo.objects.filter(emp_updated_by=self.request.GET.get('emp_updated_by'))
        if not employee_industry:
            raise ValidationError({'message': ' Employee Industry info details not exist','status':204})
        return employee_industry



@api_view(['post'])
# @permission_classes((AllowAny,))
def sendOtpmail(request):
    data=request.data
    phone=data['phone']
    email=data['email']
    sendotpvar=data['sendotpvar']
    digits = "0123456789"
    try:
        if sendotpvar=="email":

            user = SelfRegistration.objects.get(username=email)
            if user:
                pass
                OTP = ""
                for i in range(6):
                    OTP += digits[math.floor(random.random() * 10)]
                print(OTP)
                user.phone_otp = OTP
                user.save()
                OTP="333333"
                headers = {
                    'accept': 'application/json',
                    'api-key': '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',
                    'content-type': 'application/json',
                }
                data = '{ "sender":{ "name":"VENDORSIN COMMERCE PVT LTD", "email":"admin@vendorsin.com" }, "to":[ { "email":"'+email+'' \
                                                                                                                                 '", "name":"Harish" } ], "subject":"OTP Confirmation", "templateId":1 ,"params":{"OTP":'+OTP+'}''}'


            # data = '{ "sender":{ "name":"VENDORSIN COMMERCE PVT LTD", "email":"admin@vendorsin.com" },"subject":"This is my default subject line","templateId":96,"to":[ { "email":"harishshetty7459@gmail.com", "name":"harish" } ]'

                response = requests.post('https://api.sendinblue.com/v3/smtp/email', headers=headers, data=data)
                print("----")
                print(response)
                print("----")

        if sendotpvar=="phone":
            phoneuser = SelfRegistration.objects.get(phone_number=phone)
            if phoneuser:
                OTP = "234543"
                for i in range(6):
                    OTP += digits[math.floor(random.random() * 10)]
                print(OTP)
                user.phone_otp = OTP
                user.save()

                apikey = 'YTU3NjhmMDdmYjFlYzA2OWY0YzhlNjA3YmEyYjMxNGM='
                numbers = '918095994214'
                message = OTP + ' Is The OTP To Verify Your Mobile Number On VENDORSIN COMMERCE Self Registration Portal. Do Not Share It With Anyone .'
                sender = 'VSINVC'

                data = urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
                                               'message': message, 'sender': sender,
                                               'Template Name': 'REGISTRATION OTP'})
                data = data.encode('utf-8')
                request = urllib.request.Request("https://api.textlocal.in/send/?")
                f = urllib.request.urlopen(request, data)
                fr = f.read()
                print(fr)

        if sendotpvar=="Both":
            emailuser = SelfRegistration.objects.get(username=email)
            if emailuser:
                OTP = ""
                for i in range(6):
                    OTP += digits[math.floor(random.random() * 10)]
                print(OTP)
                emailuser.email_otp = OTP
                emailuser.save()
                headers = {
                    'accept': 'application/json',
                    'api-key': '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',
                    'content-type': 'application/json',
                }
                data = '{ "sender":{ "name":"VENDORSIN COMMERCE PVT LTD", "email":"admin@vendorsin.com" }, "to":[ { "email":"' + email + '' \
                                                                                                                                         '", "name":"Harish" } ], "subject":"VENDORSIN Registration OTP", "templateId":6 ,"params":{"OTP":' + OTP + '}''}'

                response = requests.post('https://api.sendinblue.com/v3/smtp/email', headers=headers, data=data)
                print("----")
                print(response)
                print("----")


            phoneuser = SelfRegistration.objects.get(phone_number=phone)
            if phoneuser:
                OTP=""
                for i in range(6):
                    OTP += digits[math.floor(random.random() * 10)]
                print(OTP)
                phoneuser.phone_otp = OTP
                phoneuser.save()

                apikey = 'YTU3NjhmMDdmYjFlYzA2OWY0YzhlNjA3YmEyYjMxNGM='
                numbers = '91'+phone
                message = OTP + ' Is The OTP To Verify Your Mobile Number On VENDORSIN COMMERCE Self Registration Portal. Do Not Share It With Anyone .'
                sender = 'VSINVC'

                data = urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
                                               'message': message, 'sender': sender})
                data = data.encode('utf-8')
                request = urllib.request.Request("https://api.textlocal.in/send/?")
                f = urllib.request.urlopen(request, data)
                fr = f.read()
                print(fr)


            return Response({'status': 200, 'message': 'ok'}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
# @permission_classes((AllowAny,))
def sendbluemail(request):
    data=request.data
    email = data['email']
    digits = "0123456789"
    try:
        emailuser = SelfRegistration.objects.get(username=email)
        if emailuser:
            OTP = ""
            for i in range(6):
                OTP += digits[math.floor(random.random() * 10)]
            print(OTP)
            emailuser.email_otp = OTP
            emailuser.save()
            headers = {
                'accept': 'application/json',
                'api-key': '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',
                'content-type': 'application/json',
            }
            data = '{ "sender":{ "name":"VENDORSIN COMMERCE PVT LTD", "email":"admin@vendorsin.com" }, "to":[ { "email":"' + email + '' \
                                                                                                                                 '", "name":"Harish" } ], "subject":"VENDORSIN Registration OTP", "templateId":6 ,"params":{"OTP":' + OTP + '}''}'

        # data = '{ "sender":{ "name":"VENDORSIN COMMERCE PVT LTD", "email":"admin@vendorsin.com" },"subject":"This is my default subject line","templateId":96,"to":[ { "email":"harishshetty7459@gmail.com", "name":"harish" } ]'

            response = requests.post('https://api.sendinblue.com/v3/smtp/email', headers=headers, data=data)
            print("----")
            print(response)
            print("----")

        return Response({'status': 200, 'message': 'ok','data':OTP}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
# @permission_classes((AllowAny,))
def sendbluemailforgot(request):
    data=request.data
    email = data['email']
    digits = "0123456789"
    try:
        emailuser = SelfRegistration.objects.get(username=email)
        if emailuser:
            OTP = ""
            for i in range(6):
                OTP += digits[math.floor(random.random() * 10)]
            print(OTP)
            emailuser.email_otp = OTP
            emailuser.save()
            headers = {
                'accept': 'application/json',
                'api-key': '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',
                'content-type': 'application/json',
            }
            data = '{ "sender":{ "name":"VENDORSIN COMMERCE PVT LTD", "email":"admin@vendorsin.com" }, "to":[ { "email":"' + email + '' \
                                                                                                                                     '", "name":"Harish" } ], "subject":"Reset Password Vendorsin Portals", "templateId":20,"params":{"OTP":' + OTP + '}''}'
        # data = '{ "sender":{ "name":"VENDORSIN COMMERCE PVT LTD", "email":"admin@vendorsin.com" },"subject":"This is my default subject line","templateId":96,"to":[ { "email":"harishshetty7459@gmail.com", "name":"harish" } ]'

            response = requests.post('https://api.sendinblue.com/v3/smtp/email', headers=headers, data=data)
            print("----")
            print(response)
            print("----")

        return Response({'status': 200, 'message': 'ok','data':OTP}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
# @permission_classes((AllowAny,))
def sendSMS(request):
    data=request.data
    digits = "0123456789"
    phone=data['phone']
    try:
        phoneuser = SelfRegistration.objects.get(phone_number=phone)
        if phoneuser:
            OTP = ""
            for i in range(6):
                OTP += digits[math.floor(random.random() * 10)]
            print(OTP)
            phoneuser.phone_otp = OTP
            phoneuser.save()

            apikey = 'YTU3NjhmMDdmYjFlYzA2OWY0YzhlNjA3YmEyYjMxNGM='
            numbers = '91' + phone
            message = OTP + ' Is The OTP To Verify Your Mobile Number On VENDORSIN COMMERCE Self Registration Portal. Do Not Share It With Anyone .'
            sender = 'VSINVC'

            data = urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
                                           'message': message, 'sender': sender})
            data = data.encode('utf-8')
            request = urllib.request.Request("https://api.textlocal.in/send/?")
            f = urllib.request.urlopen(request, data)
            fr = f.read()
            print(fr)

        return Response({'status': 200, 'message': "Success",'data':OTP}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
# @permission_classes((AllowAny,))
def checkotp(request):
    data=request.data
    userid=data['userid']
    try:
        user = SelfRegistration.objects.get(id=userid)
        if user:
            if user.phone_otp==data['phone_otp'] and user.email_otp==data['email_otp']:

                return Response({'status': 200, 'message': "Both OTP Matching"}, status=200)
            else:
                return Response({'status': 202, 'message': "OTP Not Matching"}, status=202)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
# @permission_classes((AllowAny,))
def checkemailotp(request):
    data = request.data
    userid = data['userid']
    try:
        user = SelfRegistration.objects.get(id=userid)
        if user:
            if user.email_otp == data['email_otp']:

                return Response({'status': 200, 'message': "OTP Matching"}, status=200)
            else:
                return Response({'status': 202, 'message': "OTP Not Matching"}, status=202)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
# @permission_classes((AllowAny,))
def checkphoneotp(request):
    data=request.data
    userid=data['userid']
    otp=data['phone_otp']
    try:
        user = SelfRegistration.objects.get(id=userid)
        if user:
            if user.phone_otp==otp:
                return Response({'status': 200, 'message': "Both OTP Matching"}, status=200)
            else:
                return Response({'status': 202, 'message': "OTP Not Matching"}, status=202)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
# @permission_classes((AllowAny,))
def checkotpemailt(request):
    data=request.data
    userid=data['userid']
    try:
        user = SelfRegistration.objects.get(id=userid)
        if user:
            if user.phone_otp==data['phone_otp'] and user.email_otp==data['email_otp']:

                return Response({'status': 200, 'message': "Both OTP Matching"}, status=200)
            else:
                return Response({'status': 202, 'message': "OTP Not Matching"}, status=202)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
# @permission_classes((AllowAny,))
def changeemail(request):
    data=request.data
    userid=data['userid']
    email=data['email']
    digits = "0123456789"
    try:
        user = SelfRegistration.objects.get(id=userid)
        if user:
            if user.username!=email:
                user.username = email
                user.save()

                OTP = ""
                for i in range(6):
                    OTP += digits[math.floor(random.random() * 10)]
                print(OTP)
                user.email_otp = OTP
                user.save()
                headers = {
                    'accept': 'application/json',
                    'api-key': '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',
                    'content-type': 'application/json',
                }
                data = '{ "sender":{ "name":"VENDORSIN COMMERCE PVT LTD", "email":"admin@vendorsin.com" }, "to":[ { "email":"' + email + '' \
                                                                                                                                         '", "name":"Harish" } ], "subject":"VENDORSIN Registration OTP", "templateId":6 ,"params":{"OTP":' + OTP + '}''}'

                # data = '{ "sender":{ "name":"VENDORSIN COMMERCE PVT LTD", "email":"admin@vendorsin.com" },"subject":"This is my default subject line","templateId":96,"to":[ { "email":"harishshetty7459@gmail.com", "name":"harish" } ]'

                response = requests.post('https://api.sendinblue.com/v3/smtp/email', headers=headers, data=data)
                print("----")
                print(response)
                print("----")

                return Response({'status': 200, 'message': "success"}, status=200)
            else:
                return Response({'status': 202, 'message': "Already Exist"}, status=202)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
# @permission_classes((AllowAny,))
def changephone(request):
    data = request.data
    userid = data['userid']
    phone = data['phone']
    digits = "0123456789"
    try:
        user = SelfRegistration.objects.get(id=userid)
        if user:
            if user.phone_number != phone:
                user.phone_number = phone
                user.save()
                OTP = ""
                for i in range(6):
                    OTP += digits[math.floor(random.random() * 10)]
                print(OTP)
                user.phone_otp = OTP
                user.save()

                apikey = 'YTU3NjhmMDdmYjFlYzA2OWY0YzhlNjA3YmEyYjMxNGM='
                numbers = '91' + phone
                message = OTP + ' Is The OTP To Verify Your Mobile Number On VENDORSIN COMMERCE Self Registration Portal. Do Not Share It With Anyone .'
                sender = 'VSINVC'

                data = urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
                                               'message': message, 'sender': sender})
                data = data.encode('utf-8')
                request = urllib.request.Request("https://api.textlocal.in/send/?")
                f = urllib.request.urlopen(request, data)
                fr = f.read()
                print(fr)

                return Response({'status': 200, 'message': "success"}, status=200)
            else:
                return Response({'status': 202, 'message': "Already Exist"}, status=202)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


# -------------------------------------user-dp-upload----------------------------------------------------
@api_view(['post'])
# @permission_classes((AllowAny,))
def uploaduserprofile(request):
    data = request.data
    try:
        profileimgobj = SelfRegistration.objects.get(id=data['userid'])
        if profileimgobj:
            profileimgobj.profile_cover_photo = data['profileimg']
            profileimgobj.save()
            return Response({'status': 200, 'message': 'profile uploaded'}, status=200)
        else:
            return Response({'status': 404, 'message': 'user not found'}, status=404)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
# @permission_classes((AllowAny,))
def phone_otp_verify(request):
    data=request.data
    phoneotp=data['phoneotp']
    phonenumber=data['phonenumber']
    try:
        regobj=SelfRegistration.objects.get(phone_number=phonenumber)
        if regobj.phone_otp==phoneotp and regobj.phone_number==phonenumber:
            return Response({'status':200,'message':'Phone Otp Verified'},status=200)
        else:
            return Response({'status': 204, 'message': 'Phone otp not verified or otp is not correct'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
# @permission_classes((AllowAny,))
def email_otp_verify(request):
    data=request.data
    emailotp=data['emailotp']
    emailid=data['emailid']
    try:
        regobj=SelfRegistration.objects.get(username=emailid)
        if regobj.email_otp==emailotp and regobj.username==emailid:
            return Response({'status':200,'message':'Email Otp Verified'},status=200)
        else:
            return Response({'status': 204, 'message': 'Email otp not verified or otp is not correct'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




# @api_view(['post'])
# # @permission_classes((AllowAny,))
# def employee_login(request):
#     data = request.data
#     password = data['password']
#     email_id = data['email_id']
#     try:
#         employeeobj = SelfRegistration.objects.get(email_id=email_id)
#         if employeeobj:
#             if check_password(password, employeeobj.password) and employeeobj.email_id == email_id:
#                 return Response({'status': 200, 'message': 'Employee Logged in successfully'}, status=200)
#             else:
#                 return Response({'status': 424, 'message': 'Password entered is not correct,Please Check Once'},
#                             status=424)
#
#     except ObjectDoesNotExist as e:
#         return Response({'status': 404, 'error': "Email not exist"}, status=404)
#
#     except Exception as e:
#         return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
# @permission_classes((AllowAny,))
def getcompanycode(request):
    data=request.data
    usercompcode=""
    try:
        basicobj=BasicCompanyDetails.objects.filter().last()
        print(basicobj)
        Basicobjuser=BasicCompanyDetails.objects.filter(updated_by=data['updated_by']).values()
        if len(Basicobjuser)!=0:
            usercompcode=Basicobjuser[0].get('company_code')
            return Response({'status': 200, 'lastcompanycode':basicobj.company_code,'usercode':usercompcode}, status=200)
        else:
            return Response({'status': 202, 'lastcompanycode': basicobj.company_code, 'usercode':0},
                            status=202)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



class ContactDetailsViewset(viewsets.ModelViewSet):
    queryset = ContactDetails.objects.all()
    serializer_class = ContactDetailsSerializer
    # permission_classes = (AllowAny,)

    def get_queryset(self):
        # overriding get_queryset by passing updated_by
        contactobj = ContactDetails.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by('id')
        if not contactobj:
            raise ValidationError({'message': 'Contact Details not exist', 'status': 204})
        return contactobj

class CommunicationDetailsViewset(viewsets.ModelViewSet):
    queryset = CommunicationDetails.objects.all()
    serializer_class = CommunicationDetailsSerializer
    # permission_classes = (AllowAny,)

    def get_queryset(self):
        # overriding get_queryset by passing updated_by
        communicationobj = CommunicationDetails.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by('id')
        if not communicationobj:
            raise ValidationError({'message': 'Communication Details not exist', 'status': 204})
        return communicationobj


@api_view(['post'])
def get_profile_photo(request):
    data=request.data
    try:
        regobj=SelfRegistration.objects.filter(id=data['userid']).values('profile_cover_photo')
        if len(regobj)>0:
            return Response({'status':200,'message':'Profile Photo','data':regobj},status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'No Present'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['put'])
def update_basic_details(request):
    data=request.data
    userid=data['userid']
    gst_number=data['gst_number']
    company_name=data['company_name']
    company_type=data['company_type']
    listing_date=data['listing_date']
    pan_number=data['pan_number']
    tax_payer_type=data['tax_payer_type']
    msme_registered=data['msme_registered']
    company_established=data['company_established']
    registered_iec=data['registered_iec']
    industrial_scale=data['industrial_scale']
    bill_address=data['bill_address']
    bill_country=data['bill_country']
    bill_state=data['bill_state']
    bill_city=data['bill_city']
    bill_pincode=data['bill_pincode']
    bill_landmark=data['bill_landmark']
    bill_location=data['bill_location']
    ship_address=data['ship_address']
    ship_country=data['ship_country']
    ship_state=data['ship_state']
    ship_city=data['ship_city']
    ship_pincode=data['ship_pincode']
    ship_landmark=data['ship_landmark']
    ship_location=data['ship_location']
    try:
        basicobj=BasicCompanyDetails.objects.filter(updated_by_id=userid).values().order_by('company_code')
        billaddressbj=BillingAddress.objects.filter(updated_by_id=userid,company_code_id=basicobj[0].get('company_code')).values().order_by('id')
        shippingaddressobj=ShippingAddress.objects.filter(updated_by_id=userid,company_code_id=basicobj[0].get('company_code')).values().order_by('id')

        if len(basicobj)>0 and len(billaddressbj)>0 and len(shippingaddressobj)>0:
            basicedit=BasicCompanyDetails.objects.get(updated_by_id=basicobj[0].get('updated_by_id'),company_code=basicobj[0].get('company_code'))
            billedit=BillingAddress.objects.get(updated_by_id=billaddressbj[0].get('updated_by_id'),company_code_id=billaddressbj[0].get('company_code_id'),id=billaddressbj[0].get('id'))
            print(billedit.id)
            shipedit=ShippingAddress.objects.get(updated_by_id=shippingaddressobj[0].get('updated_by_id'),company_code_id=shippingaddressobj[0].get('company_code_id'),id=shippingaddressobj[0].get('id'))

            if basicedit and basicedit.updated_by_id!="":
                if basicedit.gst_number!=gst_number:
                    basicedit.gst_number=gst_number
                    basicedit.save()
                if basicedit.company_name!=company_name:
                    basicedit.company_name=company_name
                    basicedit.save()
                if basicedit.company_type!=company_type:
                    basicedit.company_type=company_type
                    basicedit.save()
                if basicedit.listing_date!=listing_date:
                    basicedit.listing_date=listing_date
                    basicedit.save()
                if basicedit.pan_number!=pan_number:
                    basicedit.pan_number=pan_number
                    basicedit.save()

                if basicedit.tax_payer_type!=tax_payer_type:
                    basicedit.tax_payer_type=tax_payer_type
                    basicedit.save()

                if basicedit.msme_registered!=msme_registered:
                    basicedit.msme_registered=msme_registered
                    basicedit.save()

                if basicedit.company_established!=company_established:
                    basicedit.company_established=company_established
                    basicedit.save()

                if basicedit.registered_iec!=registered_iec:
                    basicedit.registered_iec=registered_iec
                    basicedit.save()

                if basicedit.industrial_scale!=industrial_scale:
                    basicedit.industrial_scale=industrial_scale
                    basicedit.save()

                if billedit.bill_address!=bill_address:
                    billedit.bill_address=bill_address
                    billedit.save()

                if  billedit.bill_country!=bill_country:
                    billedit.bill_country=bill_country
                    billedit.save()

                if billedit.bill_state!=bill_state:
                    billedit.bill_state=bill_state
                    basicedit.save()

                if billedit.bill_city!=bill_city:
                    billedit.bill_city=bill_city
                    billedit.save()

                if billedit.bill_pincode!=bill_pincode:
                    billedit.bill_pincode=bill_pincode
                    billedit.save()

                if billedit.bill_landmark!=bill_landmark:
                    billedit.bill_landmark=bill_landmark
                    billedit.save()

                if billedit.bill_location!=bill_location:
                    billedit.bill_location=bill_location
                    billedit.save()

                if shipedit.ship_address!=ship_address:
                    shipedit.ship_address=ship_address
                    shipedit.save()

                if shipedit.ship_country!=ship_country:
                    shipedit.ship_country=ship_country
                    shipedit.save()

                if shipedit.ship_state!=ship_state:
                    shipedit.ship_state=ship_state
                    shipedit.save()

                if shipedit.ship_city!=ship_city:
                    shipedit.ship_city=ship_city
                    shipedit.save()

                if shipedit.ship_pincode!=ship_pincode:
                    shipedit.ship_pincode=ship_pincode
                    shipedit.save()

                if shipedit.ship_landmark!=ship_landmark:
                    shipedit.ship_landmark=ship_landmark
                    shipedit.save()

                if shipedit.ship_location!=ship_location:
                    shipedit.ship_location=ship_location
                    shipedit.save()
            return Response({'status': 200, 'message': 'Basic Details Updated Successfully'},
                                status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)



@api_view(['post'])
def admin_approval_mail_send(request):
    data = request.data
    digits = '0123456789'
    userid = data['userid']

    try:
        userdeatils = SelfRegistration.objects.filter(id=userid).values()
        print(userdeatils)
        recemail = userdeatils[0].get('username')
        print(recemail)
        headers = {
            'accept': 'application/json',
            'api-key': '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',
            'content-type': 'application/json',
        }
        data = '{ "sender":{ "name":"VENDORSIN COMMERCE PVT LTD", "email":"admin@vendorsin.com" }, "to":[ { "email":"' + recemail + '' \
                                                                                                                                 '", "name":"Harish" } ], "subject":"VENDORSIN Registration OTP", "templateId":8 ,"params":{"username":' + '1234' + '}''}'

        # data = '{ "sender":{ "name":"VENDORSIN COMMERCE PVT LTD", "email":"admin@vendorsin.com" },"subject":"This is my default subject line","templateId":96,"to":[ { "email":"harishshetty7459@gmail.com", "name":"harish" } ]'

        response = requests.post('https://api.sendinblue.com/v3/smtp/email', headers=headers, data=data)
        print("----")
        print(response)
        print("----")
        return Response({'status': 200, 'message': 'mail sent successfully'}, status=200)

    except ObjectDoesNotExist as e:
        return Response({'status': 424, 'error': "email not exist"}, status=404)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes([AllowAny])
def registration_list_by_user_id(request):
    data=request.data
    emptydata=[]
    try:
        regobj=SelfRegistration.objects.filter(username=data['email_id']).values()
        print(regobj)
        if regobj[0].get('user_type')!="Buyer":
            if len(regobj)>0:
                userval=regobj[0].get('id')
                basicobj = BasicCompanyDetails.objects.filter(updated_by=userval).values()
                if basicobj:
                    industry_info = IndustrialInfo.objects.filter(updated_by=userval).values()
                    if industry_info:
                        industry_hierarchy = IndustrialHierarchy.objects.filter(updated_by=userval).values()
                        if industry_hierarchy:
                            bankdetails = BankDetails.objects.filter(updated_by=userval).values()
                            if bankdetails:
                                legalobj = LegalDocuments.objects.filter(updated_by=userval).values()
                                if legalobj:
                                    emptydata.append({"id":userval,
                                                      "user_type": regobj[0].get('user_type'),
                                                      'company_code': basicobj[0].get('company_code'),
                                                       "registration_status": "Legal Documents"})
                                else:
                                    emptydata.append({"id":userval,
                                                      "user_type": regobj[0].get('user_type'),
                                                      'company_code': basicobj[0].get('company_code'),
                                                      "registration_status": "Bank Details"})

                            else:
                                emptydata.append({"id":userval,
                                                  "user_type": regobj[0].get('user_type'),
                                                  'company_code': basicobj[0].get('company_code'),
                                                  "registration_status": "Industry hierarchy"})

                        else:
                            emptydata.append({"id":userval,
                                              "user_type": regobj[0].get('user_type'),
                                              'company_code': basicobj[0].get('company_code'),
                                              "registration_status": "Seller Info"})
                    else:
                        emptydata.append({"id":userval,
                                          "user_type": regobj[0].get('user_type'),
                                          'company_code':basicobj[0].get('company_code'),
                                          "registration_status": "Basic Company Details"})

                else:
                    emptydata.append({"id": userval,
                                      "user_type":regobj[0].get('user_type'),
                                      "registration_status": "Self Registration",
                                      })

            return Response({'status': 200, 'message':'ok','data':emptydata,'usertype':regobj[0].get('user_type')}, status=200)

        else:
            print("buyer")
            if len(regobj) > 0:
                userval = regobj[0].get('id')
                basicobj = BasicCompanyDetails.objects.filter(updated_by=userval).values()
                if basicobj:
                    if basicobj:
                        industry_info = IndustrialInfo.objects.filter(updated_by=userval).values()
                        if industry_info:
                            legalobj = LegalDocuments.objects.filter(updated_by=userval).values()
                            if legalobj:
                                emptydata.append({"id": userval,
                                                      "user_type": regobj[0].get('user_type'),
                                                      'company_code': basicobj[0].get('company_code'),
                                                      "registration_status": "Legal Documents"})

                            else:
                                emptydata.append({"id": userval,
                                                  "user_type": regobj[0].get('user_type'),
                                                  'company_code': basicobj[0].get('company_code'),
                                                  "registration_status": "Seller Info"})
                        else:
                            emptydata.append({"id": userval,
                                              "user_type": regobj[0].get('user_type'),
                                              'company_code': basicobj[0].get('company_code'),
                                              "registration_status": "Basic Company Details"})
                    else:
                        emptydata.append({"id": userval,
                                          "user_type": regobj[0].get('user_type'),
                                          "registration_status": "Self Registration",
                                          })





            return Response({'status': 200, 'message': 'ok', 'data': emptydata, 'usertype': regobj[0].get('user_type')},
                            status=200)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['post'])
# @permission_classes([AllowAny])
def employee_registration_list_by_user_id(request):
    data=request.data
    emptydata=[]
    try:
        regobj=SelfRegistration.objects.filter(username=data['email_id']).values()
        if len(regobj)>0:
            userval=regobj[0].get('id')
            print(userval)
            basicobj = Employee_CompanyDetails.objects.filter(emp_updated_by_id=userval).values()
            if basicobj:
                industry_info = Employee_IndustryInfo.objects.filter(emp_updated_by_id=userval).values()
                if industry_info:
                    emptydata.append({"id": userval,
                                      "user_type": regobj[0].get('user_type'),
                                      "emp_company_code": basicobj[0].get('emp_company_code'),
                                      "registration_status": "Industry Info Details"})

                else:
                    emptydata.append({"id":userval,
                                      "user_type": regobj[0].get('user_type'),
                                      "emp_company_code": basicobj[0].get('emp_company_code'),
                                      "registration_status": "Basic Info Details"})

            else:
                emptydata.append({"id": userval,
                                  "user_type":regobj[0].get('user_type'),
                                  "registration_status": "Self Registration",
                                  })
            return Response({'status': 200, 'message':'Employee Company Details','data':emptydata}, status=200)
        else:
            return Response({'status': 204, 'message': 'No data with this id'}, status=204)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)



@api_view(['put'])
def changeempinddetails(request):
    try:
        data=request.data
        userid=data['emp_updated_by']
        empobj=Employee_IndustryInfo.objects.get(emp_updated_by=userid)
        if empobj:
            empobj.emp_nature_of_business=data['emp_nature_of_business']
            empobj.emp_supply_capabilites=data['emp_supply_capabilites']
            empobj.emp_industry_to_serve=data['emp_industry_to_serve']
            empobj.emp_updated_by=SelfRegistration.objects.get(id=userid)
            empobj.save()
        return Response({'status': 200, 'message': 'ok'}, status=200)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['put'])
def changecompprofile(request):
    try:
        data=request.data
        dept=data['dept']
        desig=data['desig']
        gstno=data['gstno']
        cname=data['cname']
        ctype=data['ctype']
        cyear=data['cyear']
        mloc=data['mloc']
        industryscale=data['iscale']
        currency=data['currency']
        userid=data['userid']

        regobj=SelfRegistration.objects.get(id=userid)
        if regobj:
            regobj.department=dept
            regobj.designation=desig
            regobj.save()
            empobj=Employee_CompanyDetails.objects.get(emp_updated_by=userid)
            empobj.emp_company_name=cname
            empobj.emp_tax_id_or_vat=gstno
            empobj.emp_company_established=cyear
            empobj.emp_industrial_scale=industryscale
            empobj.emp_market_location=mloc
            empobj.emp_company_type=ctype
            empobj.emp_currency=currency
            empobj.emp_updated_by=SelfRegistration.objects.get(id=userid)
            empobj.save()

        return Response({'status': 200, 'message': 'ok'}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
def buyer_login(request):
    data=request.data
    emailid=data['emailid']
    password=data['password']
    try:
        regobj=SelfRegistration.objects.get(username=emailid)
        if regobj:
            if check_password(password,regobj.password) and regobj.username==emailid:
                return Response({'status':200,'message':'Buyer Login Success'},status=200)
            else:
                return Response({'status': 424, 'message': 'Password entered is not correct,Please Check Once'},
                                status=424)
    except ObjectDoesNotExist as e:
        return Response({'status': 404, 'error': "Email not exist"}, status=404)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def employeelogin(request):
    try:
        data=request.data
        email=data['email']
        Regobj=SelfRegistration.objects.filter(username=email).values()
        print(Regobj)
        if Regobj:
            empcompobj=Employee_CompanyDetails.objects.filter(emp_updated_by=Regobj[0].get('id')).values()
            if empcompobj:
                print(empcompobj)
                industryobj=Employee_IndustryInfo.objects.filter(emp_updated_by=Regobj[0].get('id')).values()
                if industryobj:
                    return Response({'status': 200, 'Regstatus': 'industryinfo','userid':Regobj[0].get('id'),'companycode':empcompobj[0].get('emp_company_code')}, status=200)
                else:
                    return Response({'status': 200, 'Registatus': 'Companyinfo','userid':Regobj[0].get('id'),'companycode':empcompobj[0].get('emp_company_code')}, status=200)

            else:
                return Response({'status': 200, 'Registatus': 'self Registration','userid':Regobj[0].get('id'),'companycode':'NA'}, status=200)

        else:
            return Response({'status': 200, 'Registatus': 'not exist'}, status=200)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

