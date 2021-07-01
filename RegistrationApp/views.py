from __future__ import print_function
import time
import urllib

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
import itertools
import json
import math
import random




from django.contrib.auth.hashers import make_password, check_password
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError
import requests
# from mailchimp3 import MailChimp
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
    ShippingAddress_Others, EmployeeRegistration, Employee_CompanyDetails, Employee_IndustryInfo
from .serializers import SelfRegistrationSerializer, SelfRegistrationSerializerSample, BasicCompanyDetailsSerializers, \
    BillingAddressSerializer, ShippingAddressSerializer, IndustrialInfoSerializer, IndustrialHierarchySerializer, \
    BankDetailsSerializer, LegalDocumentsSerializers, BasicCompanyDetailsOthersSerializers, \
    EmployeeRegistrationSerializer, Employee_CompanyDetailsSerializers, Employee_IndustryInfoSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status

# from mailchimp_marketing import Client
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
# from Vendorsinprojectversion2.settings import (MAILCHIMP_API_KEY,MAILCHIMP_DATA_CENTER,MAILCHIMP_EMAIL_LIST_ID)

class SelfRegisterView(viewsets.ModelViewSet):
    # Register user information
    queryset = SelfRegistration.objects.all()
    serializer_class = SelfRegistrationSerializer
    permission_classes = (AllowAny,)

class SelfRegistrationSampleView(viewsets.ModelViewSet):
    # registration user information sample view
    queryset= SelfRegistration_Sample.objects.all()
    serializer_class = SelfRegistrationSerializerSample
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        # Hash password but passwords are not required
        if ('password' in self.request.data):
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()

class LegalDocumentsView(viewsets.ModelViewSet):
    # legal document view
    permission_classes = (AllowAny,)
    queryset = LegalDocuments.objects.all()
    serializer_class = LegalDocumentsSerializers
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        legalobj = LegalDocuments.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if not legalobj:
            raise ValidationError({'message': 'Legal Documentss details not exist', 'status': 204})
        return legalobj


class Logout(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['post'])
@permission_classes((AllowAny,))
def phone_verification_otp(request):
    # phone number verification by OTP
    data = request.data
    digits = "0123456789"
    phone_number = data['phone_number']
    phone_number_otp= "+91"+str(phone_number)
    print(type(phone_number_otp))
    try:
        user = SelfRegistration.objects.get(phone_number=phone_number)
        if user:
            pass
            OTP = ""
            for i in range(6):
                OTP += digits[math.floor(random.random() * 10)]
            print(OTP)
            user.phone_otp = OTP
            user.save()
            mjtoken = 'a68496eb4e6d4286887b3196db434fc0'
            print(mjtoken)
            headers = {
                'Authorization': f"Bearer {mjtoken}",
                'Content-Type': 'application/json',
            }
            data = '{ "From": "VendorsIn", "To": "'+phone_number_otp+'", "Text": "Your OTP for Registration to Vendorsin portal is '+OTP+" Please donot share your OTP to anyone"'" }'
            # data = '{ "Text": "Have a nice SMS flight with Mailjet !", "To":'++919482212344", "From": "VendorsIn" }'
            response = requests.post('https://api.mailjet.com/v4/sms-send', headers=headers, data=data)
            print(response)
        return Response({'status': 200, 'message': 'OTP successfully sent to phone'}, status=200)
    except ObjectDoesNotExist as e:
        return Response({'status': 404, 'error': "phone number not exist"}, status=404)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['post'])
@permission_classes((AllowAny,))
def email_verification_otp(request):
    # email id verification by otp sending to mail
    data = request.data
    email = data['email']
    digits = '0123456789'
    OTP = ""
    try:
        user = SelfRegistration.objects.get(username=email)
        print(user)
        if user:
            for i in range(6):
                OTP += digits[math.floor(random.random() * 10)]
            mailchimp = MailchimpTransactional.Client('14kMF-44pCPZu8XbNkAzFA')
            message = {
                "from_email": "admin@vendorsin.com",
                "subject": "Mail Verification OTP",
                "text":"You mail verificaton OTP is"+" "+OTP+" "+"Please Don't Share Your OTP \n Thank You",
                "to": [
                    {
                        "email": user.username,
                        "type": "to"
                    }
                ]
            }
            response = mailchimp.messages.send({"message": message})
            print(response)
            return Response({'status': 200, 'message': 'Email sent successfully'}, status=200)
        else:
            return Response({'status': 202, 'message': 'Not present'}, status=202)
    except ObjectDoesNotExist as e:
        return Response({'status': 404, 'error': "Email not exist"}, status=404)
    except ApiClientError as error:
        return Response({'status': 500, 'error': error}, status=500)


