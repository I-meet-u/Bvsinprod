from __future__ import print_function
import math
import urllib
from datetime import datetime, date
from itertools import chain

from django_filters import rest_framework as filters
import requests
from django.db.models import Q
from django.shortcuts import render
# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

from BiddingApp.models import VendorProductBidding, SourceList_CreateItems, SelectVendorsForBiddingProduct, \
    BuyerProductBidding, PurchaseOrder, SourcePublish, SourceAwards, Awards
from MastersApp.models import MaincoreMaster
from MaterialApp.models import LandingPageBidding, LandingPageBidding_Publish, VendorProduct_BasicDetails, \
    awardpostedRFQ
from RegistrationApp.models import BasicCompanyDetails, IndustrialInfo, IndustrialHierarchy, BillingAddress
from .models import *
from .serializers import *
from .service import get_open_bid_list, get_vendor_award_list, get_purchase_order_vendor_list, get_source_created_items, \
    get_deadline_date, total_all_responses_buyer, get_vendor_published_list, get_source_list_leads, \
    get_business_connections, get_business_requests_list, get_business_accept_list, get_listed_list_response


class InviteVendorView(viewsets.ModelViewSet):
    # permission_classes = [permissions.AllowAny]
    queryset = InviteVendor.objects.all()
    serializer_class = InviteVendorSerializer

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
            else:
                regobj = SelfRegistration.objects.filter(id=user_id).values()
                basicobj = BasicCompanyDetails.objects.filter(updated_by_id=regobj[0].get('id')).values()
                company_namesender = basicobj[0].get('company_name')
                print(company_name, 'register_company')

                # Configure API key authorization: api-key
                configuration = sib_api_v3_sdk.Configuration()
                configuration.api_key[
                    'api-key'] = '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'

                # Uncomment below lines to configure API key authorization using: partner-key
                # configuration = sib_api_v3_sdk.Configuration()
                # configuration.api_key['partner-key'] = 'YOUR_API_KEY'

                # create an instance of the API class
                api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
                send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=[{"email": email_id, "name": contact_name}],
                                                               template_id=16, params={"username": contact_name,
                                                                                       "receiverCompany": company_name,
                                                                                       "senderCompany": company_namesender},
                                                               subject='Business Invitation Collaboration'
                                                               )  # SendSmtpEmail | Values to send a transactional email

                try:
                    # Send a transactional email
                    api_response = api_instance.send_transac_email(send_smtp_email)
                    pprint(api_response)
                except ApiException as e:
                    print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
            return super().create(request, *args, **kwargs)


        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)

    def get_queryset(self):
        inviteobj = InviteVendor.objects.filter(updated_by_invites=self.request.GET.get('updated_by')).order_by(
            'invite_id')
        if inviteobj:
            return inviteobj
        raise ValidationError({'message': "Invited list by this user is not present", "status": 204})

class BusinessRequestFilter(filters.FilterSet):
    industry_to_serve = filters.CharFilter(lookup_expr='icontains')
    nature_of_business=filters.CharFilter(lookup_expr='icontains')
    company_name = filters.CharFilter(lookup_expr='icontains')
    state = filters.CharFilter(lookup_expr='icontains')
    send_status=filters.CharFilter(lookup_expr='icontains')
    city=filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = BusinessRequest
        fields = ('company_code', 'company_name','state','industry_to_serve','nature_of_business','send_status','updated_by','city')

class BusinessRequestView(viewsets.ModelViewSet):
    # permission_classes = [permissions.AllowAny]
    queryset = BusinessRequest.objects.all()
    serializer_class = BusinessRequestSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields  = ['industry_to_serve','nature_of_business']
    filterset_class = BusinessRequestFilter


class InternalVendorView(viewsets.ModelViewSet):
    # permission_classes = [permissions.AllowAny]
    queryset = InternalVendor.objects.all()
    serializer_class = InternalVendorSerializer

    def create(self, request, *args, **kwargs):
        ccode = request.data.get('ccode', None)
        userid=request.data.get('userid',None)
        try:
            if len(ccode)>0:
                print(ccode)
                for i in range(0,len(ccode)):
                    basicobj=BasicCompanyDetails.objects.filter(company_code=ccode[i]).values()
                    print(len(basicobj),'length')
                    address=BillingAddress.objects.filter(company_code=basicobj[0].get('company_code')).values()
                    regobj=SelfRegistration.objects.get(id=basicobj[0].get('updated_by_id'))
                    print(regobj.id)
                    hierarchyvalues = IndustrialHierarchy.objects.filter(company_code_id=ccode[i]).values()
                    InternalVendor.objects.create(company_code=basicobj[0].get('company_code'),
                                                  company_name=basicobj[0].get('company_name'),
                                                  city=address[0].get('bill_city'),
                                                  state=address[0].get('bill_state'),
                                                  nature_of_business=regobj.nature_of_business,
                                                  email_id=regobj.username,
                                                  phone_number=regobj.phone_number,
                                                  maincore=hierarchyvalues[0].get('maincore'),
                                                  category=hierarchyvalues[0].get('category'),
                                                  sub_category=hierarchyvalues[0].get('subcategory'),
                                                  updated_by=SelfRegistration.objects.get(id=userid),
                                                  created_by=userid
                                                  )
                return Response({'status': 201, 'message': "Internal Vendor Created"}, status=201)
            else:
                return Response({'status': 204, 'message': "Company Code Not Present"}, status=204)

        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def getinternalvendor(request):
    data = request.data
    try:
        intobj = InternalVendor.objects.filter(updated_by=data['updated_by']).values().order_by('internal_vendor_id')
        if len(intobj)>0:
            return Response({'status': 200,'message':'Internal Vendor List','data': intobj}, status=200)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=204)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


class InternalBuyerView(viewsets.ModelViewSet):
    # permission_classes = [permissions.AllowAny]
    queryset = InternalBuyer.objects.all()
    serializer_class = InternalBuyerSerializer

    def create(self, request, *args, **kwargs):
        ccode = request.data.get('ccode', None)
        userid = request.data.get('userid', None)
        try:
            if len(ccode) > 0:
                print(ccode)
                for i in range(0, len(ccode)):
                    basicobj = BasicCompanyDetails.objects.filter(company_code=ccode[i]).values()
                    print(len(basicobj), 'length')
                    print(basicobj[0].get('updated_by_id'),'bascic')
                    address = BillingAddress.objects.filter(company_code=basicobj[0].get('company_code')).values()
                    regobj = SelfRegistration.objects.get(id=basicobj[0].get('updated_by_id'))
                    print(regobj.id)
                    industryinfo = IndustrialInfo.objects.filter(company_code_id=ccode[i]).values()
                    InternalBuyer.objects.create(company_code=basicobj[0].get('company_code'),
                                                  company_name=basicobj[0].get('company_name'),
                                                  city=address[0].get('bill_city'),
                                                  state=address[0].get('bill_state'),
                                                  nature_of_business=regobj.nature_of_business,
                                                  email_id=regobj.username,
                                                  phone_number=regobj.phone_number,
                                                  industry_to_serve=industryinfo[0].get('industry_to_serve'),
                                                  updated_by=SelfRegistration.objects.get(id=userid),
                                                  created_by=userid
                                                  )
                return Response({'status': 201, 'message': "Internal Buyer Created"}, status=201)
            else:
                return Response({'status': 204, 'message': "Company Code Not Present"}, status=204)

        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)
