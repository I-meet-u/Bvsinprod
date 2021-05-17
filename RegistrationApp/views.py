import math
import random

from django.contrib.auth.hashers import make_password, check_password
from mailjet_rest import Client

import requests
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SelfRegistration, SelfRegistration_Sample, BasicCompanyDetails, BillingAddress, ShippingAddress, \
    IndustrialInfo, IndustrialHierarchy, BankDetails
from .serializers import SelfRegistrationSerializer, SelfRegistrationSerializerSample, BasicCompanyDetailsSerializers, \
    BillingAddressSerializer, ShippingAddressSeializer, IndustrialInfoSerializer, IndustrialHierarchySerializer, \
    BankDetailsSerializer
from rest_framework.permissions import AllowAny


class SelfRegisterView(viewsets.ModelViewSet):
    # Register user information
    queryset = SelfRegistration.objects.all()
    serializer_class = SelfRegistrationSerializer
    permission_classes = (AllowAny,)


class SelfRegistrationSampleView(viewsets.ModelViewSet):
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


#
# @api_view(['post'])
# def deleteuser(request):
#     data=request.data
#     userid=data['userid']
#     try:
#         regs=Registration.objects.get(id=userid)
#         print(regs.id)
#         regobj=Registration_sample.objects.get(id=regs.id)
#         print(regobj.id)
#         basicobj=BasiCompanyInfo.objects.filter(user_id_id=regobj.id).values()
#         if basicobj:
#             return Response({'status':200,'message':'Valid user'},status=200)
#         else:
#             reg=Registration.objects.get(id=userid)
#             reg.delete()
#             return Response({'status':204,'error':'deleted'},status=204)
#     except Exception as e:
#         return Response({'status': 500, 'error': str(e)}, status=500)


class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['post'])
def phone_verification_otp(request):
    data = request.data
    digits = "0123456789"
    phone_number = data['phone_number']
    phone_number_otp= "+91"+str(phone_number)
    print(type(phone_number_otp))
    try:
        user = SelfRegistration.objects.get(phone_number=phone_number)
        if user:
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
def email_verification_otp(request):
    data = request.data
    digits = '0123456789'
    email = data['email']
    try:
        user = SelfRegistration.objects.get(username=email)
        if user:
            api_key = '15dd5580cada57242e99c2ebc87dfd96'
            api_secret = '352ffb29187a798012b1cfdc7eb9f62f'
            OTP = ""
            for i in range(6):
                OTP += digits[math.floor(random.random() * 10)]
            mailjet = Client(auth=(api_key, api_secret), version='v3.1')
            data1 = {'Messages': [
                {"From": {"Email": "admin@vendorson.com", "Name": "Vendors In"}, "To": [{"Email": email}],
                 "Subject": "OTP Confirmation",
                 "TextPart": "Dear Sir|Madam" + "\n\n This is the OTP for email verification" +" "+OTP+ "\n\nThis is System Generated Email Please Don't Reply For This Mail" + "\n\n Thank You"}]}

            result = mailjet.send.create(data=data1)
            print(result)
            if result.status_code == 200:
                user.email_otp = OTP
                user.save()
            return Response({'status': 200, 'message':'OTP successfully sent to mail'}, status=200)
    except ObjectDoesNotExist as e:
        return Response({'status': 404, 'error': "Email not exist"}, status=404)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes([AllowAny])
def get_token_key_by_userid(request):
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
    data = request.data
    try:
        auth_token_userid=Token.objects.filter(key=data['token']).values('user_id')
        return Response({'status': 202,'data':auth_token_userid}, status=202)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
def email_verification_otp_to_change_email(request):
    data = request.data
    digits = '0123456789'
    mail = data['mail']
    try:

        api_key = '15dd5580cada57242e99c2ebc87dfd96'
        api_secret = '352ffb29187a798012b1cfdc7eb9f62f'
        OTP = ""
        for i in range(6):
            OTP += digits[math.floor(random.random() * 10)]
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data1 = {'Messages': [
                {"From": {"Email": "admin@vendorson.com", "Name": "Vendors In"}, "To": [{"Email": mail}],
                 "Subject": "OTP Confirmation",
                 "TextPart": "Dear Sir|Madam" + "\n\n This is the OTP for email verification to change your email" + " "+ OTP + "\n\nThis is System Generated Email Please Don't Reply For This Mail" + "\n\n Thank You"
                 }]}
        result = mailjet.send.create(data=data1)
        if result.status_code == 200:
            return Response({'status': 200, 'message':'OTP successfully sent to your mail','OTP':OTP}, status=200)
        else:
            return Response({'status': 202, 'message': 'OTP not sent to your email'}, status=202)
    except ObjectDoesNotExist as e:
        return Response({'status': 404, 'error': "Email not exist"}, status=404)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def change_email(request):
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
    data = request.data
    digits = "0123456789"
    phonenumber = data['phonenumber']
    phone_number_otp = "+91" + str(phonenumber)
    try:
        OTP = ""
        for i in range(6):
            OTP += digits[math.floor(random.random() * 10)]
            print(OTP)

        mjtoken = 'a68496eb4e6d4286887b3196db434fc0'
        print(mjtoken)
        headers = {'Authorization': f"Bearer {mjtoken}",'Content-Type': 'application/json',}
        data = '{ "From": "VendorsIn", "To": "' + phone_number_otp + '", "Text": "Your OTP for phone number verification to change phone number ' + OTP + " Please donot share your OTP to anyone"'" }'
        response = requests.post('https://api.mailjet.com/v4/sms-send', headers=headers, data=data)
        print(response)
        return Response({'status': 200, 'message': 'OTP Sent Successfully','OTP':OTP}, status=200)
    except ObjectDoesNotExist as e:
        return Response({'status': 404, 'error': "phone number not exist"}, status=404)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def change_phonenumber(request):
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



