from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from rest_framework.response import Response

from RegistrationApp.models import SelfRegistration
from .models import VendorProductsDetail

from .serializers import VendorProductsDetailSerializer

class VendorProductsDetailView(viewsets.ModelViewSet):
    queryset = VendorProductsDetail.objects.all()
    serializer_class = VendorProductsDetailSerializer

    def create(self, request, *args, **kwargs):
        data=request.data
        core_sector=data['core_sector']
        category=data['category']
        sub_category=data['sub_category']
        product_category=data['product_category']
        product_subcategory=data['product_subcategory']
        product_type=data['product_type']
        product_name=data['product_name']
        product_description=data['product_description']
        product_document=data['product_document']
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
        p_andf_charges=data['p_andf_charges']
        fright_charges=data['fright_charges']
        warrenty_or_guarantee=data['warrenty_or_guarantee']
        userid=data['userid']
        type=data['type']
        try:
            vedordetailsobj = VendorProductsDetail.objects.filter(updated_by=userid).order_by('-numeric').values()
            if type=='auto':
                if vedordetailsobj:
                    VendorProductsDetail.objects.create(core_sector=core_sector,category=category,sub_category=sub_category,product_category=product_category,product_subcategory=product_subcategory,product_type=product_type,product_code=vedordetailsobj[0].get('numeric'),product_description=product_description,product_document=product_document,
                                                        numeric=vedordetailsobj[0].get('numeric')+1,add_image1=add_image1,add_image2=add_image2,add_image3=add_image3,add_image4=add_image4,uom=uom,quantity=quantity,hsn_sac=hsn_sac,unit_price=unit_price,discount=discount,tax=tax,sku_id=sku_id,country_of_origin=country_of_origin,currency=currency,
                                                        p_andf_charges=p_andf_charges,fright_charges=fright_charges,warrenty_or_guarantee=warrenty_or_guarantee,created_by=userid,updated_by=SelfRegistration.objects.get(id=userid),product_name=product_name)
                else:
                    print('not exist')
                    VendorProductsDetail.objects.create(core_sector=core_sector, category=category, sub_category=sub_category,product_category=product_category, product_subcategory=product_subcategory,product_type=product_type, product_code=100001,product_description=product_description, product_document=product_document,
                                                        numeric=100002, add_image1=add_image1, add_image2=add_image2,add_image3=add_image3, add_image4=add_image4, uom=uom, quantity=quantity,hsn_sac=hsn_sac, unit_price=unit_price, discount=discount, tax=tax,sku_id=sku_id, country_of_origin=country_of_origin, currency=currency,
                                                        p_andf_charges=p_andf_charges, fright_charges=fright_charges,warrenty_or_guarantee=warrenty_or_guarantee, created_by=userid,updated_by=SelfRegistration.objects.get(id=userid),product_name=product_name)
                return Response({'status': 201, 'message': 'Vendor Product Created'}, status=201)
            if type=='manual':
                product_code = data['product_code']
                if vedordetailsobj:
                    VendorProductsDetail.objects.create(core_sector=core_sector,category=category,sub_category=sub_category, product_category=product_category, product_subcategory=product_subcategory,product_type=product_type,product_code=product_code,product_description=product_description,product_document=product_document,
                                                        numeric=vedordetailsobj[0].get('numeric'),add_image1=add_image1, add_image2=add_image2,add_image3=add_image3, add_image4=add_image4, uom=uom,quantity=quantity, hsn_sac=hsn_sac, unit_price=unit_price,discount=discount, tax=tax, sku_id=sku_id,country_of_origin=country_of_origin, currency=currency,
                                                        p_andf_charges=p_andf_charges, fright_charges=fright_charges,warrenty_or_guarantee=warrenty_or_guarantee, created_by=userid,updated_by=SelfRegistration.objects.get(id=userid),product_name=product_name)
                    return Response({'status': 201, 'message': 'Vendor Product Manual Created'}, status=201)


        except Exception as e:
            return Response({'status':500,'error':str(e)},status=500)










#
# class GeneralProductsDetailsView(viewsets.ModelViewSet):
#     queryset = GeneralProductsDetails.objects.all()
#     serializer_class = GeneralProductsDetailsSerializer
#
#
# class PricingOfferView(viewsets.ModelViewSet):
#     queryset = PricingOffer.objects.all()
#     serializer_class = PricingOfferSerializer
#
# class TechnicalDetailsView(viewsets.ModelViewSet):
#     queryset = TechnicalDetails.objects.all()
#     serializer_class = TechnicalDetailsSerializer
#
# class ProductFeaturesView(viewsets.ModelViewSet):
#     queryset = ProductFeatures.objects.all()
#     serializer_class = ProductFeaturesSerializer
#