@api_view(['post'])
# @permission_classes((AllowAny,))
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

@api_view(['post'])
# @permission_classes((AllowAny,))
def external_vendor(request):
    data = request.data
    userid = data['userid']
    internalarray = []
    externalarray = []
    try:
        regobjdata= SelfRegistration.objects.filter(Q(user_type='Vendor')| Q(user_type='Both'), ~Q(id=userid),admin_approve='Approved').values().order_by('id')
        internalobj = InternalVendor.objects.filter(updated_by_id=userid).values()
        for i in range(0, len(internalobj)):
            internalarray.append(internalobj[i].get('company_code'))
        if len(regobjdata)>0:
            for i in range(0, len(regobjdata)):
                basicobj = BasicCompanyDetails.objects.get(updated_by_id=regobjdata[i].get('id'))
                industryobj = IndustrialInfo.objects.get(updated_by_id=regobjdata[i].get('id'),company_code=basicobj.company_code)
                hierarchyobj = IndustrialHierarchy.objects.get(updated_by_id=regobjdata[i].get('id'))
                billingobj = BillingAddress.objects.filter(updated_by_id=regobjdata[i].get('id')).values()
                if basicobj.company_code not in internalarray:
                    externalarray.append({'company_code': basicobj.company_code,
                                          'company_name': basicobj.company_name,
                                          'nature_of_business': industryobj.nature_of_business,
                                          'industry_to_serve': industryobj.industry_to_serve,
                                          'maincore': hierarchyobj.maincore,
                                          'category': hierarchyobj.category,
                                          'subcategory': hierarchyobj.subcategory,
                                          'bill_city': billingobj[0].get('bill_city'),
                                          'bill_state': billingobj[0].get('bill_state'),
                                          'gst_number':basicobj.gst_number,
                                          'phone_no':regobjdata[i].get('phone_number'),
                                          'email_id':regobjdata[i].get('username')
                                          })

            return Response({'status': 200, 'message': 'External Vendor List', 'data': externalarray}, status=200)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=204)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
