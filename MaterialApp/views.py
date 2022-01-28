from datetime import datetime, date
from itertools import chain

from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from LandingPageApp.models import CompanyReviewAndRating
from MastersApp.models import CategoryMaster, MaincoreMaster, SubCategoryMaster
from RegistrationApp.models import SelfRegistration, IndustrialInfo, BillingAddress, BasicCompanyDetails, \
    IndustrialHierarchy
from .models import *
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from .serializers import *


class VendorProduct_GeneralDetailsView(viewsets.ModelViewSet):
    queryset = VendorProduct_GeneralDetails.objects.all()
    serializer_class = VendorProduct_GeneralDetailsSerializer




class VendorProduct_TechnicalSpecificationsView(viewsets.ModelViewSet):
    queryset = VendorProduct_TechnicalSpecifications.objects.all()
    serializer_class = VendorProduct_TechnicalSpecificationsSerialzer


    def create(self, request, *args, **kwargs):
        technicaldetailslist = request.data['technicaldetails']
        updated_by = request.data.get('updated_by',None)
        vendor_products=request.data.get('vendor_products',None)
        try:
            if updated_by is None:
                return Response({'status': 204, 'message': 'Enter user id or user id not exist'}, status=204)
            for i in range(0, len(technicaldetailslist)):
                VendorProduct_TechnicalSpecifications.objects.create(item_specification=technicaldetailslist[i].get('item_specification'),
                                                                      item_description=technicaldetailslist[i].get('item_description'),
                                                                      vendor_products=VendorProduct_BasicDetails.objects.get(vendor_product_id=vendor_products),
                                                                      updated_by=SelfRegistration.objects.get(id=updated_by),
                                                                      created_by=updated_by)
            return Response({'status': 201, 'message': 'Vendor Product Technical Specifications Are Added'}, status=201)
        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)

class VendorProduct_ProductFeaturesView(viewsets.ModelViewSet):
    queryset = VendorProduct_ProductFeatures.objects.all()
    serializer_class = VendorProduct_ProductFeaturesSerializer

    def create(self, request, *args, **kwargs):
        productfeatureslist = request.data['productfeatureslist']
        updated_by = request.data.get('updated_by',None)
        vendor_products = request.data.get('vendor_products', None)
        try:
            if updated_by is None:
                return Response({'status':204,'message':'Enter user id or user id not exist'},status=204)
            for i in range(0, len(productfeatureslist)):
                VendorProduct_ProductFeatures.objects.create(
                    product_item_specification=productfeatureslist[i].get('product_item_specification'),
                    product_item_description=productfeatureslist[i].get('product_item_description'),
                    vendor_products=VendorProduct_BasicDetails.objects.get(vendor_product_id=vendor_products),
                    updated_by=SelfRegistration.objects.get(id=updated_by),
                    created_by=updated_by
                )
            return Response({'status': 201, 'message': 'Vendor Product Features Are Added'}, status=201)
        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)



class VendorProduct_DocumentsView(viewsets.ModelViewSet):
    queryset = VendorProduct_Documents.objects.all()
    serializer_class = VendorProduct_DocumentsSerializer
    parser_classes = [MultiPartParser]

class ItemCodeSettingsView(viewsets.ModelViewSet):
    # permission_classes = [permissions.AllowAny]
    queryset = ItemCodeSettings.objects.all()
    serializer_class = ItemCodeSettingsSerializer
    ordering = ['id']

    def create(self, request, *args, **kwargs):
        item_type = request.data.get('item_type',None)
        prefix = request.data.get('prefix',None)
        numeric = request.data.get('numeric',None)
        suffix = request.data.get('suffix',None)
        userid=request.data.get('userid',None)
        try:
            code_format=prefix+suffix+str(numeric)
            request.data['code_format']=code_format
            request.data['updated_by']=userid
            request.data['created_by']=userid
            return super().create(request, *args, **kwargs)

        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)

    def get_queryset(self):
        itemcodeobj=ItemCodeSettings.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if itemcodeobj:
            return itemcodeobj
        raise ValidationError({'message':'Item Code details of particular user id is not exist','status':204})



@api_view(['post'])
# @permission_classes((AllowAny,))
def get_itemtype_based_on_userid(request):
    data=request.data
    userid=data['userid']
    itemtype=data['itemtype']
    try:
        if itemtype=='Product':
            productobj=BuyerProductDetails.objects.filter(updated_by=userid,buyer_item_type=itemtype,buyer_product_status="Active").values().order_by('buyer_product_id')
            if len(productobj)>0:
                return Response({'status': 200, 'message': 'Buyer Product List','data':productobj}, status=200)
            else:
                return Response({'status': 202, 'message': 'Not Present'}, status=202)

        elif itemtype == 'Service':
            productobjservice = BuyerServiceDetails.objects.filter(updated_by=userid,
                                                            buyer_service_item_type=itemtype,buyer_service_status='Active').values().order_by('buyer_service_id')
            if len(productobjservice)>0:
                return Response({'status': 200, 'message': 'Buyer Service List', 'data': productobjservice}, status=200)
            else:
                return Response({'status': 202, 'message': 'Not Present'}, status=202)
        elif itemtype == 'Machinary & equipments':
            productobjmachinary = BuyerMachinaryDetails.objects.filter(updated_by=userid,
                                                                   buyer_machinary_item_type=itemtype,buyer_machinary_product_status='Active').values().order_by('buyer_machinary_id')
            if len(productobjmachinary)>0:
                return Response({'status': 200, 'message': 'Buyer Machinary List', 'data': productobjmachinary}, status=200)
            else:
                return Response({'status': 202, 'message': 'Not Present'}, status=202)
        else:
            return Response({'status': 204, 'error':'Not present or itemtype is wrong','data':[]}, status=204)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
# @permission_classes((AllowAny,))
def item_code_settings_list(request):
    data=request.data
    userid=data['userid']
    itemtype=data['itemtype']
    try:
        itemcodeobj=ItemCodeSettings.objects.filter(updated_by=userid).values().order_by('id')
        if len(itemcodeobj)>0:
            if itemtype == 'Product':
                itemcodeobjproduct= ItemCodeSettings.objects.filter(updated_by=userid, item_type=itemtype).values().order_by('id')
                return Response({'status': 200, 'message': 'Product Item Code', 'data':itemcodeobjproduct}, status=200)
            elif itemtype=='Service':
                itemcodeobjservice = ItemCodeSettings.objects.filter(updated_by=userid, item_type=itemtype).values().order_by('id')
                return Response({'status': 200, 'message': 'Service Item Code', 'data': itemcodeobjservice}, status=200)

            elif itemtype=='Machinery_and_Equipments':
                itemcodeobjmachinary = ItemCodeSettings.objects.filter(updated_by=userid, item_type=itemtype).values().order_by('id')
                return Response({'status': 200, 'message': 'Machinary Item Code', 'data': itemcodeobjmachinary}, status=200)

            else:
                return Response({'status': 204, 'error':'Not present or itemtype is wrong','data':[]}, status=204)
        else:
            return Response({'status': 202, 'error': 'Data Not Present For this user id'}, status=202)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

#-----------------------------------------------------------------------
@api_view(['put'])
# @permission_classes([AllowAny,])
def disable_buyer_product(request):
    # disable buyer product by changing status from Active to Disabled by passing primary key(buyerproductid)
    data=request.data
    itemtype=data['itemtype']

    try:
        if itemtype=='Product':
            buyerproductid = data['buyerproductid']
            userid = data['userid']
            buyerproductobj=BuyerProductDetails.objects.filter(buyer_product_id__in=buyerproductid,buyer_item_type=itemtype,updated_by_id=userid).values()
            if len(buyerproductobj)>0:
                for i in range(0,len(buyerproductobj)):
                    buyerproductobjget=BuyerProductDetails.objects.get(buyer_product_id=buyerproductobj[i].get('buyer_product_id'))
                    if buyerproductobjget.buyer_product_status=='Active':
                        buyerproductobjget.buyer_product_status='Disabled'
                        buyerproductobjget.save()
                    else:
                        return Response({'status': 202, 'message': 'Already status disabled'},status=202)
                return Response({'status':200,'message':'Buyer Product Master status changed to disabled'},status=200)
            else:
                return Response({'status': 424, 'message': 'Not Present'},
                                status=424)
        elif itemtype=='Service':
            buyerserviceid = data['buyerserviceid']
            userid = data['userid']
            buyerserviceobj = BuyerServiceDetails.objects.filter(buyer_service_id__in=buyerserviceid,buyer_service_item_type=itemtype,updated_by_id=userid).values()
            if len(buyerserviceobj) > 0:
                for i in range(0, len(buyerserviceobj)):
                    buyerserviceobjget = BuyerServiceDetails.objects.get(
                        buyer_service_id=buyerserviceobj[i].get('buyer_service_id'))
                    if buyerserviceobjget.buyer_service_status == 'Active':
                        buyerserviceobjget.buyer_service_status = 'Disabled'
                        buyerserviceobjget.save()
                    else:
                        return Response({'status': 202, 'message': 'Already status disabled'}, status=202)
                return Response({'status': 200, 'message': 'Buyer Service Master status changed to disabled'},
                                status=200)
            else:
                return Response({'status': 424, 'message': 'Not Present'},status=424)
        elif itemtype=='Machinary & equipments':
            buyermachinaryid = data['buyermachinaryid']
            userid = data['userid']
            buyermachinaryobj = BuyerMachinaryDetails.objects.filter(buyer_machinary_id__in=buyermachinaryid,buyer_machinary_item_type=itemtype,updated_by_id=userid).values()
            print(buyermachinaryobj)
            if len(buyermachinaryobj) > 0:
                for i in range(0, len(buyermachinaryobj)):
                    buyermachinaryget = BuyerMachinaryDetails.objects.get(
                        buyer_machinary_id=buyermachinaryobj[i].get('buyer_machinary_id'))
                    if buyermachinaryget.buyer_machinary_product_status == 'Active':
                        buyermachinaryget.buyer_machinary_product_status = 'Disabled'
                        buyermachinaryget.save()
                    else:
                        return Response({'status': 202, 'message': 'Already status disabled'}, status=202)
                return Response({'status': 200, 'message': 'Buyer Machinary Master status changed to disabled'},
                                status=200)
            else:
                return Response({'status': 204, 'message': 'Not exist'}, status=204)
        else:
            return Response({'status':424,'message':'Please enter item type propery or mis-spelled item type'},status=424)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)



@api_view(['put'])
# @permission_classes([AllowAny,])
def enable_buyer_product(request):
    # enable buyer product by changing status from Disabled to Active by passing primary key(buyerproductid)
    data=request.data
    itemtype=data['itemtype']
    try:
        if itemtype=='Product':
            buyerproductid = data['buyerproductid']
            userid=data['userid']

            buyerproductobj=BuyerProductDetails.objects.filter(buyer_product_id__in=buyerproductid,buyer_item_type=itemtype,updated_by_id=userid).values()
            if len(buyerproductobj)>0:
                for i in range(0,len(buyerproductobj)):
                    buyerproductobjget=BuyerProductDetails.objects.get(buyer_product_id=buyerproductobj[i].get('buyer_product_id'))
                    if buyerproductobjget.buyer_product_status=='Disabled':
                        buyerproductobjget.buyer_product_status='Active'
                        buyerproductobjget.save()
                    else:
                        return Response({'status': 202, 'message': 'Already status enabled'},status=202)
                return Response({'status':200,'message':'Buyer Product Master status changed to enabled'},status=200)
            else:
                return Response({'status': 204, 'message': 'Not exist'}, status=204)
        elif itemtype=='Service':
            buyerserviceid = data['buyerserviceid']
            userid = data['userid']

            buyerserviceobj = BuyerServiceDetails.objects.filter(buyer_service_id__in=buyerserviceid,
                                                                 buyer_service_item_type=itemtype,
                                                                 updated_by_id=userid).values()
            if len(buyerserviceobj)>0:
                for i in range(0, len(buyerserviceobj)):
                    buyerserviceobjget = BuyerServiceDetails.objects.get(
                        buyer_service_id=buyerserviceobj[i].get('buyer_service_id'))
                    if buyerserviceobjget.buyer_service_status == 'Disabled':
                        buyerserviceobjget.buyer_service_status = 'Active'
                        buyerserviceobjget.save()
                    else:
                        return Response({'status': 202, 'message': 'Already status enabled'}, status=202)
                return Response({'status': 200, 'message': 'Buyer Service  Master status changed to enabled'},
                                status=200)
            else:
                return Response({'status': 204, 'message': 'Not exist'}, status=204)
        elif itemtype=='Machinary & equipments':
            buyermachinaryid = data['buyermachinaryid']
            userid = data['userid']

            buyermachinaryobj =  BuyerMachinaryDetails.objects.filter(buyer_machinary_id__in=buyermachinaryid,
                                                                 buyer_machinary_item_type=itemtype,
                                                                 updated_by_id=userid).values()
            if len(buyermachinaryobj)>0:
                for i in range(0, len(buyermachinaryobj)):
                    buyermachinaryobjget = BuyerMachinaryDetails.objects.get(
                        buyer_machinary_id=buyermachinaryobj[i].get('buyer_machinary_id'))
                    if buyermachinaryobjget.buyer_machinary_product_status == 'Disabled':
                        buyermachinaryobjget.buyer_machinary_product_status = 'Active'
                        buyermachinaryobjget.save()
                    else:
                        return Response({'status': 202, 'message': 'Already status enabled'}, status=202)
                return Response({'status': 200, 'message': 'Buyer Machinary  Master status changed to enabled'},
                                status=200)
            else:
                return Response({'status': 204, 'message': 'Not exist'}, status=204)
        else:
            return Response({'status':424,'message':'Item type is mispelled, Please check itemtype'},status=424)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)




@api_view(['post'])
# @permission_classes([AllowAny,])
def delete_buyer_product(request):
    # delete buyer_product  by passing primary key(buyerproductid)
    data = request.data
    itemtype=data['itemtype']
    try:
        if itemtype=='Product':
            buyerproductid = data['buyerproductid']
            userid=data['userid']
            buyerproductobj = BuyerProductDetails.objects.filter(buyer_product_id__in=buyerproductid,buyer_item_type=itemtype,updated_by_id=userid).values()
            if len(buyerproductobj)>0:
                for i in range(0, len(buyerproductobj)):
                    buyerproductobjget = BuyerProductDetails.objects.get(buyer_product_id=buyerproductobj[i].get('buyer_product_id'))
                    if buyerproductobjget:
                        buyerproductobjget.delete()

                return Response({'status': 204, 'message': 'Buyer Product Master data deleted'}, status=204)
            else:
                return Response({'status':200,'message':'Buyer Product Master data not present or already deleted'},status=200)
        elif itemtype=='Service':
            buyerserviceid = data['buyerserviceid']
            userid=data['userid']
            buyerserviceobj = BuyerServiceDetails.objects.filter(buyer_service_id__in=buyerserviceid,buyer_service_item_type=itemtype,updated_by_id=userid).values()
            if len(buyerserviceobj)>0:
                for i in range(0, len(buyerserviceobj)):
                    buyerserviceobjget = BuyerServiceDetails.objects.get(buyer_service_id=buyerserviceobj[i].get('buyer_service_id'))
                    if buyerserviceobjget:
                        buyerserviceobjget.delete()

                return Response({'status': 204, 'message': 'Buyer Service Master data deleted'}, status=204)
            else:
                return Response({'status':200,'message':'Buyer Service Master data not present or already deleted'},status=200)
        elif itemtype=='Machinary & equipments':
            buyermachinaryid = data['buyermachinaryid']
            userid=data['userid']
            buyermachinaryobj = BuyerMachinaryDetails.objects.filter(buyer_machinary_id__in=buyermachinaryid,buyer_machinary_item_type=itemtype,updated_by_id=userid).values()
            if len(buyermachinaryobj)>0:
                for i in range(0, len(buyermachinaryobj)):
                    buyermachinaryobjget = BuyerMachinaryDetails.objects.get(buyer_machinary_id=buyermachinaryobj[i].get('buyer_machinary_id'))
                    if buyermachinaryobjget:
                        buyermachinaryobjget.delete()

                return Response({'status': 204, 'message': 'Buyer Machinary Master data deleted'}, status=204)
            else:
                return Response({'status':200,'message':'Buyer Machinary Master data not present or already deleted'},status=200)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


class VendorProduct_BasicDetailsView(viewsets.ModelViewSet):
    # permission_classes = [permissions.AllowAny]
    queryset = VendorProduct_BasicDetails.objects.all()
    serializer_class = VendorProduct_BasicDetailsSerializer
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        vendorproductobj = VendorProduct_BasicDetails.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by('vendor_product_id')
        if vendorproductobj:
            return vendorproductobj
        raise ValidationError({'message': 'Vendor Product Details Not Present', 'status': 204})



