from itertools import chain

from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from RegistrationApp.models import SelfRegistration, IndustrialInfo, BillingAddress
from .models import *

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
            productobj=BuyerProductDetails.objects.filter(updated_by=userid,buyer_item_type=itemtype).values().order_by('buyer_product_id')
            if len(productobj)>0:
                return Response({'status': 200, 'message': 'Buyer Product List','data':productobj}, status=200)
            else:
                return Response({'status': 202, 'message': 'Not Present'}, status=202)

        elif itemtype == 'Service':
            productobjservice = BuyerServiceDetails.objects.filter(updated_by=userid,
                                                            buyer_service_item_type=itemtype).values().order_by('buyer_service_id')
            if len(productobjservice)>0:
                return Response({'status': 200, 'message': 'Buyer Service List', 'data': productobjservice}, status=200)
            else:
                return Response({'status': 202, 'message': 'Not Present'}, status=202)
        elif itemtype == 'Machinary & equipments':
            productobjmachinary = BuyerMachinaryDetails.objects.filter(updated_by=userid,
                                                                   buyer_machinary_item_type=itemtype).values().order_by('buyer_machinary_id')
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
        buyer_additional_specifications = request.data.get('buyer_additional_specifications',None)
        buyer_add_product_supplies = request.data.get('buyer_add_product_supplies',None)
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
                                                                  buyer_additional_specifications=buyer_additional_specifications,
                                                                  buyer_add_product_supplies=buyer_add_product_supplies,
                                                                  updated_by=SelfRegistration.objects.get(id=userid),
                                                                  created_by=userid)
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
                                                                  buyer_additional_specifications=buyer_additional_specifications,
                                                                  buyer_add_product_supplies=buyer_add_product_supplies,
                                                                  updated_by=SelfRegistration.objects.get(id=userid),
                                                                  created_by=userid)
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
        buyer_service_additional_specifications = request.data.get('buyer_service_additional_specifications',None)
        buyer_service_add_product_supplies = request.data.get('buyer_service_add_product_supplies',None)
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
                                                                  buyer_service_additional_specifications=buyer_service_additional_specifications,
                                                                  buyer_service_add_product_supplies=buyer_service_add_product_supplies,
                                                                  updated_by=SelfRegistration.objects.get(id=userid),
                                                                  created_by=userid)
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
                                                                  buyer_service_additional_specifications=buyer_service_additional_specifications,
                                                                  buyer_service_add_product_supplies=buyer_service_add_product_supplies,
                                                                  updated_by=SelfRegistration.objects.get(id=userid),
                                                                  created_by=userid)
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
        buyer_machinary_additional_specifications = request.data.get('buyer_machinary_additional_specifications',None)
        buyer_machinary_add_product_supplies = request.data.get('buyer_machinary_add_product_supplies',None)
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
                                                                  buyer_machinary_additional_specifications=buyer_machinary_additional_specifications,
                                                                  buyer_machinary_add_product_supplies=buyer_machinary_add_product_supplies,
                                                                  updated_by=SelfRegistration.objects.get(id=userid),
                                                                  created_by=userid)
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
                                                                  buyer_machinary_additional_specifications=buyer_machinary_additional_specifications,
                                                                  buyer_machinary_add_product_supplies=buyer_machinary_add_product_supplies,
                                                                  updated_by=SelfRegistration.objects.get(id=userid),
                                                                  created_by=userid)
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

                    if productobjget.buyer_document != buyer_document:
                        productobjget.buyer_document = buyer_document
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

@api_view(['post'])
@permission_classes((AllowAny,))
def get_vendor_details_by_sub_category(request):
    data=request.data
    subcategoryname=data['subcategoryname']
    vendordetails=[]
    ccodearray=[]
    try:
        vendorobj = VendorProduct_BasicDetails.objects.filter(sub_category__icontains=subcategoryname).distinct('sub_category','company_code').values()
        for i in range(0,len(vendorobj)):
            basicobj=BasicCompanyDetails.objects.get(company_code=vendorobj[i].get('company_code'))
            regobj=SelfRegistration.objects.filter(id=basicobj.updated_by_id).values()
            industryobj=IndustrialInfo.objects.get(company_code=vendorobj[i].get('company_code'))
            billobj=BillingAddress.objects.filter(company_code_id=vendorobj[i].get('company_code')).values()
            vendordetails.append({
                'company_name':basicobj.company_name,
                'name': regobj[0].get('contact_person'),
                'email':regobj[0].get('username'),
                'phone_number':regobj[0].get('phone_number'),
                'profile_photo': regobj[0].get('profile_cover_photo'),
                'city':billobj[0].get('bill_city')
                # 'nature_of_business':industryobj.nature_of_business,
                # 'industry_to_serve':industryobj.industry_to_serve
            })
        return Response({'status': 200, 'message': 'ok','data':vendordetails},status=status.HTTP_200_OK)


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