@api_view(['post'])
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def get_userid_by_token(request):
    # get user_id by passing token
    data = request.data
    try:
        auth_token_userid=Token.objects.filter(key=data['token']).values('user_id')
        return Response({'status': 202,'data':auth_token_userid}, status=202)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
@permission_classes((AllowAny,))
def email_verification_otp_to_change_email(request):
    # email verification to change mail
    data = request.data
    email = data['email']
    digits = '0123456789'
    OTP = ""
    try:
        user = SelfRegistration.objects.get(username=email)
        print(user)
        if user:
            for i in range(6):
                OTP += digits[math.floor(random.random() * 10)]
            mailchimp = MailchimpTransactional.Client('14kMF-44pCPZu8XbNkAzFA')
            message = {
                "from_email": "admin@vendorsin.com",
                "subject": "Mail Verification OTP",
                "to": [
                    {
                        "email": user.username,
                        "type": "to"
                    }
                ]
            }
            response = mailchimp.messages.send({"message": message})
            print(response)
            return Response({'status': 200, 'message': 'Email sent successfully'}, status=200)
        else:
            return Response({'status': 202, 'message': 'Not present'}, status=202)
    except ObjectDoesNotExist as e:
        return Response({'status': 404, 'error': "Email not exist"}, status=404)
    except ApiClientError as error:
        return Response({'status': 500, 'error': error}, status=500)

@api_view(['post'])
@permission_classes((AllowAny,))
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
@permission_classes((AllowAny,))
def phone_otp_verfication_to_change_phonenumber(request):
    # otp verification to change phone number
    data = request.data
    digits = "0123456789"
    phonenumber = data['phonenumber']
    phone_number_otp = "+91" + str(phonenumber)
    try:
        pass
        # OTP = ""
        # for i in range(6):
        #     OTP += digits[math.floor(random.random() * 10)]
        #     print(OTP)
        #
        # mjtoken = 'a68496eb4e6d4286887b3196db434fc0'
        # print(mjtoken)
        # headers = {'Authorization': f"Bearer {mjtoken}",'Content-Type': 'application/json',}
        # data = '{ "From": "VendorsIn", "To": "' + phone_number_otp + '", "Text": "Your OTP for phone number verification to change phone number ' + OTP + " Please donot share your OTP to anyone"'" }'
        # response = requests.post('https://api.mailjet.com/v4/sms-send', headers=headers, data=data)
        # print(response)
        return Response({'status': 200, 'message': 'OTP Sent Successfully'}, status=200)
    except ObjectDoesNotExist as e:
        return Response({'status': 404, 'error': "phone number not exist"}, status=404)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
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
@permission_classes((AllowAny,))
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
@permission_classes((AllowAny,))
def change_password_with_email(request):
    # change password by using email_id
    data = request.data
    password=data['password']
    try:
        user = SelfRegistration.objects.get(username=data['email'])
        if user:
            if check_password(password,user.password):
                return Response({'status': 202, 'message': 'Password already present'}, status=202)
            else:
                user.set_password(password)
                user.save()
                return Response({'status': 200, 'message': 'Password changed successfully'}, status=200)
        else:
            return Response({'status': 424, 'message': "Email not exist"}, status=424)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['post'])
@permission_classes((AllowAny,))
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
@permission_classes((AllowAny,))
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
@permission_classes((AllowAny,))
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

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        basicobj = BasicCompanyDetails.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if not basicobj:
            raise ValidationError({'message': 'Basic Details not exist','status':204})
        return basicobj


class BillingAddressView(viewsets.ModelViewSet):
    # billing address viewsets
    permission_classes = (AllowAny,)
    queryset = BillingAddress.objects.all()
    serializer_class = BillingAddressSerializer

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        basicobj = BillingAddress.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if not basicobj:
            raise ValidationError({'message': 'Billing Address not exist', 'status': 204})
        return basicobj



class ShippingAddressView(viewsets.ModelViewSet):
    # shipping address viewsets
    permission_classes = (AllowAny,)
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        basicobj = ShippingAddress.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if not basicobj:
            raise ValidationError({'message': 'Shipping Address not exist', 'status': 204})
        return basicobj


