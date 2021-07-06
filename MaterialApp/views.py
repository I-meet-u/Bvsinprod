from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from RegistrationApp.models import SelfRegistration
from .models import VendorProduct_BasicDetails, VendorProduct_GeneralDetails, VendorProduct_TechnicalSpecifications, \
    VendorProduct_ProductFeatures, VendorProduct_Documents, BuyerProductDetails

from .serializers import VendorProduct_BasicDetailsSerializer, VendorProduct_GeneralDetailsSerializer, \
    VendorProduct_TechnicalSpecificationsSerialzer, VendorProduct_ProductFeaturesSerializer, \
    VendorProduct_DocumentsSerializer, BuyerProductDetailsSerializer


# class VendorProduct_BasicDetailsView(viewsets.ModelViewSet):
#     queryset = VendorProduct_BasicDetails.objects.all()
#     serializer_class = VendorProduct_BasicDetailsSerializer
#
#     def create(self, request, *args, **kwargs):
#         data=request.data
#         core_sector = data['core_sector']
#         category = data['category']
#         sub_category = data['sub_category']
#         product_category = data['product_category']
#         product_type=data['product_type']
#         item_type = data['item_type']
#         item_name = data['item_name']
#         item_description=data['item_description']
#         final_selling_price = data['final_selling_price']
#         add_image1 = data['add_image1']
#         add_image2 = data['add_image2']
#         add_image3 = data['add_image3']
#         add_image4 = data['add_image4']
#         uom = data['uom']
#         quantity = data['quantity']
#         hsn_sac = data['hsn_sac']
#         unit_price = data['unit_price']
#         discount = data['discount']
#         tax = data['tax']
#         sku_id = data['sku_id']
#         country_of_origin = data['country_of_origin']
#         currency = data['currency']
#         userid = data['userid']
#         type = data['type']
#         try:
#
#             vedordetailsobj = VendorProduct_BasicDetails.objects.filter(updated_by=userid).order_by('-numeric').values()
#             if type == 'auto':
#                 if vedordetailsobj:
#                     vendorobj = VendorProduct_BasicDetails.objects.create(core_sector=core_sector, category=category,sub_category=sub_category,product_category=product_category,product_type=product_type,item_type=item_type,item_code=vedordetailsobj[0].get('numeric'),item_name=item_name,item_description=item_description,
#                                                                           final_selling_price=final_selling_price,
#                                                                           numeric=vedordetailsobj[0].get('numeric') + 1,add_image1=add_image1, add_image2=add_image2,add_image3=add_image3, add_image4=add_image4,
#                                                                           uom=uom, quantity=quantity, hsn_sac=hsn_sac,unit_price=unit_price, discount=discount, tax=tax,sku_id=sku_id,country_of_origin=country_of_origin,
#                                                                           currency=currency,created_by=userid,updated_by=SelfRegistration.objects.get(id=userid))
#                 else:
#                     print('not exist')
#                     vendorobj = VendorProduct_BasicDetails.objects.create(core_sector=core_sector, category=category,sub_category=sub_category,product_category=product_category,product_type=product_type,item_type=item_type, item_code=100001,item_name=item_name,item_description=item_description,
#                                                                           final_selling_price=final_selling_price,numeric=100002, add_image1=add_image1,add_image2=add_image2, add_image3=add_image3,add_image4=add_image4,
#                                                                           uom=uom, quantity=quantity,hsn_sac=hsn_sac,unit_price=unit_price,discount=discount, tax=tax, sku_id=sku_id,
#                                                                           country_of_origin=country_of_origin,currency=currency,created_by=userid,
#                                                                           updated_by=SelfRegistration.objects.get(id=userid))
#             if type == 'manual':
#                 item_code = data['item_code']
#                 vendorobj=VendorProduct_BasicDetails.objects.count()
#                 if vendorobj==0:
#                     print('s')
#                     vendorobj = VendorProduct_BasicDetails.objects.create(core_sector=core_sector, category=category,sub_category=sub_category,product_category=product_category,item_name=item_name,product_type=product_type, item_type=item_type,item_code=item_code,item_description=item_description,
#                                                                           final_selling_price=final_selling_price,numeric='100001',add_image1=add_image1, add_image2=add_image2,add_image3=add_image3, add_image4=add_image4,
#                                                                           uom=uom, quantity=quantity, hsn_sac=hsn_sac,unit_price=unit_price, discount=discount, tax=tax,sku_id=sku_id,country_of_origin=country_of_origin,
#                                                                           currency=currency,created_by=userid,updated_by=SelfRegistration.objects.get(id=userid))
#                 else:
#                     vendorobj = VendorProduct_BasicDetails.objects.create(core_sector=core_sector,
#                                                                           category=category,sub_category=sub_category,product_category=product_category,item_name=item_name,product_type=product_type,
#                                                                           item_type=item_type, item_code=item_code,item_description=item_description,
#                                                                           final_selling_price=final_selling_price,numeric=vedordetailsobj[0].get('numeric'), add_image1=add_image1,
#                                                                           add_image2=add_image2,add_image3=add_image3,add_image4=add_image4,uom=uom, quantity=quantity,hsn_sac=hsn_sac, unit_price=unit_price,
#                                                                           discount=discount, tax=tax, sku_id=sku_id,country_of_origin=country_of_origin,
#                                                                           currency=currency, created_by=userid,updated_by=SelfRegistration.objects.get(id=userid))
#
#
#                 return Response({'status': 201, 'message': 'Vendor Product  Created'}, status=201)
#             else:
#                 return Response({'status': 204, 'message': 'Not Present or enter type name properly'}, status=204)
#         except Exception as e:
#             return Response({'status': 500, 'error': str(e)}, status=500)



