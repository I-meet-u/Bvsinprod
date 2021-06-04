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
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import SelfRegistration, SelfRegistration_Sample, BasicCompanyDetails, BillingAddress, ShippingAddress, \
    IndustrialInfo, IndustrialHierarchy, BankDetails, LegalDocuments, BasicCompanyDetails_Others
from .serializers import SelfRegistrationSerializer, SelfRegistrationSerializerSample, BasicCompanyDetailsSerializers, \
    BillingAddressSerializer, ShippingAddressSerializer, IndustrialInfoSerializer, IndustrialHierarchySerializer, \
    BankDetailsSerializer, LegalDocumentsSerializers, BasicCompanyDetailsOthersSerializers
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
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['post'])
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
            # for i in range(6):
            #     OTP += digits[math.floor(random.random() * 10)]
            # print(OTP)
            # user.phone_otp = OTP
            # user.save()
            # mjtoken = 'a68496eb4e6d4286887b3196db434fc0'
            # print(mjtoken)
            # headers = {
            #     'Authorization': f"Bearer {mjtoken}",
            #     'Content-Type': 'application/json',
            # }
            # data = '{ "From": "VendorsIn", "To": "'+phone_number_otp+'", "Text": "Your OTP for Registration to Vendorsin portal is '+OTP+" Please donot share your OTP to anyone"'" }'
            # # data = '{ "Text": "Have a nice SMS flight with Mailjet !", "To":'++919482212344", "From": "VendorsIn" }'
            # response = requests.post('https://api.mailjet.com/v4/sms-send', headers=headers, data=data)
            # print(response)
        return Response({'status': 200, 'message': 'OTP successfully sent to phone'}, status=200)
    except ObjectDoesNotExist as e:
        return Response({'status': 404, 'error': "phone number not exist"}, status=404)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['post'])
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
    queryset =IndustrialHierarchy.objects.all()
    serializer_class=IndustrialHierarchySerializer

class BankDetailsView(viewsets.ModelViewSet):
    # bank details viewsets
    queryset =BankDetails.objects.all()
    serializer_class=BankDetailsSerializer

    def get_queryset(self):
        # it determines the list of objects that you want to display by passing userid(updated_by)
        bankobj = BankDetails.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if not bankobj:
            raise ValidationError({'message': 'Bank Details not exist','status':204})
        return bankobj

@api_view(['post'])
def get_basic_info_by_gst(request):
    # get basic_details by passing gst_number
    data=request.data
    gst_no=data['gst_no']
    basicdetailslist=[]
    try:
        basicobj=BasicCompanyDetails.objects.get(gst_number=gst_no)
        print(basicobj.company_code)
        if basicobj:
            billobj=BillingAddress.objects.get(company_code_id=basicobj.company_code)
            shipobj=ShippingAddress.objects.get(company_code_id=basicobj.company_code)
            basicdetailslist.append({
                'gst_number':basicobj.gst_number,
                'company_name':basicobj.company_name,
                'company_code':basicobj.company_code,
                'company_type':basicobj.company_type,
                'listing_date':basicobj.listing_date,
                'pan_number':basicobj.pan_number,
                'tax_payer_type':basicobj.tax_payer_type,
                'msme_registered':basicobj.msme_registered,
                'company_established':basicobj.company_established,
                'registered_iec':basicobj.registered_iec,
                'industrial_scale':basicobj.industrial_scale,
                'bill_address':billobj.bill_address,
                'bill_country':billobj.bill_country,
                'bill_city':billobj.bill_city,
                'bill_pincode':billobj.bill_pincode,
                'bill_landmark':billobj.bill_landmark,
                'bill_location':billobj.bill_location,
                'ship_address':shipobj.ship_address,
                'ship_country':shipobj.ship_country,
                'ship_city':shipobj.ship_city,
                'ship_pincode':shipobj.ship_pincode,
                'ship_landmark':shipobj.ship_landmark,
                'ship_location':shipobj.ship_location,
                'updated_by':basicobj.updated_by_id
            })
            return Response({'status': 200, 'message': 'Basic Details List','data':basicdetailslist}, status=200)
        else:
            return Response({'status':204,'message':'Not Present'},status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)



@api_view(['post'])
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
    queryset = BasicCompanyDetails_Others.objects.all()
    serializer_class = BasicCompanyDetailsOthersSerializers

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        basicobj = BasicCompanyDetails_Others.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if not basicobj:
            raise ValidationError({'message': 'Basic Details not exist','status':204})
        return basicobj
