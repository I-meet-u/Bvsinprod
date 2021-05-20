
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
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

@api_view(['post'])
def get_category_by_maincore(request):
    data=request.data
    maincoreid=data['maincoreid']
    try:
        catobj=CategoryMaster.objects.filter(maincore_id=maincoreid).values()
        if catobj:
            return Response({'status':200,'message':'Category List','data':catobj},status=200)
        else:
            return Response({'status': 204, 'message':'No categoreis are found'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['post'])
def get_subcategory_by_category(request):
    data=request.data
    categoryid=data['categoryid']
    try:
        subcatobj=SubCategoryMaster.objects.filter(category_id__in=categoryid).values()
        if subcatobj:
            return Response({'status':200,'message':'SubCategory List','data':subcatobj},status=200)
        else:
            return Response({'status': 204, 'message':'No subcategories are found'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['post'])
def maincore_search(request):
    data=request.data
    maincore_name=data['maincore_name']
    try:
        maincoreobj=MaincoreMaster.objects.filter(maincore_name__icontains=maincore_name).values()
        if maincoreobj:
            return Response({'status':200,'message':'Maincore search success','data':maincoreobj},status=200)
        else:
            return Response({'status':204,'message':'No maincore content'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def category_search(request):
    data=request.data
    category_name=data['category_name']
    try:
        categoryobj=CategoryMaster.objects.filter(category_name__icontains=category_name).values()
        if categoryobj:
            return Response({'status':200,'message':'Category search success','data':categoryobj},status=200)
        else:
            return Response({'status':204,'message':'No category content'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def sub_cateory_search(request):
    data=request.data
    sub_category_name=data['sub_category_name']
    try:
        subcategoryobj=SubCategoryMaster.objects.filter(sub_category_name__icontains=sub_category_name).values()
        if subcategoryobj:
            return Response({'status':200,'message':'SubCategory search success','data':subcategoryobj},status=200)
        else:
            return Response({'status':204,'message':'No subcategory content'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)