class VendorProduct_GeneralDetailsView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = VendorProduct_GeneralDetails.objects.all()
    serializer_class = VendorProduct_GeneralDetailsSerializer


class VendorProduct_TechnicalSpecificationsView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = VendorProduct_TechnicalSpecifications.objects.all()
    serializer_class = VendorProduct_TechnicalSpecificationsSerialzer


    def create(self, request, *args, **kwargs):
        technicaldetailslist = request.data['technicaldetails']
        updated_by = request.data.get('updated_by',None)
        print(updated_by)
        try:
            if updated_by is None:
                return Response({'status': 204, 'message': 'Enter user id or user id not exist'}, status=204)
            for i in range(0, len(technicaldetailslist)):
                VendorProduct_TechnicalSpecifications.objects.create(item_specification=technicaldetailslist[i].get('item_specification'),
                                                                      item_description=technicaldetailslist[i].get('item_description'),
                                                                      description=technicaldetailslist[i].get('description'),
                                                                      vendor_products=VendorProduct_BasicDetails.objects.get(vendor_product_id=technicaldetailslist[i].get('vendor_products')),
                                                                      updated_by=SelfRegistration.objects.get(id=updated_by),
                                                                      created_by=updated_by)
            return Response({'status': 201, 'message': 'Vendor Product Techinal Specifications Are Added'}, status=201)
        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)

class VendorProduct_ProductFeaturesView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = VendorProduct_ProductFeatures.objects.all()
    serializer_class = VendorProduct_ProductFeaturesSerializer

    def create(self, request, *args, **kwargs):
        productfeatureslist = request.data['productfeatureslist']
        updated_by = request.data.get('updated_by',None)
        try:
            if updated_by is None:
                return Response({'status':204,'message':'Enter user id or user id not exist'},status=204)
            for i in range(0, len(productfeatureslist)):
                VendorProduct_ProductFeatures.objects.create(
                    product_item_specification=productfeatureslist[i].get('product_item_specification'),
                    product_item_description=productfeatureslist[i].get('product_item_description'),
                    description=productfeatureslist[i].get('description'),
                    vendor_products=VendorProduct_BasicDetails.objects.get(vendor_product_id=productfeatureslist[i].get('vendor_products')),
                    updated_by=SelfRegistration.objects.get(id=updated_by),
                    created_by=updated_by
                )
            return Response({'status': 201, 'message': 'Vendor Product Features Are Added'}, status=201)
        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)