@api_view(['put'])
# @permission_classes((AllowAny,))
def updated_item_code_settings_and_item_code(request):
    data=request.data
    userid=data['userid']
    prefix=data['prefix']
    suffix=data['suffix']
    numeric=data['numeric']
    itemtype=data['itemtype']
    try:
        itemcodesettingsobj=ItemCodeSettings.objects.filter(updated_by=userid,item_type=itemtype).order_by('-id').values()
        if len(itemcodesettingsobj)>0:
            itemcodeobj=ItemCodeSettings.objects.get(updated_by=userid,id=itemcodesettingsobj[0].get('id'))
            if itemcodeobj.prefix !=prefix:
                itemcodeobj.prefix=prefix
                itemcodeobj.save()
            if itemcodeobj.suffix!=suffix:
                itemcodeobj.suffix=suffix
                itemcodeobj.save()

            if itemcodeobj.numeric!=numeric:
                itemcodeobj.numeric=numeric
                itemcodeobj.save()

                value = itemcodeobj.prefix + itemcodeobj.suffix + itemcodeobj.numeric
                itemcodeobj.code_format=value
                itemcodeobj.save()


            if itemtype=='Product':
                itemcodeobj1=BuyerProductDetails.objects.filter(updated_by_id=userid,buyer_item_type=itemtype).order_by('-buyer_product_id').values()
                if len(itemcodeobj1)>0:
                    itemvalue=BuyerProductDetails.objects.get(buyer_product_id=itemcodeobj1[0].get('buyer_product_id'),updated_by_id=itemcodeobj1[0].get('updated_by_id'))
                    print(itemvalue.buyer_product_id)
                    if itemvalue.buyer_item_code!=itemcodeobj.prefix+itemcodeobj.suffix+itemcodeobj.numeric:
                        itemvalue.buyer_item_code=itemcodeobj.prefix+itemcodeobj.suffix+itemcodeobj.numeric
                        itemvalue.save()
                    if itemvalue.buyer_numeric!=itemcodeobj.numeric:
                        itemvalue.buyer_numeric=int(itemcodeobj.numeric)+1
                        itemvalue.save()

                    if itemvalue.buyer_prefix !=itemcodeobj.prefix:
                        itemvalue.buyer_prefix=itemcodeobj.prefix
                        itemvalue.save()

                    if itemvalue.buyer_suffix != itemcodeobj.suffix:
                        itemvalue.buyer_suffix = itemcodeobj.suffix
                        itemvalue.save()

                    return Response({'status':202,'message':'Buyer item code for product and item Code Settings for Product are Updated'},status=202)

                else:
                    return Response({'status': 200, 'message': 'Buyer Product Not Present'}, status=200)
            elif itemtype=='Service':
                itemcodeobjservice = BuyerServiceDetails.objects.filter(updated_by_id=userid,
                                                                  buyer_service_item_type=itemtype).order_by('-buyer_service_id').values()
                if len(itemcodeobjservice) > 0:
                    itemvalue = BuyerServiceDetails.objects.get(buyer_service_id=itemcodeobjservice[0].get('buyer_service_id'),
                        updated_by_id=itemcodeobjservice[0].get('updated_by_id'))
                    print(itemvalue.buyer_service_id)
                    if itemvalue.buyer_service_item_code != itemcodeobj.prefix+itemcodeobj.suffix+itemcodeobj.numeric:
                        itemvalue.buyer_service_item_code = itemcodeobj.prefix+itemcodeobj.suffix+itemcodeobj.numeric
                        itemvalue.save()
                    if itemvalue.buyer_service_numeric != itemcodeobj.numeric:
                        itemvalue.buyer_service_numeric = int(itemcodeobj.numeric) + 1
                        itemvalue.save()

                    if itemvalue.buyer_service_prefix != itemcodeobj.prefix:
                        itemvalue.buyer_service_prefix = itemcodeobj.prefix
                        itemvalue.save()

                    if itemvalue.buyer_service_suffix != itemcodeobj.suffix:
                        itemvalue.buyer_service_suffix = itemcodeobj.suffix
                        itemvalue.save()
                    return Response({'status': 202,
                                     'message': 'Buyer item code for service and item Code Settings for Service are Updated'},status=202)

                else:
                    return Response({'status': 200, 'message': 'Buyer Service Not Present'}, status=200)

            else:
                if itemtype=='Machinary & equipments':
                    itemcodeobjmachinary = BuyerMachinaryDetails.objects.filter(updated_by_id=userid,
                                                                      buyer_machinary_item_type=itemtype).order_by('-buyer_machinary_id').values()
                    if len(itemcodeobjmachinary) > 0:
                        itemvalue = BuyerMachinaryDetails.objects.get(buyer_machinary_id=itemcodeobjmachinary[0].get('buyer_machinary_id'),updated_by_id=itemcodeobjmachinary[0].get('updated_by_id'))
                        print(itemvalue.buyer_machinary_id)
                        if itemvalue.buyer_machinary_item_code != itemcodeobj.prefix+itemcodeobj.suffix+itemcodeobj.numeric:
                            itemvalue.buyer_machinary_item_code = itemcodeobj.prefix+itemcodeobj.suffix+itemcodeobj.numeric
                            itemvalue.save()
                        if itemvalue.buyer_machinary_numeric != itemcodeobj.numeric:
                            itemvalue.buyer_machinary_numeric = int(itemcodeobj.numeric) + 1
                            itemvalue.save()

                        if itemvalue.buyer_machinary_prefix != itemcodeobj.prefix:
                            itemvalue.buyer_machinary_prefix = itemcodeobj.prefix
                            itemvalue.save()

                        if itemvalue.buyer_machinary_suffix != itemcodeobj.suffix:
                            itemvalue.buyer_machinary_suffix = itemcodeobj.suffix
                            itemvalue.save()
                        return Response({'status': 202,
                                         'message': 'Buyer item code for machinary and item Code Settings for Machinary are Updated'},status=202)

                    else:
                        return Response({'status': 200, 'message': 'Buyer Machinary Not Present'}, status=200)


        else:
            return Response({'status':204,'message':'Item Code Settings data for this user id is not present'},status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['post'])
# @permission_classes((AllowAny,))
def get_item_code_details_by_userid_itemtype(request):
    data=request.data
    item_type=data['item_type']
    userid=data['userid']
    try:
        itemcodeobj=ItemCodeSettings.objects.filter(updated_by_id=userid,item_type=item_type).values()
        if itemcodeobj:
            return Response({'status': 200, 'message': 'Item Code Settings Based on Item Type Success','data':itemcodeobj}, status=200)
        else:
            return Response({'status': 204, 'message': 'Data No Present for this item type and user'}, status=204)



    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)






class BuyerProductDetailsView(viewsets.ModelViewSet):
    # permission_classes = [permissions.AllowAny]
    queryset = BuyerProductDetails.objects.all()
    serializer_class = BuyerProductDetailsSerializer
    # parser_classes = (MultiPartParser,)
    ordering_fields = ['buyer_product_id']
    ordering = ['buyer_product_id']


    def create(self, request, *args, **kwargs):
        buyer_item_type=request.data.get('buyer_item_type',None)
        buyer_item_name=request.data.get('buyer_item_name',None)
        buyer_item_description=request.data.get('buyer_item_description',None)
        buyer_uom=request.data.get('buyer_uom',None)
        buyer_hsn_sac = request.data.get('buyer_hsn_sac',None)
        buyer_unit_price = request.data.get('buyer_unit_price',None)
        buyer_category = request.data.get('buyer_category',None)
        buyer_department = request.data.get('buyer_department',None)
        buyer_item_group = request.data.get('buyer_item_group',None)
        buyer_annual_consumption = request.data.get('buyer_annual_consumption',None)
        buyer_safety_stock = request.data.get('buyer_safety_stock',None)
        buyer_model_no = request.data.get('buyer_model_no',None)
        buyer_document = request.data.get('buyer_document',None)
        buyer_document_1 = request.data.get('buyer_document_1', None)
        buyer_document_2 = request.data.get('buyer_document_2', None)
        buyer_additional_specifications = request.data.get('buyer_additional_specifications',None)
        buyer_add_product_supplies = request.data.get('buyer_add_product_supplies',None)
        custom_code=request.data.get('custom_code',None)
        userid = request.data.get('userid',None)
        try:
            itemcodesettingsobj = ItemCodeSettings.objects.filter(updated_by=userid,item_type='Product').order_by('-id').values()
            if len(itemcodesettingsobj) > 0:
                buyerproductobj = BuyerProductDetails.objects.filter(updated_by=userid).order_by('-buyer_numeric').values()
                if len(buyerproductobj)==0:
                    print("data not exist")
                    buyerobj = BuyerProductDetails.objects.create(buyer_item_type=buyer_item_type,
                                                                  buyer_prefix=itemcodesettingsobj[0].get('prefix'),
                                                                  buyer_suffix=itemcodesettingsobj[0].get('suffix'),
                                                                  buyer_numeric=str(int(itemcodesettingsobj[0].get('numeric')) + 1),
                                                                  buyer_item_code=itemcodesettingsobj[0].get(
                                                                      'code_format'),
                                                                  buyer_item_name=buyer_item_name,
                                                                  buyer_item_description=buyer_item_description,
                                                                  buyer_uom=buyer_uom,
                                                                  buyer_hsn_sac=buyer_hsn_sac,
                                                                  buyer_unit_price=buyer_unit_price,
                                                                  buyer_category=buyer_category,
                                                                  buyer_department=buyer_department,
                                                                  buyer_item_group=buyer_item_group,
                                                                  buyer_annual_consumption=buyer_annual_consumption,
                                                                  buyer_safety_stock=buyer_safety_stock,
                                                                  buyer_model_no=buyer_model_no,
                                                                  buyer_document=buyer_document,
                                                                  buyer_document_1=buyer_document_1,
                                                                  buyer_document_2=buyer_document_2,
                                                                  buyer_additional_specifications=buyer_additional_specifications,
                                                                  buyer_add_product_supplies=buyer_add_product_supplies,
                                                                  updated_by=SelfRegistration.objects.get(id=userid),
                                                                  created_by=userid,
                                                                  custom_code=custom_code
                                                                  )
                else:
                    buyerobj = BuyerProductDetails.objects.create(buyer_item_type=buyer_item_type,
                                                                  buyer_prefix=buyerproductobj[0].get('buyer_prefix'),
                                                                  buyer_suffix=buyerproductobj[0].get('buyer_suffix'),
                                                                  buyer_numeric=int(buyerproductobj[0].get('buyer_numeric')) + 1,
                                                                  buyer_item_code=buyerproductobj[0].get('buyer_prefix') + buyerproductobj[0].get('buyer_suffix')+buyerproductobj[0].get('buyer_numeric'),
                                                                  buyer_item_name=buyer_item_name,
                                                                  buyer_item_description=buyer_item_description,
                                                                  buyer_uom=buyer_uom,
                                                                  buyer_hsn_sac=buyer_hsn_sac,
                                                                  buyer_unit_price=buyer_unit_price,
                                                                  buyer_category=buyer_category,
                                                                  buyer_department=buyer_department,
                                                                  buyer_item_group=buyer_item_group,
                                                                  buyer_annual_consumption=buyer_annual_consumption,
                                                                  buyer_safety_stock=buyer_safety_stock,
                                                                  buyer_model_no=buyer_model_no,
                                                                  buyer_document=buyer_document,
                                                                  buyer_document_1=buyer_document_1,
                                                                  buyer_document_2=buyer_document_2,
                                                                  buyer_additional_specifications=buyer_additional_specifications,
                                                                  buyer_add_product_supplies=buyer_add_product_supplies,
                                                                  updated_by=SelfRegistration.objects.get(id=userid),
                                                                  created_by=userid,
                                                                  custom_code=custom_code
                                                                  )
                return Response({'status':201,'message':'Buyer Product Created'},status=201)
            else:
                return Response(
                    {'status': 204, 'message': 'Item Code Settings Not Present,Please Create Item Code in Settings'},
                    status=204)

        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)

    def get_queryset(self):
        buyerproductobj=BuyerProductDetails.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if buyerproductobj:
            return buyerproductobj
        raise ValidationError({'message':'Buyer Product Details Not Present','status':204})


class BuyerServiceDetailsView(viewsets.ModelViewSet):
    # permission_classes = [permissions.AllowAny]
    queryset = BuyerServiceDetails.objects.all()
    serializer_class = BuyerServiceDetailsSerializer
    # parser_classes = (MultiPartParser,)


    def create(self, request, *args, **kwargs):
        buyer_service_item_type=request.data.get('buyer_service_item_type',None)
        buyer_service_item_name=request.data.get('buyer_service_item_name',None)
        buyer_service_item_description=request.data.get('buyer_service_item_description',None)
        buyer_service_uom=request.data.get('buyer_service_uom',None)
        buyer_service_hsn_sac = request.data.get('buyer_service_hsn_sac',None)
        buyer_service_unit_price = request.data.get('buyer_service_unit_price',None)
        buyer_service_category = request.data.get('buyer_service_category',None)
        buyer_service_department = request.data.get('buyer_service_department',None)
        buyer_service_item_group = request.data.get('buyer_service_item_group',None)
        buyer_service_annual_consumption = request.data.get('buyer_service_annual_consumption',None)
        buyer_service_safety_stock = request.data.get('buyer_service_safety_stock',None)
        buyer_service_model_no = request.data.get('buyer_service_model_no',None)
        buyer_service_document = request.data.get('buyer_service_document',None)
        buyer_service_document_1 = request.data.get('buyer_service_document_1',None)
        buyer_service_document_2 = request.data.get('buyer_service_document_2',None)
        buyer_service_additional_specifications = request.data.get('buyer_service_additional_specifications',None)
        buyer_service_add_product_supplies = request.data.get('buyer_service_add_product_supplies',None)
        custom_code=request.data.get('custom_code',None)
        userid = request.data.get('userid',None)
        try:
            itemcodesettingsobj = ItemCodeSettings.objects.filter(updated_by=userid,item_type='Service').order_by('-id').values()
            if len(itemcodesettingsobj) > 0:
                buyerserviceobj = BuyerServiceDetails.objects.filter(updated_by=userid).order_by('-buyer_service_numeric').values()
                if len(buyerserviceobj)==0:
                    print("data not exist")
                    buyerserviceobj = BuyerServiceDetails.objects.create(buyer_service_item_type=buyer_service_item_type,
                                                                  buyer_service_prefix=itemcodesettingsobj[0].get('prefix'),
                                                                  buyer_service_suffix=itemcodesettingsobj[0].get('suffix'),
                                                                  buyer_service_numeric=int(itemcodesettingsobj[0].get('numeric')) + 1,
                                                                  buyer_service_item_code=itemcodesettingsobj[0].get('prefix')+itemcodesettingsobj[0].get('suffix')+str(itemcodesettingsobj[0].get('numeric')),
                                                                  buyer_service_item_name=buyer_service_item_name,
                                                                  buyer_service_item_description=buyer_service_item_description,
                                                                  buyer_service_uom=buyer_service_uom,
                                                                  buyer_service_hsn_sac=buyer_service_hsn_sac,
                                                                  buyer_service_unit_price=buyer_service_unit_price,
                                                                  buyer_service_category=buyer_service_category,
                                                                  buyer_service_department=buyer_service_department,
                                                                  buyer_service_item_group=buyer_service_item_group,
                                                                  buyer_service_annual_consumption=buyer_service_annual_consumption,
                                                                  buyer_service_safety_stock=buyer_service_safety_stock,
                                                                  buyer_service_model_no=buyer_service_model_no,
                                                                  buyer_service_document=buyer_service_document,
                                                                  buyer_service_document_1=buyer_service_document_1,
                                                                  buyer_service_document_2=buyer_service_document_2,
                                                                  buyer_service_additional_specifications=buyer_service_additional_specifications,
                                                                  buyer_service_add_product_supplies=buyer_service_add_product_supplies,
                                                                  updated_by=SelfRegistration.objects.get(id=userid),
                                                                  created_by=userid,
                                                                  custom_code=custom_code
                                                                         )
                else:
                    buyerserviceobj = BuyerServiceDetails.objects.create(buyer_service_item_type=buyer_service_item_type,
                                                                  buyer_service_prefix=buyerserviceobj[0].get('buyer_service_prefix'),
                                                                  buyer_service_suffix=buyerserviceobj[0].get('buyer_service_suffix'),
                                                                  buyer_service_numeric=int(buyerserviceobj[0].get('buyer_service_numeric')) + 1,
                                                                  buyer_service_item_code=buyerserviceobj[0].get('buyer_service_prefix') + buyerserviceobj[0].get('buyer_service_suffix')+buyerserviceobj[0].get('buyer_service_numeric'),
                                                                  buyer_service_item_name=buyer_service_item_name,
                                                                  buyer_service_item_description=buyer_service_item_description,
                                                                  buyer_service_uom=buyer_service_uom,
                                                                  buyer_service_hsn_sac=buyer_service_hsn_sac,
                                                                  buyer_service_unit_price=buyer_service_unit_price,
                                                                  buyer_service_category=buyer_service_category,
                                                                  buyer_service_department=buyer_service_department,
                                                                  buyer_service_item_group=buyer_service_item_group,
                                                                  buyer_service_annual_consumption=buyer_service_annual_consumption,
                                                                  buyer_service_safety_stock=buyer_service_safety_stock,
                                                                  buyer_service_model_no=buyer_service_model_no,
                                                                  buyer_service_document=buyer_service_document,
                                                                  buyer_service_document_1=buyer_service_document_1,
                                                                  buyer_service_document_2=buyer_service_document_2,
                                                                  buyer_service_additional_specifications=buyer_service_additional_specifications,
                                                                  buyer_service_add_product_supplies=buyer_service_add_product_supplies,
                                                                  updated_by=SelfRegistration.objects.get(id=userid),
                                                                  created_by=userid,
                                                                  custom_code=custom_code
                                                                         )
                return Response({'status':201,'message':'Buyer Service Created'},status=201)
            else:
                return Response(
                    {'status': 204, 'message': 'Item Code Settings Not Present for Service,Please Create Service Item Code in Settings'},
                    status=204)

        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)

    def get_queryset(self):
        buyerserviceobj=BuyerServiceDetails.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if buyerserviceobj:
            return buyerserviceobj
        raise ValidationError({'message':'Buyer Service Details Not Present','status':204})


