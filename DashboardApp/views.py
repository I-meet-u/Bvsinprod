import math
import urllib

import requests
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

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


