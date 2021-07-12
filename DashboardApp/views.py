import math
import urllib
from itertools import chain

import requests
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from RegistrationApp.models import BasicCompanyDetails, IndustrialInfo, IndustrialHierarchy, BillingAddress
from .models import *
from .serializers import *


class InviteVendorView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = InviteVendor.objects.all()
    serializer_class = InviteVendorSerializer
    ordering_fields = ['invite_id']
    ordering = ['invite_id']

    def create(self, request, *args, **kwargs):
        company_name = request.data.get('company_name', None)
        contact_name = request.data.get('contact_name', None)
        email_id = request.data.get('email_id', None)
        phone_number = request.data.get('phone_number', None)
        user_id = request.data.get('user_id', None)
        type_user = request.data.get('type_user', None)
        regarray = []
        try:
            request.data['updated_by_invites'] = user_id
            request.data['created_by'] = user_id
            regobj = SelfRegistration.objects.filter().values('username')
            for i in range(0, len(regobj)):
                regarray.append(regobj[i].get('username'))
            if email_id in regarray:
                return Response({'status': 202, 'message': 'Email Id already present in Registration'}, status=202)
            return super().create(request, *args, **kwargs)
            #
            # headers = {
            #     'accept': 'application/json',
            #     'api-key': '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',
            #     'content-type': 'application/json',
            # }
            # data = '{ "sender":{ "name":"VENDORSIN COMMERCE PVT LTD", "email":"admin@vendorsin.com" }, "to":[ { "email":"' + email_id + '' \
            #                                                                                                                          '", "name":"Harish" } ], "subject":"You have been invited to Vendorsin Commerce as a Vendor,Please Dont Share this mail to anyone",''}'
            # print(data,'xcxc')
            # response = requests.post('https://api.sendinblue.com/v3/smtp/email', headers=headers, data=data)
            # print("----")
            # print(response)
            # print("----")


        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)

    def get_queryset(self):
        inviteobj = InviteVendor.objects.filter(updated_by_invites=self.request.GET.get('updated_by')).order_by(
            'invite_id')
        if inviteobj:
            return inviteobj
        raise ValidationError({'message': "Invited list by this user is not present", "status": 204})


class BusinessRequestView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = BusinessRequest.objects.all()
    serializer_class = BusinessRequestSerializer
    ordering_fields = ['id']
    ordering = ['id']


class InternalVendorView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = InternalVendor.objects.all()
    serializer_class = InternalVendorSerializer
    ordering_fields = ['internal_vendor_id']
    ordering = ['internal_vendor_id']

    def create(self, request, *args, **kwargs):
        ccode = request.data.get('ccode', None)
        try:
            hierarchyvalues = IndustrialHierarchy.objects.filter(company_code_id__in=ccode).values()
            if len(hierarchyvalues) > 0:
                basicobj = BasicCompanyDetails.objects.filter(company_code__in=ccode).values()
                for i in range(0, len(basicobj)):
                    basicdata = BasicCompanyDetails.objects.get(company_code=basicobj[i].get('company_code'))
                    regobj = SelfRegistration.objects.get(id=basicdata.updated_by_id)
                    hierarchyobj = IndustrialHierarchy.objects.get(company_code=basicdata.company_code)
                    industryinfoobj = IndustrialInfo.objects.get(company_code=basicdata.company_code)
                    address = BillingAddress.objects.filter(company_code=basicdata.company_code).values()
                    InternalVendor.objects.create(company_code=basicdata.company_code,
                                                  company_name=basicdata.company_name,
                                                  city=address[0].get('bill_city'),
                                                  state=address[0].get('bill_state'),
                                                  nature_of_business=industryinfoobj.nature_of_business,
                                                  email_id=regobj.username,
                                                  phone_number=regobj.phone_number,
                                                  maincore=hierarchyobj.maincore,
                                                  category=hierarchyobj.category,
                                                  sub_category=hierarchyobj.subcategory,
                                                  updated_by=SelfRegistration.objects.get(id=basicdata.updated_by_id),
                                                  created_by=basicdata.updated_by_id
                                                  )
                return Response({'status': 201, 'message': "Internal Vendor Created"}, status=201)
            else:
                return Response({'status': 204, 'message': "Company Code Not Present"}, status=204)

        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)


class InternalBuyerView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = InternalBuyer.objects.all()
    serializer_class = InternalBuyerSerializer
    ordering_fields = ['internal_buyer_id']
    ordering = ['internal_buyer_id']