class BuyerMachinaryDetailsView(viewsets.ModelViewSet):
    # permission_classes = [permissions.AllowAny]
    queryset = BuyerMachinaryDetails.objects.all()
    serializer_class = BuyerMachinaryDetailsSerializer
    # parser_classes = (MultiPartParser,)


    def create(self, request, *args, **kwargs):
        buyer_machinary_item_type=request.data.get('buyer_machinary_item_type',None)
        buyer_machinary_item_name=request.data.get('buyer_machinary_item_name',None)
        buyer_machinary_item_description=request.data.get('buyer_machinary_item_description',None)
        buyer_machinary_uom=request.data.get('buyer_machinary_uom',None)
        buyer_machinary_hsn_sac = request.data.get('buyer_machinary_hsn_sac',None)
        buyer_machinary_unit_price = request.data.get('buyer_machinary_unit_price',None)
        buyer_machinary_category = request.data.get('buyer_machinary_category',None)
        buyer_machinary_department = request.data.get('buyer_machinary_department',None)
        buyer_machinary_item_group = request.data.get('buyer_machinary_item_group',None)
        buyer_machinary_annual_consumption = request.data.get('buyer_machinary_annual_consumption',None)
        buyer_machinary_safety_stock = request.data.get('buyer_machinary_safety_stock',None)
        buyer_machinary_model_no = request.data.get('buyer_machinary_model_no',None)
        buyer_machinary_document = request.data.get('buyer_machinary_document',None)
        buyer_machinary_document_1 = request.data.get('buyer_machinary_document_1', None)
        buyer_machinary_document_2= request.data.get('buyer_machinary_document_2', None)
        buyer_machinary_additional_specifications = request.data.get('buyer_machinary_additional_specifications',None)
        buyer_machinary_add_product_supplies = request.data.get('buyer_machinary_add_product_supplies',None)
        custom_code = request.data.get('custom_code', None)
        userid = request.data.get('userid',None)
        try:
            itemcodesettingsobj = ItemCodeSettings.objects.filter(updated_by=userid,item_type='Machinary & equipments').order_by('-id').values()
            if len(itemcodesettingsobj) > 0:
                buyermachinaryobj = BuyerMachinaryDetails.objects.filter(updated_by=userid).order_by('-buyer_machinary_numeric').values()
                if len(buyermachinaryobj)==0:
                    print("data not exist")
                    buyermachinary = BuyerMachinaryDetails.objects.create(buyer_machinary_item_type=buyer_machinary_item_type,
                                                                  buyer_machinary_prefix=itemcodesettingsobj[0].get('prefix'),
                                                                  buyer_machinary_suffix=itemcodesettingsobj[0].get('suffix'),
                                                                  buyer_machinary_numeric=int(itemcodesettingsobj[0].get('numeric')) + 1,
                                                                  buyer_machinary_item_code=itemcodesettingsobj[0].get('prefix')+itemcodesettingsobj[0].get('suffix')+str(itemcodesettingsobj[0].get('numeric')),
                                                                  buyer_machinary_item_name=buyer_machinary_item_name,
                                                                  buyer_machinary_item_description=buyer_machinary_item_description,
                                                                  buyer_machinary_uom=buyer_machinary_uom,
                                                                  buyer_machinary_hsn_sac=buyer_machinary_hsn_sac,
                                                                  buyer_machinary_unit_price=buyer_machinary_unit_price,
                                                                  buyer_machinary_category=buyer_machinary_category,
                                                                  buyer_machinary_department=buyer_machinary_department,
                                                                  buyer_machinary_item_group=buyer_machinary_item_group,
                                                                  buyer_machinary_annual_consumption=buyer_machinary_annual_consumption,
                                                                  buyer_machinary_safety_stock=buyer_machinary_safety_stock,
                                                                  buyer_machinary_model_no=buyer_machinary_model_no,
                                                                  buyer_machinary_document=buyer_machinary_document,
                                                                  buyer_machinary_document_1=buyer_machinary_document_1,
                                                                  buyer_machinary_document_2=buyer_machinary_document_2,
                                                                  buyer_machinary_additional_specifications=buyer_machinary_additional_specifications,
                                                                  buyer_machinary_add_product_supplies=buyer_machinary_add_product_supplies,
                                                                  updated_by=SelfRegistration.objects.get(id=userid),
                                                                  created_by=userid,
                                                                  custom_code=custom_code
                                                                          )
                else:
                    buyermachinary = BuyerMachinaryDetails.objects.create(buyer_machinary_item_type=buyer_machinary_item_type,
                                                                  buyer_machinary_prefix=buyermachinaryobj[0].get('buyer_machinary_prefix'),
                                                                  buyer_machinary_suffix=buyermachinaryobj[0].get('buyer_machinary_suffix'),
                                                                  buyer_machinary_numeric=int(buyermachinaryobj[0].get('buyer_machinary_numeric')) + 1,
                                                                  buyer_machinary_item_code=buyermachinaryobj[0].get('buyer_machinary_prefix') + buyermachinaryobj[0].get('buyer_machinary_suffix')+buyermachinaryobj[0].get('buyer_machinary_numeric'),
                                                                  buyer_machinary_item_name=buyer_machinary_item_name,
                                                                  buyer_machinary_item_description=buyer_machinary_item_description,
                                                                  buyer_machinary_uom=buyer_machinary_uom,
                                                                  buyer_machinary_hsn_sac=buyer_machinary_hsn_sac,
                                                                  buyer_machinary_unit_price=buyer_machinary_unit_price,
                                                                  buyer_machinary_category=buyer_machinary_category,
                                                                  buyer_machinary_department=buyer_machinary_department,
                                                                  buyer_machinary_item_group=buyer_machinary_item_group,
                                                                  buyer_machinary_annual_consumption=buyer_machinary_annual_consumption,
                                                                  buyer_machinary_safety_stock=buyer_machinary_safety_stock,
                                                                  buyer_machinary_model_no=buyer_machinary_model_no,
                                                                  buyer_machinary_document=buyer_machinary_document,
                                                                  buyer_machinary_document_1=buyer_machinary_document_1,
                                                                  buyer_machinary_document_2=buyer_machinary_document_2,
                                                                  buyer_machinary_additional_specifications=buyer_machinary_additional_specifications,
                                                                  buyer_machinary_add_product_supplies=buyer_machinary_add_product_supplies,
                                                                  updated_by=SelfRegistration.objects.get(id=userid),
                                                                  created_by=userid,
                                                                  custom_code=custom_code
                                                                          )
                return Response({'status':201,'message':'Buyer Equipments Created'},status=201)
            else:
                return Response(
                    {'status': 204, 'message': 'Item Code Settings Not Present for Equipments,Please Create Equipments Item Code in Settings'},
                    status=204)

        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)

    def get_queryset(self):
        buyermachinaryobjval=BuyerMachinaryDetails.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if buyermachinaryobjval:
            return buyermachinaryobjval
        raise ValidationError({'message':'Buyer Machinary Details Not Present','status':204})



@api_view(['post'])
# @permission_classes((AllowAny,))
def advance_search_buyer_product(request):
    # advance search buyer product
    data = request.data
    buyer_item_type=data['buyer_item_type']
    buyer_item_code = data['buyer_item_code']
    buyer_item_name = data['buyer_item_name']
    buyer_item_description = data['buyer_item_description']
    buyer_uom = data['buyer_uom']
    buyer_hsn_sac = data['buyer_hsn_sac']
    buyer_unit_price=data['buyer_unit_price']
    buyer_category=data['buyer_category']
    buyer_department=data['buyer_department']
    buyer_item_group=data['buyer_item_group']
    buyer_model_no=data['buyer_model_no']
    updated_by=data['updated_by']

    try:
        buyerproductadvancesearch = BuyerProductDetails.objects.filter(updated_by_id=updated_by).filter(
            buyer_item_type__icontains=buyer_item_type).filter(buyer_item_code__icontains=buyer_item_code).filter(
            buyer_item_name__icontains=buyer_item_name). \
            filter(buyer_item_description__icontains=buyer_item_description).filter(
            buyer_uom__icontains=buyer_uom).filter(
            buyer_hsn_sac__icontains=buyer_hsn_sac).filter(buyer_unit_price__icontains=buyer_unit_price).filter(buyer_category__icontains=buyer_category).filter(
            buyer_department__icontains=buyer_department).filter(buyer_item_group__icontains=buyer_item_group).filter(buyer_model_no__icontains=buyer_model_no).values()

        return Response({'status': '200', 'message': 'Buyer Product Advance Search', 'data': buyerproductadvancesearch},
                        status=200)
    except Exception as e:
        return Response({'status': '500', 'error': str(e)}, status=500)




