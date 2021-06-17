from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from rest_framework.response import Response

from .models import VendorProductsDetail

from .serializers import VendorProductsDetailSerializer

class VendorProductsDetailView(viewsets.ModelViewSet):
    queryset = VendorProductsDetail.objects.all()
    serializer_class = VendorProductsDetailSerializer


    # def create(self, request, *args, **kwargs):
    #     updated_by=request.data.get('updated_by',None)
    #     # numeric=request.data.get('numeric',None)
    #     # product_code=request.data.get('product_code',None)
    #     product_type=request.data.get('product_type',None)
    #     # numeric = self.kwargs.get('numeric',None)
    #     print(product_type)
    #     try:
    #         productobj=VendorProductsDetail.objects.filter(updated_by=updated_by).order_by('-numeric').values()
    #         if product_type == 'auto':
    #             if len(productobj)==0:
    #                 numeric1 = 100002
    #                 # numeric=numeric1
    #                 product_code = '100001'
    #
    #                 print('data not there')
    #                 return super().create(request, *args, **kwargs)
    #
    #             # else:
    #             #     print('s coming')
    #             #     numeric=productobj[0].get('numeric')+1
    #             #     print(numeric,'n')
    #             #     product_code=productobj[0].get('numeric')
    #             #     print(product_code)
    #             # return super(VendorProductsDetailView, self).create(request, *args, **kwargs)
    #             # return super().create(request, *args, **kwargs)
    #         if product_type=='manual':
    #             productobj1 = VendorProductsDetail.objects.filter(updated_by=updated_by).order_by('-numeric').values()
    #             if len(productobj1) == 0 or productobj1 == " ":
    #                 return Response({'status':202,'message':'No products present'},status=202)
    #             else:
    #                 numeric = productobj1[0].get('numeric')
    #                 print(numeric)
    #                 # productobj1.update()
    #                 # product_code=productcode
    #         # return super().create(request, *args, **kwargs)
    #         # else:
    #         #     return Response({'status':'204','message':'Type is not correct,enter proper type either manual or auto'},status=204)
    #     except Exception as e:
    #         return Response({'status':500,'error':str(e)},status=500)
    #
    #
    #     # except Exception as e:
    #     #     return Response({'status':500,'error':str(e)},status=500)
    #     # productvalues=VendorProductsDetail.objects.filter(id=productobj.id).values()




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