@api_view(['post'])
@permission_classes((AllowAny,))
def get_all_details_for_business_request(request):
    data = request.data
    regid = []
    userid = data['userid']
    ccode = []
    business_request = []
    try:
        regobj = SelfRegistration.objects.filter().values()
        for i in range(0, len(regobj)):
            regid.append(regobj[i].get('id'))
        basicobj1 = BasicCompanyDetails.objects.filter(updated_by__in=regid).values()
        for i in range(0, len(basicobj1)):
            ccode.append(basicobj1[i].get('company_code'))
        industryhierarchy = IndustrialHierarchy.objects.filter(company_code__in=ccode).values()
        if len(industryhierarchy) > 0:
            for j in range(0, len(industryhierarchy)):
                x = industryhierarchy[j].get('company_code_id')
                print(x)
                inudstryobj = IndustrialInfo.objects.filter(company_code=x).values()
                basicobj = BasicCompanyDetails.objects.filter(company_code=x).values()
                bill_obj = BillingAddress.objects.filter(company_code=x).values()
                business_request.append({'maincore': industryhierarchy[j].get('maincore'),
                                         'category': industryhierarchy[j].get('category'),
                                         'subcategory': industryhierarchy[j].get('subcategory'),
                                         'bill_city': basicobj[0].get('bill_city'),
                                         'bill_state': bill_obj[0].get('bill_state'),
                                         'nature_of_business': inudstryobj[0].get('nature_of_business'),
                                         'industry_to_serve': inudstryobj[0].get('industry_to_serve'),
                                         'company_code': basicobj[0].get('company_code'),
                                         'company_name': basicobj[0].get('company_name')

                                         })
            return Response({'status': 200, 'message': 'Business Request List', 'data': business_request}, status=200)
        else:
            return Response({'status': 202, 'message': 'No data'}, status=202)



    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