class VendorProduct_DocumentsView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = VendorProduct_Documents.objects.all()
    serializer_class = VendorProduct_DocumentsSerializer

    # def create(self, request, *args, **kwargs):
    #     vendorproductdocumentslist = request.data['vendorproductdocumentslist']
    #     updated_by = request.data.get('updated_by', None)
    #     try:
    #         if updated_by is None:
    #             return Response({'status': 204, 'message': 'Enter user id or user id not exist'}, status=204)
    #         for i in range(0, len(vendorproductdocumentslist)):
    #             VendorProduct_ProductFeatures.objects.create(
    #                 product_item_specification=vendorproductdocumentslist[i].get('product_item_specification'),
    #                 product_item_description=vendorproductdocumentslist[i].get('product_item_description'),
    #                 description=vendorproductdocumentslist[i].get('description'),
    #                 vendor_products=VendorProduct_BasicDetails.objects.get(
    #                     vendor_product_id=vendorproductdocumentslist[i].get('vendor_products')),
    #                 updated_by=SelfRegistration.objects.get(id=updated_by),
    #                 created_by=updated_by
    #             )
    #         return Response({'status': 201, 'message': 'Vendor Product Features Are Added'}, status=201)
    #     except Exception as e:
    #         return Response({'status': 500, 'error': str(e)}, status=500)

# @api_view(['post'])
# def vendor_product_create(request):
#     data=request.data
#
#                 #
#                 # vendor_id={
#                 #     'vendor_product_id':vendorobj.vendor_product_id
#                 # }
#
#         vendorgeneraldetailsobj=VendorProduct_GeneralDetails.objects.create(p_f_charges=data['p_f_charges'],frieght_charges=data['frieght_charges'],delivery=data['delivery'],warranty=data['warranty'],brand_make=data['brand_make'],department=data['department'],
#                                                                      guarantee=data['guarantee'],model_no=data['model_no'],min_order_quantity=data['min_order_quantity'],after_sale_service=data['after_sale_service'],
#                                                                      part_no=data['part_no'],packing_type=data['packing_type'],not_covered_w_g=data['not_covered_w_g'],alternate_parts=data['alternate_parts'],delievery_days=data['delievery_days'],standard_measures=data['standard_measures'],product_length=data['product_length'],
#                                                                      shipping_uom=data['shipping_uom'],item_weight=data['item_weight'],product_width=data['product_width'],shipping_weight=data['shipping_weight'],after_packed_weight=data['after_packed_weight'],product_height=data['product_height'],ship_via=data['ship_via'],
#                                                                      created_by=userid,updated_by=SelfRegistration.objects.get(id=userid),vendor_products=VendorProduct_BasicDetails.objects.get(vendor_product_id=vendorobj.vendor_product_id))
#
#         vendortechincalobj=VendorProduct_TechnicalSpecifications.objects.create(item_specification=data['item_specification'],item_description=data['item_description'],created_by=userid,updated_by=SelfRegistration.objects.get(id=userid),vendor_products=VendorProduct_BasicDetails.objects.get(vendor_product_id=vendorobj.vendor_product_id))
#
#         vendorproductobj=VendorProduct_ProductFeatures.objects.create(product_item_specification=data['product_item_specification'],product_item_description=data['product_item_description'],created_by=userid,updated_by=SelfRegistration.objects.get(id=userid),vendor_products=VendorProduct_BasicDetails.objects.get(vendor_product_id=vendorobj.vendor_product_id))
#
#         vendordocumentsobj=VendorProduct_Documents.objects.create(document=data['document'],document_description=data['document_description'],created_by=userid,updated_by=SelfRegistration.objects.get(id=userid),vendor_products=VendorProduct_BasicDetails.objects.get(vendor_product_id=vendorobj.vendor_product_id))
#         return Response({'status': 201, 'message': 'Vendor Product Created'}, status=201)
#
#
#
#
#
#     except Exception as e:
#         return Response({'status':500,'error':str(e)},status=500)

