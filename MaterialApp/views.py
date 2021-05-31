# from django.shortcuts import render
#
# # Create your views here.
#
# from rest_framework import viewsets
# from .models import VendorProductsDetail, GeneralProductsDetails, PricingOffer, TechnicalDetails, ProductFeatures
#
# from .serializers import VendorProductsDetailSerializer, GeneralProductsDetailsSerializer, PricingOfferSerializer, TechnicalDetailsSerializer, ProductFeaturesSerializer
#
# class VendorProductsDetailView(viewsets.ModelViewSet):
#     queryset = VendorProductsDetail.objects.all()
#     serializer_class = VendorProductsDetailSerializer
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
