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
from .serializers import  *


class InviteVendorView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = InviteVendor.objects.all()
    serializer_class = InviteVendorSerializer
    ordering_fields = ['invite_id']
    ordering = ['invite_id']

    def create(self, request, *args, **kwargs):
        company_name=request.data.get('company_name',None)
        contact_name=request.data.get('contact_name',None)
        email_id=request.data.get('email_id',None)
        phone_number=request.data.get('phone_number',None)
        user_id=request.data.get('user_id',None)
        regarray=[]
        try:
            request.data['updated_by_invites']=user_id
            request.data['created_by']=user_id
            regobj=SelfRegistration.objects.filter().values('username')
            for i in range(0,len(regobj)):
                regarray.append(regobj[i].get('username'))
            if email_id in regarray:
                return Response({'status':202,'message':'Email Id already present in Registration'},status=202)
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
            return Response({'status':500,'error':str(e)},status=500)


    def get_queryset(self):
        inviteobj=InviteVendor.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by('invite_id')
        if inviteobj:
            return inviteobj
        raise ValidationError({'message':"Invited list by this user is not present","status":204})


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

class InternalBuyerView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = InternalBuyer.objects.all()
    serializer_class = InternalBuyerSerializer
    ordering_fields = ['internal_buyer_id']
    ordering = ['internal_buyer_id']

@api_view(['post'])
@permission_classes((AllowAny,))
def get_all_details_for_business_request(request):
    data=request.data
    regid=[]
    userid=data['userid']
    try:
        regobj1 = SelfRegistration.objects.filter(updated_by=userid).values()
        regobj=SelfRegistration.objects.filter().values()
        if len(regobj)>0:
            for i in range(0,len(regobj)):
                regid.append(regobj[i].get('id'))

            basicobj=BasicCompanyDetails.objects.filter(updated_by__in=regid).values('company_code','company_name','updated_by').order_by('company_code')
            industryhierarchy = IndustrialHierarchy.objects.filter(updated_by__in=regid).values('maincore','category','subcategory','updated_by').order_by('company_code')
            industryobj = IndustrialInfo.objects.filter(updated_by__in=regid).values('nature_of_business','supply_capabilites','industry_to_serve','updated_by').order_by('company_code')
            billingobj = BillingAddress.objects.filter(updated_by__in=regid).values('bill_city','updated_by').order_by('company_code')
            business_request = list(chain(basicobj, industryhierarchy, industryobj, billingobj))
            return Response({'status': 200, 'message': 'Business Request List','data':business_request}, status=200)
        return Response({'status': 204, 'message': 'Basic Details Not Present'}, status=204)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def external_vendor(request):
    data=request.data
    regid=[]
    userid=data['userid']
    internalarray=[]
    internalarray2=[]
    try:
        regobj1=SelfRegistration.objects.filter(id=userid).values()
        regobj=SelfRegistration.objects.filter().values()
        internalvendorobj = InternalVendor.objects.filter().values('company_code').order_by('internal_vendor_id')
        for i in range(0, len(internalvendorobj)):
            internalarray.append(internalvendorobj[i].get('company_code'))
        if len(regobj)>0:
            for i in range(0,len(regobj)):
                regid.append(regobj[i].get('id'))
            basicdata=BasicCompanyDetails.objects.filter(updated_by__in=regid).values()
            for i in range(0,len(basicdata)):
                if basicdata[i].get('company_code') not in internalarray:
                    x=basicdata[i].get('company_code')
                    internalarray2.append(x)
            basicdataobj= BasicCompanyDetails.objects.filter(company_code__in=internalarray2).values('company_code','company_name').order_by('company_code')
            industryhierarchy = IndustrialHierarchy.objects.filter(company_code__in=internalarray2).values('maincore','category','subcategory','updated_by','company_code').order_by('company_code')
            industryobj = IndustrialInfo.objects.filter(company_code__in=internalarray2).values('nature_of_business','industry_to_serve','updated_by','company_code').order_by('company_code')
            billingobj = BillingAddress.objects.filter(company_code__in=internalarray2).values('bill_city','bill_state','updated_by','company_code').order_by('company_code')
            external_vendor_array=list(chain(basicdataobj,industryhierarchy,industryobj,billingobj))
            return Response({'status': 200, 'message': 'External Vendor List','data':external_vendor_array}, status=200)
        return Response({'status': 204, 'message': 'Not Present'}, status=204)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['post'])
def advancesearch_business_request(request):
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
            company_code__icontains=company_code).filter(company_name__icontains=company_name).filter(city__icontains=city).filter(
            industry_to_serve__icontains=industry_to_serve).filter(nature_of_business__icontains=nature_of_business).filter(supply_capabilites__icontains=supply_capabilites).filter(
            maincore__icontains=maincore).filter(category__icontains=category).filter(sub_category__icontains=sub_category).values()

        return Response({'status': '200', 'message': 'Business Request Advance Search', 'data': businessrequestadvancesearch}, status=200)
    except Exception as e:
        return Response({'status': '500', 'error': str(e)}, status=500)