class IndustrialInfoView(viewsets.ModelViewSet):
    # industrail info viewsets
    permission_classes = (AllowAny,)
    queryset =IndustrialInfo.objects.all()
    serializer_class=IndustrialInfoSerializer

    def get_queryset(self):
        # it determines the list of objects that you want to display by passing userid(updated_by)
        industryinfoobj = IndustrialInfo.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if not industryinfoobj:
            raise ValidationError({'message': 'Industry info details not exist','status':204})
        return industryinfoobj


class IndustrialHierarchyView(viewsets.ModelViewSet):
    # industrial hierarchy viewsets
    permission_classes = (AllowAny,)
    queryset =IndustrialHierarchy.objects.all()
    serializer_class=IndustrialHierarchySerializer

    def get_queryset(self):
        # it determines the list of objects that you want to display by passing userid(updated_by)
        industryhierarchyobj = IndustrialHierarchy.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if not industryhierarchyobj:
            raise ValidationError({'message': 'Industry hierarchy  details not exist','status':204})
        return industryhierarchyobj

class BankDetailsView(viewsets.ModelViewSet):
    # bank details viewsets
    permission_classes = (AllowAny,)
    queryset =BankDetails.objects.all()
    serializer_class=BankDetailsSerializer

    def get_queryset(self):
        # it determines the list of objects that you want to display by passing userid(updated_by)
        bankobj = BankDetails.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if not bankobj:
            raise ValidationError({'message': 'Bank Details not exist','status':204})
        return bankobj

@api_view(['post'])
@permission_classes((AllowAny,))
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
    permission_classes = (AllowAny,)
    queryset = BasicCompanyDetails_Others.objects.all()
    serializer_class = BasicCompanyDetailsOthersSerializers

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        basicobj = BasicCompanyDetails_Others.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if not basicobj:
            raise ValidationError({'message': 'Basic Details not exist','status':204})
        return basicobj

@api_view(['post'])
@permission_classes((AllowAny,))
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


class EmployeeRegistrationView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = EmployeeRegistration.objects.all()
    serializer_class = EmployeeRegistrationSerializer

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


class Employee_CompanyDetailsView(viewsets.ModelViewSet):
    # employee company info viewset
    permission_classes = (AllowAny,)
    queryset = Employee_CompanyDetails.objects.all()
    serializer_class = Employee_CompanyDetailsSerializers

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        employeeobj = Employee_CompanyDetails.objects.filter(emp_updated_by=self.request.GET.get('emp_updated_by')).order_by('emp_company_id')
        if not employeeobj:
            raise ValidationError({'message': 'Employee Basic Details not exist','status':204})
        return employeeobj

class EmployeeIndustrialInfoView(viewsets.ModelViewSet):
    # industrail info viewsets
    permission_classes = (AllowAny,)
    queryset =Employee_IndustryInfo.objects.all()
    serializer_class=Employee_IndustryInfoSerializer

    def get_queryset(self):
        # it determines the list of objects that you want to display by passing userid(updated_by)
        employee_industry = Employee_IndustryInfo.objects.filter(emp_updated_by=self.request.GET.get('emp_updated_by')).order_by('id')
        if not employee_industry:
            raise ValidationError({'message': ' Employee Industry info details not exist','status':204})
        return employee_industry