class VendorProduct_BasicDetailsView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = VendorProduct_BasicDetails.objects.all()
    serializer_class = VendorProduct_BasicDetailsSerializer

    def create(self, request, *args, **kwargs):
        data=request.data
        core_sector = data['core_sector']
        category = data['category']
        sub_category = data['sub_category']
        product_category = data['product_category']
        product_type=data['product_type']
        item_type = data['item_type']
        item_name = data['item_name']
        item_description=data['item_description']
        final_selling_price = data['final_selling_price']
        add_image1 = data['add_image1']
        add_image2 = data['add_image2']
        add_image3 = data['add_image3']
        add_image4 = data['add_image4']
        uom = data['uom']
        quantity = data['quantity']
        hsn_sac = data['hsn_sac']
        unit_price = data['unit_price']
        discount = data['discount']
        tax = data['tax']
        sku_id = data['sku_id']
        country_of_origin = data['country_of_origin']
        currency = data['currency']
        userid = data['userid']
        type = data['type']
        try:

            vedordetailsobj = VendorProduct_BasicDetails.objects.filter(updated_by=userid).order_by('-numeric').values()
            if type == 'auto':
                if vedordetailsobj:
                    vendorobj = VendorProduct_BasicDetails.objects.create(core_sector=core_sector, category=category,sub_category=sub_category,product_category=product_category,product_type=product_type,item_type=item_type,item_code=vedordetailsobj[0].get('numeric'),item_name=item_name,item_description=item_description,
                                                                          final_selling_price=final_selling_price,
                                                                          numeric=vedordetailsobj[0].get('numeric') + 1,add_image1=add_image1, add_image2=add_image2,add_image3=add_image3, add_image4=add_image4,
                                                                          uom=uom, quantity=quantity, hsn_sac=hsn_sac,unit_price=unit_price, discount=discount, tax=tax,sku_id=sku_id,country_of_origin=country_of_origin,
                                                                          currency=currency,created_by=userid,updated_by=SelfRegistration.objects.get(id=userid))
                else:
                    print('not exist')
                    vendorobj = VendorProduct_BasicDetails.objects.create(core_sector=core_sector, category=category,sub_category=sub_category,product_category=product_category,product_type=product_type,item_type=item_type, item_code=100001,item_name=item_name,item_description=item_description,
                                                                          final_selling_price=final_selling_price,numeric=100002, add_image1=add_image1,add_image2=add_image2, add_image3=add_image3,add_image4=add_image4,
                                                                          uom=uom, quantity=quantity,hsn_sac=hsn_sac,unit_price=unit_price,discount=discount, tax=tax, sku_id=sku_id,
                                                                          country_of_origin=country_of_origin,currency=currency,created_by=userid,
                                                                          updated_by=SelfRegistration.objects.get(id=userid))
            if type == 'manual':
                item_code = data['item_code']
                vendorobj=VendorProduct_BasicDetails.objects.count()
                if vendorobj==0:
                    print('s')
                    vendorobj = VendorProduct_BasicDetails.objects.create(core_sector=core_sector, category=category,sub_category=sub_category,product_category=product_category,item_name=item_name,product_type=product_type, item_type=item_type,item_code=item_code,item_description=item_description,
                                                                          final_selling_price=final_selling_price,numeric='100001',add_image1=add_image1, add_image2=add_image2,add_image3=add_image3, add_image4=add_image4,
                                                                          uom=uom, quantity=quantity, hsn_sac=hsn_sac,unit_price=unit_price, discount=discount, tax=tax,sku_id=sku_id,country_of_origin=country_of_origin,
                                                                          currency=currency,created_by=userid,updated_by=SelfRegistration.objects.get(id=userid))
                else:
                    vendorobj = VendorProduct_BasicDetails.objects.create(core_sector=core_sector,
                                                                          category=category,sub_category=sub_category,product_category=product_category,item_name=item_name,product_type=product_type,
                                                                          item_type=item_type, item_code=item_code,item_description=item_description,
                                                                          final_selling_price=final_selling_price,numeric=vedordetailsobj[0].get('numeric'), add_image1=add_image1,
                                                                          add_image2=add_image2,add_image3=add_image3,add_image4=add_image4,uom=uom, quantity=quantity,hsn_sac=hsn_sac, unit_price=unit_price,
                                                                          discount=discount, tax=tax, sku_id=sku_id,country_of_origin=country_of_origin,
                                                                          currency=currency, created_by=userid,updated_by=SelfRegistration.objects.get(id=userid))


            return Response({'status': 201, 'message': 'Vendor Product  Created'}, status=201)
        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)