# @permission_classes([AllowAny, ])
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
# @permission_classes([AllowAny, ])
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
            print('dss')
            print(maincore)
            print(valuearray[i].get('maincore'),'sssssss')
            if valuearray[i].get('company_code').count(company_code) > 0 and bill_city.lower() in valuearray[i].get(
                'bill_city').lower() and bill_state.lower() in valuearray[i].get('bill_state').lower() and \
                    nature_of_business.lower() in valuearray[i].get(
                'nature_of_business').lower() and industry_to_serve.lower() in valuearray[i].get(
                'industry_to_serve').lower() and company_name.lower() in valuearray[i].get('company_name').lower() and \
                    maincore.lower() in valuearray[i].get('maincore') or category.lower() in valuearray[i].get('category') \
                    or subcategory.lower() in valuearray[i].get('subcategory'):
                externalarraysearch.append(valuearray[i])
            else:
                print('dddd')
                if maincore not in valuearray[i].get('maincore') and category not in valuearray[i].get('category') and subcategory not in valuearray[i].get('subcategory') and valuearray[i].get('company_code').count(company_code) > 0:
                    externalarraysearch.append(valuearray[i])
        return Response({'status': 200, 'message': 'ok', 'data': externalarraysearch}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
# @permission_classes((AllowAny,))
def buzrequestcreate(request):
    data = request.data
    compcode = data['compcode']
    userid = data['userid']
    emptyarra=[]

    try:
        businessrequest = BusinessRequest.objects.filter(company_code__in=compcode,updated_by_id=userid).values()
        for i in range(0,len(businessrequest)):
            if businessrequest[i].get('company_code') in compcode:
                return Response({'status':202,'message':'Company Code Already Present in Business Request'},status=status.HTTP_202_ACCEPTED)
            else:
                emptyarra.append(compcode)
                print(emptyarra)
        else:

            for i in range(0, len(compcode)):
                basicoj = BasicCompanyDetails.objects.filter(company_code=compcode[i]).values()
                billngaddrs = BillingAddress.objects.filter(company_code=basicoj[0].get('company_code')).values()
                Regobj = SelfRegistration.objects.get(id=basicoj[0].get('updated_by_id'))
                indobj = IndustrialInfo.objects.filter(company_code=compcode[i]).values()
                BusinessRequest.objects.create(company_code=basicoj[0].get('company_code'),
                                               company_name=basicoj[0].get('company_name'),
                                               city=billngaddrs[0].get('bill_city'), state=billngaddrs[0].get('bill_state'),
                                               nature_of_business=Regobj.nature_of_business,
                                               industry_to_serve=indobj[0].get('industry_to_serve'), created_by=userid,
                                               updated_by=SelfRegistration.objects.get(id=userid),
                                               gst_number=basicoj[0].get('gst_number'),
                                               email_id=Regobj.username,
                                               phone_number=Regobj.phone_number)

            return Response({'status': 200, 'message': 'Business Request Created'}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def sendergetbuzrequestdata(request):
    data = request.data
    userid = data['userid']
    businessrequestarray=[]
    try:
        buzobj = BusinessRequest.objects.filter(updated_by_id=userid).order_by('company_code').values()
        if len(buzobj)>0:
            for i in range(0,len(buzobj)):
                print('came')
                basicobj=BasicCompanyDetails.objects.filter(company_code=buzobj[i].get('company_code')).values()
                if len(basicobj)>0:
                    regobj=SelfRegistration.objects.get(id=basicobj[0].get('updated_by_id'))
                    businessrequestarray.append({'company_code':buzobj[i].get('company_code'),
                                                 'company_name':buzobj[i].get('company_name'),
                                                 'city':buzobj[i].get('city'),
                                                 'state':buzobj[i].get('state'),
                                                 'nature_of_business':buzobj[i].get('nature_of_business'),
                                                 'supply_capabilites':buzobj[i].get('supply_capabilites'),
                                                 'industry_to_serve':buzobj[i].get('industry_to_serve'),
                                                 'maincore':buzobj[i].get('maincore'),
                                                 'category':buzobj[i].get('category'),
                                                 'gst_number': buzobj[i].get('gst_number'),
                                                 'sub_category':buzobj[i].get('sub_category'),
                                                 'send_status':buzobj[i].get('send_status'),
                                                 'created_by':buzobj[i].get('created_by'),
                                                 'updated_by':buzobj[i].get('updated_by_id'),
                                                 'usertype':regobj.user_type


                                                 })
                else:
                    businessrequestarray.append({'company_code': buzobj[i].get('company_code'),
                                                 'company_name': buzobj[i].get('company_name'),
                                                 'city': buzobj[i].get('city'),
                                                 'state': buzobj[i].get('state'),
                                                 'nature_of_business': buzobj[i].get('nature_of_business'),
                                                 'supply_capabilites': buzobj[i].get('supply_capabilites'),
                                                 'industry_to_serve': buzobj[i].get('industry_to_serve'),
                                                 'maincore': buzobj[i].get('maincore'),
                                                 'category': buzobj[i].get('category'),
                                                 'gst_number': buzobj[i].get('gst_number'),
                                                 'sub_category': buzobj[i].get('sub_category'),
                                                 'send_status': buzobj[i].get('send_status'),
                                                 'created_by': buzobj[i].get('created_by'),
                                                 'updated_by': buzobj[i].get('updated_by_id'),
                                                 'usertype': regobj.user_type,

                                                 })

            return Response({'status': 200, 'message': 'ok', 'data': businessrequestarray}, status=200)
        else:
            return Response({'status': 204, 'message': 'No data present in business request','data':[]}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
# @permission_classes((AllowAny,))
def buzrequest(request):
    data = request.data
    userbuzdata = []

    try:
        basiccompoobj = BasicCompanyDetails.objects.filter(updated_by_id=data['userid']).values()
        if len(basiccompoobj)>0:
            businessrequest=BusinessRequest.objects.filter(company_code=basiccompoobj[0].get('company_code')).values().order_by('id')
            if len(businessrequest)>0:
                for i in range(0,len(businessrequest)):
                    regobj=SelfRegistration.objects.filter(id=businessrequest[i].get('updated_by_id')).values()
                    basival = BasicCompanyDetails.objects.filter(updated_by_id=businessrequest[i].get('updated_by_id')).values()
                    # print(basival[0].get('updated_by_id'),'ds')
                    industryinfoobj = IndustrialInfo.objects.filter(company_code_id=basival[0].get('company_code')).values()
                    billsaddrsobj = BillingAddress.objects.filter(company_code_id=basival[0].get('company_code'),updated_by_id=businessrequest[i].get('updated_by_id')).values()
                    if not billsaddrsobj:
                        states=""
                        city=""
                        userbuzdata.append({'profile_photo': regobj[0].get('profile_cover_photo'),
                                            'ccode':basival[0].get('company_code'),
                                            'cname': basival[0].get('company_name'),
                                            'gst_number': basival[0].get('gst_number'),
                                            'Industry': industryinfoobj[0].get('industry_to_serve'),
                                            'natureofbuz': industryinfoobj[0].get('nature_of_business'),
                                            'business_id': businessrequest[i].get('id'),
                                            'user_id': basival[0].get('updated_by_id'),
                                            'state':states,
                                            'city':city,
                                            'status':businessrequest[i].get('send_status')
                                            })
                    else:
                        states= billsaddrsobj[0].get('bill_state')
                        city=billsaddrsobj[0].get('bill_city')
                        userbuzdata.append({'profile_photo': regobj[0].get('profile_cover_photo'),
                                            'ccode': basival[0].get('company_code'),
                                            'cname': basival[0].get('company_name'),
                                            'gst_number': basival[0].get('gst_number'),
                                            'Industry': industryinfoobj[0].get('industry_to_serve'),
                                            'natureofbuz': industryinfoobj[0].get('nature_of_business'),
                                            'business_id': businessrequest[i].get('id'),
                                            'user_id': basival[0].get('updated_by_id'),
                                            'state': states,
                                            'city': city,
                                            'status': businessrequest[i].get('send_status')
                                            })
                return Response({'status':200,'message':'ok','data':userbuzdata},status=200)
            else:
                return Response({'status': 204, 'message': 'Company code not present in busines request','data':[]}, status=204)
        else:
            return Response({'status': 202, 'message': 'not present','data':[]}, status=202)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
# @permission_classes((AllowAny,))
def business_request_accept_reject_advance_search(request):
    data = request.data
    company_code = data['company_code']
    company_name = data['company_name']
    nature_of_business = data['nature_of_business']
    city = data['city']
    state = data['state']
    industry_type = data['industry_type']
    valuedata = data['valuedata']
    businessrequestdata = []
    try:
        for i in range(0, len(valuedata)):
            if company_code.lower() in valuedata[i].get('company_code').lower() and company_name.lower() in valuedata[
                i].get('company_name').lower() and \
                    nature_of_business.lower() in valuedata[i].get('nature_of_business').lower() and city.lower() in \
                    valuedata[i].get('city').lower() and state.lower() in valuedata[i].get('state').lower() and \
                    industry_type.lower() in valuedata[i].get('industry_type').lower():
                businessrequestdata.append(valuedata[i])
        return Response({'status': 200, 'message': 'ok', 'data': businessrequestdata}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
# @permission_classes((AllowAny,))
def search_business_request_advance_search(request):
    # business request advance search
    data = request.data
    company_code = data['company_code']
    company_name = data['company_name']
    state = data['state']
    industry_to_serve = data['industry_to_serve']
    nature_of_business = data['nature_of_business']
    send_status=data['send_status']
    userid=data['userid']
    serveappend = []
    try:
        serveappend.append(industry_to_serve)
        businessrequestadvancesearch=BusinessRequest.objects.filter(updated_by_id=userid).filter(company_code__icontains=company_code).filter(company_name__icontains=company_name).filter(state__icontains=state).filter(industry_to_serve__in=industry_to_serve).filter(nature_of_business__in=nature_of_business).filter(send_status__icontains=send_status).values()

        return Response(
            {'status': '200', 'message': 'Business Request Advance Search', 'data': businessrequestadvancesearch},
            status=200)
    except Exception as e:
        return Response({'status': '500', 'error': str(e)}, status=500)



@api_view(['put'])
def update_business_status(request):
    data = request.data
    businessid = data['businessid']
    statusval=data['statusval']
    try:
        businessobj = BusinessRequest.objects.filter(id=businessid).values().order_by('id')
        print(len(businessobj))
        if len(businessobj)>0:

            for i in range(0, len(businessobj)):
                businessobj = BusinessRequest.objects.get(id=businessobj[i].get('id'))
                print(businessobj)
                if businessobj.send_status!=statusval:
                    businessobj.send_status = statusval
                    businessobj.save()
                    businessval=BusinessRequest.objects.filter(id=businessid).values()
                    return Response({'status': 200, 'message': 'Status Updated', 'data': businessval},status=status.HTTP_200_OK)
                else:
                    return Response({'status': 202, 'message': 'Already Updated'},status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'status': 204, 'message': 'Data Not Present with this id'}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['post'])
def searchinternalvendor(request):
    data = request.data
    ccode = data['ccode']
    cname = data['cname']
    city = data['city']
    nob = data['nob']
    state = data['state']
    grp = data['grp']
    maincore = data['maincore']
    category = data['category']
    subcategory = data['subcategory']
    nature=[]

    try:
        nature.append(nob)
        if grp == "":

            internalobj = InternalVendor.objects.filter(updated_by=data['userid'], company_code=ccode,
                                                        company_name__icontains=cname, city__icontains=city,
                                                        nature_of_business__contains=nature, state__icontains=state,
                                                        maincore__icontains=[maincore], category__icontains=category,
                                                        sub_category__icontains=subcategory,
                                                        groups__isnull=True).values()
        else:

            internalobj = InternalVendor.objects.filter(updated_by=data['userid'], company_code=ccode,
                                                        company_name__icontains=cname, city__icontains=city,
                                                        nature_of_business__icontains=nob, state__icontains=state,
                                                        maincore__icontains=maincore, category__icontains=category,
                                                        sub_category__icontains=subcategory,
                                                        groups__icontains=grp).values()

        return Response({'status': 200, 'message': 'ok', 'data': internalobj}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def buyer_list(request):
    data=request.data
    userid=data['userid']
    internalbuyerarray=[]
    buyerarray=[]
    try:
        regobj = SelfRegistration.objects.filter(Q(user_type='Buyer')| Q(user_type='Both'),admin_approve='Approved').values().order_by(
            'id')
        print(len(regobj))
        internalobj = InternalBuyer.objects.filter(updated_by_id=userid).values()
        for i in range(0, len(internalobj)):
            internalbuyerarray.append(internalobj[i].get('company_code'))

        if len(regobj) > 0:
            for i in range(0, len(regobj)):
                basicobj = BasicCompanyDetails.objects.filter(updated_by_id=regobj[i].get('id')).values()
                industryobj = IndustrialInfo.objects.get(updated_by_id=regobj[i].get('id'),
                                                         company_code=basicobj[0].get('company_code'))
                # hierarchyobj = IndustrialHierarchy.objects.get(updated_by_id=regobj[i].get('id'))
                billingobj = BillingAddress.objects.filter(updated_by_id=regobj[i].get('id')).values()
                if basicobj[0].get('company_code') not in internalbuyerarray:
                    print('ok')

                    buyerarray.append({'company_code': basicobj[0].get('company_code'),
                                       'company_name': basicobj[0].get('company_name'),
                                       'nature_of_business': industryobj.nature_of_business,
                                       'industry_to_serve': industryobj.industry_to_serve,
                                       'bill_city': billingobj[0].get('bill_city'),
                                       'bill_state': billingobj[0].get('bill_state'),
                                       'phone_no': regobj[i].get('phone_number'),
                                       'email_id': regobj[i].get('username')

                                          })
                else:
                    print('already present')

            return Response({'status': 200, 'message': 'Buyer List', 'data': buyerarray}, status=200)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=204)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def add_users_internal_buyer_and_internal_vendor(request):
    data=request.data
    userid=data['userid']
    ccode=data['ccode']
    internalarray=[]
    internalbuyerarray=[]
    interalbuyer=[]
    usertype=data['usertype']
    vendorboth=data['vendorboth']
    try:

        interalvendor=InternalVendor.objects.filter(updated_by_id=userid).values()
        for i in range(0,len(interalvendor)):
            internalarray.append(interalvendor[i].get('company_code'))
        interalbuyer = InternalBuyer.objects.filter(updated_by_id=userid).values()
        for i in range(0, len(interalbuyer)):
            internalbuyerarray.append(interalbuyer[i].get('company_code'))
        basicobj = BasicCompanyDetails.objects.filter(company_code__in=ccode).values()
        if len(basicobj)>0:
            if usertype=='Vendor' and vendorboth=="False":
                for i in range(0,len(basicobj)):
                    regobjdata=SelfRegistration.objects.get(user_type='Vendor',admin_approve='Approved',id=basicobj[i].get('updated_by_id'))
                    if basicobj[i].get('company_code') not in internalarray and regobjdata.user_type=='Vendor':
                        print('internal vendor')
                        industryhierarchy=IndustrialHierarchy.objects.get(company_code_id=basicobj[i].get('company_code'))
                        billobj = BillingAddress.objects.filter(company_code_id=basicobj[i].get('company_code')).values()
                        internalvendorobj=InternalVendor.objects.create(company_code=basicobj[i].get('company_code'),
                                                                        company_name=basicobj[i].get('company_name'),
                                                                        city=billobj[0].get('bill_city'),
                                                                        state=billobj[0].get('bill_state'),
                                                                        nature_of_business=regobjdata.nature_of_business,
                                                                        email_id=regobjdata.username,
                                                                        phone_number=regobjdata.phone_number,
                                                                        maincore=industryhierarchy.maincore,
                                                                        category=industryhierarchy.category,
                                                                        sub_category=industryhierarchy.subcategory,
                                                                        created_by=userid,
                                                                        updated_by=SelfRegistration.objects.get(id=userid))
                return Response(
                    {'status': 200, 'message': 'Vendors are added to internal vendor successfully'},
                    status=200)
            elif usertype=='Buyer' and vendorboth=="False":
                for i in range(0,len(basicobj)):
                    regobjdata=SelfRegistration.objects.get(user_type='Buyer',admin_approve='Approved',id=basicobj[i].get('updated_by_id'))
                    if basicobj[i].get('company_code')  not in internalbuyerarray and regobjdata.user_type=='Buyer':
                        print('internal buyer')
                        industryinfo = IndustrialInfo.objects.get(company_code_id=basicobj[i].get('company_code'))
                        billobj = BillingAddress.objects.filter(company_code_id=basicobj[i].get('company_code')).values()
                        internalbuyerobj = InternalBuyer.objects.create(company_code=basicobj[i].get('company_code'),
                                                                        company_name=basicobj[i].get('company_name'),
                                                                        city=billobj[0].get('bill_city'),
                                                                        state=billobj[0].get('bill_state'),
                                                                        nature_of_business=regobjdata.nature_of_business,
                                                                        industry_to_serve=industryinfo.industry_to_serve,
                                                                        email_id=regobjdata.username,
                                                                        phone_number=regobjdata.phone_number,
                                                                        created_by=userid,
                                                                        updated_by=SelfRegistration.objects.get(
                                                                            id=userid))
                return Response(
                    {'status': 200, 'message': 'Buyers are added to internal buyer successfully'},
                    status=200)
            elif usertype=='Both'and vendorboth=="False":
                for i in range(0, len(basicobj)):
                    regobjdata=SelfRegistration.objects.get(user_type='Both',admin_approve='Approved',id=basicobj[i].get('updated_by_id'))
                    if basicobj[i].get('company_code') not in internalarray and basicobj[i].get('company_code') not in internalbuyerarray  and regobjdata.user_type == 'Both':
                        print('internal vendor')
                        industryhierarchy = IndustrialHierarchy.objects.get(company_code_id=basicobj[i].get('company_code'))
                        billobj = BillingAddress.objects.filter(company_code_id=basicobj[i].get('company_code')).values()
                        industryinfo = IndustrialInfo.objects.get(company_code_id=basicobj[i].get('company_code'))
                        internalvendorobj = InternalVendor.objects.create(company_code=basicobj[i].get('company_code'),
                                                                          company_name=basicobj[i].get('company_name'),
                                                                          city=billobj[0].get('bill_city'),
                                                                          state=billobj[0].get('bill_state'),
                                                                          nature_of_business=regobjdata.nature_of_business,
                                                                          email_id=regobjdata.username,
                                                                          phone_number=regobjdata.phone_number,
                                                                          maincore=industryhierarchy.maincore,
                                                                          category=industryhierarchy.category,
                                                                          sub_category=industryhierarchy.subcategory,
                                                                          created_by=userid,
                                                                          updated_by=SelfRegistration.objects.get(
                                                                              id=userid))
                        internalbuyerobj = InternalBuyer.objects.create(company_code=basicobj[i].get('company_code'),
                                                                        company_name=basicobj[i].get('company_name'),
                                                                        city=billobj[0].get('bill_city'),
                                                                        state=billobj[0].get('bill_state'),
                                                                        nature_of_business=regobjdata.nature_of_business,
                                                                        industry_to_serve=industryinfo.industry_to_serve,
                                                                        email_id=regobjdata.username,
                                                                        phone_number=regobjdata.phone_number,
                                                                        created_by=userid,
                                                                        updated_by=SelfRegistration.objects.get(
                                                                            id=userid))

                return Response({'status': 200, 'message': 'Both are added to internal vendor and internal buyer successfully'},status=200)
            elif usertype == 'Vendor' and vendorboth == "True":
                for i in range(0, len(basicobj)):
                    regobjdata = SelfRegistration.objects.get(user_type='Vendor', admin_approve='Approved',
                                                              id=basicobj[i].get('updated_by_id'))
                    if basicobj[i].get('company_code') not in internalarray and basicobj[i].get(
                            'company_code') not in internalbuyerarray and regobjdata.user_type == 'Vendor':
                        print('internal vendor')
                        industryhierarchy = IndustrialHierarchy.objects.get(company_code_id=basicobj[i].get('company_code'))
                        billobj = BillingAddress.objects.filter(company_code_id=basicobj[i].get('company_code')).values()
                        industryinfo = IndustrialInfo.objects.get(company_code_id=basicobj[i].get('company_code'))
                        internalvendorobj = InternalVendor.objects.create(company_code=basicobj[i].get('company_code'),
                                                                          company_name=basicobj[i].get('company_name'),
                                                                          city=billobj[0].get('bill_city'),
                                                                          state=billobj[0].get('bill_state'),
                                                                          nature_of_business=regobjdata.nature_of_business,
                                                                          email_id=regobjdata.username,
                                                                          phone_number=regobjdata.phone_number,
                                                                          maincore=industryhierarchy.maincore,
                                                                          category=industryhierarchy.category,
                                                                          sub_category=industryhierarchy.subcategory,
                                                                          created_by=userid,
                                                                          updated_by=SelfRegistration.objects.get(
                                                                              id=userid))
                        internalbuyerobj = InternalBuyer.objects.create(company_code=basicobj[i].get('company_code'),
                                                                        company_name=basicobj[i].get('company_name'),
                                                                        city=billobj[0].get('bill_city'),
                                                                        state=billobj[0].get('bill_state'),
                                                                        nature_of_business=regobjdata.nature_of_business,
                                                                        industry_to_serve=industryinfo.industry_to_serve,
                                                                        email_id=regobjdata.username,
                                                                        phone_number=regobjdata.phone_number,
                                                                        created_by=userid,
                                                                        updated_by=SelfRegistration.objects.get(
                                                                            id=userid))

                return Response(
                    {'status': 200, 'message': 'Vendors are added to internal vendor and internal buyer successfully'},
                    status=200)
            else:
                return Response({'status':204,'message':"user_type or vendor_both is not correct or mis-spelled"},status=204)
        else:
            return Response({'status': 202, 'message': "Details are not present for specified data or ccode is not present"},status=202)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def get_internal_buyer(request):
    data = request.data
    try:
        internalbuyer = InternalBuyer.objects.filter(updated_by=data['updated_by']).values().order_by('internal_buyer_id')
        if len(internalbuyer)>0:
            return Response({'status': 200,'message':'Internal Buyer List','data': internalbuyer}, status=200)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def all_vendors_list(request):
    data=request.data
    userid = data['userid']
    internalarray = []
    internalbuyerarray=[]
    externalarray = []
    try:
        regobjdata = SelfRegistration.objects.filter(Q(user_type='Vendor') | Q(user_type='Both'),
                                                     admin_approve='Approved').values().order_by('id')
        print(len(regobjdata),'okkkkkkkkkkkkkkkkkkkkkkkkks')
        internalobj = InternalVendor.objects.filter(updated_by_id=userid).values()
        for i in range(0, len(internalobj)):
            internalarray.append(internalobj[i].get('company_code'))
        internalbuyer = InternalBuyer.objects.filter(updated_by_id=userid).values()
        for i in range(0, len(internalbuyer)):
            internalbuyerarray.append(internalbuyer[i].get('company_code'))
        if len(regobjdata) > 0:
            for i in range(0, len(regobjdata)):
                basicobj = BasicCompanyDetails.objects.get(updated_by_id=regobjdata[i].get('id'))
                industryobj = IndustrialInfo.objects.get(updated_by_id=regobjdata[i].get('id'),
                                                         company_code=basicobj.company_code)
                billingobj = BillingAddress.objects.filter(updated_by_id=regobjdata[i].get('id')).values()
                hierarchyobj = IndustrialHierarchy.objects.get(updated_by_id=regobjdata[i].get('id'),
                                                                  company_code=basicobj.company_code)
                if basicobj.company_code not in internalarray or basicobj.company_code not in internalbuyerarray:
                    externalarray.append({'company_code': basicobj.company_code,
                                          'company_name': basicobj.company_name,
                                          'industry_scale': basicobj.industrial_scale,
                                          'nature_of_business': industryobj.nature_of_business,
                                          'industry_to_serve': industryobj.industry_to_serve,
                                           'maincore': hierarchyobj.maincore,
                                          'category': hierarchyobj.category,
                                          'subcategory': hierarchyobj.subcategory,
                                          'bill_city': billingobj[0].get('bill_city'),
                                          'bill_state': billingobj[0].get('bill_state'),
                                          'gst_number': basicobj.gst_number,
                                          'phone_no': regobjdata[i].get('phone_number'),
                                          'email_id': regobjdata[i].get('username'),
                                          'usertype':regobjdata[i].get('user_type'),
                                              })
        regobjdata1 = SelfRegistration.objects.filter(user_type='Buyer',admin_approve='Approved').values().order_by('id')
        print(len(regobjdata1), 'aa')
        if len(regobjdata1) > 0:
            for i in range(0, len(regobjdata1)):
                print(regobjdata1[i].get('id'))
                basicobj = BasicCompanyDetails.objects.get(updated_by_id=regobjdata1[i].get('id'))
                industryobj = IndustrialInfo.objects.get(updated_by_id=regobjdata1[i].get('id'),
                                                         company_code=basicobj.company_code)
                billingobj = BillingAddress.objects.filter(updated_by_id=regobjdata1[i].get('id')).values()

                if basicobj.company_code not in internalarray or basicobj.company_code not in internalbuyerarray:
                    externalarray.append({'company_code': basicobj.company_code,
                                          'company_name': basicobj.company_name,
                                          'industry_scale': basicobj.industrial_scale,
                                          'nature_of_business': industryobj.nature_of_business,
                                          'industry_to_serve': industryobj.industry_to_serve,
                                          'maincore': "",
                                          'category': "",
                                          'subcategory': "",
                                          'bill_city': billingobj[0].get('bill_city'),
                                          'bill_state': billingobj[0].get('bill_state'),
                                          'gst_number': basicobj.gst_number,
                                          'phone_no': regobjdata1[i].get('phone_number'),
                                          'email_id': regobjdata1[i].get('username'),
                                          'usertype': regobjdata1[i].get('user_type'),
                                          })



            return Response({'status': 200, 'message': 'External Vendor List', 'data': externalarray}, status=200)
        else:
            return Response({'status': 204, 'message': 'Not Present','data':[]}, status=204)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def business_request_accept_list(request):
    ccode=request.data['ccode']
    arraycode=[]
    try:
        businessacceptobj = BusinessRequest.objects.filter(company_code=ccode,send_status='Accept').values().order_by('id')
        if len(businessacceptobj)>0:
            for i in range(0, len(businessacceptobj)):
                basicobj=BasicCompanyDetails.objects.filter(updated_by_id=businessacceptobj[i].get('updated_by_id')).values()
                billobj=BillingAddress.objects.filter(updated_by_id=basicobj[0].get('updated_by_id')).values()
                inudstryinfoobj=IndustrialInfo.objects.get(updated_by_id=basicobj[0].get('updated_by_id'))
                arraycode.append({'company_code':basicobj[0].get('company_code'),
                                  'company_name':basicobj[0].get('company_name'),
                                  'gst_number':basicobj[0].get('gst_number'),
                                  'city':billobj[0].get('bill_city'),
                                  'state':billobj[0].get('bill_state'),
                                  'nature_of_business': inudstryinfoobj.nature_of_business,
                                  'industry_to_serve': inudstryinfoobj.industry_to_serve,
                                  'send_status':businessacceptobj[i].get('send_status')
                                  })
            return Response({'status': 200, 'message': 'Business Request Accepted List', 'data': arraycode}, status=200)
        else:
            return Response({'status': 204, 'message': 'Accepted List Not Present','data':[]}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def business_request_accept_list_user_id(request):
    userid=request.data['userid']
    arraycode=[]
    try:
        basicobj=BasicCompanyDetails.objects.filter(updated_by_id=userid).values()
        if len(basicobj)>0:
            businessacceptobj = BusinessRequest.objects.filter(company_code=basicobj[0].get('company_code'),send_status='Accept').values().order_by('id')
            if len(businessacceptobj)>0:
                for i in range(0, len(businessacceptobj)):
                    basicobj=BasicCompanyDetails.objects.filter(updated_by_id=businessacceptobj[i].get('updated_by_id')).values()
                    billobj=BillingAddress.objects.filter(updated_by_id=basicobj[0].get('updated_by_id')).values()
                    inudstryinfoobj=IndustrialInfo.objects.get(updated_by_id=basicobj[0].get('updated_by_id'))
                    arraycode.append({'company_code':basicobj[0].get('company_code'),
                                      'company_name':basicobj[0].get('company_name'),
                                      'gst_number':basicobj[0].get('gst_number'),
                                      'city':billobj[0].get('bill_city'),
                                      'state':billobj[0].get('bill_state'),
                                      'nature_of_business': inudstryinfoobj.nature_of_business,
                                      'industry_to_serve': inudstryinfoobj.industry_to_serve,
                                      })
                return Response({'status': 200, 'message': 'Business Request Accepted List', 'data': arraycode}, status=200)
            else:
                return Response({'status': 204, 'message': 'Accepted List Not Present','data':[]}, status=204)
        else:
            return Response({'status': 202, 'message': 'Not Present', 'data': []}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def business_request_reject_list(request):
    ccode=request.data['ccode']
    arraycode=[]
    try:
        businessrejectobj = BusinessRequest.objects.filter(company_code=ccode, send_status='Reject').values().order_by(
            'id')
        if len(businessrejectobj) > 0:
            for i in range(0, len(businessrejectobj)):
                basicobj = BasicCompanyDetails.objects.filter(updated_by_id=businessrejectobj[i].get('updated_by_id')).values()
                billobj = BillingAddress.objects.filter(updated_by_id=basicobj[0].get('updated_by_id')).values()
                industryinfoobj = IndustrialInfo.objects.get(updated_by_id=basicobj[0].get('updated_by_id'))
                arraycode.append({'company_code': basicobj[0].get('company_code'),
                                  'company_name': basicobj[0].get('company_name'),
                                  'gst_number': basicobj[0].get('gst_number'),
                                  'city': billobj[0].get('bill_city'),
                                  'state': billobj[0].get('bill_state'),
                                  'nature_of_business': industryinfoobj.nature_of_business,
                                  'industry_to_serve': industryinfoobj.industry_to_serve,
                                  'send_status':businessrejectobj[i].get('send_status')
                                  })
            return Response({'status': 200, 'message': 'Business Request Rejected List', 'data': arraycode}, status=200)
        else:
            return Response({'status': 204, 'message': 'Rejected List Not Present'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
# @permission_classes([AllowAny, ])
def advance_search_item_list(request):
    # external vendor advance search
    data = request.data
    item_code = data['item_code']
    item_name = data['item_name']
    item_type = data['item_type']
    department = data['department']
    category = data['category']
    item_group = data['item_group']
    UOM = data['UOM']
    hsn_sac = data['hsn_sac']
    unit_price = data['unit_price']
    description = data['description']
    model_no = data['model_no']
    valuearray = data['valuearray']
    itemlistarray = []
    try:
        for i in range(0, len(valuearray)):
            if item_code.lower() in valuearray[i].get('item_code').lower() and item_name.lower() in valuearray[i].get(
                    'item_name').lower() and item_type.lower() in valuearray[i].get('item_type').lower() and department.lower() in valuearray[i].get('department').lower() and category.lower() in valuearray[i].get(
                'category').lower() and item_group.lower() in valuearray[i].get('item_group').lower() and \
                    UOM.lower() in valuearray[i].get(
                'UOM').lower() and hsn_sac.lower() in valuearray[i].get(
                'hsn_sac').lower() and unit_price.lower() in valuearray[i].get('unit_price').lower() and \
                    description.lower() in valuearray[i].get('description').lower() and \
                    model_no.lower() in valuearray[i].get('model_no').lower():
                itemlistarray.append(valuearray[i])
            else:
                print('Not Present')
        return Response({'status': 200, 'message': 'ok', 'data': itemlistarray}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def buyer_dashboard_charts_counts(request):
    data=request.data
    userid=data['userid']
    from_registration=data['from_registration']
    totalsentcount = 0
    totalacceptcount = 0
    totalrejectcount = 0
    totalpendingcount = 0
    totalfullresponse = 0
    buyercharts=[]
    closedarray=[]
    listingleadsclosedarray=[]
    try:
        auth_token = request.headers['Authorization']
        print(auth_token)
        bidobj=BuyerProductBidding.objects.filter(updated_by_id=userid).values()
        print(len(bidobj),'ok')
        for i in range(0,len(bidobj)):
            print('ok')
            if bidobj[i].get('product_deadline_date') < date.today():
                print(bidobj[i].get('product_deadline_date'),'product_deadline')
                closedarray.append({'product_deadline_date':bidobj[i].get('product_deadline_date')})

        buyerbidobjpublished = BuyerProductBidding.objects.filter(updated_by_id=userid,
                                                                  product_rfq_status='Published').values()
        responsecount = total_all_responses_buyer(userid, from_registration, auth_token)
        values_list = responsecount['data']
        print(values_list, 'fdsfsdfsfffffffff')
        for i in range(0, len(values_list)):
            sent = values_list[i].get('total_sent')
            totalsentcount = totalsentcount + sent
            accept = values_list[i].get('total_accepted')
            totalacceptcount = totalacceptcount + accept
            reject = values_list[i].get('total_rejected')
            totalrejectcount = totalrejectcount + reject
            pending = values_list[i].get('pending')
            totalpendingcount = totalpendingcount + pending
            totalfullresponse = totalacceptcount + totalrejectcount
            print('--------------------------done--------------------------------')
        confirmed_po = PurchaseOrder.objects.filter(updated_by_id=userid).values()
        invitevendorobj = InviteVendor.objects.filter(updated_by_invites_id=userid).values()
        invites_approved = BusinessRequest.objects.filter(send_status='Accept', updated_by_id=userid).values()
        internalvendor = InternalVendor.objects.filter(updated_by_id=userid).values()
        # trailvendors = TrailVendors.objects.filter(updated_by_id=userid).values()
        source_published = SourcePublish.objects.filter(updated_by_id=userid).values()
        sourcelistcreateitesmsobj = SourceList_CreateItems.objects.filter(updated_by_id=userid).values()
        sourceresponse = get_source_created_items(userid, auth_token)
        pendingsourcevalues=len(sourcelistcreateitesmsobj)-len(sourceresponse['data'])
        sourceaward=SourceAwards.objects.filter(updated_by_id=userid).values()
        landingpageobj=LandingPageBidding.objects.filter(updated_by_id=userid).values()
        landingpagepending = LandingPageBidding.objects.filter(updated_by_id=userid,status='Pending').values()
        landingpagepublish= LandingPageBidding_Publish.objects.filter(updated_by_id=userid).values()
        landingpageawardobj=awardpostedRFQ.objects.filter(updated_by_id=userid).values()
        landingpageclosedobj = LandingPageBidding.objects.filter(updated_by_id=userid).values().order_by(
            'id')
        landingpageresponseobj=get_listed_list_response(userid,auth_token)
        awardobj=Awards.objects.filter(updated_by_id=userid).values()
        pending_po = Awards.objects.filter(updated_by_id=userid,postatus='Pending').values()
        businessrequestlist = get_business_requests_list(userid, auth_token)
        businessconnections = get_business_connections(userid, auth_token)
        for i in range(0, len(landingpageclosedobj)):
            deadlinedateval = datetime.strptime(landingpageclosedobj[i].get('deadline_date'), '%Y-%m-%d')
            deadlinedateconvertion = datetime.date(deadlinedateval)
            todaydate = date.today()
            if deadlinedateconvertion < todaydate:
                print('s',landingpageclosedobj[i].get('deadline_date'))
                listingleadsclosedarray.append({'deadline_date':landingpageclosedobj[i].get('deadline_date')})

        buyercharts.append({'closed_rfq':len(closedarray),
                            'rfq_published': len(buyerbidobjpublished),
                            'response_totalsentcount': totalsentcount,
                            'response_acceptedcount': totalacceptcount,
                            'response_rejected': totalrejectcount,
                            'response_pendingcount': totalpendingcount,
                            'response_totalfullresponse': totalfullresponse,
                            'confirmed_po': len(confirmed_po),
                            'pending_po':len(pending_po),
                            'total_business_invites': len(invitevendorobj),
                            'invites_approved': len(invites_approved),
                            'internal_vendor': len(internalvendor),
                            # 'trail_vendors': len(trailvendors),
                            'source_posts':len(sourcelistcreateitesmsobj),
                            'source_published': len(source_published),
                            'source_response': len(sourceresponse['data']),
                            'source_pending': pendingsourcevalues,
                            'source_awards':len(sourceaward),
                            'total_posted_items':len(landingpageobj),
                            'posted_items_pending':len(landingpagepending),
                            'posted_items_publish':len(landingpagepublish),
                            'posted_items_closed':len(listingleadsclosedarray),
                            'posted_items_response':len(landingpageresponseobj['data']),
                            'posted_items_awards':len(landingpageawardobj),
                            'bizRequestVendorLength':len(businessrequestlist['data']),
                            'bizConnectionsVendorLength':len(businessconnections['data']),
                            'buyer_awards':len(awardobj)
                            })
        return Response({'status': 200, 'message': 'Buyer Charts Count List','data':buyercharts}, status=200)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def vendor_dashboard_count(request):
    data=request.data
    userid=data['userid']
    from_registration=data['from_registration']
    totalvendorarray=[]
    vendorproductarray=[]
    closedarray=[]
    deadlinearray=[]
    try:
        auth_token = request.headers['Authorization']
        vendorobj=VendorProduct_BasicDetails.objects.filter(updated_by_id=userid).values()
        print(len(vendorobj))
        landingpagepublish=LandingPageBidding_Publish.objects.filter(updated_by_id=userid).values()
        print(len(landingpagepublish))
        landingpageobj = LandingPageBidding.objects.filter(vendor_user_id=userid).values()

        for i in range(0,len(landingpageobj)):
            deadlinedateval = datetime.strptime(landingpageobj[i].get('deadline_date'), '%Y-%m-%d')
            deadlinedateconvertion = datetime.date(deadlinedateval)
            todaydate = date.today()
            if deadlinedateconvertion > todaydate:
                print('sssss')
                closedarray.append(landingpageobj[i].get('deadline_date'))
        source_pending=get_source_list_leads(userid,auth_token)
        source_publish=SourcePublish.objects.filter(source_user_id=userid).values()
        sourceobj=SourceList_CreateItems.objects.filter(updated_by_id=userid).values()
        for i in range(0,len(sourceobj)):
            deadlinedateval = datetime.strptime(sourceobj[i].get('deadline_date'), '%Y-%m-%d')
            deadlinedateconvertion = datetime.date(deadlinedateval)
            print(deadlinedateconvertion)
            todaydate = date.today()
            print(todaydate,'todats')
            if deadlinedateconvertion > todaydate:
                print('kkk')
                deadlinearray.append(sourceobj[i].get('deadline_date'))
        sourceaward=SourceAwards.objects.filter(updated_by_id=userid).values()
        totalopenbidlist = get_open_bid_list(userid, from_registration, auth_token)
        print('\n')
        print(totalopenbidlist['data'])
        closedrfqlist = get_deadline_date(userid, from_registration, auth_token)
        publishedobj = get_vendor_published_list(userid, auth_token)
        rejectedobj = SelectVendorsForBiddingProduct.objects.filter(updated_by_id=userid,
                                                                    vendor_status='Reject').values()
        vendorsaward = get_vendor_award_list(userid, auth_token)
        award_pending = len(publishedobj['data']) - (len(vendorsaward['data']))
        purchaserodervendorslist = get_purchase_order_vendor_list(userid, auth_token)
        pending_po = len(vendorsaward['data']) - (len(purchaserodervendorslist['data']))
        inviteobj = InviteVendor.objects.filter(updated_by_invites_id=userid).values()
        businessacceptlist=get_business_accept_list(userid,auth_token)
        businessrequestlist=get_business_requests_list(userid,auth_token)
        businessconnections=get_business_connections(userid,auth_token)
        if (award_pending<0 or pending_po<0) or award_pending<0 or pending_po<0:
            print('s')
            totalvendorarray.append({'listing_leads_published_vendor': len(landingpagepublish),
                                     'listing_leads_pending_vendor': len(vendorobj),
                                     'listing_leads_closed_vendor': len(closedarray),
                                     'source_pending_vendor':len(source_pending['data']),
                                     'source_publish_vendor':len(source_publish),
                                     'source_closed_vendor':len(deadlinearray),
                                     'source_award_vendor':len(sourceaward),
                                     'rfq_publish_pending_vendor': len(totalopenbidlist['data']),
                                     'rfq_closed_bid_vendor': len(closedrfqlist['data']),
                                     'published_leads_vendor': len(publishedobj['data']),
                                     'reject_leads_vendor': len(rejectedobj),
                                     'awarded_vendor': len(vendorsaward['data']),
                                     'award_pending_vendor': 0,
                                     'confirmed_purchase_order_vendor': len(purchaserodervendorslist['data']),
                                     'pending_po_vendor': 0,
                                     'business_invite_count_vendor': len(inviteobj),
                                     'businesss_request_list_vendor': len(businessrequestlist['data']),
                                     'business_connections_vendor':len(businessconnections['data']),
                                     'invites_approved_vendor':len(businessacceptlist['data'])
                                     })
        else:
            totalvendorarray.append({'listing_leads_published_vendor': len(landingpagepublish),
                                     'listing_leads_pending_vendor': len(vendorobj),
                                     'listing_leads_closed_vendor': len(closedarray),
                                     'source_pending_vendor': len(source_pending['data']),
                                     'source_publish_vendor': len(source_publish),
                                     'source_closed_vendor': len(deadlinearray),
                                     'source_award_vendor': len(sourceaward),
                                     'rfq_publish_pending_vendor': len(totalopenbidlist['data']),
                                     'rfq_closed_bid_vendor': len(closedrfqlist['data']),
                                     'published_leads_vendor': len(publishedobj['data']),
                                     'reject_leads_vendor': len(rejectedobj),
                                     'awarded_vendor': len(vendorsaward['data']),
                                     'award_pending_vendor': award_pending,
                                     'confirmed_purchase_order_vendor_vendor': len(purchaserodervendorslist['data']),
                                     'pending_po_vendor': pending_po,
                                     'business_invite_count_vendor': len(inviteobj),
                                     'businesss_request_list_vendor': len(businessrequestlist['data']),
                                     'business_connections_vendor': len(businessconnections['data']),
                                     'invites_approved_vendor':len(businessacceptlist['data']),
                                     })

        return Response({'status': 200, 'message': 'ok', 'data': totalvendorarray}, status=200)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def update_invite_vendor_registration_status(request):
    data=request.data
    emailarray=data['emailarray']
    regarray=[]
    try:
        regobj = SelfRegistration.objects.filter().values()
        for i in range(0,len(regobj)):
            regarray.append(regobj[i].get('username'))
        inviteobj=InviteVendor.objects.filter(email_id__in=emailarray).values()
        if len(inviteobj)>0:
            for i in range(0,len(inviteobj)):
                # if inviteobj[i].get('email_id') in regarray:
                inviteval=InviteVendor.objects.get(email_id=inviteobj[i].get('email_id'))
                if inviteval.email_id==regarray:
                    print('ssssssss')
                # if inviteval.registration_status=='Not Registered':
                #     inviteval.registration_status='Registered'
                #     inviteval.save()
            return Response({'status': 200, 'message': 'Registration Status Updated'}, status=200)
        else:
            return Response({'status': 204, 'message': 'Users are not invited'}, status=204)



    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def deleteinternalvendor(request):
    data=request.data
    try:
        intvendoridarray=data['internalvendorid']
        for i in range(0,len(intvendoridarray)):
            print(intvendoridarray[i])
            intrnavendorobj=InternalVendor.objects.get(internal_vendor_id=intvendoridarray[i])
            intrnavendorobj.delete()

        return Response({'status': 200, 'message': 'Internal Users are deleted'}, status=200)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

class TrailVendorsView(viewsets.ModelViewSet):
    # permission_classes = [permissions.AllowAny]
    queryset = TrailVendors.objects.all()
    serializer_class =TrailVendorsSerializer

    def create(self, request, *args, **kwargs):
        trailarray=request.data['trailarray']
        arraytrail=[]
        try:
            trailobj = TrailVendors.objects.filter(updated_by=request.data['updated_by']).values()
            for i in range(0, len(trailobj)):
                arraytrail.append(trailobj[i].get('company_code_id'))
            print(arraytrail)
            for i in range(0,len(trailarray)):
                if trailarray[i] not in arraytrail:
                    trailobj=TrailVendors.objects.create(company_code=BasicCompanyDetails.objects.get(company_code=trailarray[i]),
                                                         created_by=request.data['created_by'],
                                                          updated_by=SelfRegistration.objects.get(id=request.data['updated_by'])
                                                             )
                else:
                    print('already present')
            return Response({'status': 201, 'message': 'Trail Vendors Created'}, status=201)

        except Exception as e:
            return Response({'status':500,'error':str(e)},status=500)

    def get_queryset(self):
        trailobj = TrailVendors.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if not trailobj:
            raise ValidationError({'message': 'Trail Vendor Details are not found', 'status': 204})
        return trailobj




@api_view(['post'])
def trail_vendor_data_based_on_userid(request):
    data=request.data
    user_id = data['user_id']
    data3=[]
    try:
        data1 = TrailVendors.objects.filter(updated_by=user_id).values()
        for i in range(0, len(data1)):
            cmp_code_name_gst= BasicCompanyDetails.objects.filter(company_code=data1[i].get('company_code_id')).values()
            ind_serve_nature_business=IndustrialInfo.objects.filter(company_code=data1[i].get('company_code_id')).values()
            city_state=BillingAddress.objects.filter(company_code=data1[i].get('company_code_id')).values()
            if cmp_code_name_gst :
                data3.append({'company_code': cmp_code_name_gst[0].get('company_code'),
                            'company_name': cmp_code_name_gst[0].get('company_name'),
                            'city': city_state[0].get('bill_city'),
                            'state': city_state[0].get('bill_state'),
                            'indurstry_to_serve': ind_serve_nature_business[0].get('industry_to_serve'),
                            'nature_of_business': ind_serve_nature_business[0].get('nature_of_business'),
                            'gst_number': cmp_code_name_gst[0].get('gst_number'),
                              })
        return Response({'status': 200, 'message': 'ok','trail_vendor_data':data3,}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)