@api_view(['post'])
# @permission_classes((AllowAny,))
def t_codes_datas(request):
    data=request.data
    searchdata=data['searchdata']
    try:

        if searchdata.lower()=="VdrP1".lower():
            return Response({'status': 200, 'message': 'Search_Success'}, status=200)
        elif searchdata.lower()=="VdrP2".lower():
            return Response({'status': 200, 'message': 'Search_Category_Success'}, status=200)
        elif searchdata.lower()=="VdrP3".lower():
            return Response({'status': 200, 'message': 'Vendor_Product_Details'}, status=200)
        elif searchdata.lower()=="VdrP4".lower():
            return Response({'status': 200, 'message': 'Pricing_Details'}, status=200)
        elif searchdata.lower()=="VdrP5".lower():
            return Response({'status': 200, 'message': 'List_And_Summary'}, status=200)
        else:
            return Response({'status': 204, 'message': 'Not_Present'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def get_all_types_of_products_by_user_id(request):
    data=request.data
    userid=data['userid']
    try:
        buyerproductobj=BuyerProductDetails.objects.filter(updated_by_id=userid).values().order_by('buyer_product_id')
        buyerserviceobj = BuyerServiceDetails.objects.filter(updated_by_id=userid).values().order_by('buyer_service_id')
        buyermachinaryobj = BuyerMachinaryDetails.objects.filter(updated_by_id=userid).values().order_by('buyer_machinary_id')
        totalproducts = list(chain(buyerproductobj, buyerserviceobj, buyermachinaryobj))
        if len(buyerproductobj) or len(buyerserviceobj) or len(buyermachinaryobj)>0:
            return Response({'status':200,'message':'All Products List','data':totalproducts},status=200)
        else:
            return Response({'status':204,'message':'Not Present'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes((AllowAny,))
def get_all_types_of_products_by_ccode(request):
    data = request.data
    ccode = data['ccode']
    try:
        basicobj=BasicCompanyDetails.objects.filter(company_code=ccode).values()
        buyerproductobj = BuyerProductDetails.objects.filter(updated_by_id=basicobj[0].get('updated_by_id')).values().order_by(
            'buyer_product_id')
        buyerserviceobj = BuyerServiceDetails.objects.filter(updated_by_id=basicobj[0].get('updated_by_id')).values().order_by(
            'buyer_service_id')
        buyermachinaryobj = BuyerMachinaryDetails.objects.filter(updated_by_id=basicobj[0].get('updated_by_id')).values().order_by(
            'buyer_machinary_id')
        totalproducts = list(chain(buyerproductobj, buyerserviceobj, buyermachinaryobj))
        if len(buyerproductobj) or len(buyerserviceobj) or len(buyermachinaryobj) > 0:
            return Response({'status': 200, 'message': 'All Products List', 'data': totalproducts}, status=200)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=204)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def vendor_product_based_on_maincore_name(request):
    data=request.data
    maincorename=data['maincorename']
    try:
        vendorobj=VendorProduct_BasicDetails.objects.filter(core_sector=maincorename).values()
        if len(vendorobj)>0:
            return Response({'status': 200, 'message': 'Success', 'data': vendorobj}, status=200)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def vendor_product_based_on_category_name(request):
    data = request.data
    categoryname = data['categoryname']
    try:
        vendorobj = VendorProduct_BasicDetails.objects.filter(category=categoryname).values()
        if len(vendorobj) > 0:
            return Response({'status': 200, 'message': 'Success', 'data': vendorobj}, status=200)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['put'])
def update_buyer_products(request):
    data=request.data
    userid=data['userid']
    itemtype=data['itemtype']
    try:
        if itemtype=='Product':
            buyer_product_id=data['buyer_product_id']
            buyer_item_name = data['buyer_item_name']
            buyer_item_description = data['buyer_item_description']
            buyer_hsn_sac = data['buyer_hsn_sac']
            buyer_uom = data['buyer_uom']
            buyer_unit_price = data['buyer_unit_price']
            buyer_category = data['buyer_category']
            buyer_department = data['buyer_department']
            buyer_item_group = data['buyer_item_group']
            buyer_annual_consumption = data['buyer_annual_consumption']
            buyer_safety_stock = data['buyer_safety_stock']
            buyer_model_no = data['buyer_model_no']
            buyer_document = data['buyer_document']
            buyer_additional_specifications = data['buyer_additional_specifications']
            buyer_add_product_supplies = data['buyer_add_product_supplies']
            buyer_document_1=data['buyer_document_1']
            buyer_document_2=data['buyer_document_2']



            productobj= BuyerProductDetails.objects.filter(updated_by_id=userid,buyer_product_id=buyer_product_id,buyer_item_type=itemtype).values()
            if len(productobj)>0:
                productobjget=BuyerProductDetails.objects.get(buyer_product_id=productobj[0].get('buyer_product_id'))
                if productobjget and productobjget.updated_by_id!=0:
                    if productobjget.buyer_uom!=buyer_uom:
                        productobjget.buyer_uom=buyer_uom
                        productobjget.save()

                    if productobjget.buyer_item_name!=buyer_item_name:
                        productobjget.buyer_item_name=buyer_item_name
                        productobjget.save()

                    if productobjget.buyer_item_description != buyer_item_description:
                        productobjget.buyer_item_description = buyer_item_description
                        productobjget.save()

                    if productobjget.buyer_hsn_sac!=buyer_hsn_sac:
                        productobjget.buyer_hsn_sac=buyer_hsn_sac
                        productobjget.save()

                    if productobjget.buyer_unit_price != buyer_unit_price:
                        productobjget.buyer_unit_price = buyer_unit_price
                        productobjget.save()

                    if productobjget.buyer_category != buyer_category:
                        productobjget.buyer_category = buyer_category
                        productobjget.save()

                    if productobjget.buyer_department != buyer_department:
                        productobjget.buyer_department = buyer_department
                        productobjget.save()

                    if productobjget.buyer_item_group != buyer_item_group:
                        productobjget.buyer_item_group = buyer_item_group
                        productobjget.save()

                    if productobjget.buyer_annual_consumption != buyer_annual_consumption:
                        productobjget.buyer_annual_consumption = buyer_annual_consumption
                        productobjget.save()

                    if productobjget.buyer_safety_stock != buyer_safety_stock:
                        productobjget.buyer_safety_stock = buyer_safety_stock
                        productobjget.save()

                    if productobjget.buyer_model_no != buyer_model_no:
                        productobjget.buyer_model_no = buyer_model_no
                        productobjget.save()
                    if buyer_document!="":
                        if productobjget.buyer_document != buyer_document:
                            productobjget.buyer_document = buyer_document
                            productobjget.save()
                    if buyer_document_1!="":
                        if productobjget.buyer_document_1!=buyer_document_1:
                            productobjget.buyer_document_1 = buyer_document_1
                            productobjget.save()

                    if buyer_document_2!="":
                        if productobjget.buyer_document_2!=buyer_document_2:
                            productobjget.buyer_document_2 = buyer_document_2
                            productobjget.save()

                    if productobjget.buyer_additional_specifications != buyer_additional_specifications:
                        productobjget.buyer_additional_specifications = buyer_additional_specifications
                        productobjget.save()

                    if productobjget.buyer_add_product_supplies != buyer_add_product_supplies:
                        productobjget.buyer_add_product_supplies = buyer_add_product_supplies
                        productobjget.save()

                    if productobjget.updated_by_id!=userid:
                        productobjget.updated_by_id=userid
                        productobjget.save()
                    productres=BuyerProductDetails.objects.filter(updated_by=userid,buyer_product_id=buyer_product_id).values()
                    return Response({'status':202,'message':'Buyer Product Updated','data':productres},status=202)

        elif itemtype == 'Service':
            buyer_service_id = data['buyer_service_id']
            buyer_service_item_name = data['buyer_service_item_name']
            buyer_service_item_description = data['buyer_service_item_description']
            buyer_service_hsn_sac = data['buyer_service_hsn_sac']
            buyer_service_uom = data['buyer_service_uom']
            buyer_service_unit_price = data['buyer_service_unit_price']
            buyer_service_category = data['buyer_service_category']
            buyer_service_department = data['buyer_service_department']
            buyer_service_item_group = data['buyer_service_item_group']
            buyer_service_annual_consumption = data['buyer_service_annual_consumption']
            buyer_service_safety_stock = data['buyer_service_safety_stock']
            buyer_service_model_no = data['buyer_service_model_no']
            buyer_service_document = data['buyer_service_document']
            buyer_service_additional_specifications = data['buyer_service_additional_specifications']
            buyer_service_add_product_supplies = data['buyer_service_add_product_supplies']
            serviceobj = BuyerServiceDetails.objects.filter(updated_by_id=userid, buyer_service_id=buyer_service_id,buyer_service_item_type=itemtype).values()
            if len(serviceobj) > 0:
                serviceobjget = BuyerServiceDetails.objects.get(buyer_service_id=serviceobj[0].get('buyer_service_id'))
                if serviceobjget and serviceobjget.updated_by_id != 0:
                    if serviceobjget.buyer_service_uom != buyer_service_uom:
                        serviceobjget.buyer_service_uom = buyer_service_uom
                        serviceobjget.save()

                    if serviceobjget.buyer_service_item_name != buyer_service_item_name:
                        serviceobjget.buyer_service_item_name = buyer_service_item_name
                        serviceobjget.save()

                    if serviceobjget.buyer_service_item_description != buyer_service_item_description:
                        serviceobjget.buyer_service_item_description = buyer_service_item_description
                        serviceobjget.save()

                    if serviceobjget.buyer_service_hsn_sac != buyer_service_hsn_sac:
                        serviceobjget.buyer_service_hsn_sac = buyer_service_hsn_sac
                        serviceobjget.save()

                    if serviceobjget.buyer_service_unit_price != buyer_service_unit_price:
                        serviceobjget.buyer_service_unit_price = buyer_service_unit_price
                        serviceobjget.save()

                    if serviceobjget.buyer_service_category != buyer_service_category:
                        serviceobjget.buyer_service_category = buyer_service_category
                        serviceobjget.save()

                    if serviceobjget.buyer_service_department != buyer_service_department:
                        serviceobjget.buyer_service_department = buyer_service_department
                        serviceobjget.save()

                    if serviceobjget.buyer_service_item_group != buyer_service_item_group:
                        serviceobjget.buyer_service_item_group = buyer_service_item_group
                        serviceobjget.save()

                    if serviceobjget.buyer_service_annual_consumption != buyer_service_annual_consumption:
                        serviceobjget.buyer_service_annual_consumption = buyer_service_annual_consumption
                        serviceobjget.save()

                    if serviceobjget.buyer_service_safety_stock != buyer_service_safety_stock:
                        serviceobjget.buyer_service_safety_stock = buyer_service_safety_stock
                        serviceobjget.save()

                    if serviceobjget.buyer_service_model_no != buyer_service_model_no:
                        serviceobjget.buyer_service_model_no = buyer_service_model_no
                        serviceobjget.save()

                    if serviceobjget.buyer_service_document != buyer_service_document:
                        serviceobjget.buyer_service_document = buyer_service_document
                        serviceobjget.save()

                    if serviceobjget.buyer_service_additional_specifications != buyer_service_additional_specifications:
                        serviceobjget.buyer_service_additional_specifications = buyer_service_additional_specifications
                        serviceobjget.save()

                    if serviceobjget.buyer_service_add_product_supplies != buyer_service_add_product_supplies:
                        serviceobjget.buyer_service_add_product_supplies = buyer_service_add_product_supplies
                        serviceobjget.save()

                    if serviceobjget.updated_by_id!=userid:
                        serviceobjget.updated_by_id=userid
                        serviceobjget.save()
                    serviceres =  BuyerServiceDetails.objects.filter(updated_by=userid, buyer_service_id=buyer_service_id).values()
                    return Response({'status': 202, 'message': 'Buyer Service Updated', 'data': serviceres}, status=202)

        elif itemtype == 'Machinary & equipments':
            buyer_machinary_id = data['buyer_machinary_id']
            buyer_machinary_item_name = data['buyer_machinary_item_name']
            buyer_machinary_item_description = data['buyer_machinary_item_description']
            buyer_machinary_uom = data['buyer_machinary_uom']
            buyer_machinary_hsn_sac = data['buyer_machinary_hsn_sac']
            buyer_machinary_unit_price = data['buyer_machinary_unit_price']
            buyer_machinary_category = data['buyer_machinary_category']
            buyer_machinary_department = data['buyer_machinary_department']
            buyer_machinary_item_group = data['buyer_machinary_item_group']
            buyer_machinary_annual_consumption = data['buyer_machinary_annual_consumption']
            buyer_machinary_safety_stock = data['buyer_machinary_safety_stock']
            buyer_machinary_model_no = data['buyer_machinary_model_no']
            buyer_machinary_document = data['buyer_machinary_document']
            buyer_machinary_additional_specifications = data['buyer_machinary_additional_specifications']
            buyer_machinary_add_product_supplies = data['buyer_machinary_add_product_supplies']
            machinaryobj = BuyerMachinaryDetails.objects.filter(updated_by_id=userid, buyer_machinary_id=buyer_machinary_id,
                                                            buyer_machinary_item_type=itemtype).values()
            if len(machinaryobj) > 0:
                machinaryobjget = BuyerMachinaryDetails.objects.get(buyer_machinary_id=machinaryobj[0].get('buyer_machinary_id'))
                if machinaryobjget and machinaryobjget.updated_by_id != 0:
                    if machinaryobjget.buyer_machinary_item_name != buyer_machinary_item_name:
                        machinaryobjget.buyer_machinary_item_name = buyer_machinary_item_name
                        machinaryobjget.save()

                    if machinaryobjget.buyer_machinary_uom != buyer_machinary_uom:
                        machinaryobjget.buyer_machinary_uom = buyer_machinary_uom
                        machinaryobjget.save()

                    if machinaryobjget.buyer_machinary_item_description != buyer_machinary_item_description:
                        machinaryobjget.buyer_machinary_item_description = buyer_machinary_item_description
                        machinaryobjget.save()

                    if machinaryobjget.buyer_machinary_hsn_sac != buyer_machinary_hsn_sac:
                        machinaryobjget.buyer_machinary_hsn_sac = buyer_machinary_hsn_sac
                        machinaryobjget.save()

                    if machinaryobjget.buyer_machinary_unit_price != buyer_machinary_unit_price:
                        machinaryobjget.buyer_machinary_unit_price = buyer_machinary_unit_price
                        machinaryobjget.save()

                    if machinaryobjget.buyer_machinary_category != buyer_machinary_category:
                        machinaryobjget.buyer_machinary_category = buyer_machinary_category
                        machinaryobjget.save()

                    if machinaryobjget.buyer_machinary_department != buyer_machinary_department:
                        machinaryobjget.buyer_machinary_department = buyer_machinary_department
                        machinaryobjget.save()

                    if machinaryobjget.buyer_machinary_item_group != buyer_machinary_item_group:
                        machinaryobjget.buyer_machinary_item_group = buyer_machinary_item_group
                        machinaryobjget.save()

                    if machinaryobjget.buyer_machinary_annual_consumption != buyer_machinary_annual_consumption:
                        machinaryobjget.buyer_machinary_annual_consumption = buyer_machinary_annual_consumption
                        machinaryobjget.save()

                    if machinaryobjget.buyer_machinary_safety_stock != buyer_machinary_safety_stock:
                        machinaryobjget.buyer_machinary_safety_stock = buyer_machinary_safety_stock
                        machinaryobjget.save()

                    if machinaryobjget.buyer_machinary_model_no != buyer_machinary_model_no:
                        machinaryobjget.buyer_machinary_model_no = buyer_machinary_model_no
                        machinaryobjget.save()

                    if machinaryobjget.buyer_machinary_document != buyer_machinary_document:
                        machinaryobjget.buyer_machinary_document = buyer_machinary_document
                        machinaryobjget.save()

                    if machinaryobjget.buyer_machinary_additional_specifications != buyer_machinary_additional_specifications:
                        machinaryobjget.buyer_machinary_additional_specifications = buyer_machinary_additional_specifications
                        machinaryobjget.save()

                    if machinaryobjget.buyer_machinary_add_product_supplies != buyer_machinary_add_product_supplies:
                        machinaryobjget.buyer_machinary_add_product_supplies = buyer_machinary_add_product_supplies
                        machinaryobjget.save()

                    if machinaryobjget.updated_by_id != userid:
                        machinaryobjget.updated_by_id = userid
                        machinaryobjget.save()
                    machinaryres = BuyerMachinaryDetails.objects.filter(updated_by=userid, buyer_machinary_id=buyer_machinary_id).values()
                    return Response({'status': 202, 'message': 'Buyer Machinary Updated', 'data': machinaryres}, status=202)
        else:
            return Response({'status':200,'message':'Item type name is not correct,Please check'},status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def get_product_all_details_based_on_id_and_userid(request):
    data=request.data
    userid = data['userid']
    productid = data['productid']
    itemtype = data['itemtype']
    try:
        if itemtype=='Product':
            productitemobj=BuyerProductDetails.objects.filter(updated_by_id=userid,buyer_product_id=productid,buyer_item_type=itemtype).values()
            if len(productitemobj)>0:
                return Response({'status':200,'message':'Buyer Product Details','data':productitemobj},status=200)
            # else:
            #     return Response({'status':204,'message':'Not Present'},status=204)
        elif itemtype=='Service':
            productserviceitemobj = BuyerServiceDetails.objects.filter(updated_by_id=userid, buyer_service_id=productid,
                                                                buyer_service_item_type=itemtype).values()
            if len(productserviceitemobj)>0:
                return Response({'status': 200, 'message': 'Buyer Service Details', 'data': productserviceitemobj}, status=200)
        elif itemtype=='Machinary & equipments':
            productmachinaryitemobj=BuyerMachinaryDetails.objects.filter(updated_by_id=userid, buyer_machinary_id=productid,
                                                                buyer_machinary_item_type=itemtype).values()
            if len(productmachinaryitemobj)>0:
                return Response({'status': 200, 'message': 'Buyer Machinary Details', 'data': productmachinaryitemobj},
                                status=200)
        else:
            return Response({'status': 204, 'message': 'Item type is not correct',},
                            status=204)



    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def buyer_product_search(request):
    data=request.data
    itemcode=data['itemcode']
    itemtype = data['itemtype']
    itemname=data['itemname']
    itemdes = data['itemdes']
    hsn = data['hsn']
    uom = data['uom']
    dep=data['dep']
    cate=data['cate']
    unitprice = data['unitprice']
    itemgroup=data['itemgroup']
    modelno=data['modelno']
    valuearray=data['valuearray']
    status=data['status']
    buyerproductsearch=[]
    try:
        for i in range(0,len(valuearray)):
            if itemcode.lower() in valuearray[i].get('itemcode').lower() \
                    and itemtype.lower() in valuearray[i].get('itemtype').lower() \
                    and itemname.lower() in valuearray[i].get('itemname').lower() \
                and itemdes.lower() in valuearray[i].get('itemdes').lower() \
                and hsn.lower() in valuearray[i].get('hsn').lower() \
                and uom.lower() in valuearray[i].get('uom').lower()\
                and dep.lower() in valuearray[i].get('dep').lower() \
                and cate.lower() in valuearray[i].get('cate').lower()\
                and unitprice.lower() in valuearray[i].get('unitprice').lower() \
                and itemgroup.lower() in valuearray[i].get('itemgroup').lower() \
                and modelno.lower() in valuearray[i].get('modelno').lower() and status.lower() in valuearray[i].get('status').lower():
                buyerproductsearch.append(valuearray[i])
        return Response({'status': 200, 'message': 'Buyer Product Search Success', 'data': buyerproductsearch}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def get_product_all_details_based_on_id_multiple_and_userid(request):
    data=request.data
    userid = data['userid']
    itemcode = data['itemcode']
    itemtype = data['itemtype']
    try:
        if itemtype=='Product':
            productitemobj=BuyerProductDetails.objects.filter(updated_by_id=userid,buyer_item_code__in=itemcode,buyer_item_type=itemtype).values()
            if len(productitemobj)>0:
                return Response({'status':200,'message':'Buyer Product Details','data':productitemobj},status=200)
            # else:
            #     return Response({'status':204,'message':'Not Present'},status=204)
        elif itemtype=='Service':
            productserviceitemobj = BuyerServiceDetails.objects.filter(updated_by_id=userid, buyer_service_item_code__in=itemcode,
                                                                buyer_service_item_type=itemtype).values()
            if len(productserviceitemobj)>0:
                return Response({'status': 200, 'message': 'Buyer Service Details', 'data': productserviceitemobj}, status=200)
        elif itemtype=='Machinary & equipments':
            productmachinaryitemobj=BuyerMachinaryDetails.objects.filter(updated_by_id=userid, buyer_machinary_item_code__in=itemcode,
                                                                buyer_machinary_item_type=itemtype).values()
            if len(productmachinaryitemobj)>0:
                return Response({'status': 200, 'message': 'Buyer Machinary Details', 'data': productmachinaryitemobj},
                                status=200)
        else:
            return Response({'status': 204, 'message': 'Item type is not correct'},
                            status=204)



    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def advance_search_vendor_product(request):
    data=request.data
    # item_code=data['item_code']
    item_name=data['item_name']
    uom=data['uom']
    maincore=data['maincore']
    category=data['category']
    subcategory=data['subcategory']
    status=data['status']
    currency=data['currency']
    hsn_sac=data['hsn_sac']
    userid=data['userid']
    try:
        advancesearchobj=VendorProduct_BasicDetails.objects.filter(updated_by_id=userid).filter(item_name__icontains=item_name)\
            .filter(uom__icontains=uom).filter(core_sector__icontains=maincore).filter(category__icontains=category).filter(sub_category__icontains=subcategory)\
            .filter(status__icontains=status).filter(currency__icontains=currency).filter(hsn_sac__icontains=hsn_sac).values()
        return Response({'status':200,'message':'Vendor Product Advance Search','data':advancesearchobj},status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes((AllowAny,))
def fetch_vendor_product_basic_details_by_category(request):
    data=request.data
    try:
        vendorobj=VendorProduct_BasicDetails.objects.filter(category=data['category_name']).values().order_by('vendor_product_id')
        if len(vendorobj)>0:
            return Response({'status': 200, 'message': 'Vendor Product Basic Details List', 'data':vendorobj},status=200)
        else:
            return Response({'status': 204, 'message': 'Not Present'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

# @api_view(['post'])
# def get_previous_value_of_buyer_details(request):
#     data=request.data
#     userid=data['userid']
#     itemtype=data['itemtype']
#     try:
#         if itemtype=='Product':
#             buyerproductobj=BuyerProductDetails.objects.filter(buyer_item_type=itemtype,updated_by_id=userid).order_by('-').values()
#             if len(buyerproductobj)>0:
#                 buyer_product={
#                     'numeric':buyerproductobj[0].get('buyer_numeric'),
#                     'item_code':buyerproductobj[0].get('buyer_prefix')+buyerproductobj[0].get('buyer_suffix')+buyerproductobj,
#                     'user_id':buyerproductobj[0].get('updated_by_id')
#                 }
#                 return Response({'status': 200, 'message': 'Buyer Product List','data':buyer_product},status=200)
#             else:
#                 itemcodesettings = ItemCodeSettings.objects.filter(item_type=itemtype,updated_by_id=userid).values()
#                 if len(itemcodesettings)>0:
#                     product_item_code={
#                         'item_code':itemcodesettings[0].get('code_format'),
#                         'user_id':itemcodesettings[0].get('updated_by_id')
#                     }
#                     return Response({'status': 200, 'message': 'Code Settings Product','data':product_item_code}, status=200)
#                 else:
#                     return Response({'status': 204, 'message':'Code Settings for Product for this particular user id is not present,Please set your code in code settings'}, status=204)
#
#
#         elif itemtype=='Service':
#             buyerserviceobj = BuyerServiceDetails.objects.filter(buyer_service_item_type=itemtype, updated_by_id=userid).last()
#             if buyerserviceobj:
#                 buyer_service = {
#                     'item_code': buyerserviceobj.buyer_service_item_code,
#                     'user_id': buyerserviceobj.updated_by_id
#                 }
#                 return Response({'status': 200, 'message': 'Buyer Service List', 'data': buyer_service}, status=200)
#             else:
#                 itemcodesettings = ItemCodeSettings.objects.filter(item_type=itemtype, updated_by_id=userid).values()
#                 if len(itemcodesettings) > 0:
#                     service_item_code = {
#                         'item_code': itemcodesettings[0].get('code_format'),
#                         'user_id': itemcodesettings[0].get('updated_by_id')
#                     }
#                     return Response({'status': 200, 'message': 'Code Settings Service', 'data': service_item_code},
#                                     status=200)
#                 else:
#                     return Response({'status': 204,
#                                      'message': 'Code Settings for Service for this particular user id is not present,Please set your code in code settings'},
#                                     status=204)
#
#         elif itemtype=='Machinary & equipments':
#                 buyermachinaryobj = BuyerMachinaryDetails.objects.filter(buyer_machinary_item_type=itemtype, updated_by_id=userid).last()
#                 if buyermachinaryobj:
#                     buyer_machinary = {
#                         'item_code': buyermachinaryobj.buyer_machinary_item_code,
#                         'user_id': buyermachinaryobj.updated_by_id
#                     }
#                     return Response({'status': 200, 'message': 'Buyer Machinary List', 'data': buyer_machinary}, status=200)
#                 else:
#                     itemcodesettings = ItemCodeSettings.objects.filter(item_type=itemtype,
#                                                                        updated_by_id=userid).values()
#                     if len(itemcodesettings) > 0:
#                         machinary_item_code = {
#                             'item_code': itemcodesettings[0].get('code_format'),
#                             'user_id': itemcodesettings[0].get('updated_by_id')
#                         }
#                         return Response({'status': 200, 'message': 'Code Settings Machinary', 'data': machinary_item_code},
#                                         status=200)
#                     else:
#                         return Response({'status': 204,
#                                          'message': 'Code Settings for Machinary for this partiuclar user id is not present,Please set your code in code settings'},
#                                         status=204)
#         else:
#             return Response({'status': 204, 'message': 'item_type is mis-spelled or not present'}, status=204)
#
#     except Exception as e:
#         return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def get_previous_value_of_buyer_details(request):
    data=request.data
    userid=data['userid']
    itemtype=data['itemtype']
    try:
        if itemtype=='Product':
            buyerproductobj=BuyerProductDetails.objects.filter(buyer_item_type=itemtype,updated_by_id=userid).last()
            if buyerproductobj:
                buyer_product={
                    'numeric':int(buyerproductobj.buyer_numeric),
                    'item_code':buyerproductobj.buyer_prefix+buyerproductobj.buyer_suffix+buyerproductobj.buyer_numeric,
                    'user_id':buyerproductobj.updated_by_id
                }
                return Response({'status': 200, 'message': 'Buyer Product List','data':buyer_product},status=200)
            else:
                itemcodesettings = ItemCodeSettings.objects.filter(item_type=itemtype, updated_by_id=userid).values()
                if len(itemcodesettings)>0:
                    product_item_code={
                        'item_code':itemcodesettings[0].get('code_format'),
                        'user_id':itemcodesettings[0].get('updated_by_id')
                    }
                    return Response({'status': 200, 'message': 'Code Settings Product','data':product_item_code}, status=200)
                else:
                    return Response({'status': 204, 'message':'Code Settings for Product for this particular user id is not present,Please set your code in code settings'}, status=204)


        elif itemtype=='Service':
            buyerserviceobj = BuyerServiceDetails.objects.filter(buyer_service_item_type=itemtype, updated_by_id=userid).last()
            if buyerserviceobj:
                buyer_service = {
                    'numeric': buyerserviceobj.buyer_service_numeric,
                    'item_code': buyerserviceobj.buyer_service_prefix+buyerserviceobj.buyer_service_suffix+buyerserviceobj.buyer_service_numeric,
                    'user_id': buyerserviceobj.updated_by_id
                }
                return Response({'status': 200, 'message': 'Buyer Service List', 'data': buyer_service}, status=200)
            else:
                itemcodesettings = ItemCodeSettings.objects.filter(item_type=itemtype, updated_by_id=userid).values()
                if len(itemcodesettings) > 0:
                    service_item_code = {
                        'item_code': itemcodesettings[0].get('code_format'),
                        'user_id': itemcodesettings[0].get('updated_by_id')
                    }
                    return Response({'status': 200, 'message': 'Code Settings Service', 'data': service_item_code},
                                    status=200)
                else:
                    return Response({'status': 204,
                                     'message': 'Code Settings for Service for this particular user id is not present,Please set your code in code settings'},
                                    status=204)

        elif itemtype=='Machinary & equipments':
                buyermachinaryobj = BuyerMachinaryDetails.objects.filter(buyer_machinary_item_type=itemtype, updated_by_id=userid).last()
                if buyermachinaryobj:
                    buyer_machinary = {
                        'numeric': int(buyermachinaryobj.buyer_machinary_numeric),
                        'item_code': buyermachinaryobj.buyer_machinary_prefix+buyermachinaryobj.buyer_machinary_suffix+buyermachinaryobj.buyer_machinary_numeric,
                        'user_id': buyermachinaryobj.updated_by_id
                    }
                    return Response({'status': 200, 'message': 'Buyer Machinary List', 'data': buyer_machinary}, status=200)
                else:
                    itemcodesettings = ItemCodeSettings.objects.filter(item_type=itemtype,
                                                                       updated_by_id=userid).values()
                    if len(itemcodesettings) > 0:
                        machinary_item_code = {
                            'item_code': itemcodesettings[0].get('code_format'),
                            'user_id': itemcodesettings[0].get('updated_by_id')
                        }
                        return Response({'status': 200, 'message': 'Code Settings Machinary', 'data': machinary_item_code},
                                        status=200)
                    else:
                        return Response({'status': 204,
                                         'message': 'Code Settings for Machinary for this partiuclar user id is not present,Please set your code in code settings'},
                                        status=204)
        else:
            return Response({'status': 204, 'message': 'item_type is mis-spelled or not present'}, status=204)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes((AllowAny,))
def fetch_vendor_product_general_details(request):
    data=request.data
    vendor_product_id=data['vendor_product_id']
    try:
        vendorgeneralproductobj=VendorProduct_GeneralDetails.objects.filter(vendor_products_id=vendor_product_id).values()
        if len(vendorgeneralproductobj)>0:
            return Response({'status':200,'message':'Vendor Product General Details List','data':vendorgeneralproductobj},status=status.HTTP_200_OK)
        else:
            return Response({'status':204,'message':'Vendor Product General Details Not Present'},status=status.HTTP_204_NO_CONTENT)


    except Exception as e:
        return Response({'status':500,'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['post'])
@permission_classes((AllowAny,))
def fetch_vendor_product_technical_details(request):
    data = request.data
    vendor_product_id = data['vendor_product_id']
    try:
        vendortechnicalproductobj = VendorProduct_TechnicalSpecifications.objects.filter(
            vendor_products_id=vendor_product_id).values()
        if len(vendortechnicalproductobj) > 0:
            return Response({'status': 200, 'message': 'Vendor Product Techincal Details List','data':vendortechnicalproductobj},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'Vendor Product Techincal Details Not Present'},
                            status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['post'])
@permission_classes((AllowAny,))
def fetch_vendor_product_productfeatures_details(request):
    data = request.data
    vendor_product_id = data['vendor_product_id']
    try:
        vendorproductfeaturesobj = VendorProduct_ProductFeatures.objects.filter(
            vendor_products_id=vendor_product_id).values()
        if len(vendorproductfeaturesobj) > 0:
            return Response({'status': 200, 'message': 'Vendor Product Product_Features Details List','data':vendorproductfeaturesobj},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'Vendor Product Product_Features Details Not Present'},
                            status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['post'])
@permission_classes((AllowAny,))
def fetch_vendor_product_document_details(request):
    data = request.data
    vendor_product_id = data['vendor_product_id']
    try:
        vendorproductdocumentsobj = VendorProduct_Documents.objects.filter(
            vendor_products_id=vendor_product_id).values()
        if len(vendorproductdocumentsobj) > 0:
            return Response({'status': 200, 'message': 'Vendor Product Documents Details List','data':vendorproductdocumentsobj},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'Vendor Product Documents Details Not Present'},
                            status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['post'])
# @permission_classes((AllowAny,))
# def get_vendor_details_by_sub_category(request):
#     data=request.data
#     subcategoryname=data['subcategoryname']
#     vendordetails=[]
#     ccodearray=[]
#     try:
#         vendorobj = VendorProduct_BasicDetails.objects.filter(sub_category__icontains=subcategoryname).distinct('sub_category','company_code').values()
#         for i in range(0,len(vendorobj)):
#             basicobj=BasicCompanyDetails.objects.filter(company_code=vendorobj[i].get('company_code')).values()
#             regobj=SelfRegistration.objects.filter(id=basicobj[0].get('updated_by_id')).values()
#             industryobj=IndustrialInfo.objects.get(company_code=vendorobj[i].get('company_code'))
#             billobj=BillingAddress.objects.filter(company_code_id=vendorobj[i].get('company_code')).values()
#             vendordetails.append({
#                 'company_name':basicobj[0].get('company_name'),
#                 'name': regobj[0].get('contact_person'),
#                 'email':regobj[0].get('username'),
#                 'phone_number':regobj[0].get('phone_number'),
#                 'profile_photo': regobj[0].get('profile_cover_photo'),
#                 'city':billobj[0].get('bill_city')
#                 # 'nature_of_business':industryobj.nature_of_business,
#                 # 'industry_to_serve':industryobj.industry_to_serve
#             })
#         return Response({'status': 200, 'message': 'ok','data':vendordetails},status=status.HTTP_200_OK)
#
#
#     except Exception as e:
#         return Response({'status':500,'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['post'])
@permission_classes((AllowAny,))
def get_vendor_details_by_sub_category(request):
    data=request.data
    key=data['key']
    subcategoryname=data['subcategoryname']
    vendordetails=[]
    ccodearray=[]
    average=0
    try:
        if key=='vsinadmindb':
            vendorobj = VendorProduct_BasicDetails.objects.filter(sub_category__icontains=subcategoryname).distinct('sub_category','company_code').values()
            if len(vendorobj)>0:
                for i in range(0,len(vendorobj)):
                    print(vendorobj[i].get('company_code'))
                    basicobj=BasicCompanyDetails.objects.filter(company_code=vendorobj[i].get('company_code')).values()
                    regobj=SelfRegistration.objects.filter(id=basicobj[0].get('updated_by_id')).values()
                    industryobj=IndustrialInfo.objects.filter(company_code=vendorobj[i].get('company_code')).values()
                    billobj=BillingAddress.objects.filter(company_code_id=vendorobj[i].get('company_code')).values()
                    hierarchyobj=IndustrialHierarchy.objects.filter(company_code_id=vendorobj[i].get('company_code')).values()
                    reviewobj = CompanyReviewAndRating.objects.filter(company_code=vendorobj[i].get('company_code')).values()
                    print(len(reviewobj))
                    if len(reviewobj) > 0:
                        print('sssssssssssss')
                        sum = 0
                        for rating in reviewobj:
                            sum = sum + rating['rating']
                            if len(reviewobj) > 0:
                                average = sum / len(reviewobj)
                            else:
                                average = 0
                        print(average,'Aaaaaaaaa')
                    else:
                        pass
                    vendordetails.append({
                        'company_name':basicobj[0].get('company_name'),
                        'name': regobj[0].get('contact_person'),
                        'email':regobj[0].get('username'),
                        'phone_number':regobj[0].get('phone_number'),
                        'profile_photo': regobj[0].get('profile_cover_photo'),
                        'city':billobj[0].get('bill_city'),
                        'nature_of_business':industryobj[0].get('nature_of_business'),
                        'industry_to_serve':industryobj[0].get('industry_to_serve'),
                        'user_type': regobj[0].get('user_type'),
                        'bill_city': billobj[0].get('bill_city'),
                        'bill_address': billobj[0].get('bill_address'),
                        'maincore': hierarchyobj[0].get('maincore'),
                        'category': hierarchyobj[0].get('category'),
                        'subcategory': hierarchyobj[0].get('subcategory'),
                        'industrial_scale': basicobj[0].get('industrial_scale'),
                        'registered_date': regobj[0].get('created_on'),
                        'rating': round(average)
                    })
                return Response({'status': 200, 'message': 'ok','data':vendordetails},status=status.HTTP_200_OK)

            else:
                return Response({'status': 204, 'message': 'Vendor Product Details Not Present', 'data': vendordetails}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'status': 401, 'message': 'UnAuthorized'},status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['post'])
def fetch_vendor_product_basic_details_by_subcategory(request):
    try:
        vendorobj=VendorProduct_BasicDetails.objects.filter(sub_category=request.data['sub_category']).values().order_by('vendor_product_id')
        if len(vendorobj)>0:
            return Response({'status': 200, 'message': 'Vendor Product Basic Details By SubCategory List', 'data': vendorobj}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['post'])
@permission_classes((AllowAny,))
def fetch_vendor_product_basic_details_by_userid_all(request):
    try:
        vendorobj=VendorProduct_BasicDetails.objects.filter(updated_by_id=request.data['userid']).values().order_by('vendor_product_id')
        if len(vendorobj)>0:
            return Response({'status': 200, 'message': 'Vendor Product Basic Details By User Id List', 'data': vendorobj}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['post'])
def landing_page_bidding_create(request):
    data = request.data
    publish_date = data['publish_date']
    deadline_date = data['deadline_date']
    delivery_terms = data['delivery_terms']
    packaging_forwarding = data['packaging_forwarding']
    # priority = data['priority']
    payment_terms = data['payment_terms']
    quantity = data['quantity']
    vendor_product_pk = data['vendor_product_pk']
    product_name=data['product_name']
    # vendor_product_subcategory = data['vendor_product_subcategory']
    # vendors_code = data['vendors_code']
    userid=data['userid']
    vendor_user_id = data['vendor_user_id']
    vendorcodearray=[]
    company_namearray=[]
    try:
        vendorobj = VendorProduct_BasicDetails.objects.filter(item_name=product_name).distinct('updated_by_id').values()
        if len(vendorobj)>0:
            print(len(vendorobj))
            for i in range(0, len(vendorobj)):
                print(len(vendorobj))
                pname=vendorobj[i].get('item_name')
                print(pname,'ok')
                useridcode=vendorobj[i].get('updated_by_id')
                print(useridcode,'sfsd')
                basic = BasicCompanyDetails.objects.get(updated_by_id=useridcode)
                vendorcodearray.append(basic.company_code)
                print(vendorcodearray,'ok')
                company_namearray.append(basic.company_name)
                print(basic.updated_by_id)
                regobj = SelfRegistration.objects.get(id=basic.updated_by_id)
                print(regobj.username)
                configuration = sib_api_v3_sdk.Configuration()
                configuration.api_key[
                    'api-key'] = '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'

                api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
                subject = "Posted RFQ"
                text_content = "Dear , " + regobj.contact_person + "\n\n" + "This  " + basic.company_name + " company name posted RFQ by your product name i.e by " + pname
                sender = {"name": "Admin", "email": "admin@vendorsin.com"}
                # text_content = 'Hello '+regobj.contact_person+',''\n You are selected for bidding'
                to = [{"email": regobj.username, "name": regobj.contact_person}]
                reply_to = {"email": "admin@vendorsin.com", "name": "Admin"}
                send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=reply_to, text_content=text_content,
                                                               sender=sender, subject=subject)
                print(send_smtp_email, 'okkkkkkkkkkkkkkkkkkk')
                api_response = api_instance.send_transac_email(send_smtp_email)
                pprint(api_response)
            landingpagebiddingobj = LandingPageBidding.objects.create(publish_date=publish_date,
                                                                      deadline_date=deadline_date,
                                                                      delivery_terms=delivery_terms,
                                                                      packaging_forwarding=packaging_forwarding,
                                                                      # priority=priority,
                                                                      payment_terms=payment_terms,
                                                                      quantity=quantity,
                                                                      vendor_product_pk=vendor_product_pk,
                                                                      updated_by=SelfRegistration.objects.get(
                                                                          id=userid),
                                                                      created_by=userid,
                                                                      vendors_code=vendorcodearray,
                                                                      company_name=company_namearray,
                                                                      product_name=product_name,
                                                                      vendor_user_id=vendor_user_id

                                                                      )
            data={
                'id':landingpagebiddingobj.id
            }


            return Response({'status': 201, 'message': 'Post RFQ','data':data},status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 204, 'message': 'Product Name is not present'}, status=status.HTTP_204_NO_CONTENT)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def get_landing_page_bidding_by_userid_buyer_list(request):
    i=0
    try:
        getlistbyuserid=LandingPageBidding.objects.filter(updated_by_id=request.data['userid']).values().order_by('id')
        while i<len(getlistbyuserid):
            vendorproductdetails=VendorProduct_BasicDetails.objects.filter(vendor_product_id=getlistbyuserid[i].get('vendor_product_pk')).values()
            if vendorproductdetails:
                getlistbyuserid[i].setdefault('final_selling_price',vendorproductdetails[0].get('final_selling_price'))
                getlistbyuserid[i].setdefault('item_description',vendorproductdetails[0].get('item_description'))
                getlistbyuserid[i].setdefault('item_type',vendorproductdetails[0].get('item_type'))
                getlistbyuserid[i].setdefault('unit_price',vendorproductdetails[0].get('unit_price'))
                getlistbyuserid[i].setdefault('uom',vendorproductdetails[0].get('uom'))
            i=i+1

        return Response({'status': 200, 'message': 'Buyer Post rfq list by userid', 'data': getlistbyuserid},
                        status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def get_landing_page_bidding_by_userid_vendors_list(request):
    data=request.data
    userid=data['userid']
    vendorlandingpagebidarray=[]
    try:
        basicobj=BasicCompanyDetails.objects.filter(updated_by_id=userid).values().order_by('company_code')
        if len(basicobj)>0:
            ccodearray=[basicobj[0].get('company_code')]
            print(ccodearray)
            landingobj=LandingPageBidding.objects.filter(vendors_code__contains=ccodearray).values().order_by('id')
            print(len(landingobj))
            if len(landingobj)>0:
                for i in range(0,len(landingobj)):
                    basicobj1=BasicCompanyDetails.objects.filter(updated_by_id=landingobj[i].get('updated_by_id')).values()
                    vendorproductobj=VendorProduct_BasicDetails.objects.filter(updated_by_id=userid,item_name=landingobj[i].get('product_name')).values()
                    billobj=BillingAddress.objects.filter(updated_by_id=landingobj[i].get('updated_by_id')).values()
                    if len(billobj)>0 and len(vendorproductobj)>0:
                        vendorlandingpagebidarray.append({'vendor_code':basicobj1[0].get('company_code'),
                                                          'vendor_company_name':basicobj1[0].get('company_name'),
                                                          'item_name':landingobj[i].get('product_name'),
                                                          'item_description':vendorproductobj[0].get('item_description'),
                                                          'uom':vendorproductobj[0].get('uom'),
                                                          'publish_date':landingobj[i].get('publish_date'),
                                                          'deadline_date':landingobj[i].get('deadline_date'),
                                                          'delivery_terms':landingobj[i].get('delivery_terms'),
                                                          'packaging_forwarding':landingobj[i].get('packaging_forwarding'),
                                                          'priority':landingobj[i].get('priority'),
                                                          'payment_terms':landingobj[i].get('payment_terms'),
                                                          'quantity':landingobj[i].get('quantity'),
                                                          'item_code':vendorproductobj[0].get('item_code'),
                                                          'item_type':landingobj[i].get('item_type'),
                                                          'bill_city':billobj[0].get('bill_city')


                                                          })
                    else:
                        vendorlandingpagebidarray.append({'vendor_code': basicobj1[0].get('company_code'),
                                                          'vendor_company_name': basicobj1[0].get('company_name'),
                                                          'item_name': landingobj[i].get('product_name'),
                                                          'item_description': "",
                                                          'uom': "",
                                                          'publish_date': landingobj[i].get('publish_date'),
                                                          'deadline_date': landingobj[i].get('deadline_date'),
                                                          'delivery_terms': landingobj[i].get('delivery_terms'),
                                                          'packaging_forwarding': landingobj[i].get(
                                                              'packaging_forwarding'),
                                                          'priority': landingobj[i].get('priority'),
                                                          'payment_terms': landingobj[i].get('payment_terms'),
                                                          'quantity': landingobj[i].get('quantity'),
                                                          'item_code': "",
                                                          'item_type': landingobj[i].get('item_type'),
                                                          'bill_city': ""

                                                          })

                return Response({'status': 200, 'message': 'Vendor Post rfq list by userid','data':vendorlandingpagebidarray},
                                status=status.HTTP_200_OK)
            else:
                return Response({'status': 204, 'message': 'Vendor Post rfq is not present'},
                                status=status.HTTP_204_NO_CONTENT)
        else:

            return Response({'status': 202, 'message': 'Not Present'},status=200)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['post'])
@permission_classes((AllowAny,))
def fetch_vendor_product_basic_details_by_pk(request):
    try:
        vendorobjpk=VendorProduct_BasicDetails.objects.filter(vendor_product_id=request.data['vendor_product_id']).values().order_by('vendor_product_id')
        if len(vendorobjpk)>0:
            return Response({'status': 200, 'message': 'Vendor Product Basic Details List by id', 'data': vendorobjpk}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






@api_view(['post'])
def landing_page_listing_leads_pending_list(request):
    data=request.data
    userid=data['userid']
    vendorproductarray=[]
    try:
        openleadslistobj=LandingPageBidding.objects.filter(vendor_user_id=userid,status='Pending').values().order_by('id')
        if len(openleadslistobj)>0:
            for i in range(0,len(openleadslistobj)):
                # print(len(openleadslistobj),'leeeeeeeeeeeeeeeeeeeeeeee')
                # print(openleadslistobj[i].get('deadline_date'),'pok')
                deadlinedateval = datetime.strptime(openleadslistobj[i].get('deadline_date'), '%Y-%m-%d')
                deadlinedateconvertion = datetime.date(deadlinedateval)
                todaydate = date.today()
                if deadlinedateconvertion > todaydate:
                    print('yes')
                    # print(openleadslistobj[i].get('vendor_product_pk'),'ok')
                    vendorobj=VendorProduct_BasicDetails.objects.filter(vendor_product_id=openleadslistobj[i].get('vendor_product_pk')).values()
                    if len(vendorobj)>0:
                        basicobj=BasicCompanyDetails.objects.filter(updated_by_id=openleadslistobj[i].get('updated_by_id')).values()
                        vendorproductarray.append({'id':openleadslistobj[i].get('id'),
                                                   'publish_date':openleadslistobj[i].get('publish_date'),
                                                   'deadline_date': openleadslistobj[i].get('deadline_date'),
                                                   'delivery_terms': openleadslistobj[i].get('delivery_terms'),
                                                   'packaging_forwarding': openleadslistobj[i].get('packaging_forwarding'),
                                                   'priority': openleadslistobj[i].get('priority'),
                                                   'payment_terms': openleadslistobj[i].get('payment_terms'),
                                                   'quantity': openleadslistobj[i].get('quantity'),
                                                   'vendor_product_pk': openleadslistobj[i].get('vendor_product_pk'),
                                                   'item_type': openleadslistobj[i].get('item_type'),
                                                   'vendors_code': basicobj[0].get('company_code'),
                                                   'created_by': openleadslistobj[i].get('created_by'),
                                                   'updated_by': openleadslistobj[i].get('updated_by'),
                                                   'company_name': basicobj[0].get('company_name'),
                                                   'status': openleadslistobj[i].get('status'),
                                                   'product_name': openleadslistobj[i].get('product_name'),
                                                   'vendor_user_id': openleadslistobj[i].get('vendor_user_id'),
                                                   'product_description':vendorobj[0].get('item_description'),
                                                   'uom':vendorobj[0].get('uom')
                                                   })
                    else:
                        pass
                else:
                    print('deadline is expired')

            return Response({'status': 200, 'message': 'Open Leads List of Listing Leads','data':vendorproductarray}, status=200)
        else:
            return Response({'status':204,'message':'Data Not Present','data':vendorproductarray},status=204)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['put'])
def update_landing_page_status_to_decline(request):
    data=request.data
    landingbidpk=data['landingbidpk']
    userid=data['userid']
    try:
        landingobj=LandingPageBidding.objects.filter(id=landingbidpk,vendor_user_id=userid).values()
        if len(landingobj)>0:
            landingget=LandingPageBidding.objects.get(id=landingobj[0].get('id'))
            if landingget.status=='Pending':
                landingget.status='Reject'
                landingget.save()
                landingobjtotal = LandingPageBidding.objects.filter(vendor_user_id=userid,status='Reject').values().order_by('id')

                return Response({'status': 200, 'message': 'Rejected','data':landingobjtotal},status=200)
            elif landingget.status=='Reject':
                return Response({'status': 202, 'message': 'status already rejected'}, status=202)
            else:
                return Response({'status': 202, 'message': 'status already published'}, status=202)
        else:
            return Response({'status': 204, 'message': 'Data Not Present for this id'}, status=204)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def get_landing_page_bidding_by_pk(request):
    data=request.data
    landingpk=data['landingpk']
    basicarray={}
    try:
        landingobj=LandingPageBidding.objects.filter(id=landingpk).values()
        if len(landingobj)>0:
            basicobj = BasicCompanyDetails.objects.filter(updated_by_id=landingobj[0].get('updated_by_id')).values()
            billobj=BillingAddress.objects.filter(updated_by_id=landingobj[0].get('updated_by_id')).values()
            vendorproductobj=VendorProduct_BasicDetails.objects.filter(vendor_product_id=landingobj[0].get('vendor_product_pk')).values()
            basicarray.setdefault('ccode',str(basicobj[0].get('company_code')))
            basicarray.setdefault('cname',basicobj[0].get('company_name'))
            landingobj[0].setdefault('basic_details',basicarray)
            landingobj[0].setdefault('bill_city',billobj[0].get('bill_city'))
            return Response({'status':200,'message':'Landing Page Bidding List','landingpagedata':landingobj,'vendorproductdata':vendorproductobj},status=200)
        else:
            return Response({'status':204,'message':'Not Present','data':landingobj},status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




class LandingPageBiddingRFQAwardsSerializerViewSet(viewsets.ModelViewSet):
    queryset = awardpostedRFQ.objects.all()
    serializer_class = LandingPageBiddingRFQAwardsSerializer

    def create(self, request, *args, **kwargs):
        landingpagepublishobj=LandingPageBidding_Publish.objects.filter(id__in=request.data['landing_page_bidding_publish_id']).values()
        print(len(landingpagepublishobj))
        for i in range(0,len(landingpagepublishobj)):
            ccode=landingpagepublishobj[i].get('company_code')
            cname=landingpagepublishobj[i].get('company_name')
            basic = BasicCompanyDetails.objects.get(company_code=ccode)
            print(basic.company_code, 'fdfdf')
            regobj = SelfRegistration.objects.get(id=basic.updated_by_id)
            print(regobj.username)
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key[
                'api-key'] = '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'

            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
            subject = "Published  RFQ"
            text_content = "Dear " + regobj.contact_person + "\n\n" + "Your  " + basic.company_name + " company is awarded." + "\n\n" + "NOTE: Please Don't Share this to anyone"
            sender = {"name": "VENDORSIN COMMERCE PRIVATE LIMITED", "email": "admin@vendorsin.com"}
            # text_content = 'Hello '+regobj.contact_person+',''\n You are selected for bidding'
            to = [{"email": regobj.username, "name": regobj.contact_person}]
            reply_to = {"email": "admin@vendorsin.com", "name": "Admin"}
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=reply_to, text_content=text_content,
                                                           sender=sender, subject=subject)
            print(send_smtp_email)
            api_response = api_instance.send_transac_email(send_smtp_email)
            pprint(api_response)
        return super().create(request, *args, **kwargs)
    def get_queryset(self):
        landingpageobj = awardpostedRFQ.objects.filter(
            updated_by=self.request.GET.get('updated_by')).order_by('id')
        if landingpageobj:
            return landingpageobj
        raise ValidationError({'message': 'Award is not exist', 'status': 204})


@api_view(['post'])
def getawardlistoflistingleadsnew(request):
    data=request.data
    res=[]
    landing_vendor_publish_leading_data=[]
    userid=data['userid']
    try:
        awardpostedRFQobj=awardpostedRFQ.objects.filter(updated_by=userid).values()
        for i in range(len(awardpostedRFQobj)):
            dummyvar=LandingPageBidding_Publish.objects.filter(id__in=awardpostedRFQobj[i].get('landing_page_bidding_publish_id')).values()
            print(len(dummyvar))
            for j in range(0,len(dummyvar)):
                dummyvar[j].__setitem__('award_pk', awardpostedRFQobj[i].get('id'))
            res = list(chain(landing_vendor_publish_leading_data, dummyvar))
        return Response({'status': 200, 'message': 'Ok', 'data':res}, status=200)
    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)

@api_view(['post'])
def getbuyerpostedresponse(request):
    data=request.data
    userid=data['userid']
    res=[]
    try:
        landingpagebidd=LandingPageBidding.objects.filter(updated_by=SelfRegistration.objects.get(id=userid)).values()
        print(landingpagebidd)
        for i in range(len(landingpagebidd)):
            vendor_product_details=VendorProduct_BasicDetails.objects.filter(vendor_product_id=landingpagebidd[i].get('vendor_product_pk')).values()
            if vendor_product_details:
                landingpagevendorbidpublishobj=LandingPageBidding_Publish.objects.filter(listing_leads=landingpagebidd[i].get('id')).values()
                res.append({
                            'landong_page_pk':landingpagebidd[i].get('id'),
                            'productname':landingpagebidd[i].get('product_name'),
                            'productdesc':vendor_product_details[0].get('item_description'),
                            'Quantity':landingpagebidd[i].get('quantity'),
                            'Priority':landingpagebidd[i].get('priority'),
                            'publish_date':landingpagebidd[i].get('publish_date'),
                            'deadline_date':landingpagebidd[i].get('deadline_date'),
                            'count_of_res':len(landingpagevendorbidpublishobj)})
        return Response({'status': 200, 'message': 'Ok','data':res}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def get_buyer_posted_response_by_pk(request):
    data=request.data
    landingpk=data['landingpk']
    try:
        landingpagebidd=LandingPageBidding.objects.filter(id=landingpk).values()
        if len(landingpagebidd)>0:
            landingpagevendorbidpublishobj=LandingPageBidding_Publish.objects.filter(listing_leads=landingpagebidd[0].get('id')).values()
            return Response({'status': 200, 'message': 'Listing Leads Publish','data':landingpagevendorbidpublishobj,'buyer_data':landingpagebidd}, status=200)
        else:
            return Response({'status':204,'message':'Listing Leads Not Present'},status=204)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def fetch_vendor_product_details_by_userid_and_pk(request):
    data=request.data
    userid=data['userid']
    vendorpk=data['vendorpk']
    try:
        vendorobj=VendorProduct_BasicDetails.objects.filter(updated_by_id=userid,vendor_product_id=vendorpk).values()
        if len(vendorobj)>0:
            vendorproductobj=VendorProduct_BasicDetails.objects.filter(vendor_product_id=vendorobj[0].get('vendor_product_id')).values().order_by('vendor_product_id')
            vendorproductgeneraldetailsobj=VendorProduct_GeneralDetails.objects.filter(vendor_products_id=vendorobj[0].get('vendor_product_id')).values().order_by('id')
            vendortechincalobj = VendorProduct_TechnicalSpecifications.objects.filter(
                vendor_products_id=vendorobj[0].get('vendor_product_id')).values().order_by('id')
            vendorproductfeaturesobj = VendorProduct_ProductFeatures.objects.filter(
                vendor_products_id=vendorobj[0].get('vendor_product_id')).values().order_by('id')
            vendordocumentsobj = VendorProduct_Documents.objects.filter(
                vendor_products_id=vendorobj[0].get('vendor_product_id')).values().order_by('id')
            vendorproductalldata = list(chain(vendorproductobj, vendorproductgeneraldetailsobj,vendortechincalobj,vendorproductfeaturesobj,vendordocumentsobj))

            return Response({'status': 200, 'message': 'Vendor Product List','data':vendorproductalldata}, status=200)
        else:
            return Response({'status': 204, 'message': 'Data Not Present'}, status=204)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def landing_page_listing_leads_closed_list(request):
    data=request.data
    userid=data['userid']
    vendorproductarray=[]
    try:
        openleadslistobj=LandingPageBidding.objects.filter(vendor_user_id=userid,status='Pending').values().order_by('id')
        if len(openleadslistobj)>0:
            for i in range(0,len(openleadslistobj)):
                deadlinedateval = datetime.strptime(openleadslistobj[i].get('deadline_date'), '%Y-%m-%d')
                deadlinedateconvertion = datetime.date(deadlinedateval)
                todaydate = date.today()
                if deadlinedateconvertion < todaydate:
                    print('s')
                    vendorproductarray.append({'id':openleadslistobj[i].get('id'),
                                               'publish_date':openleadslistobj[i].get('publish_date'),
                                               'deadline_date': openleadslistobj[i].get('deadline_date'),
                                               'delivery_terms': openleadslistobj[i].get('delivery_terms'),
                                               'packaging_forwarding': openleadslistobj[i].get('packaging_forwarding'),
                                               'priority': openleadslistobj[i].get('priority'),
                                               'payment_terms': openleadslistobj[i].get('payment_terms'),
                                               'quantity': openleadslistobj[i].get('quantity'),
                                               'vendor_product_pk': openleadslistobj[i].get('vendor_product_pk'),
                                               'item_type': openleadslistobj[i].get('item_type'),
                                               'vendors_code': openleadslistobj[i].get('vendors_code'),
                                               'created_by': openleadslistobj[i].get('created_by'),
                                               'updated_by': openleadslistobj[i].get('updated_by'),
                                               'company_name': openleadslistobj[i].get('company_name'),
                                               'status': openleadslistobj[i].get('status'),
                                               'product_name': openleadslistobj[i].get('product_name'),
                                               'vendor_user_id': openleadslistobj[i].get('vendor_user_id')
                                               })
                else:
                    print('deadline is expired')

            return Response({'status': 200, 'message': 'Open Leads List of Listing Leads','data':vendorproductarray}, status=200)
        else:
            return Response({'status':204,'message':'Data Not Present','data':vendorproductarray},status=204)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def fetch_general_details_by_foreign_key(request):

    data=request.data
    vendorproductid=data['vendorproductid']
    try:
        vendorgeneraldetailsobj=VendorProduct_GeneralDetails.objects.filter(vendor_products=vendorproductid).values().order_by('id')
        if len(vendorgeneraldetailsobj)>0:
            return Response({'status': 200, 'message': 'Vendor Product General Details List', 'data': vendorgeneraldetailsobj},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['post'])
def fetch_techincal_specification_by_foreign_key(request):
    data=request.data
    vendorproductid=data['vendorproductid']
    try:
        vendortechincalspecifiactionsobj=VendorProduct_TechnicalSpecifications.objects.filter(vendor_products=vendorproductid).values().order_by('id')
        if len(vendortechincalspecifiactionsobj)>0:
            return Response({'status': 200, 'message': 'Vendor Product Technical Specification Details List', 'data': vendortechincalspecifiactionsobj},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['post'])
def fetch_product_features_by_foreign_key(request):
    data=request.data
    vendorproductid=data['vendorproductid']
    try:
        vendorproductfeaturesobj=VendorProduct_ProductFeatures.objects.filter(vendor_products_id=vendorproductid).values().order_by('id')
        if len(vendorproductfeaturesobj)>0:
            return Response({'status': 200, 'message': 'Vendor Product Features Details List', 'data': vendorproductfeaturesobj},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['post'])
def fetch_product_documents_foreign_key(request):
    data=request.data
    vendorproductid=data['vendorproductid']
    try:
        vendorproductdocumentsobj=VendorProduct_Documents.objects.filter(vendor_products_id=vendorproductid).values().order_by('id')
        if len(vendorproductdocumentsobj)>0:
            return Response({'status': 200, 'message': 'Vendor Product Documents Details List', 'data': vendorproductdocumentsobj},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['post'])
def get_landing_page_bidding_list_response(request):
    data=request.data
    userid = data['userid']
    resarry = []
    try:
        landingpageobj=LandingPageBidding.objects.filter(updated_by_id=userid).values()
        print(len(landingpageobj))
        if len(landingpageobj)>0:
            for i in range(0,len(landingpageobj)):
                print(landingpageobj[i].get('id'))
                listpublishobj=LandingPageBidding_Publish.objects.filter(listing_leads=landingpageobj[i].get('id')).values()
                print('publis----------',len(listpublishobj))
                if listpublishobj:
                    resarry.append({'type':listpublishobj[i].get('item_type'),
                                    'item_name':listpublishobj[i].get('item_name'),
                                    'description':listpublishobj[i].get('item_description'),
                                    'UOM':listpublishobj[i].get('uom'),
                                    'qty':listpublishobj[i].get('quantity'),
                                    'publishcount':len(listpublishobj)})

            return Response({'status': 200,'message':'ok','data':resarry},status=200)
        else:
            return Response({'status': 204, 'message': 'Not Present', 'data': []}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def fetch_vendor_product_details_by_pk(request):
    data=request.data
    vendorpk=data['vendorpk']
    try:
        vendorobj=VendorProduct_BasicDetails.objects.filter(vendor_product_id=vendorpk).values()
        if len(vendorobj)>0:
            vendorproductobj=VendorProduct_BasicDetails.objects.filter(vendor_product_id=vendorobj[0].get('vendor_product_id')).values().order_by('vendor_product_id')
            vendorproductgeneraldetailsobj=VendorProduct_GeneralDetails.objects.filter(vendor_products_id=vendorobj[0].get('vendor_product_id')).values().order_by('id')
            vendortechincalobj = VendorProduct_TechnicalSpecifications.objects.filter(
                vendor_products_id=vendorobj[0].get('vendor_product_id')).values().order_by('id')
            vendorproductfeaturesobj = VendorProduct_ProductFeatures.objects.filter(
                vendor_products_id=vendorobj[0].get('vendor_product_id')).values().order_by('id')
            vendordocumentsobj = VendorProduct_Documents.objects.filter(
                vendor_products_id=vendorobj[0].get('vendor_product_id')).values().order_by('id')
            vendorproductalldata = list(chain(vendorproductobj, vendorproductgeneraldetailsobj,vendortechincalobj,vendorproductfeaturesobj,vendordocumentsobj))

            return Response({'status': 200, 'message': 'Vendor Product List','data':vendorproductalldata}, status=200)
        else:
            return Response({'status': 204, 'message': 'Data Not Present'}, status=204)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def get_landing_page_bidding_by_pid(request):
    try:
        getlistbyuserid=LandingPageBidding.objects.filter(id=request.data['id']).values()
        if len(getlistbyuserid)>0:
            return Response({'status': 200, 'message': 'Buyer Post rfq list by id','data':getlistbyuserid}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'Buyer Post rfq list is not present'},
                            status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def get_buyer_award_details_by_userid(request):
    awardarray=[]
    try:
        getawardobj=awardpostedRFQ.objects.filter(updated_by_id=request.data['updated_by_id']).values().order_by('id')
        if len(getawardobj)>0:
            for i in range(0,len(getawardobj)):
                # print(getawardobj[i].get('landingpage_bidding_id_id'),'--------------------------------------------')
                awardobj=LandingPageBidding.objects.filter(id=getawardobj[i].get('landingpage_bidding_id_id')).values().order_by('id')
                userid = awardobj[0].get('updated_by_id')
                print(userid)
                basicobj = BasicCompanyDetails.objects.filter(updated_by_id=userid).values()
                cname = basicobj[0].get('company_name')
                code = basicobj[0].get('company_code')
                print(cname, 'company name')
                if len(awardobj)>0:
                    landingpagepublish=LandingPageBidding_Publish.objects.filter(listing_leads_id=awardobj[0].get('id')).values()
                    if len(landingpagepublish)>0:
                        awardarray.append({'cname':cname,
                                           'code':code,
                                           'item_name':landingpagepublish[0].get('item_name'),
                                           'quantity':getawardobj[0].get('quantity'),
                                           'buyer_publish_date':getawardobj[0].get('buyer_publish_date'),
                                           'buyer_deadLine_date':getawardobj[0].get('buyer_deadLine_date'),
                                           'po_status':getawardobj[0].get('po_status'),
                                           'item_description':landingpagepublish[0].get('item_description'),
                                           'total_amount':landingpagepublish[0].get('total_amount'),
                                           'userid': basicobj[0].get('updated_by_id'),
                                           'awarded_date':getawardobj[0].get('awarded_date')
                        })
                    else:
                        print('not present')
                        awardarray.append({'cname': cname,
                                           'code': code,
                                           'item_name': landingpagepublish[i].get('item_name'),
                                           'quantity': getawardobj[0].get('quantity'),
                                           'buyer_publish_date': getawardobj[0].get('buyer_publish_date'),
                                           'buyer_deadLine_date': getawardobj[0].get('buyer_deadLine_date'),
                                           'po_status': getawardobj[0].get('po_status'),
                                           'item_description': "",
                                           'total_amount': "",
                                           'userid': basicobj[0].get('updated_by_id'),
                                             'awarded_date':getawardobj[0].get('awarded_date')
                                           })
                else:
                    return Response({'status': 204, 'message': 'buyer award data not exist'},
                                        status=status.HTTP_204_NO_CONTENT)

            return Response({'status': 200, 'message': 'Award data','data':awardarray}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'Buyer Post rfq list is not present'},
                            status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


class LandingPageBiddingRFQ_SelectVendorSerializerview(viewsets.ModelViewSet):
    queryset = landingpagelistingleadsselectvendors.objects.all()
    serializer_class = LandingPageBiddingRFQ_SelectVendorSerializer

    def create(self, request, *args, **kwargs):
        LandingPageBiddingid=request.data.get('LandingPageBiddingid',None)
        vendor_product_pk=request.data.get('vendor_product_pk',None)
        try:
            landingobj=LandingPageBidding.objects.filter(id=LandingPageBiddingid).values()
            print(landingobj[0].get('vendor_product_pk'))
            vendorobj=VendorProduct_BasicDetails.objects.filter(vendor_product_id=landingobj[0].get('vendor_product_pk')).values()
            print(vendorobj[0].get('sub_category'))
            vendorproductdata=VendorProduct_BasicDetails.objects.filter(sub_category__icontains=vendorobj[0].get('sub_category')).values().order_by('vendor_product_id')
            for i in range(0,len(vendorproductdata)):
                selectlanding=landingpagelistingleadsselectvendors.objects.create(selectedvendorcode=vendorproductdata[i].get('company_code'),
                                                                                  vendor_product_pk=vendor_product_pk,
                                                                                  LandingPageBiddingid=LandingPageBidding.objects.get(id=LandingPageBiddingid)
                                                                                  )

            return Response({'status':201,'message':'Listing Leads Created'},status=201)


        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def pending_list_listing_leads(request):
    data=request.data
    userid=data['userid']
    landingarray=[]
    try:
        # landingpageobj = LandingPageBidding.objects.filter(vendor_user_id=userid).values()
        # print("len==",len(landingpageobj))
        #
        # if len(landingpageobj) > 0:
        basicobj1 = BasicCompanyDetails.objects.filter(updated_by_id=userid).values()
        if len(basicobj1)>0:
            landingvendors = landingpagelistingleadsselectvendors.objects.filter(selectedvendorcode=basicobj1[0].get('company_code'),listingstatus='Pending').values()
            if len(landingvendors)>0:
                for i in range(0,len(landingvendors)):

                    landingdata=LandingPageBidding.objects.filter(id=landingvendors[i].get('LandingPageBiddingid_id')).values()
                    print(landingdata[0].get('updated_by_id'))
                    vendorobj=VendorProduct_BasicDetails.objects.filter(vendor_product_id=landingdata[0].get('vendor_product_pk')).values()
                    basicobj = BasicCompanyDetails.objects.filter(updated_by_id=landingdata[0].get('updated_by_id')).values().order_by('company_code')
                    billingobj=BillingAddress.objects.filter(updated_by_id=basicobj[0].get('updated_by_id')).values().order_by('id')
                    landingarray.append({'company_code':basicobj[0].get('company_code'),
                                         'company_name': basicobj[0].get('company_name'),
                                         'city':billingobj[0].get('bill_city'),
                                         'item_name':vendorobj[0].get('item_name'),
                                         'item_description': vendorobj[0].get('item_description'),
                                         'uom':vendorobj[0].get('uom'),
                                         'quantity':landingdata[0].get('quantity'),
                                         'publish_date': landingdata[0].get('publish_date'),
                                         'deadline_date': landingdata[0].get('deadline_date'),
                                         'vendor_user_id': landingdata[0].get('vendor_user_id'),
                                         'landing_page_pk': landingdata[0].get('id'),
                                         'landing_vendors':landingvendors[i].get('id')
                                         })
                return Response({'status': 200, 'message': 'Listing Leads List','data':landingarray}, status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present','daata':landingarray},status=status.HTTP_204_NO_CONTENT)
        else:
            pass

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def update_status_from_pending_to_reject(request):
    data=request.data
    landing_pk=data['landing_pk']
    try:
        landingobj=landingpagelistingleadsselectvendors.objects.filter(id=landing_pk).values()
        if len(landingobj)>0:
            landingdata=landingpagelistingleadsselectvendors.objects.get(id=landingobj[0].get('id'))
            if landingdata.listingstatus=='Pending':
                landingdata.listingstatus='Reject'
                landingdata.save()
                return Response({'status': 200, 'message': 'Rejected'}, status=200)
            else:
                return Response({'status':202 , 'message': 'Status Already Rejected'}, status=202)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['put'])
def update_status_from_pending_to_published(request):
    data=request.data
    landing_pk=data['landing_pk']
    try:
        landingobj=landingpagelistingleadsselectvendors.objects.filter(id=landing_pk).values()
        if len(landingobj)>0:
            landingdata=landingpagelistingleadsselectvendors.objects.get(id=landingobj[0].get('id'))
            if landingdata.listingstatus=='Pending':
                landingdata.listingstatus='Published'
                landingdata.save()
                return Response({'status': 200, 'message': 'Status Changed to Published'}, status=200)
            else:
                return Response({'status':202 , 'message': 'Status Already Published'}, status=202)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def landing_page_listing_leads_rejected_list(request):
    data = request.data
    userid = data['userid']
    vendorproductarray = []
    try:
        openleadslistobj = LandingPageBidding.objects.filter(vendor_user_id=userid, status='Reject').values().order_by(
            'id')
        if len(openleadslistobj) > 0:
            for i in range(0, len(openleadslistobj)):
                # print(len(openleadslistobj),'leeeeeeeeeeeeeeeeeeeeeeee')
                # print(openleadslistobj[i].get('deadline_date'),'pok')
                deadlinedateval = datetime.strptime(openleadslistobj[i].get('deadline_date'), '%Y-%m-%d')
                deadlinedateconvertion = datetime.date(deadlinedateval)
                todaydate = date.today()
                if deadlinedateconvertion > todaydate:
                    print('yes')
                    # print(openleadslistobj[i].get('vendor_product_pk'),'ok')
                    vendorobj = VendorProduct_BasicDetails.objects.filter(
                        vendor_product_id=openleadslistobj[i].get('vendor_product_pk')).values()
                    if len(vendorobj) > 0:
                        basicobj = BasicCompanyDetails.objects.filter(
                            updated_by_id=openleadslistobj[i].get('updated_by_id')).values()
                        vendorproductarray.append({'id': openleadslistobj[i].get('id'),
                                                   'publish_date': openleadslistobj[i].get('publish_date'),
                                                   'deadline_date': openleadslistobj[i].get('deadline_date'),
                                                   'delivery_terms': openleadslistobj[i].get('delivery_terms'),
                                                   'packaging_forwarding': openleadslistobj[i].get(
                                                       'packaging_forwarding'),
                                                   'priority': openleadslistobj[i].get('priority'),
                                                   'payment_terms': openleadslistobj[i].get('payment_terms'),
                                                   'quantity': openleadslistobj[i].get('quantity'),
                                                   'vendor_product_pk': openleadslistobj[i].get('vendor_product_pk'),
                                                   'item_type': openleadslistobj[i].get('item_type'),
                                                   'vendors_code': basicobj[0].get('company_code'),
                                                   'created_by': openleadslistobj[i].get('created_by'),
                                                   'updated_by': openleadslistobj[i].get('updated_by'),
                                                   'company_name': basicobj[0].get('company_name'),
                                                   'status': openleadslistobj[i].get('status'),
                                                   'product_name': openleadslistobj[i].get('product_name'),
                                                   'vendor_user_id': openleadslistobj[i].get('vendor_user_id'),
                                                   'product_description': vendorobj[0].get('item_description'),
                                                   'uom': vendorobj[0].get('uom')
                                                   })
                    else:
                        pass
                else:
                    print('deadline is expired')

            return Response({'status': 200, 'message': 'Open Leads List of Listing Leads', 'data': vendorproductarray},
                            status=200)
        else:
            return Response({'status': 204, 'message': 'Data Not Present', 'data': vendorproductarray}, status=204)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def landing_page_published_list_by_user_id(request):
    data=request.data
    try:
        landingpublishobj=LandingPageBidding_Publish.objects.filter(updated_by_id=data['userid'],id=data['vendor_pk']).values().order_by('listing_leads_id')
        if len(landingpublishobj)>0:
            for i in range(0,len(landingpublishobj)):
                landingobj=LandingPageBidding.objects.filter(id=landingpublishobj[i].get('listing_leads_id')).values().order_by('id')
                basicobj = BasicCompanyDetails.objects.filter(updated_by_id=landingobj[0].get('updated_by_id')).values()
                billobj=BillingAddress.objects.filter(updated_by_id=landingobj[0].get('updated_by_id')).values()
                # print(basicobj[0].get('company_code'),'cccccccc')
                if len(landingobj)>0:
                    for j in range(0,len(landingobj)):
                        landingpublishobj[i].__setitem__('buyer_packaging_forwarding',landingobj[0].get('packaging_forwarding'))
                        landingpublishobj[i].__setitem__('buyer_payment_terms',
                                                         landingobj[0].get('payment_terms'))
                        landingpublishobj[i].__setitem__('buyer_delivery_terms',
                                                         landingobj[0].get('delivery_terms'))
                        landingpublishobj[i].__setitem__('buyer_pk',
                                                         landingobj[0].get('id'))
                        landingpublishobj[i].__setitem__('buyer_company_code',basicobj[0].get('company_code'))
                        landingpublishobj[i].__setitem__('buyer_company_name', basicobj[0].get('company_name'))
                        landingpublishobj[i].__setitem__('buyer_city', billobj[0].get('bill_city'))
                        landingpublishobj[i].__setitem__('publish_date',landingobj[0].get('publish_date'))
                else:
                    pass

            return Response({'status':200,'message':'ok','data':landingpublishobj},status=200)
        else:
            return Response({'status': 204, 'message': 'Data Not Present'}, status=204)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def landing_page_listing_leads_expired_list(request):
    data = request.data
    userid = data['userid']
    vendorproductarray = []
    try:
        openleadslistobj = LandingPageBidding.objects.filter(vendor_user_id=userid).values().order_by(
            'id')
        if len(openleadslistobj) > 0:
            for i in range(0, len(openleadslistobj)):
                deadlinedateval = datetime.strptime(openleadslistobj[i].get('deadline_date'), '%Y-%m-%d')
                deadlinedateconvertion = datetime.date(deadlinedateval)
                todaydate = date.today()
                if deadlinedateconvertion < todaydate:
                    print('yes')
                    vendorobj = VendorProduct_BasicDetails.objects.filter(
                        vendor_product_id=openleadslistobj[i].get('vendor_product_pk')).values()
                    if len(vendorobj) > 0:
                        basicobj = BasicCompanyDetails.objects.filter(
                            updated_by_id=openleadslistobj[i].get('updated_by_id')).values()
                        vendorproductarray.append({'id': openleadslistobj[i].get('id'),
                                                   'publish_date': openleadslistobj[i].get('publish_date'),
                                                   'deadline_date': openleadslistobj[i].get('deadline_date'),
                                                   'delivery_terms': openleadslistobj[i].get('delivery_terms'),
                                                   'packaging_forwarding': openleadslistobj[i].get(
                                                       'packaging_forwarding'),
                                                   'priority': openleadslistobj[i].get('priority'),
                                                   'payment_terms': openleadslistobj[i].get('payment_terms'),
                                                   'quantity': openleadslistobj[i].get('quantity'),
                                                   'vendor_product_pk': openleadslistobj[i].get('vendor_product_pk'),
                                                   'item_type': openleadslistobj[i].get('item_type'),
                                                   'vendors_code': basicobj[0].get('company_code'),
                                                   'created_by': openleadslistobj[i].get('created_by'),
                                                   'updated_by': openleadslistobj[i].get('updated_by'),
                                                   'company_name': basicobj[0].get('company_name'),
                                                   'status': openleadslistobj[i].get('status'),
                                                   'product_name': openleadslistobj[i].get('product_name'),
                                                   'vendor_user_id': openleadslistobj[i].get('vendor_user_id'),
                                                   'product_description': vendorobj[0].get('item_description'),
                                                   'uom': vendorobj[0].get('uom')
                                                   })
                    else:
                        pass
                else:
                    print('deadline is not expired')

            return Response({'status': 200, 'message': 'Open Leads Expired List of Listing Leads', 'data': vendorproductarray},
                            status=200)
        else:
            return Response({'status': 204, 'message': 'Data Not Present', 'data': vendorproductarray}, status=204)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def landing_page_published_list(request):
    data=request.data
    published_array=[]
    try:
        landingpublishobj=LandingPageBidding_Publish.objects.filter(updated_by_id=data['userid']).values().order_by('id')
        if len(landingpublishobj)>0:
            for i in range(0,len(landingpublishobj)):
                landingobj = LandingPageBidding.objects.filter(id=landingpublishobj[i].get('listing_leads_id')).values().order_by('id')
                basicobj=BasicCompanyDetails.objects.filter(updated_by_id=landingobj[0].get('updated_by_id')).values()
                landingpublishobj[i].__setitem__('buyer_company_name',
                                                 basicobj[0].get('company_name'))
                landingpublishobj[i].__setitem__('buyer_company_code',
                                                 basicobj[0].get('company_code'))

            return Response({'status':200,'message':'Published Listing Leads','data':landingpublishobj},status=200)
        else:
            return Response({'status': 204, 'message': 'Data Not Present'}, status=204)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['put'])
def updatelandingpagevendor_publish_update(request):
    data=request.data
    pkid=data['pkid']
    try:
        obj=LandingPageBidding_Publish.objects.get(id=pkid)
        if obj:
            obj.unit_rate=data['unit_rate']
            obj.tax=data['tax']
            obj.discount=data['discount']
            obj.total_amount=data['total_amount']
            obj.pf_charges=data['pf_charges']
            obj.payment_charges=data['payment_charges']
            obj.delivery_charges=data['delivery_charges']
            obj.save()

            return Response({'status': 200, 'message': 'Updated'}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def get_award_list_by_pk_value(request):
    data=request.data
    id=data['id']
    try:
        landingobj = LandingPageBidding_Publish.objects.filter(id=id).values().order_by('id')
        if len(landingobj)>0:
            return Response({'status': 200, 'message': 'Ok', 'data':landingobj}, status=200)
        else:
            return Response({'status': 204, 'message': 'Data Not Present'}, status=204)

    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)

@api_view(['put'])
def listing_leads_po_status_update(request):
    data = request.data
    awardpk = data['awardpk']
    try:
        awardobj = awardpostedRFQ.objects.filter(id=awardpk).values()
        if len(awardobj) > 0:
            awards = awardpostedRFQ.objects.get(id=awardpk)
            if awards.po_status == 'Pending':
                awards.po_status = 'PO_Sent'
                awards.save()
                return Response({'status': 200, 'message': 'Listing Leads PO sent successfully ', 'data': awards.po_status}, status=200)
            else:
                if awards.po_status=='PO_Sent':
                    return Response({'status': 202, 'message': 'PO Already Sent'}, status=202)
                else:
                    return Response({'status': 202, 'message': 'PO sent failed or po not sent'}, status=202)

        else:
            return Response({'status': 204, 'message': 'No data found'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


class LandingPageListingLeadsPurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = LandingPageListingLeadsPurchaseOrder.objects.all()
    serializer_class = LandingPageListingLeadsPurchaseOrderSerializer
    parser = [MultiPartParser]

    def create(self, request, *args, **kwargs):
        landing_page_publish_pk=request.data.get('landing_page_publish_pk',None)
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key[
            'api-key'] = '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'
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
        }
        landingobj=LandingPageBidding_Publish.objects.filter(id=landing_page_publish_pk).values()
        basicobj = BasicCompanyDetails.objects.get(company_code=landingobj[0].get('company_code'))
        regobj = SelfRegistration.objects.get(id=basicobj.updated_by_id)
        print(regobj.username, 'ok')
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": regobj.username, "name": regobj.contact_person}],
            template_id=24, params={
                "itemname":request.data['item_name'],
                "itemdescription":request.data['item_description'],
                "podate": request.data['PO_date'],
                "ponum": request.data['PO_num'],
                "poexpires": request.data['PO_expirydate'],
                "quantity":landingobj[0].get('quantity'),
                "companyname": basicobj.company_name
            },
            headers=headers,
            subject='PO Confirmation'
        )  # SendSmtpEmail | Values to send a transactional email
        # Send a transactional email
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        poobj = LandingPageListingLeadsPurchaseOrder.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by('id')
        if poobj:
            return poobj
        raise ValidationError(
            {'message': 'Listing leads Purchase Order details of particular user id is not exist', 'status': 204})



@api_view(['post'])
@permission_classes([AllowAny, ])
def main_cat_subcat_data(request):
    data = request.data
    main_coreid = data['maincore_id']
    cat_id= data['cat_id']
    sub_cat_text = data['sub_cat_text']
    try:
        maincoredetails=MaincoreMaster.objects.filter(maincore_id=main_coreid).values()
        category_text = CategoryMaster.objects.filter(category_id=cat_id).values()
        if maincoredetails:
            if category_text:
                SubProdDetaile_data=VendorProduct_BasicDetails.objects.filter(core_sector=maincoredetails[0].get('maincore_name'),category=category_text[0].get('category_name'),sub_category=sub_cat_text).values()
                CatProdDetaile_data=VendorProduct_BasicDetails.objects.filter(core_sector=maincoredetails[0].get('maincore_name'),category=category_text[0].get('category_name')).values()
        return Response({'status': 200, 'message': 'Ok', 'subcategoryproducts': SubProdDetaile_data,'categoryproducts': CatProdDetaile_data,}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


class LandingPageBidding_PublishViewSet(viewsets.ModelViewSet):
    queryset = LandingPageBidding_Publish.objects.all()
    serializer_class = LandingPageBidding_PublishSerializer

    def create(self, request, *args, **kwargs):
        # listing_leads=request.data.get('listing_leads',None)
        # print(listing_leads)
        total_amount=float(request.data['total_amount'])
        arraydata=[]
        list1=[]
        listobj = LandingPageBidding.objects.filter(id=request.data['listing_leads']).values()
        print(listobj[0].get('id'))
        if len(listobj) > 0:
            listval = LandingPageBidding.objects.get(id=listobj[0].get('id'))
            if listval.status == 'Pending':
                listval.status = 'Published'
                listval.save()

            publishobj =LandingPageBidding_Publish.objects.filter(updated_by=request.data['updated_by'],listing_leads=request.data['listing_leads']).values().order_by('total_amount')
            for i in range(0,len(publishobj)):
                print(type(publishobj[0].get('total_amount')))
                x=float(publishobj[i].get('total_amount'))
                print(type(x),'xxxxxxxxxx type')
                arraydata.append(x)
                arraydata.sort(reverse=True)
            print(arraydata)
            l1=arraydata[0]
            l2=arraydata[1]
            l3=arraydata[2]
            print(l1,l2,l3)
            if total_amount <l1 and total_amount<l2 and total_amount<l3:
                basic = BasicCompanyDetails.objects.get(company_code=request.data['company_code'])
                print(basic.company_code, 'fdfdf')
                regobj = SelfRegistration.objects.get(id=basic.updated_by_id)
                print(regobj.username)
                configuration = sib_api_v3_sdk.Configuration()
                configuration.api_key[
                    'api-key'] = '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'

                api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
                subject = "Published  RFQ"
                text_content = "Dear " + regobj.contact_person + "\n\n" + "Your  " + basic.company_name + " company is published." + "\n\n" + "NOTE: Please Don't Share this to anyone"
                sender = {"name": "VENDORSIN COMMERCE PRIVATE LIMITED", "email": "admin@vendorsin.com"}
                # text_content = 'Hello '+regobj.contact_person+',''\n You are selected for bidding'
                to = [{"email": regobj.username, "name": regobj.contact_person}]
                reply_to = {"email": "admin@vendorsin.com", "name": "Admin"}
                send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=reply_to, text_content=text_content,
                                                               sender=sender, subject=subject)
                print(send_smtp_email)
                api_response = api_instance.send_transac_email(send_smtp_email)
                pprint(api_response)
                return super().create(request, *args, **kwargs)
            else:
                return Response({'status':202,'message':'Top published datas are already present'},status=202)

            # basic = BasicCompanyDetails.objects.get(company_code=request.data['company_code'])
            # print(basic.company_code, 'fdfdf')
            # regobj = SelfRegistration.objects.get(id=basic.updated_by_id)
            # print(regobj.username)
            # configuration = sib_api_v3_sdk.Configuration()
            # configuration.api_key[
            #     'api-key'] = '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'
            #
            # api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
            # subject = "Published  RFQ"
            # text_content = "Dear " + regobj.contact_person + "\n\n" + "Your  " + basic.company_name + " company is published." + "\n\n" + "NOTE: Please Don't Share this to anyone"
            # sender = {"name": "VENDORSIN COMMERCE PRIVATE LIMITED", "email": "admin@vendorsin.com"}
            # # text_content = 'Hello '+regobj.contact_person+',''\n You are selected for bidding'
            # to = [{"email": regobj.username, "name": regobj.contact_person}]
            # reply_to = {"email": "admin@vendorsin.com", "name": "Admin"}
            # send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=reply_to, text_content=text_content,
            #                                                sender=sender, subject=subject)
            # print(send_smtp_email)
            # api_response = api_instance.send_transac_email(send_smtp_email)
            # pprint(api_response)
            # return super().create(request, *args, **kwargs)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=204)

    def get_queryset(self):
        landingpageobj = LandingPageBidding_Publish.objects.filter(
            updated_by=self.request.GET.get('updated_by')).order_by('id')
        if landingpageobj:
            return landingpageobj
        raise ValidationError({'message': 'landing Page details of particular user id is not exist', 'status': 204})

@api_view(['post'])
def store_vendor_publish(request):
    try:
        data=request.data
        listing_leads=data['listing_leads']
        updated_by=data['updated_by']
        total_amount=data['total_amount']
        i=0
        count=0
        Vendor_publish_obj=LandingPageBidding_Publish.objects.filter(listing_leads=listing_leads).values().order_by('total_amount')
        if len(Vendor_publish_obj)>3:
            while i<len(Vendor_publish_obj):
                print(Vendor_publish_obj[i].get('total_amount'))
                if  float(total_amount)>float(Vendor_publish_obj[i].get('total_amount')):
                    count=count+1
                    if count==3:
                        return Response({'status': 202, 'message': 'Upto level 3 data exist'}, status=202)
                i=i+1
            if count<3:
                LandingPageBidding_Publish.objects.create(item_type=data['item_type'],
                                                          company_name=data['company_name'],
                                                          company_code=data['company_code'], priority=data['priority'],
                                                          deadline_date=data['deadline_date'],
                                                          item_name=data['item_name'],
                                                          item_description=data['item_description'], uom=data['uom'],
                                                          quantity=data['quantity'], hsn_sac=['hsn_sac'],
                                                          category=data['category'],
                                                          unit_rate=data['unit_rate'], tax=data['tax'],
                                                          discount=data['discount'],
                                                          total_amount=data['total_amount'],
                                                          pf_charges=data['pf_charges'],
                                                          payment_charges=data['payment_charges'],
                                                          delivery_charges=data['delivery_charges'],
                                                          listing_leads=LandingPageBidding.objects.get(id=data['listing_leads']), created_by=updated_by,
                                                          updated_by=SelfRegistration.objects.get(id=updated_by))
        else:
            LandingPageBidding_Publish.objects.create(item_type=data['item_type'],company_name=data['company_name'],
                                                      company_code=data['company_code'],priority=data['priority'],
                                                      deadline_date=data['deadline_date'],item_name=data['item_name'],
                                                      item_description=data['item_description'],uom=data['uom'],
                                                      quantity=data['quantity'],hsn_sac=['hsn_sac'],category=data['category'],
                                                      unit_rate=data['unit_rate'],tax=data['tax'],discount=data['discount'],
                                                      total_amount=data['total_amount'],pf_charges=data['pf_charges'],
                                                      payment_charges=data['payment_charges'],delivery_charges=data['delivery_charges'],
                                                      listing_leads=LandingPageBidding.objects.get(id=data['listing_leads']),
                                                      created_by=updated_by,
                                                      updated_by=SelfRegistration.objects.get(id=updated_by))
        return Response({'status': 200, 'message': 'ok'}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def vendor_product_details_based_on_itemtype(request):
    data= request.data
    try:
        if data['token'] == "vsinadmindb":
            product_details_data =VendorProduct_BasicDetails.objects.filter(item_type='Service').values()
            return Response({'status': 200, 'message': 'ok', 'product_details_data':product_details_data}, status=200)
        else:
            return Response({'status': 400, 'message': 'Bad request'}, status=400)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
@permission_classes((AllowAny,))
def fetch_vendor_product_basic_details_by_ccode(request):
    data=request.data
    key=data['key']
    try:
        if key=='vsinadmin':
            basicobj=BasicCompanyDetails.objects.filter(company_code=data['company_code']).values()
            vendorobj=VendorProduct_BasicDetails.objects.filter(updated_by_id=basicobj[0].get('updated_by_id')).values().order_by('vendor_product_id')
            if len(vendorobj)>0:
                return Response({'status': 200, 'message': 'Vendor Product Basic Details List', 'data': vendorobj}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return  Response({'status':401,'message':'UnAuthorized'},status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['post'])
@permission_classes((AllowAny,))
def get_vendor_product_details_based_on_ccode_distinct(request):
    data=request.data
    key=data['key']
    ccode=data['ccode']
    resarray=[]
    newval=[]
    try:
        if key=='vsinadmin':
            vendorobj=VendorProduct_BasicDetails.objects.filter(company_code=ccode).distinct('core_sector','category','sub_category','company_code').values()
            if len(vendorobj)>0:
                for i in range(0,len(vendorobj)):
                    maincoreobj=MaincoreMaster.objects.filter(maincore_name=vendorobj[i].get('core_sector')).values()
                    categoryobj = CategoryMaster.objects.filter(category_name=vendorobj[i].get('category')).values()
                    subcategoryobj = SubCategoryMaster.objects.filter(sub_category_name=vendorobj[i].get('sub_category')).values()
                    resarray.append({
                        'maincore':vendorobj[i].get('core_sector'),
                        'maincore_id':maincoreobj[0].get('maincore_id'),
                        'mainore_image':maincoreobj[0].get('maincore_image'),
                        'category': vendorobj[i].get('category'),
                        'category_id': categoryobj[0].get('category_id'),
                        'category_image': categoryobj[0].get('category_image'),
                        'sub_category': vendorobj[i].get('sub_category'),
                        'sub_category_id':subcategoryobj[0].get('sub_category_id'),
                        'sub_category_image': subcategoryobj[0].get('sub_category_image'),
                        'company_code':vendorobj[i].get('company_code')



                    })
                return Response({'status': 200, 'message': 'Vendor Product Basic Details List', 'data': resarray},
                                status=status.HTTP_200_OK)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({'status': 401, 'message': 'UnAuthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['post'])
@permission_classes((AllowAny,))
def get_vendor_product_details_difference_industry_category(request):
    data=request.data
    key=data['key']
    ccode=data['ccode']
    resarray=[]
    newval=[]
    try:
        if key=="vsinadmin":
            vendorobjmaincore=VendorProduct_BasicDetails.objects.filter(company_code=ccode).distinct('core_sector').values()
            vendorobjcategory=VendorProduct_BasicDetails.objects.filter(company_code=ccode).distinct('category').values()
            vendorobjsubcategory=VendorProduct_BasicDetails.objects.filter(company_code=ccode).distinct('sub_category').values()
        return Response({'status': 200, 'message': 'Vendor Product Basic Details List', 'maincore': vendorobjmaincore,
                        'category':vendorobjcategory,'Subcategory':vendorobjsubcategory},
                    status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['post'])
@permission_classes((AllowAny,))
def get_vendor_product_details_based_on_maincore(request):
    data=request.data
    key=data['key']
    ccode=data['ccode']
    maincore=data['maincore']
    resarray=[]
    newval=[]
    try:
        if key=="vsinadmin":
            vendorobjmaincore=VendorProduct_BasicDetails.objects.filter(company_code=ccode,core_sector=maincore).values()

        return Response({'status': 200, 'message': 'Vendor Product Basic Details List', 'maincore': vendorobjmaincore},
                    status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['post'])
@permission_classes((AllowAny,))
def get_vendor_product_details_based_on_category(request):
    data=request.data
    key=data['key']
    ccode=data['ccode']
    category=data['category']
    resarray=[]
    newval=[]
    try:
        if key=="vsinadmin":
            vendorobjcategory=VendorProduct_BasicDetails.objects.filter(company_code=ccode,category=category).values()

        return Response({'status': 200, 'message': 'Vendor Product Basic Details List', 'category': vendorobjcategory},
                    status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['post'])
@permission_classes((AllowAny,))
def get_vendor_product_details_based_on_subcategory(request):
    data=request.data
    key=data['key']
    ccode=data['ccode']
    sub_category=data['sub_category']
    resarray=[]
    newval=[]
    try:
        if key=="vsinadmin":
            vendorobjcategory=VendorProduct_BasicDetails.objects.filter(company_code=ccode,sub_category=sub_category).distinct().values()
            if len(vendorobjcategory)>0:
                return Response({'status': 200, 'message': 'Vendor Product Basic Details List', 'category': vendorobjcategory},
                                status=status.HTTP_200_OK)
            else:
                return Response(
                    {'status': 204, 'message': 'Data Not Present'},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'status': 401, 'message': 'UnAuthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['post'])
@permission_classes((AllowAny,))
def get_vendor_product_details_based_on_main_id_cat_id_subcat_name(request):
    data=request.data
    key=data['key']
    main_core_id=data['main_core_id']
    cat_id=data['cat_id']
    sub_cat_name=data['sub_cat_name']
    try:
        if key == "vsinadmin":
            vendorprodata1=MaincoreMaster.objects.filter(maincore_id=main_core_id).values()
            vendorprodata2 = CategoryMaster.objects.filter(category_id=cat_id).values()
            vendorprodata3 = SubCategoryMaster.objects.filter(sub_category_name=sub_cat_name).values()
            if vendorprodata1:
                if vendorprodata2:
                    if vendorprodata3:
                        vendorprodata4=VendorProduct_BasicDetails.objects.filter(core_sector=vendorprodata1[0].get('maincore_name'),category=vendorprodata2[0].get('category_name'),sub_category=vendorprodata3[0].get('sub_category_name')).values()
                        if len(vendorprodata4)>0:
                            return Response({'status': 200, 'message': 'ok', 'data': vendorprodata4},
                                            status=status.HTTP_200_OK)
                        else:
                            return Response({'status': 204, 'message': 'ok', 'data': 'Vendor Product Details Not Present'},
                                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'status': 401, 'message':'UnAuthorized'},
                            status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['post'])
@permission_classes((AllowAny,))
def get_vendor_product_details_by_pk(request):
    data=request.data
    key=data['key']
    vendorpk=data['vendorpk']
    try:

        if key == "vsinadmindb":
            vendor_product_basic_details = VendorProduct_BasicDetails.objects.filter(
                vendor_product_id=vendorpk).values().order_by('vendor_product_id')
            vendor_product_general_details = VendorProduct_GeneralDetails.objects.filter(
                vendor_products=vendorpk).values().order_by('vendor_products')
            vendor_product_technical_specifications = VendorProduct_TechnicalSpecifications.objects.filter(
                vendor_products=vendorpk).values().order_by('vendor_products')
            vendor_product_features = VendorProduct_ProductFeatures.objects.filter(
                vendor_products=vendorpk).values().order_by('vendor_products')
            vendor_product_documents = VendorProduct_Documents.objects.filter(vendor_products=vendorpk).values().order_by(
                'vendor_products')
            if len(vendor_product_basic_details)>0:
                return Response({'status': 200, 'message': 'ok',
                                 'vendor_product_basic_details': vendor_product_basic_details,
                                 'vendor_product_general_details': vendor_product_general_details,
                                 'vendor_product_technical_specifications': vendor_product_technical_specifications,
                                 'vendor_product_features': vendor_product_features,
                                 'vendor_product_documents': vendor_product_documents},
                                status=status.HTTP_200_OK)
            else:
                return Response({'status': 204, 'message': 'vendor product basic details are not present'},
                                status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'status': 401, 'message': 'UnAuthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['post'])
@permission_classes((AllowAny,))
def get_admin_added_vendor_product_details(request):
    data=request.data
    key=data['key']
    admin_create=data['admin_create']
    try:
        if key=='vsinadmindb':
            vendorobj=VendorProduct_BasicDetails.objects.filter(admin_create=True).values().order_by('vendor_product_id')
            if len(vendorobj):
                return Response({'status':200,'message':'Admin Create Product Details List','data':vendorobj},status=200)
            else:
                return Response({'status': 204, 'message': 'Admin Create Product Details List Not Present', 'data': vendorobj},
                                status=204)
        else:
            return Response({'status': 401, 'message': 'UnAuthorized'}, status=status.HTTP_401_UNAUTHORIZED)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['put'])
def edit_technical_specifications(request):
    data = request.data
    technicaldetailslist = data['technicaldetails']
    updated_by =data['updated_by']
    vendor_products =data['vendor_products']
    try:
         for i in range(0,len(technicaldetailslist)):
             print(len(technicaldetailslist))
             vendorobj=VendorProduct_TechnicalSpecifications.objects.filter(vendor_products_id=vendor_products,updated_by_id=updated_by).values().order_by('id')
             if len(vendorobj)>0:
                 print(vendorobj[i].get('id'))
                 vendorvalue=VendorProduct_TechnicalSpecifications.objects.get(id=vendorobj[i].get('id'))
                 if vendorvalue.item_specification!=technicaldetailslist[i].get('item_specification'):
                     vendorvalue.item_specification=technicaldetailslist[i].get('item_specification')
                     vendorvalue.save()
                 if vendorvalue.item_description != technicaldetailslist[i].get('item_description'):
                     vendorvalue.item_description = technicaldetailslist[i].get('item_description')
                     vendorvalue.save()
             else:
                 print('not present')
         return Response({'status': 202, 'message': 'Vendor Product Technical Specifications Are Updated'}, status=202)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['PUT'])
@permission_classes((AllowAny,))
def update_vendor_product_basic_details(request,vendor_product_id=None):
    if request.data['key']=='vsinadmindb':
        try:
            vendorobj=VendorProduct_BasicDetails.objects.get(vendor_product_id=vendor_product_id)
        except VendorProduct_BasicDetails.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method=='PUT':
            serializer=VendorProduct_BasicDetailsSerializer(vendorobj,request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return  Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'status':401,'message':'UnAuthorized'},status=status.HTTP_401_UNAUTHORIZED)