#
# @api_view(['post'])
# @permission_classes((AllowAny,))
# def external_vendor(request):
#     data=request.data
#     regid=[]
#     userid=data['userid']
#     internalarray=[]
#     internalarray2=[]
#     try:
#         regobj1=SelfRegistration.objects.filter(id=userid).values()
#         regobj=SelfRegistration.objects.filter().values()
#         internalvendorobj = InternalVendor.objects.filter().values('company_code').order_by('internal_vendor_id')
#         for i in range(0, len(internalvendorobj)):
#             internalarray.append(internalvendorobj[i].get('company_code'))
#         if len(regobj)>0:
#             for i in range(0,len(regobj)):
#                 regid.append(regobj[i].get('id'))
#             basicdata=BasicCompanyDetails.objects.filter(updated_by__in=regid).values()
#             for i in range(0,len(basicdata)):
#                 if basicdata[i].get('company_code') not in internalarray:
#                     x=basicdata[i].get('company_code')
#                     internalarray2.append(x)
#             basicdataobj= BasicCompanyDetails.objects.filter(company_code__in=internalarray2).values('company_code','company_name').order_by('company_code')
#             industryhierarchy = IndustrialHierarchy.objects.filter(company_code__in=internalarray2).values('maincore','category','subcategory','updated_by','company_code').order_by('company_code')
#             industryobj = IndustrialInfo.objects.filter(company_code__in=internalarray2).values('nature_of_business','industry_to_serve','updated_by','company_code').order_by('company_code')
#             billingobj = BillingAddress.objects.filter(company_code__in=internalarray2).values('bill_city','bill_state','updated_by','company_code').order_by('company_code')
#             external_vendor_array=list(chain(basicdataobj,industryhierarchy,industryobj,billingobj))
#             return Response({'status': 200, 'message': 'External Vendor List','data':external_vendor_array}, status=200)
#         return Response({'status': 204, 'message': 'Not Present'}, status=204)
#
#
#     except Exception as e:
#         return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def external_vendor(request):
    data = request.data
    regid = []
    userid = data['userid']
    internalarray = []
    ccode = []
    externalarray = []

    try:
        regobj1 = SelfRegistration.objects.filter(id=userid).values()
        regobj = SelfRegistration.objects.filter().values()
        internalvendorobj = InternalVendor.objects.filter().values('company_code').order_by('internal_vendor_id')
        for i in range(0, len(internalvendorobj)):
            internalarray.append(internalvendorobj[i].get('company_code'))
        for i in range(0, len(regobj)):
            regid.append(regobj[i].get('id'))
        basicobj1 = BasicCompanyDetails.objects.filter(updated_by__in=regid).values()
        for i in range(0, len(basicobj1)):
            if basicobj1[i].get('company_code') not in internalarray:
                ccode.append(basicobj1[i].get('company_code'))
        industryhierarchy = IndustrialHierarchy.objects.filter(company_code__in=ccode).values()
        if len(industryhierarchy) > 0:
            for j in range(0, len(industryhierarchy)):
                x = industryhierarchy[j].get('company_code_id')
                print(x)
                inudstryobj = IndustrialInfo.objects.filter(company_code=x).values()
                basicobj = BasicCompanyDetails.objects.filter(company_code=x).values()
                bill_obj = BillingAddress.objects.filter(company_code=x).values()
                externalarray.append({'maincore': industryhierarchy[j].get('maincore'),
                                      'category': industryhierarchy[j].get('category'),
                                      'subcategory': industryhierarchy[j].get('subcategory'),
                                      'bill_city': basicobj[0].get('bill_city'),
                                      'bill_state': bill_obj[0].get('bill_state'),
                                      'nature_of_business': inudstryobj[0].get('nature_of_business'),
                                      'industry_to_serve': inudstryobj[0].get('industry_to_serve'),
                                      'company_code': basicobj[0].get('company_code'),
                                      'company_name': basicobj[0].get('company_name')

                                      })

            return Response({'status': 200, 'message': 'External Vendor List', 'data': externalarray}, status=200)
        else:
            return Response({'status': 202, 'message': 'Not Present'}, status=202)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def advance_search_business_request(request):
    # business request advance search
    data = request.data
    company_code = data['company_code']
    company_name = data['company_name']
    city = data['city']
    nature_of_business = data['nature_of_business']
    supply_capabilites = data['supply_capabilites']
    industry_to_serve = data['industry_to_serve']
    maincore = data['maincore']
    category = data['category']
    sub_category = data['sub_category']

    try:
        businessrequestadvancesearch = BusinessRequest.objects.filter(updated_by=data['userid']).filter(
            company_code__icontains=company_code).filter(company_name__icontains=company_name).filter(
            city__icontains=city).filter(
            industry_to_serve__icontains=industry_to_serve).filter(
            nature_of_business__icontains=nature_of_business).filter(
            supply_capabilites__icontains=supply_capabilites).filter(
            maincore__icontains=maincore).filter(category__icontains=category).filter(
            sub_category__icontains=sub_category).values()

        return Response(
            {'status': '200', 'message': 'Business Request Advance Search', 'data': businessrequestadvancesearch},
            status=200)
    except Exception as e:
        return Response({'status': '500', 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes([AllowAny, ])
def advance_search_invite_vendor(request):
    # advance search invite vendor
    data = request.data
    company_name = data['company_name']
    contact_name = data['contact_name']
    email_id = data['email_id']
    phone_number = data['phone_number']
    registration_status = data['registration_status']
    approval_status = data['approval_status']

    try:
        invitevendoradvancesearch = InviteVendor.objects.filter(updated_by_invites=data['userid']).filter(
            company_name__icontains=company_name).filter(contact_name__icontains=contact_name).filter(
            email_id__icontains=email_id). \
            filter(phone_number__icontains=phone_number).filter(
            registration_status__icontains=registration_status).filter(
            approval_status__icontains=approval_status).values()

        return Response({'status': '200', 'message': 'Invite Vendor Advance Search', 'data': invitevendoradvancesearch},
                        status=200)
    except Exception as e:
        return Response({'status': '500', 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def advance_search_external_vendor(request):
    # external vendor advance search
    data = request.data
    maincore = data['maincore']
    category = data['category']
    subcategory = data['subcategory']
    bill_city = data['bill_city']
    bill_state = data['bill_state']
    nature_of_business = data['nature_of_business']
    industry_to_serve = data['industry_to_serve']
    company_code = data['company_code']
    company_name = data['company_name']
    valuearray = data['valuearray']
    externalarraysearch = []
    try:
        for i in range(0, len(valuearray)):
            if valuearray[i].get('company_code').count(company_code) > 0 and maincore.lower() in valuearray[i].get(
                    'maincore') and category.lower() in valuearray[i].get('category') and \
                    subcategory.lower() in valuearray[i].get('subcategory') and bill_city.lower() in valuearray[i].get(
                'bill_city').lower() and bill_state.lower() in valuearray[i].get('bill_state') and \
                    nature_of_business.lower() in valuearray[i].get(
                'nature_of_business') and industry_to_serve.lower() in valuearray[i].get(
                'industry_to_serve') and company_name.lower() in valuearray[i].get('company_name').lower():
                externalarraysearch.append(valuearray[i])
            else:
                print('Not Present')
        return Response({'status': 200, 'message': 'ok', 'data': externalarraysearch}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)