# @api_view(['post'])
# def waiting_mail_for_admin_approval(request):
#     data = request.data
#     digits = '0123456789'
#     userid = data['company_user_id']
#
#     try:
#         userdeatils = SelfRegistration.objects.filter(id=userid).values()
#         print(userdeatils)
#         recemail = userdeatils[0].get('username')
#         print(recemail)
#         username = userdeatils[0].get('full_name')
#         print(username)
#         api_key = '15dd5580cada57242e99c2ebc87dfd96'
#         api_secret = '352ffb29187a798012b1cfdc7eb9f62f'
#         OTP = ""
#         for i in range(6):
#             OTP += digits[math.floor(random.random() * 10)]
#         mailjet = Client(auth=(api_key, api_secret), version='v3.1')
#         data1 = {'Messages': [
#             {"From": {"Email": "admin@vendorson.com", "Name": "Vendors In"}, "To": [{"Email": recemail}],
#              "Subject": "Wait For admin Approval",
#              "TextPart": "Dear Sir|Madam" + "\n\n Waiting for admin approval mail" + "\n\nThis is System Generated Email Please Don't Reply For This Mail" + "\n\n Thank You"
#
#              }]}
#         result = mailjet.send.create(data=data1)
#         print(result)
#         return Response({'status': 200, 'message': 'Waiting for admin approval for mail sent successfully'}, status=200)
#
#     except ObjectDoesNotExist as e:
#         return Response({'status': 424, 'error': "Email not exist"}, status=404)
#
#     except Exception as e:
#         return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def otp_session_time_out_of_phone_and_email(request):
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
    queryset = BasicCompanyDetails.objects.all()
    serializer_class = BasicCompanyDetailsSerializers

    def get_queryset(self):
        basicobj = BasicCompanyDetails.objects.filter(user_id=self.request.GET.get('user_id'))
        if not basicobj:
            raise ValidationError({'message': 'Related Documents are not present for this user'})
        return basicobj


class BillingAddressView(viewsets.ModelViewSet):
    queryset = BillingAddress.objects.all()
    serializer_class = BillingAddressSerializer

class ShippingAddressView(viewsets.ModelViewSet):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSeializer


class IndustrialInfoView(viewsets.ModelViewSet):
    queryset =IndustrialInfo.objects.all()
    serializer_class=IndustrialInfoSerializer

class IndustrialHierarchyView(viewsets.ModelViewSet):
    queryset =IndustrialHierarchy.objects.all()
    serializer_class=IndustrialHierarchySerializer

class BankDetailsView(viewsets.ModelViewSet):
    queryset =BankDetails.objects.all()
    serializer_class=BankDetailsSerializer