class BuyerProductDetailsView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = BuyerProductDetails.objects.all()
    serializer_class = BuyerProductDetailsSerializer

@api_view(['post'])
@permission_classes((AllowAny,))
def buyer_product_create(request):
    data=request.data
    userid=data['userid']
    ccode=data['ccode']
    buyerdetailsobj=BuyerProductDetails.objects.filter(updated_by=userid).order_by('-buyer_numeric').values()
    if buyerdetailsobj:
        buyerobj=BuyerProductDetails.objects.create(buyer_item_type=data['buyer_item_type'],buyer_numeric=buyerdetailsobj[0].get('buyer_numeric')+1,buyer_item_code=str(ccode)+"-"+str(buyerdetailsobj[0].get('buyer_numeric')),buyer_item_name=data['buyer_item_name'],buyer_item_description=data['buyer_item_description'],
                                                    buyer_uom=data['buyer_uom'],buyer_hsn_sac=data['buyer_hsn_sac'],buyer_unit_price=data['buyer_unit_price'],
                                                    buyer_category=data['buyer_category'],buyer_department=data['buyer_department'],buyer_item_group=data['buyer_item_group'],
                                                    buyer_annual_consumption=data['buyer_annual_consumption'],buyer_safety_stock=data['buyer_safety_stock'],buyer_model_no=data['buyer_model_no'],buyer_document=data['buyer_document'],
                                                    buyer_additional_specifications=data['buyer_additional_specifications'],buyer_add_product_supplies=data['buyer_add_product_supplies'],
                                                    updated_by=SelfRegistration.objects.get(id=userid),created_by=userid)

    else:
        print("data not exist")
        buyerobj = BuyerProductDetails.objects.create(buyer_item_type=data['buyer_item_type'],
                                               buyer_numeric=1002,buyer_item_code=str(ccode)+"-"+"1001",buyer_item_name=data['buyer_item_name'],buyer_item_description=data['buyer_item_description'],
                                               buyer_uom=data['buyer_uom'], buyer_hsn_sac=data['buyer_hsn_sac'],buyer_unit_price=data['buyer_unit_price'],buyer_category=data['buyer_category'], buyer_department=data['buyer_department'],
                                               buyer_item_group=data['buyer_item_group'],buyer_annual_consumption=data['buyer_annual_consumption'],buyer_safety_stock=data['buyer_safety_stock'],buyer_model_no=data['buyer_model_no'],
                                               buyer_document=data['buyer_document'],buyer_additional_specifications=data['buyer_additional_specifications'],buyer_add_product_supplies=data['buyer_add_product_supplies'],
                                               updated_by=SelfRegistration.objects.get(id=userid),created_by=userid)

    # productbuyer=BuyerProductDetails.objects.filter(buyer_product_id=buyerobj.buyer_product_id).values()
    return Response({'status':201,'message':'Buyer Product Created'},status=201)
