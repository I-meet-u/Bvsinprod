from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from RegistrationApp.models import SelfRegistration
from .models import VendorProduct_BasicDetails, VendorProduct_GeneralDetails,VendorProduct_TechnicalSpecifications,VendorProduct_ProductFeatures,VendorProduct_Documents

from .serializers import VendorProduct_BasicDetailsSerializer, VendorProduct_GeneralDetailsSerializer, \
    VendorProduct_TechnicalSpecificationsSerialzer, VendorProduct_ProductFeaturesSerializer, \
    VendorProduct_DocumentsSerializer


class VendorProduct_BasicDetailsView(viewsets.ModelViewSet):
    queryset = VendorProduct_BasicDetails.objects.all()
    serializer_class = VendorProduct_BasicDetailsSerializer


class VendorProduct_GeneralDetailsView(viewsets.ModelViewSet):
    queryset = VendorProduct_GeneralDetails.objects.all()
    serializer_class = VendorProduct_GeneralDetailsSerializer


class VendorProduct_TechnicalSpecificationsView(viewsets.ModelViewSet):
    queryset = VendorProduct_TechnicalSpecifications.objects.all()
    serializer_class = VendorProduct_TechnicalSpecificationsSerialzer

class VendorProduct_ProductFeaturesView(viewsets.ModelViewSet):
    queryset = VendorProduct_ProductFeatures.objects.all()
    serializer_class = VendorProduct_ProductFeaturesSerializer

class VendorProduct_DocumentsView(viewsets.ModelViewSet):
    queryset = VendorProduct_Documents.objects.all()
    serializer_class = VendorProduct_DocumentsSerializer

@api_view(['post'])
def vendor_product_create(request):
    data=request.data
    core_sector=data['core_sector']
    category=data['category']
    sub_category=data['sub_category']
    product_category=data['product_category']
    item_type=data['item_type']
    item_name=data['item_name']
    final_selling_price=data['final_selling_price']
    add_image1=data['add_image1']
    add_image2=data['add_image2']
    add_image3=data['add_image3']
    add_image4=data['add_image4']
    uom=data['uom']
    quantity=data['quantity']
    hsn_sac=data['hsn_sac']
    unit_price=data['unit_price']
    discount=data['discount']
    tax=data['tax']
    sku_id=data['sku_id']
    country_of_origin=data['country_of_origin']
    currency=data['currency']
    pricing=data['pricing']
    request_on_quote=data['request_on_quote']
    price_range=data['price_range']
    userid=data['userid']
    type=data['type']
    try:

        vedordetailsobj = VendorProduct_BasicDetails.objects.filter(updated_by=userid).order_by('-numeric').values()
        if type=='auto':
            if vedordetailsobj:
                vendorobj=VendorProduct_BasicDetails.objects.create(core_sector=core_sector,category=category,sub_category=sub_category,product_category=product_category,item_type=item_type,item_code=vedordetailsobj[0].get('numeric'),item_name=item_name,final_selling_price=final_selling_price,
                                                    numeric=vedordetailsobj[0].get('numeric')+1,add_image1=add_image1,add_image2=add_image2,add_image3=add_image3,add_image4=add_image4,uom=uom,quantity=quantity,hsn_sac=hsn_sac,unit_price=unit_price,discount=discount,tax=tax,sku_id=sku_id,country_of_origin=country_of_origin,currency=currency,
                                                    pricing=pricing,request_on_quote=request_on_quote,price_range=price_range,created_by=userid,updated_by=SelfRegistration.objects.get(id=userid))
            else:
                print('not exist')
                vendorobj=VendorProduct_BasicDetails.objects.create(core_sector=core_sector, category=category, sub_category=sub_category,product_category=product_category,item_type=item_type, item_code=100001,item_name=item_name,final_selling_price=final_selling_price,
                                                    numeric=100002, add_image1=add_image1, add_image2=add_image2,add_image3=add_image3, add_image4=add_image4, uom=uom, quantity=quantity,hsn_sac=hsn_sac, unit_price=unit_price, discount=discount, tax=tax,sku_id=sku_id, country_of_origin=country_of_origin, currency=currency,
                                                    pricing=pricing, request_on_quote=request_on_quote,price_range=price_range, created_by=userid,updated_by=SelfRegistration.objects.get(id=userid))
        if type=='manual':
            item_code = data['item_code']
            if vedordetailsobj:
                vendorobj=VendorProduct_BasicDetails.objects.create(core_sector=core_sector,category=category,sub_category=sub_category, product_category=product_category,item_name=item_name,item_type=item_type,item_code=item_code,final_selling_price=final_selling_price,
                                                    numeric=vedordetailsobj[0].get('numeric'),add_image1=add_image1, add_image2=add_image2,add_image3=add_image3, add_image4=add_image4, uom=uom,quantity=quantity, hsn_sac=hsn_sac, unit_price=unit_price,discount=discount, tax=tax, sku_id=sku_id,country_of_origin=country_of_origin, currency=currency,
                                                    pricing=pricing, request_on_quote=request_on_quote,price_range=price_range, created_by=userid,updated_by=SelfRegistration.objects.get(id=userid))
                # return Response({'status': 201, 'message': 'Vendor Product Manual Created'}, status=201)
                #
                # vendor_id={
                #     'vendor_product_id':vendorobj.vendor_product_id
                # }

        vendorgeneraldetailsobj=VendorProduct_GeneralDetails.objects.create(p_f_charges=data['p_f_charges'],frieght_charges=data['frieght_charges'],delivery=data['delivery'],warranty=data['warranty'],brand_make=data['brand_make'],department=data['department'],
                                                                     guarantee=data['guarantee'],model_no=data['model_no'],min_order_quantity=data['min_order_quantity'],after_sale_service=data['after_sale_service'],
                                                                     part_no=data['part_no'],packing_type=data['packing_type'],not_covered_w_g=data['not_covered_w_g'],alternate_parts=data['alternate_parts'],delievery_days=data['delievery_days'],standard_measures=data['standard_measures'],product_length=data['product_length'],
                                                                     shipping_uom=data['shipping_uom'],item_weight=data['item_weight'],product_width=data['product_width'],shipping_weight=data['shipping_weight'],after_packed_weight=data['after_packed_weight'],product_height=data['product_height'],ship_via=data['ship_via'],
                                                                     created_by=userid,updated_by=SelfRegistration.objects.get(id=userid),vendor_products=VendorProduct_BasicDetails.objects.get(vendor_product_id=vendorobj.vendor_product_id))

        vendortechincalobj=VendorProduct_TechnicalSpecifications.objects.create(item_specification=data['item_specification'],item_description=data['item_description'],created_by=userid,updated_by=SelfRegistration.objects.get(id=userid),vendor_products=VendorProduct_BasicDetails.objects.get(vendor_product_id=vendorobj.vendor_product_id))

        vendorproductobj=VendorProduct_ProductFeatures.objects.create(product_item_specification=data['product_item_specification'],product_item_description=data['product_item_description'],created_by=userid,updated_by=SelfRegistration.objects.get(id=userid),vendor_products=VendorProduct_BasicDetails.objects.get(vendor_product_id=vendorobj.vendor_product_id))

        vendordocumentsobj=VendorProduct_Documents.objects.create(document=data['document'],document_description=data['document_description'],created_by=userid,updated_by=SelfRegistration.objects.get(id=userid),vendor_products=VendorProduct_BasicDetails.objects.get(vendor_product_id=vendorobj.vendor_product_id))
        return Response({'status': 201, 'message': 'Vendor Product Created'}, status=201)





    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)