# @api_view(['put'])
# def update_basic_company_info1(request):
#     data=request.data
#     try:
#         basic_compinfo_obj = BasiCompanyInfo.objects.filter(company_code=data['company_code']).values()
#         basic_compinfo_user = BasiCompanyInfo.objects.get(user_id=data['user_id'])
#         marketloc=data['marketloc']
#         msmereg=data['msmereg']
#         indusscale=data['indusscale']
#         website=data['website']
#         natureofbuz=data['natureofbuz']
#         servicearealocal=data['servicearealocal']
#         serservicearearegional=data['serservicearearegional']
#         servicearenational=data['servicearenational']
#         serviceareainternational=data['serviceareainternational']
#         serviceareaworld=data['serviceareaworld']
#         created_by_id = data['created_by_id']
#         updated_by_id = data['updated_by_id']
#         bill_address=data['bill_address']
#         bill_city=data['bill_city']
#         bill_state=data['bill_state']
#         bill_country = data['bill_country']
#         bill_pincode = data['bill_pincode']
#         bill_landmark = data['bill_landmark']
#         bill_location = data['bill_location']
#
#         ship_address=data['ship_address']
#         ship_city = data['ship_city']
#         ship_state = data['ship_state']
#         ship_country = data['ship_country']
#         ship_pincode = data['ship_pincode']
#         ship_landmark = data['ship_landmark']
#         ship_location = data['ship_location']
#         if basic_compinfo_obj and updated_by_id !="":
#             if basic_compinfo_user.business_type!=marketloc:
#                 basic_compinfo_user.business_type=marketloc
#                 basic_compinfo_user.save()
#             if basic_compinfo_user.msme_registered!=msmereg:
#                 basic_compinfo_user.msme_registered=msmereg
#                 basic_compinfo_user.save()
#             if  basic_compinfo_user.industrial_scale!=indusscale:
#                 basic_compinfo_user.industrial_scale = indusscale
#                 basic_compinfo_user.save()
#             if basic_compinfo_user.website!=website:
#                 basic_compinfo_user.website = website
#                 basic_compinfo_user.save()
#             if basic_compinfo_user.natureofbuz != natureofbuz:
#                 basic_compinfo_user.natureofbuz = natureofbuz
#                 basic_compinfo_user.save()
#             if basic_compinfo_user.service_area_local!=servicearealocal:
#                 basic_compinfo_user.service_area_local=servicearealocal
#                 basic_compinfo_user.save()
#             if basic_compinfo_user.service_area_regional!=serservicearearegional:
#                 basic_compinfo_user.service_area_regional = serservicearearegional
#                 basic_compinfo_user.save()
#             if basic_compinfo_user.service_area_national!=servicearenational:
#                 basic_compinfo_user.service_area_national = servicearenational
#                 basic_compinfo_user.save()
#             if basic_compinfo_user.service_area_international!=serviceareainternational:
#                 basic_compinfo_user.service_area_international = serviceareainternational
#                 basic_compinfo_user.save()
#             if basic_compinfo_user.service_area_worldwide!=serviceareaworld:
#                 basic_compinfo_user.service_area_worldwide = serviceareaworld
#                 basic_compinfo_user.save()
#             if basic_compinfo_user.bill_address != bill_address:
#                 basic_compinfo_user.bill_address = bill_address
#                 basic_compinfo_user.save()
#             if basic_compinfo_user.bill_city != bill_city:
#                 basic_compinfo_user.bill_city = bill_city
#                 basic_compinfo_user.save()
#             if basic_compinfo_user.bill_state != bill_state:
#                 basic_compinfo_user.bill_state = bill_state
#                 basic_compinfo_user.save()
#             if basic_compinfo_user.bill_country != bill_country:
#                 basic_compinfo_user.bill_country = bill_country
#                 basic_compinfo_user.save()
#             if basic_compinfo_user.bill_pincode != bill_pincode:
#                 basic_compinfo_user.bill_pincode = bill_pincode
#                 basic_compinfo_user.save()
#             if basic_compinfo_user.bill_landmark != bill_landmark:
#                 basic_compinfo_user.bill_landmark = bill_landmark
#                 basic_compinfo_user.save()
#             if basic_compinfo_user.bill_location != bill_location:
#                 basic_compinfo_user.bill_location = bill_location
#                 basic_compinfo_user.save()
#             if basic_compinfo_user.ship_address != ship_address:
#                 basic_compinfo_user.ship_address = ship_address
#                 basic_compinfo_user.save()
#             if basic_compinfo_user.ship_city != ship_city:
#                 basic_compinfo_user.ship_city = ship_city
#                 basic_compinfo_user.save()
#             if basic_compinfo_user.ship_state != ship_state:
#                 basic_compinfo_user.ship_state = ship_state
#                 basic_compinfo_user.save()
#             if basic_compinfo_user.ship_country != ship_country:
#                 basic_compinfo_user.ship_country = ship_country
#                 basic_compinfo_user.save()
#             if basic_compinfo_user.ship_pincode != ship_pincode:
#                 basic_compinfo_user.ship_pincode = ship_pincode
#                 basic_compinfo_user.save()
#             if basic_compinfo_user.ship_landmark != ship_landmark:
#                 basic_compinfo_user.ship_landmark = ship_landmark
#                 basic_compinfo_user.save()
#             if basic_compinfo_user.ship_location != ship_location:
#                 basic_compinfo_user.ship_location = ship_location
#                 basic_compinfo_user.save()
#             return Response({'status': 200, 'message': 'details updated',"data":basic_compinfo_obj}, status=200)
#     except Exception as e:
#         return Response({'status': 500, 'message': str(e)}, status=500)
#--------------------------------------venndor-info-get---------------------------