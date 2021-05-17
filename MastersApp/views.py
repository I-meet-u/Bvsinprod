
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import MainCoreMasterSerializer, CategoryMasterSerializer, SubcategoryMasterSerializer, \
    CountryMasterSerializer, StateMasterSerializer, CityMasterSerializer, IndustryToServeMasterSerializer, \
    NatureOfBusinessMasterSerializer, SupplyCapabilitiesMasterSerializer, PincodeMasterSerializer
from .models import MaincoreMaster, CategoryMaster, SubCategoryMaster, CountryMaster, StateMaster, CityMaster, \
    IndustryToServeMaster,NatureOfBusinessMaster,SupplyCapabilitiesMaster,PincodeMaster


# Create your views here.
class IndustryToServeMasterView(viewsets.ModelViewSet):
    queryset = IndustryToServeMaster.objects.all()
    serializer_class = IndustryToServeMasterSerializer

class NatureOfBusinessMasterView(viewsets.ModelViewSet):
    queryset = NatureOfBusinessMaster.objects.all()
    serializer_class =NatureOfBusinessMasterSerializer


class SupplyCapabilitiesMasterView(viewsets.ModelViewSet):
    queryset = SupplyCapabilitiesMaster.objects.all()
    serializer_class =SupplyCapabilitiesMasterSerializer




class MaincoreMasterView(viewsets.ModelViewSet):
    queryset = MaincoreMaster.objects.all()
    serializer_class = MainCoreMasterSerializer

class CategoryMasterView(viewsets.ModelViewSet):
    queryset =CategoryMaster.objects.all()
    serializer_class=CategoryMasterSerializer

class SubCategoryMasterView(viewsets.ModelViewSet):
    queryset = SubCategoryMaster.objects.all()
    serializer_class = SubcategoryMasterSerializer

class CountryMasterView(viewsets.ModelViewSet):
    queryset = CountryMaster.objects.all()
    serializer_class = CountryMasterSerializer

class StateMasterView(viewsets.ModelViewSet):
    queryset = StateMaster.objects.all()
    serializer_class = StateMasterSerializer


class CityMasterView(viewsets.ModelViewSet):
    queryset = CityMaster.objects.all()
    serializer_class = CityMasterSerializer



class PincodeMasterView(viewsets.ModelViewSet):
    queryset = PincodeMaster.objects.all()
    serializer_class = PincodeMasterSerializer