#
# @api_view(['get'])
# @permission_classes([AllowAny])
# def registration_list(request):
#     emptydata=list()
#     try:
#         regobj=SelfRegistration.objects.filter().values()
#         for i in range(0,len(regobj)):
#             val=regobj[i].get('id')
#             basicobj=BasicCompanyDetails.objects.filter(updated_by=val).values()
#             # basics = BasicCompanyDetails.objects.get(updated_by=val)
#             industry_info = IndustrialInfo.objects.filter(updated_by=val).values()
#             industry_hierarchy = IndustrialHierarchy.objects.filter(updated_by=val).values()
#             bankdetails = BankDetails.objects.filter(updated_by=val).values()
#             legalobj = LegalDocuments.objects.filter(updated_by=val).values()
#             emptydata.append({
#                 "username": regobj[i].get('contact_person'),
#                 "user_type": regobj[i].get('user_type'),
#                 "email": regobj[i].get('username'),
#                 "phone_number": regobj[i].get('phone_number'),
#                 "nature_of_business": regobj[i].get('nature_of_business'),
#                 "business_type": regobj[i].get('business_to_serve'),
#                 # "register_status": "Company Details",
#             })
#
#             if basicobj:
#                 if industry_info:
#                     if industry_hierarchy:
#                         if bankdetails:
#                             if legalobj:
#                                     return Response({'status': 200, 'mesage': 'upto legal obj', 'data': emptydata}, status=200)
#                             else:
#                                 return Response({'status': 200, 'mesage': 'upto bank', 'data': emptydata},
#                                                 status=200)
#                         else:
#                             return Response({'status': 200, 'mesage': 'upto industry hierarchy', 'data': emptydata}, status=200)
#                     else:
#                         return Response({'status': 200, 'mesage': 'upto industry info', 'data': emptydata},
#                                         status=200)
#                 else:
#                     return Response({'status': 200, 'mesage': 'upto basic info', 'data': emptydata}, status=200)
#             else:
#                 return Response({'status': 200, 'mesage': 'not present'}, status=200)
#
#
#
#
#
#
#
#         return Response({'status':200,'mesage':'ok','data':emptydata},status=200)
#
#     except Exception as e:
#         return Response({'status':500,'error':str(e)},status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
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
                message = OTP + 'Is The OTP To Verify Your Mobile Number On VENDORSIN COMMERCE Self Registration Portal. Do Not Share It With Anyone .'
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
                                                                                                                                         '", "name":"Harish" } ], "subject":"OTP Confirmation", "templateId":1 ,"params":{"OTP":' + OTP + '}''}'

                # data = '{ "sender":{ "name":"VENDORSIN COMMERCE PVT LTD", "email":"admin@vendorsin.com" },"subject":"This is my default subject line","templateId":96,"to":[ { "email":"harishshetty7459@gmail.com", "name":"harish" } ]'

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
                message = OTP + 'Is The OTP To Verify Your Mobile Number On VENDORSIN COMMERCE Self Registration Portal. Do Not Share It With Anyone .'
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
@permission_classes((AllowAny,))
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
                                                                                                                                 '", "name":"Harish" } ], "subject":"OTP Confirmation", "templateId":1 ,"params":{"OTP":' + OTP + '}''}'

        # data = '{ "sender":{ "name":"VENDORSIN COMMERCE PVT LTD", "email":"admin@vendorsin.com" },"subject":"This is my default subject line","templateId":96,"to":[ { "email":"harishshetty7459@gmail.com", "name":"harish" } ]'

            response = requests.post('https://api.sendinblue.com/v3/smtp/email', headers=headers, data=data)
            print("----")
            print(response)
            print("----")

        return Response({'status': 200, 'message': 'ok','data':OTP}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes((AllowAny,))
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
            message = OTP + 'Is The OTP To Verify Your Mobile Number On VENDORSIN COMMERCE Self Registration Portal. Do Not Share It With Anyone .'
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
@permission_classes((AllowAny,))
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
@permission_classes((AllowAny,))
def checkemailotp(request):
    data = request.data
    userid = data['userid']
    try:
        user = SelfRegistration.objects.get(id=userid)
        if user:
            if user.email_otp == data['email_otp']:
                return Response({'status': 200, 'message': "Both OTP Matching"}, status=200)
            else:
                return Response({'status': 202, 'message': "OTP Not Matching"}, status=202)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def checkphoneotp(request):
    data=request.data
    userid=data['userid']
    try:
        user = SelfRegistration.objects.get(id=userid)
        if user:
            if user.phone_otp==data['phone_otp']:

                return Response({'status': 200, 'message': "Both OTP Matching"}, status=200)
            else:
                return Response({'status': 202, 'message': "OTP Not Matching"}, status=202)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
@permission_classes((AllowAny,))
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
@permission_classes((AllowAny,))
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
                                                                                                                                         '", "name":"Harish" } ], "subject":"OTP Confirmation", "templateId":1 ,"params":{"OTP":' + OTP + '}''}'

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
@permission_classes((AllowAny,))
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
                message = OTP + 'Is The OTP To Verify Your Mobile Number On VENDORSIN COMMERCE Self Registration Portal. Do Not Share It With Anyone .'
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
@permission_classes((AllowAny,))
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
@permission_classes((AllowAny,))
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
@permission_classes((AllowAny,))
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




@api_view(['post'])
@permission_classes((AllowAny,))
def employee_login(request):
    data = request.data
    password = data['password']
    email_id = data['email_id']
    try:
        employeeobj = EmployeeRegistration.objects.get(email_id=email_id)
        if employeeobj:
            if check_password(password, employeeobj.password) and employeeobj.email_id == email_id:
                return Response({'status': 200, 'message': 'Employee Logged in successfully'}, status=200)
            else:
                return Response({'status': 424, 'message': 'Password entered is not correct,Please Check Once'},
                            status=424)

    except ObjectDoesNotExist as e:
        return Response({'status': 404, 'error': "Email not exist"}, status=404)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)







