import math
import urllib
from itertools import chain

import requests
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from MastersApp.models import MaincoreMaster
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
        intobj = InternalVendor.objects.filter(updated_by=data['updated_by']).values()
        return Response({'status': 200, 'data': intobj}, status=200)

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
        regobj=SelfRegistration.objects.filter(admin_approve='Approved').values().order_by('id')
        if len(regobj)>0:
            for i in range(0,len(regobj)):
                basicobj=BasicCompanyDetails.objects.get(updated_by_id=regobj[i].get('id'))
                industryobj=IndustrialInfo.objects.get(updated_by_id=regobj[i].get('id'),company_code=basicobj.company_code)
                print(industryobj.company_code_id,'indsutry')
                hierarchyobj = IndustrialHierarchy.objects.get(updated_by_id=regobj[i].get('id'))
                billingobj=BillingAddress.objects.filter(updated_by_id=regobj[i].get('id')).values()
                externalarray.append({'company_code':basicobj.company_code,
                                      'company_name':basicobj.company_name,
                                      'nature_of_business':industryobj.nature_of_business,
                                      'industry_to_serve': industryobj.industry_to_serve,
                                      'maincore': hierarchyobj.maincore,
                                      'category': hierarchyobj.category,
                                      'subcategory': hierarchyobj.subcategory,
                                      'bill_city': billingobj[0].get('bill_city'),
                                      'bill_state': billingobj[0].get('bill_state'),

                                      })


            return Response({'status': 200, 'message': 'External Vendor List', 'data': externalarray},status=200)

        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=204)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)





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
@permission_classes([AllowAny, ])
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
                    'maincore').lower() and category.lower() in valuearray[i].get('category').lower() and subcategory.lower() in valuearray[i].get('subcategory').lower() and bill_city.lower() in valuearray[i].get(
                'bill_city').lower() and bill_state.lower() in valuearray[i].get('bill_state').lower() and \
                    nature_of_business.lower() in valuearray[i].get(
                'nature_of_business').lower() and industry_to_serve.lower() in valuearray[i].get(
                'industry_to_serve').lower() and company_name.lower() in valuearray[i].get('company_name').lower():
                externalarraysearch.append(valuearray[i])
            else:
                print('Not Present')
        return Response({'status': 200, 'message': 'ok', 'data': externalarraysearch}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
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
                                               updated_by=SelfRegistration.objects.get(id=userid))

            return Response({'status': 200, 'message': 'ok'}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def sendergetbuzrequestdata(request):
    data = request.data
    userid = data['userid']
    businessrequestarray=[]
    try:
        buzobj = BusinessRequest.objects.filter(updated_by=userid).order_by('company_code').values()
        for i in range(0,len(buzobj)-1):
            print(i)
            if buzobj[i].get('company_code')==buzobj[i+1].get('company_code'):
                pass
            else:
                businessrequestarray.append({'company_code':buzobj[i].get('company_code'),
                                             'company_name':buzobj[i].get('company_name'),
                                             'city':buzobj[i].get('city'),
                                             'state':buzobj[i].get('state'),
                                             'nature_of_business':buzobj[i].get('nature_of_business'),
                                             'supply_capabilites':buzobj[i].get('supply_capabilites'),
                                             'industry_to_serve':buzobj[i].get('industry_to_serve'),
                                             'maincore':buzobj[i].get('maincore'),
                                             'category':buzobj[i].get('category'),
                                             'sub_category':buzobj[i].get('sub_category'),
                                             'send_status':buzobj[i].get('send_status'),
                                             'created_by':buzobj[i].get('created_by'),
                                             'updated_by':buzobj[i].get('updated_by')

                                             })

        businessrequestarray.append(buzobj[len(buzobj)-1])
        return Response({'status': 200, 'message': 'ok', 'data': businessrequestarray}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def buzrequest(request):
    data = request.data
    userbuzdata = []

    try:
        basiccompoobj = BasicCompanyDetails.objects.get(updated_by_id=data['userid'])
        print(basiccompoobj.company_code)
        businessrequest=BusinessRequest.objects.filter(company_code=basiccompoobj.company_code).values().order_by('id')
        if len(businessrequest)>0:
            for i in range(0,len(businessrequest)):
                regobj=SelfRegistration.objects.filter(id=businessrequest[i].get('updated_by_id')).values()
                # print(regobj[0].get('id'))
                basival = BasicCompanyDetails.objects.get(updated_by_id=businessrequest[i].get('updated_by_id'))
                print(basival.updated_by_id,'ds')
                industryinfoobj = IndustrialInfo.objects.filter(company_code_id=basival.company_code).values()
                billsaddrsobj = BillingAddress.objects.filter(company_code_id=basival.company_code,updated_by_id=businessrequest[i].get('updated_by_id')).values()
                if not billsaddrsobj:
                    states=""
                    city=""
                    userbuzdata.append({'profile_photo': regobj[0].get('profile_cover_photo'),
                                        'ccode': basival.company_code,
                                        'cname': basival.company_name,
                                        'gst_number': basival.gst_number,
                                        'Industry': industryinfoobj[0].get('industry_to_serve'),
                                        'natureofbuz': industryinfoobj[0].get('nature_of_business'),
                                        'business_id': businessrequest[i].get('id'),
                                        'user_id': basival.updated_by_id,
                                        'state':states,
                                        'city':city
                                        })
                else:
                    states= billsaddrsobj[0].get('bill_state')
                    city=billsaddrsobj[0].get('bill_city')
                    userbuzdata.append({'profile_photo': regobj[0].get('profile_cover_photo'),
                                        'ccode': basival.company_code,
                                        'cname': basival.company_name,
                                        'gst_number': basival.gst_number,
                                        'Industry': industryinfoobj[0].get('industry_to_serve'),
                                        'natureofbuz': industryinfoobj[0].get('nature_of_business'),
                                        'business_id': businessrequest[i].get('id'),
                                        'user_id': basival.updated_by_id,
                                        'state': states,
                                        'city': city
                                        })
            return Response({'status':200,'message':'ok','data':userbuzdata},status=200)
        else:
            return Response({'status': 204, 'message': 'Company code not present in busines request'}, status=204)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
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
@permission_classes((AllowAny,))
def search_business_request_advance_search(request):
    # business request advance search
    data = request.data
    company_code = data['company_code']
    company_name = data['company_name']
    state = data['state']
    industry_to_serve = data['industry_to_serve']
    nature_of_business = data['nature_of_business']
    send_status=data['send_status']
    serveappend = []
    try:
        serveappend.append(industry_to_serve)
        businessrequestadvancesearch = BusinessRequest.objects.filter(updated_by=data['userid']).filter(
            company_code__icontains=company_code).filter(company_name__icontains=company_name).filter(state__icontains=state).filter(industry_to_serve__contains=serveappend).filter(nature_of_business__0__icontains=nature_of_business).filter(send_status__icontains=send_status).values()

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

