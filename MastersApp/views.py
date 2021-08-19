
from itertools import chain

from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from datetime import datetime
import io, csv

from rest_framework.views import APIView

from AdminApp.models import AdminRegister
from .serializers import *
from .models import  *

from .paginations import CustomPagination

# Create your views here.
# class LimitOffsetPagination(PageNumberPagination):
#     default_limit=5
#     limit=5
#     offset=5
#     max_limit=1000


class IndustryToServeMasterView(viewsets.ModelViewSet):
    # industry_servce master viewsets
    permission_classes = (AllowAny,)
    queryset = IndustryToServeMaster.objects.all().order_by('industry_id')
    serializer_class = IndustryToServeMasterSerializer

class NatureOfBusinessMasterView(viewsets.ModelViewSet):
    # nature_of_business mster viewsets
    permission_classes = (AllowAny,)
    queryset = NatureOfBusinessMaster.objects.all().order_by('nature_of_business_id')
    serializer_class =NatureOfBusinessMasterSerializer


class SupplyCapabilitiesMasterView(viewsets.ModelViewSet):
    # supply_capability  viewsets
    permission_classes = (AllowAny,)
    queryset = SupplyCapabilitiesMaster.objects.all().order_by('supply_capability_id')
    serializer_class =SupplyCapabilitiesMasterSerializer

class MaincoreMasterView(viewsets.ModelViewSet):
    # maincore_master  master viewsets
    permission_classes = (AllowAny,)
    queryset = MaincoreMaster.objects.all().order_by('maincore_id')
    serializer_class = MainCoreMasterSerializer

class CategoryMasterView(viewsets.ModelViewSet):
    # category_master  viewsets
    permission_classes = (AllowAny,)
    queryset =CategoryMaster.objects.all().order_by('category_id')
    serializer_class=CategoryMasterSerializer

class SubCategoryMasterView(viewsets.ModelViewSet):
    # sub_category_master  viewsets
    permission_classes = (AllowAny,)
    queryset = SubCategoryMaster.objects.all().order_by('sub_category_id')
    serializer_class = SubcategoryMasterSerializer


class PincodeMasterView(viewsets.ModelViewSet):
    # pincode_master  viewsets
    permission_classes = (AllowAny,)
    queryset = PincodeMaster.objects.all().order_by('pincode_id')
    serializer_class = PincodeMasterSerializer

class UOMMasterView(viewsets.ModelViewSet):
    # UOM_master = viewsets
    permission_classes = (AllowAny,)
    queryset = UOMMaster.objects.all().order_by('uom_id')
    serializer_class= UOMMasterSerializer


# def get_queryset(self):
    #     # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
    #     uommasterobj = UOMMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by('uom_id')
    #     if uommasterobj:
    #         return uommasterobj
    #     raise ValidationError({'message': 'UOM Master details not exist', 'status': 204})


class DepartmentMasterView(viewsets.ModelViewSet):
    # department_master  viewsets
    permission_classes = (AllowAny,)
    queryset = DepartmentMaster.objects.all().order_by('department_id')
    serializer_class = DepartmentMasterSerializer
    # ordering_fields = ['department_id']
    # ordering  = ['department_id']

    # def get_queryset(self):
    #     # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
    #     departmentmasterobj = DepartmentMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by('department_id')
    #     if departmentmasterobj:
    #         return  departmentmasterobj
    #     raise ValidationError({'message': 'Department Master details not exist', 'status': 204})

class DesignationMasterView(viewsets.ModelViewSet):
    # designation_master viewsets
    permission_classes = (AllowAny,)
    queryset = DesignationMaster.objects.all().order_by('designation_id')
    serializer_class = DesignationMasterSerializer
    # ordering_fields = ['designation_id']
    # ordering = ['designation_id']


    # def get_queryset(self):
    #     # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
    #     designationmasterobj = DesignationMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by(
    #         'designation_id')
    #     if designationmasterobj:
    #         return designationmasterobj
    #     raise ValidationError({'message': 'Designation Master details not exist', 'status': 204})

class TaxMasterView(viewsets.ModelViewSet):
    # tax_master  viewsets
    permission_classes = (AllowAny,)
    queryset = TaxMaster.objects.all().order_by('tax_id')
    serializer_class = TaxMasterSerializer

    # def get_queryset(self):
    #     # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
    #     taxmasterobj = TaxMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by(
    #         'tax_id')
    #     if taxmasterobj:
    #         return taxmasterobj
    #     raise ValidationError({'message': 'Tax Master details not exist', 'status': 204})


class HSNMasterSerializerView(viewsets.ModelViewSet):
    # hsn_master  viewsets
    permission_classes = (AllowAny,)
    queryset = HSNMaster.objects.all().order_by('hsn_id')
    serializer_class = HSNMasterSerializer

    # def get_queryset(self):
    #     # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
    #     hsnmasterobj = HSNMaster.objects.filter(updated_by=self.request.GET.get('updated_by'))
    #     if hsnmasterobj:
    #         return hsnmasterobj
    #     raise ValidationError({'message': 'HSN Master details not exist', 'status': 204})


class SACMasterView(viewsets.ModelViewSet):
    # sac_master  viewsets
    permission_classes = (AllowAny,)
    queryset = SACMaster.objects.all().order_by('sac_id')
    serializer_class = SACMasterSerializer

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        sacmasterobj = SACMaster.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if sacmasterobj:
            return sacmasterobj

        raise ValidationError({'message': 'SAC Master details not exist', 'status': 204})

class CurrencyMasterView(viewsets.ModelViewSet):
    # currency_master viewsets
    permission_classes = (AllowAny,)
    queryset = CurrencyMaster.objects.all().order_by('currency_id')
    serializer_class = CurrencyMasterSerializer

    # def get_queryset(self):
    #     # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
    #     currencymasterobj = CurrencyMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by(
    #         'currency_id')
    #     if currencymasterobj:
    #         return  currencymasterobj
    #
    #     raise ValidationError({'message': 'Currency Master details not exist', 'status': 204})

class PFChargesMasterView(viewsets.ModelViewSet):
    # pf_charges master viewsets
    permission_classes = (AllowAny,)
    queryset = PFChargesMaster.objects.all().order_by('pf_charge_id')
    serializer_class = PFChargesMasterSerializer

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        pfmasterobj = PFChargesMaster.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if pfmasterobj:
            return pfmasterobj
        raise ValidationError({'message': 'PF Charges Master details not exist', 'status': 204})

class FrieghtChargesMasterView(viewsets.ModelViewSet):
    # frieght_charges master viewsets
    permission_classes = (AllowAny,)
    queryset = FrieghtChargesMaster.objects.all().order_by('frieght_id')
    serializer_class = FrieghtChargesMasterSerializer

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        frieghtmasterobj = FrieghtChargesMaster.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if frieghtmasterobj:
            return  frieghtmasterobj
        raise ValidationError({'message': 'Frieght Master details not exist', 'status': 204})

class WarrantyMasterView(viewsets.ModelViewSet):
    # warranty_master viewsets
    permission_classes = (AllowAny,)
    queryset = WarrantyMaster.objects.all().order_by('warranty_id')
    serializer_class = WarrantyMasterSerializer

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        warrantymasterobj = WarrantyMaster.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if warrantymasterobj:
            return warrantymasterobj

        raise ValidationError({'message': 'Warranty Master details not exist', 'status': 204})

class GuaranteeMasterView(viewsets.ModelViewSet):
    # warranty_master viewsets
    permission_classes = (AllowAny,)
    queryset = GuaranteeMaster.objects.all().order_by('guarantee_id')
    serializer_class =GuaranteeMasterSerializer

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        guaranteemasterobj = GuaranteeMaster.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if guaranteemasterobj:
            return  guaranteemasterobj
        raise ValidationError({'message': 'Guarantee Master details not exist', 'status': 204})

class DeliveryMasterView(viewsets.ModelViewSet):
    # delivery_master viewsets
    permission_classes = (AllowAny,)
    queryset = DeliveryMaster.objects.all().order_by('delivery_id')
    serializer_class = DeliveryMasterSerializer
    #
    # def get_queryset(self):
    #     # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
    #     deliverymasterobj = DeliveryMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by(
    #         'delivery_id')
    #     if deliverymasterobj:
    #         return  deliverymasterobj
    #
    #     raise ValidationError({'message': 'Delivery Master details not exist', 'status': 204})

class CountryMasterView(viewsets.ModelViewSet):
    # country_master viewsets
    permission_classes = (AllowAny,)
    queryset = CountryMaster.objects.all().order_by('country_id')
    serializer_class = CountryMasterSerializer

    # def get_queryset(self):
    #     # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
    #     countrymasterobj = CountryMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by(
    #         'country_id')
    #     if countrymasterobj:
    #         return  countrymasterobj
    #
    #     raise ValidationError({'message': 'Country Master details not exist', 'status': 204})

class DivisionMasterView(viewsets.ModelViewSet):
    # division viewsets
    permission_classes = (AllowAny,)
    queryset = DivisionMaster.objects.all().order_by('division_id')
    serializer_class = DivisionMasterSerializer

@api_view(['post'])
@permission_classes((AllowAny,))
def get_category_by_maincore(request):
    # getting categories list by passing maincore_id
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
@permission_classes((AllowAny,))
def get_subcategory_by_category(request):
    #  getting sub-categories list by passing category_id
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
@permission_classes((AllowAny,))
def maincore_search(request):
    # maincore_name search passing maincore_name
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
@permission_classes((AllowAny,))
def category_search(request):
    # category-name search passing category_name
    data=request.data
    mid=data['mid']
    category_name=data['category_name']
    try:
        categoryobj=CategoryMaster.objects.filter(maincore=mid,category_name__icontains=category_name).values()
        if categoryobj:
            return Response({'status':200,'message':'Category search success','data':categoryobj},status=200)
        else:
            return Response({'status':204,'message':'No category content'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def sub_category_search(request):
    # sub-category-name search passing sub_category_name
    data=request.data
    catid=data['catid']
    sub_category_name=data['sub_category_name']
    try:
        subcategoryobj=SubCategoryMaster.objects.filter(category__in=catid,sub_category_name__icontains=sub_category_name).values()
        if subcategoryobj:
            return Response({'status':200,'message':'SubCategory search success','data':subcategoryobj},status=200)
        else:
            return Response({'status':204,'message':'No subcategory content'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def disable_nature_of_business_master(request):
    # disable nature_of_business by changing status from Active to Disabled by passing primary key(natureid)
    data=request.data
    natureid=data['natureid']
    try:
        natureobj=NatureOfBusinessMaster.objects.filter(nature_of_business_id__in=natureid).values()
        if natureobj:
            for i in range(0,len(natureobj)):
                print(natureobj[i].get('nature_of_business_id'))
                natureobjget=NatureOfBusinessMaster.objects.get(nature_of_business_id=natureobj[i].get('nature_of_business_id'))
                print(natureobjget)
                if natureobjget.status=='Active':
                    natureobjget.status='Disabled'
                    natureobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status disabled'}, status=202)
            return Response({'status':200,'message':'Nature of business status changed to disabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['put'])
@permission_classes([AllowAny,])
def enable_nature_of_business_master(request):
    # enable nature_of_business by changing status from Disabled to Active by passing primary key(natureid)
    data=request.data
    natureid=data['natureid']
    try:
        natureobj=NatureOfBusinessMaster.objects.filter(nature_of_business_id__in=natureid).values()
        if natureobj:
            for i in range(0,len(natureobj)):
                print(natureobj[i].get('nature_of_business_id'))
                natureobjget=NatureOfBusinessMaster.objects.get(nature_of_business_id=natureobj[i].get('nature_of_business_id'))
                print(natureobjget)
                if natureobjget.status=='Disabled':
                    natureobjget.status='Active'
                    natureobjget.save()
            return Response({'status':204,'message':'Already status enabled'},status=204)
        return Response({'status': 202, 'message': 'Nature of business status changed to emabled'}, status=202)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['post'])
@permission_classes([AllowAny,])
def delete_nature_of_business_master(request):
    # delete nature_of_business by passing primary key(natureid)
    data=request.data
    natureid=data['natureid']
    try:
        natureobj=NatureOfBusinessMaster.objects.filter(nature_of_business_id__in=natureid).values()
        if natureobj:
            for i in range(0,len(natureobj)):
                print(natureobj[i].get('nature_of_business_id'))
                natureobjget=NatureOfBusinessMaster.objects.get(nature_of_business_id=natureobj[i].get('nature_of_business_id'))
                if natureobjget:
                    natureobjget.delete()

            return Response({'status': 204, 'message': 'Nature of business data deleted'}, status=204)
        return Response({'status':200,'message':'Nature of business data not present or already deleted'},status=200)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['put'])
@permission_classes([AllowAny,])
def disable_industry_serve_masters(request):
    # disable industry_serve by changing status from Active to Disabled by passing primary key(industryid)
    data=request.data
    industryid=data['industryid']
    try:
        industryobj=IndustryToServeMaster.objects.filter(industry_id__in=industryid).values()
        print(industryobj)
        if industryobj:
            for i in range(0,len(industryobj)):
                print(industryobj[i].get('industry_id'))
                industryobjget=IndustryToServeMaster.objects.get(industry_id=industryobj[i].get('industry_id'))
                print(industryobjget)
                if industryobjget.status=='Active':
                    industryobjget.status='Disabled'
                    industryobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status disabled'}, status=202)
            return Response({'status':200,'message':'Inudstry serve status changed to disabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['put'])
@permission_classes([AllowAny,])
def enable_industry_serve_masters(request):
    # enable industry_serve by changing status from Disabled to Active by passing primary key(industryid)
    data=request.data
    industryid=data['industryid']
    try:
        industryobj=IndustryToServeMaster.objects.filter(industry_id__in=industryid).values()
        print(industryobj)
        if industryobj:
            for i in range(0,len(industryobj)):
                print(industryobj[i].get('industry_id'))
                industryobjget=IndustryToServeMaster.objects.get(industry_id=industryobj[i].get('industry_id'))
                print(industryobjget)
                if industryobjget.status=='Disabled':
                    industryobjget.status='Active'
                    industryobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status enabled'}, status=202)
            return Response({'status':200,'message':'Inudstry serve status changed to enabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['post'])
@permission_classes([AllowAny,])
def delete_industry_serve_masters(request):
    # delete industry_serve by passing primary key(industryid)
    data=request.data
    industryid=data['industryid']
    try:
        industryobj=IndustryToServeMaster.objects.filter(industry_id__in=industryid).values()
        print(industryobj)
        if industryobj:
            for i in range(0,len(industryobj)):
                industryobjget=IndustryToServeMaster.objects.get(industry_id=industryobj[i].get('industry_id'))
                if industryobjget:
                    industryobjget.delete()

            return Response({'status': 204, 'message': 'Industry Serve data deleted'}, status=204)
        return Response({'status':202,'message':'Industry data not present or already deleted'},status=202)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['put'])
@permission_classes([AllowAny,])
def disable_supply_capabilities_master(request):
    # disable supply_capabilities by changing status from Active to Disabled by passing primary key(supplyid)
    data=request.data
    supplyid=data['supplyid']
    try:
        supplyobj=SupplyCapabilitiesMaster.objects.filter(supply_capability_id__in=supplyid).values()
        if supplyobj:
            for i in range(0,len(supplyobj)):
                print(supplyobj[i].get('supply_capability_id'))
                supplyobjget=SupplyCapabilitiesMaster.objects.get(supply_capability_id=supplyobj[i].get('supply_capability_id'))
                print(supplyobjget)
                if supplyobjget.status=='Active':
                    supplyobjget.status='Disabled'
                    supplyobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status disabled'}, status=202)
            return Response({'status':200,'message':'Supply capabilites status changed to disabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['put'])
@permission_classes([AllowAny,])
def enable_supply_capabilities_master(request):
    # enable supply_capabilities by changing status from Disabled to Active by passing primary key(supplyid)
    data=request.data
    supplyid=data['supplyid']
    try:
        supplyobj=SupplyCapabilitiesMaster.objects.filter(supply_capability_id__in=supplyid).values()
        if supplyobj:
            for i in range(0,len(supplyobj)):
                print(supplyobj[i].get('supply_capability_id'))
                supplyobjget=SupplyCapabilitiesMaster.objects.get(supply_capability_id=supplyobj[i].get('supply_capability_id'))
                print(supplyobjget)
                if supplyobjget.status=='Disabled':
                    supplyobjget.status='Active'
                    supplyobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status enabled'}, status=202)
            return Response({'status':200,'message':'Supply capabilites changed to enabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['post'])
@permission_classes([AllowAny,])
def delete_supply_capabilities_master(request):
    # delete supply_capabilities  passing primary key(supplyid)
    data=request.data
    supplyid=data['supplyid']
    try:
        supplyobj=SupplyCapabilitiesMaster.objects.filter(supply_capability_id__in=supplyid).values()
        if supplyobj:
            for i in range(0,len(supplyobj)):
                print(supplyobj[i].get('supply_capability_id'))
                supplyobjget=SupplyCapabilitiesMaster.objects.get(supply_capability_id=supplyobj[i].get('supply_capability_id'))
                if supplyobjget:
                    supplyobjget.delete()
            return Response({'status':204,'message':'Supply capabilites data deleted'},status=204)
        return Response({'status': 200, 'message': 'Supply capabilites data not present or already deleted'}, status=200)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['post'])
@permission_classes([AllowAny,])
def delete_uom_master(request):
    data=request.data
    uomid=data['uomid']
    try:
        uomobj=UOMMaster.objects.filter(uom_id__in=uomid).values()
        if len(uomobj)>0:
            for i in range(0,len(uomobj)):
                uomget=UOMMaster.objects.get(uom_id=uomobj[i].get('uom_id'))
                if uomget:
                    uomget.delete()
            return Response({'status': 204, 'message': 'UOM details are deleted'}, status=204)
        return Response({'status': 202, 'message': 'UOM data not present or already deleted'}, status=202)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def disable_uom_master(request):
    data=request.data
    uomid=data['uomid']
    try:
        uomobj=UOMMaster.objects.filter(uom_id__in=uomid).values()
        if len(uomobj)>0:
            for i in range(0,len(uomobj)):
                uomget=UOMMaster.objects.get(uom_id=uomobj[i].get('uom_id'))
                if uomget.status=='Active':
                    uomget.status='Disabled'
                    uomget.save()
                else:
                    return Response({'status':202,'message':'UOM status already changed to disabled'},status=202)
            return Response({'status': 202, 'message': 'UOM status changed to disabled'}, status=202)
        return Response({'status': 204, 'message': 'UOM data not present'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def enable_uom_master(request):
    data=request.data
    uomid=data['uomid']
    try:
        uomobj=UOMMaster.objects.filter(uom_id__in=uomid).values()
        if len(uomobj)>0:
            for i in range(0,len(uomobj)):
                uomget=UOMMaster.objects.get(uom_id=uomobj[i].get('uom_id'))
                if uomget.status=='Disabled':
                    uomget.status='Active'
                    uomget.save()
                else:
                    return Response({'status':202,'message':'UOM masters already enabled'},status=202)
            return Response({'status': 202, 'message': 'UOM status changed to enable'}, status=202)
        return Response({'status': 204, 'message': 'UOM data not present'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['get'])
@permission_classes([AllowAny,])
def all_masters(request):
    masterslist=[]
    try:
        maincoremasterobj=MaincoreMaster.objects.filter().values().order_by('maincore_id')
        if maincoremasterobj:
            masterslist.append({'maincore_masters':maincoremasterobj})
        categorymasterobj=CategoryMaster.objects.filter().values().order_by('category_id')
        if categorymasterobj:
            masterslist.append({'category_master': categorymasterobj})
        subcategorymasterobj=SubCategoryMaster.objects.filter().values().order_by('sub_category_id')
        if subcategorymasterobj:
            masterslist.append({'sub_category_master': subcategorymasterobj})
        uommasterobj=UOMMaster.objects.filter().values().order_by('uom_id')
        if uommasterobj:
            masterslist.append({'uom_master': uommasterobj})
        departmentmasterobj = DepartmentMaster.objects.filter().values().order_by('department_id')
        if departmentmasterobj:
            masterslist.append({'department_master': departmentmasterobj})
        designationmasterobj = DesignationMaster.objects.filter().values().order_by('designation_id')
        if designationmasterobj:
            masterslist.append({'designation_master': designationmasterobj})
        taxmasterobj=TaxMaster.objects.filter().values().order_by('tax_id')
        if taxmasterobj:
            masterslist.append({'tax_master': taxmasterobj})
        hsnmasterobj = HSNMaster.objects.filter().values()
        if hsnmasterobj:
            masterslist.append({'hsn_master': hsnmasterobj})
        sacmasterobj = SACMaster.objects.filter().values()
        if sacmasterobj:
            masterslist.append({'sac_master': sacmasterobj})
        currencymasterobj = CurrencyMaster.objects.filter().values()
        if currencymasterobj:
            masterslist.append({'currency_master': currencymasterobj})
        pfchargesmasterobj = PFChargesMaster.objects.filter().values()
        if pfchargesmasterobj:
            masterslist.append({'p_f_charges_master': pfchargesmasterobj})
        freightmasterobj = FrieghtChargesMaster.objects.filter().values()
        if freightmasterobj:
            masterslist.append({'freight_master': freightmasterobj})
        warrantymasterobj = WarrantyMaster.objects.filter().values()
        if warrantymasterobj:
            masterslist.append({'warranty_master': warrantymasterobj})
        guaranteemasterobj = GuaranteeMaster.objects.filter().values()
        if guaranteemasterobj:
            masterslist.append({'guarantee_master': guaranteemasterobj})
        deliverymasterobj = DeliveryMaster.objects.filter().values()
        if deliverymasterobj:
            masterslist.append({'delivery_master': deliverymasterobj})
        transitinsurancemasterobj=TransitInsuranceMaster.objects.filter().values()
        if transitinsurancemasterobj:
            masterslist.append({'transit_insurance_master': transitinsurancemasterobj})
        pricebasismasterobj=PriceBasisMaster.objects.filter().values()
        if pricebasismasterobj:
            masterslist.append({'price_basis_master': pricebasismasterobj})
        inspectionmasterobj=InspectionMaster.objects.filter().values()
        if inspectionmasterobj:
            masterslist.append({'inspection_master': inspectionmasterobj})
        validitymasterobj=ValidityMaster.objects.filter().values()
        if validitymasterobj:
            masterslist.append({'validity_master': validitymasterobj})
        liquidateddamagesmasterobj=LiquidatedDamageMaster.objects.filter().values()
        if liquidateddamagesmasterobj:
            masterslist.append({'liquidated_damage_master': liquidateddamagesmasterobj})
        taxesdutiesmasterobj=TaxesAndDutiesMaster.objects.filter().values()
        if taxesdutiesmasterobj:
            masterslist.append({'taxes_duties_master': taxesdutiesmasterobj})
        testqapmasterobj = TestAndQapMaster.objects.filter().values()
        if testqapmasterobj:
            masterslist.append({'test_qap_master': testqapmasterobj})
        performanceguaranteemasterobj=PerformanceGuaranteesMaster.objects.filter().values()
        if performanceguaranteemasterobj:
            masterslist.append({'performance_guarantee_master':performanceguaranteemasterobj})
        return Response({'status': 200, 'message': 'Masters List','data':masterslist}, status=200)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def disable_maincore_master(request):
    # disable maincore master by changing status from Active to Disabled by passing primary key(maincoreid)
    data=request.data
    maincoreid=data['maincoreid']
    try:
        maincoreobj=MaincoreMaster.objects.filter(maincore_id__in=maincoreid).values()
        if maincoreobj:
            for i in range(0,len(maincoreobj)):
                print(maincoreobj[i].get('maincore_id'))
                maincoreobjget=MaincoreMaster.objects.get(maincore_id=maincoreobj[i].get('maincore_id'))
                print(maincoreobjget)
                if maincoreobjget.status=='Active':
                    maincoreobjget.status='Disabled'
                    maincoreobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status disabled'}, status=202)
            return Response({'status':200,'message':'Maincore Master status changed to disabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['put'])
@permission_classes([AllowAny,])
def enable_maincore_master(request):
    # enable maincore master by changing status from Disabled to Active by passing primary key(maincoreid)
    data=request.data
    maincoreid=data['maincoreid']
    try:
        maincoreobj=MaincoreMaster.objects.filter(maincore_id__in=maincoreid).values()
        if maincoreobj:
            for i in range(0,len(maincoreobj)):
                print(maincoreobj[i].get('supply_capability_id'))
                maincoreobjget=MaincoreMaster.objects.get(maincore_id=maincoreobj[i].get('maincore_id'))
                print(maincoreobjget)
                if maincoreobjget.status=='Disabled':
                    maincoreobjget.status='Active'
                    maincoreobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status enabled'}, status=202)
            return Response({'status':200,'message':'Maincore Master status changed to enabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['post'])
@permission_classes([AllowAny,])
def delete_maincore_master(request):
    # delete maincore master  passing primary key(maincoreid)
    data=request.data
    maincoreid=data['maincoreid']
    try:
        maincoreobj=MaincoreMaster.objects.filter(maincore_id__in=maincoreid).values()
        if maincoreobj:
            for i in range(0,len(maincoreobj)):
                print(maincoreobj[i].get('supply_capability_id'))
                maincoreobjget=MaincoreMaster.objects.get(maincore_id=maincoreobj[i].get('maincore_id'))
                if maincoreobjget:
                    maincoreobjget.delete()
            return Response({'status':204,'message':'Maincore Masters data deleted'},status=204)
        return Response({'status': 200, 'message': 'Maincore Masters data not present or already deleted'}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def disable_category_master(request):
    # disable category master by changing status from Disabled to Active by passing primary key(categoryid)
    data=request.data
    categoryid=data['categoryid']
    try:
        categoryobj=CategoryMaster.objects.filter(category_id__in=categoryid).values()
        if categoryobj:
            for i in range(0,len(categoryobj)):
                print(categoryobj[i].get('category_id'))
                categoryobjget=CategoryMaster.objects.get(category_id=categoryobj[i].get('category_id'))
                print(categoryobjget)
                if categoryobjget.status=='Active':
                    categoryobjget.status='Disabled'
                    categoryobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status disabled'}, status=202)
            return Response({'status':200,'message':'Category Master status changed to disabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def enable_category_master(request):
    # enable category master by changing status from Disabled to Active by passing primary key(categoryid)
    data=request.data
    categoryid=data['categoryid']
    try:
        categoryobj=CategoryMaster.objects.filter(category_id__in=categoryid).values()
        if categoryobj:
            for i in range(0,len(categoryobj)):
                print(categoryobj[i].get('category_id'))
                categoryobjget=CategoryMaster.objects.get(category_id=categoryobj[i].get('category_id'))
                print(categoryobjget)
                if categoryobjget.status=='Disabled':
                    categoryobjget.status='Active'
                    categoryobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status enabled'}, status=202)
            return Response({'status':200,'message':'Category Master status changed to enabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['post'])
@permission_classes([AllowAny,])
def delete_category_master(request):
    # delete category master by passing primary key(categoryid)
    data=request.data
    categoryid=data['categoryid']
    try:
        categoryobj=CategoryMaster.objects.filter(category_id__in=categoryid).values()
        if categoryobj:
            for i in range(0,len(categoryobj)):
                categoryobjget=CategoryMaster.objects.get(category_id=categoryobj[i].get('category_id'))
                if categoryobjget:
                    categoryobjget.delete()
            return Response({'status': 204, 'message': 'Category Masters data deleted'}, status=204)
        return Response({'status': 200, 'message': 'Category Masters data not present or already deleted'},
                            status=200)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def disable_sub_category_master(request):
    # disable sub_category master by changing status from Disabled to Active by passing primary key(subcategoryid)
    data=request.data
    subcategoryid=data['subcategoryid']
    try:
        subcategoryobj=SubCategoryMaster.objects.filter(sub_category_id__in=subcategoryid).values()
        if subcategoryobj:
            for i in range(0,len(subcategoryobj)):
                print(subcategoryobj[i].get('sub_category_id'))
                subcategoryobjget=SubCategoryMaster.objects.get(sub_category_id=subcategoryobj[i].get('sub_category_id'))
                print(subcategoryobjget)
                if subcategoryobjget.status=='Active':
                    subcategoryobjget.status='Disabled'
                    subcategoryobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status Disabled'}, status=202)
            return Response({'status':200,'message':'Sub Category Master status changed to Disabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def enable_sub_category_master(request):
    # enable sub_category master by changing status from Disabled to Active by passing primary key(subcategoryid)
    data=request.data
    subcategoryid=data['subcategoryid']
    try:
        subcategoryobj=SubCategoryMaster.objects.filter(sub_category_id__in=subcategoryid).values()
        if subcategoryobj:
            for i in range(0,len(subcategoryobj)):
                print(subcategoryobj[i].get('sub_category_id'))
                subcategoryobjget=SubCategoryMaster.objects.get(sub_category_id=subcategoryobj[i].get('sub_category_id'))
                print(subcategoryobjget)
                if subcategoryobjget.status=='Disabled':
                    subcategoryobjget.status='Active'
                    subcategoryobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status enabled'}, status=202)
            return Response({'status':200,'message':'Sub Category Master status changed to enabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['post'])
@permission_classes([AllowAny,])
def delete_sub_category_master(request):
    # delete sub_category master by passing primary key(subcategoryid)
    data=request.data
    subcategoryid=data['subcategoryid']
    try:
        subcategoryobj=SubCategoryMaster.objects.filter(sub_category_id__in=subcategoryid).values()
        if subcategoryobj:
            for i in range(0,len(subcategoryobj)):
                subcategoryobjget=SubCategoryMaster.objects.get(sub_category_id=subcategoryobj[i].get('sub_category_id'))
                if subcategoryobjget:
                    subcategoryobjget.delete()
            return Response({'status': 204, 'message': 'Sub Category Masters data deleted'}, status=204)
        return Response({'status': 200, 'message': 'Sub Category Masters data not present or already deleted'},
                            status=200)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)



class IndustryServeUploadView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        rowdata=[]
        alldata=[]
        paramFile =request.data['csv_industry_file']
        # portfolio1 = csv.DictReader(paramFile)
        # list_of_dict = list(portfolio1)
        decoded_file = paramFile.read().decode()
        # upload_products_csv.delay(decoded_file, request.user.pk)
        io_string = io.StringIO(decoded_file)
        list_of_dict = csv.DictReader(io_string)
        try:
            industryobj = IndustryToServeMaster.objects.filter().values()
            for i in range(0,len(industryobj)):
                rowdata.append(industryobj[i].get('industry_name'))
            print(rowdata)
            for row in list_of_dict:
                if row['industry_name'] not in rowdata and row!="":
                    industryobj1= IndustryToServeMaster.objects.last()
                    print('no data,sorry')
                    code = int(industryobj1.industry_code)
                    # print(code)
                    industrycodeval=code+1
                    # print(industrycodeval,'cxc')
                    objs = [
                        IndustryToServeMaster(
                            industry_name=row['industry_name'],
                            csv_industry=paramFile,
                            industry_code=industrycodeval

                        )]
                    msg = IndustryToServeMaster.objects.bulk_create(objs)
                    print(msg, 'meeeee')
                else:
                    if row['industry_name'] in rowdata:
                        rowdata.append(row['industry_name'])
                        print(row['industry_name'],'already present')
                        continue
            return Response({'status': 200, 'message': 'ok','data':rowdata}, status=200)

        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)


class ItemGroupMasterView(viewsets.ModelViewSet):
    # item group master viewsets
    permission_classes = (AllowAny,)
    queryset = ItemGroupMaster.objects.all()
    serializer_class= ItemGroupMasterSerializer
    ordering_fields = ['item_group_id']
    ordering = ['item_group_id']

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        itemgroupobj = ItemGroupMaster.objects.filter(updated_by=self.request.GET.get('updated_by'))
        itemgroupdataobj=ItemGroupMaster.objects.filter(admins=1).values()
        itemgroupval=list(chain(itemgroupobj,itemgroupdataobj))
        if itemgroupobj:
            return itemgroupobj
        elif itemgroupdataobj and itemgroupobj:
            return  itemgroupval
        raise ValidationError({'message': 'Item group Master details not exist','status': 204})




@api_view(['put'])
@permission_classes([AllowAny,])
def disable_item_group_master(request):
    # disable item group master by changing status from Disabled to Active by passing primary key(subcategoryid)
    data=request.data
    itemgroupid=data['itemgroupid']
    try:
        itemgroupobj=ItemGroupMaster.objects.filter(item_group_id__in=itemgroupid).values()
        if itemgroupobj:
            for i in range(0,len(itemgroupobj)):
                print(itemgroupobj[i].get('item_group_id'))
                itemgroupobjget=ItemGroupMaster.objects.get(item_group_id=itemgroupobj[i].get('item_group_id'))
                print(itemgroupobjget)
                if itemgroupobjget.status=='Active':
                    itemgroupobjget.status='Disabled'
                    itemgroupobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status Disabled'}, status=202)
            return Response({'status':200,'message':'Item group Master status changed to Disabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def enable_item_group_master(request):
    # enable item group master by changing status from Disabled to Active by passing primary key(subcategoryid)
    data=request.data
    itemgroupid=data['itemgroupid']
    try:
        itemgroupobj=ItemGroupMaster.objects.filter(item_group_id__in=itemgroupid).values()
        if itemgroupobj:
            for i in range(0,len(itemgroupobj)):
                print(itemgroupobj[i].get('item_group_id'))
                itemgroupobjget=ItemGroupMaster.objects.get(item_group_id=itemgroupobj[i].get('item_group_id'))
                print(itemgroupobjget)
                if itemgroupobjget.status=='Disabled':
                    itemgroupobjget.status='Active'
                    itemgroupobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status Enabled'}, status=202)
            return Response({'status':200,'message':'Item group Master status changed to Enabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['post'])
@permission_classes([AllowAny,])
def delete_item_group_master(request):
    # enable item group master by changing status from Disabled to Active by passing primary key(subcategoryid)
    data=request.data
    itemgroupid=data['itemgroupid']
    try:
        itemgroupobj=ItemGroupMaster.objects.filter(item_group_id__in=itemgroupid).values()
        if itemgroupobj:
            for i in range(0,len(itemgroupobj)):
                print(itemgroupobj[i].get('item_group_id'))
                itemgroupobjget=ItemGroupMaster.objects.get(item_group_id=itemgroupobj[i].get('item_group_id'))
                print(itemgroupobjget)
                if itemgroupobjget:
                    itemgroupobjget.delete()
            return Response({'status':204, 'message':'Item group Master status data deleted'},status=204)
        return Response({'status': 200, 'message': 'Item group Masters data not present or already deleted'},
                        status=200)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)




@api_view(['put'])
@permission_classes([AllowAny,])
def disable_hsn_master(request):
    # disable hsn_master by changing status from Active to Disabled by passing primary key(hsnid)
    data=request.data
    hsnid=data['hsnid']
    try:
        hsnobj=HSNMaster.objects.filter(hsn_id__in=hsnid).values()
        if hsnobj:
            for i in range(0,len(hsnobj)):
                hsnobjget=HSNMaster.objects.get(hsn_id=hsnobj[i].get('hsn_id'))
                print(hsnobjget)
                if hsnobjget.status=='Active':
                    hsnobjget.status='Disabled'
                    hsnobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status disabled'}, status=202)
            return Response({'status':200,'message':'HSN Master status changed to disabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def enable_hsn_master(request):
    # enable hsn_master by changing status from Active to Disabled by passing primary key(hsnid)
    data=request.data
    hsnid=data['hsnid']
    try:
        hsnobj=HSNMaster.objects.filter(hsn_id__in=hsnid).values()
        if hsnobj:
            for i in range(0,len(hsnobj)):
                hsnobjget=HSNMaster.objects.get(hsn_id=hsnobj[i].get('hsn_id'))
                print(hsnobjget)
                if hsnobjget.status=='Disabled':
                    hsnobjget.status='Active'
                    hsnobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status enabled'}, status=202)
            return Response({'status':200,'message':'HSN Master status changed to enabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['post'])
@permission_classes([AllowAny,])
def delete_hsn_master(request):
    # delete hsn_master by passing primary key(hsnid)
    data=request.data
    hsnid=data['hsnid']
    try:
        hsnobj=HSNMaster.objects.filter(hsn_id__in=hsnid).values()
        if hsnobj:
            for i in range(0,len(hsnobj)):
                hsnobjget=HSNMaster.objects.get(hsn_id=hsnobj[i].get('hsn_id'))
                if hsnobjget:
                    hsnobjget.delete()

            return Response({'status': 204, 'message': 'HSN Master data deleted'}, status=204)
        return Response({'status':200,'message':'HSN Master data not present or already deleted'},status=200)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)




@api_view(['put'])
@permission_classes([AllowAny,])
def disable_sac_master(request):
    # disable sac_master by changing status from Active to Disabled by passing primary key(sacid)
    data=request.data
    sacid=data['sacid']
    try:
        sacobj=SACMaster.objects.filter(sac_id__in=sacid).values()
        if sacobj:
            for i in range(0,len(sacobj)):
                sacobjget=SACMaster.objects.get(sac_id=sacobj[i].get('sac_id'))
                print(sacobjget)
                if sacobjget.status=='Active':
                    sacobjget.status='Disabled'
                    sacobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status disabled'}, status=202)
            return Response({'status':200,'message':'SAC Master status changed to disabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def enable_sac_master(request):
    # enable sac_master by changing status from Active to Disabled by passing primary key(sacid)
    data=request.data
    sacid=data['sacid']
    try:
        sacobj=SACMaster.objects.filter(sac_id__in=sacid).values()
        if sacobj:
            for i in range(0,len(sacobj)):
                sacobjget=SACMaster.objects.get(sac_id=sacobj[i].get('sac_id'))
                print(sacobjget)
                if sacobjget.status=='Disabled':
                    sacobjget.status='Active'
                    sacobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status enabled'}, status=202)
            return Response({'status':200,'message':'SAC Master status changed to enabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['post'])
@permission_classes([AllowAny,])
def delete_sac_master(request):
    # delete hsn_master by passing primary key(sacid)
    data=request.data
    sacid=data['sacid']
    try:
        sacobj=SACMaster.objects.filter(sac_id__in=sacid).values()
        if sacobj:
            for i in range(0,len(sacobj)):
                sacobjget=SACMaster.objects.get(sac_id=sacobj[i].get('sac_id'))
                if sacobjget:
                    sacobjget.delete()

            return Response({'status': 204, 'message': 'SAC Master data deleted'}, status=204)
        return Response({'status':200,'message':'SAC Master data not present or already deleted'},status=200)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def disable_currency_master(request):
    # disable currency_master by changing status from Active to Disabled by passing primary key(currencyid)
    data=request.data
    currencyid=data['currencyid']
    try:
        currencyobj=CurrencyMaster.objects.filter(currency_id__in=currencyid).values()
        if currencyobj:
            for i in range(0,len(currencyobj)):
                currencyobjget=CurrencyMaster.objects.get(currency_id=currencyobj[i].get('currency_id'))
                if currencyobjget.status=='Active':
                    currencyobjget.status='Disabled'
                    currencyobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status disabled'}, status=202)
            return Response({'status':200,'message':'Currency Master status changed to disabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def enable_currency_master(request):
    # enable currency_master by changing status from Active to Disabled by passing primary key(currencyid)
    data=request.data
    currencyid=data['currencyid']
    try:
        currencyobj=CurrencyMaster.objects.filter(currency_id__in=currencyid).values()
        if currencyobj:
            for i in range(0,len(currencyobj)):
                currencyobjget=CurrencyMaster.objects.get(currency_id=currencyobj[i].get('currency_id'))
                if currencyobjget.status=='Disabled':
                    currencyobjget.status='Active'
                    currencyobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status enabled'}, status=202)
            return Response({'status':200,'message':'Currency Master status changed to enabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['post'])
@permission_classes([AllowAny,])
def delete_currency_master(request):
    # delete currency_master by passing primary key(currencyid)
    data=request.data
    currencyid=data['currencyid']
    try:
        currencyobj = CurrencyMaster.objects.filter(currency_id__in=currencyid).values()
        if currencyobj:
            for i in range(0, len(currencyobj)):
                currencyobjget = CurrencyMaster.objects.get(currency_id=currencyobj[i].get('currency_id'))
                if currencyobjget:
                    currencyobjget.delete()

            return Response({'status': 204, 'message': 'Currency Master data deleted'}, status=204)
        return Response({'status':200,'message':'Currency Master data not present or already deleted'},status=200)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)






@api_view(['put'])
@permission_classes([AllowAny,])
def enable_frieght_charges_master(request):
    # enable frieght by changing status from Active to Disabled by passing primary key(freightid)
    data=request.data
    frieght_id=data['frieght_id']
    try:
        frieghtobj=FrieghtChargesMaster.objects.filter(frieght_id__in=frieght_id).values()
        if frieghtobj:
            for i in range(0,len(frieghtobj)):
                freightobjget=FrieghtChargesMaster.objects.get(frieght_id=frieghtobj[i].get('frieght_id'))
                if freightobjget.status=='Disabled':
                    freightobjget.status='Active'
                    freightobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status enabled'}, status=202)
            return Response({'status':200,'message':'Frieght Charges Master status changed to enabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def disable_frieght_charges_master(request):
    # disable frieght by changing status from Active to Disabled by passing primary key(freightid)
    data=request.data
    frieght_id=data['frieght_id']
    try:
        frieghtobj=FrieghtChargesMaster.objects.filter(frieght_id__in=frieght_id).values()
        if frieghtobj:
            for i in range(0,len(frieghtobj)):
                freightobjget=FrieghtChargesMaster.objects.get(frieght_id=frieghtobj[i].get('frieght_id'))
                if freightobjget.status=='Active':
                    freightobjget.status='Disabled'
                    freightobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status disabled'}, status=202)
            return Response({'status':200,'message':'Frieght Charges Master status changed to disabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['post'])
@permission_classes([AllowAny,])
def delete_freight_master(request):
    # delete frieght_master by passing primary key(frieghtid)
    data=request.data
    frieght_id = data['frieght_id']
    try:
        freightobj = FrieghtChargesMaster.objects.filter(frieght_id__in=frieght_id).values()
        if freightobj:
            for i in range(0, len(freightobj)):
                frieghtobjget = FrieghtChargesMaster.objects.get(frieght_id=freightobj[i].get('frieght_id'))
                if frieghtobjget:
                    frieghtobjget.delete()

            return Response({'status': 204, 'message': 'Frieght Master data deleted'}, status=204)
        return Response({'status':200,'message':'Frieght Master data not present or already deleted'},status=200)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)



@api_view(['post'])
@permission_classes([AllowAny,])
def pf_charges_master_get_by_userid(request):
    data=request.data
    userid = data['userid']
    try:
        pfchargeobj = PFChargesMaster.objects.filter(updated_by=userid).values()
        pfchargeadmin=PFChargesMaster.objects.filter(admins=1).values()
        pfchargeval=list(chain(pfchargeobj,pfchargeadmin))
        if len(pfchargeobj)!=0 or len(pfchargeadmin)!=0:
            return Response({'status':200,'message':'PF charges all data','data':pfchargeval},status=200)
        elif len(pfchargeobj)==0 or len(pfchargeadmin)!=0:
            return Response({'status': 200, 'message': 'pf charge admins datas', 'data': pfchargeadmin}, status=200)
        elif len(pfchargeobj)!=0 and len(pfchargeadmin)!=0:
            return Response({'status': 200, 'message': 'pf charge all datas datas', 'data': pfchargeval}, status=200)
        else:
            return Response({'status':204,'message':'noo'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['put'])
@permission_classes([AllowAny,])
def disable_pf_charge_master(request):
    # disable pf_charge_master by changing status from Active to Disabled by passing primary key(pfchargeid)
    data=request.data
    pfchargeid=data['pfchargeid']
    try:
        pfchargeobj=PFChargesMaster.objects.filter(pf_charge_id__in=pfchargeid).values()
        if pfchargeobj:
            for i in range(0,len(pfchargeobj)):
                pfchargeobjget=PFChargesMaster.objects.get(pf_charge_id=pfchargeobj[i].get('pf_charge_id'))
                if pfchargeobjget.status=='Active':
                    pfchargeobjget.status='Disabled'
                    pfchargeobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status disabled'}, status=202)
            return Response({'status':200,'message':'PF Charges Master status changed to disabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def enable_pf_charge_master(request):
    # enable pf_charge master by changing status from Active to Disabled by passing primary key(pfchargeid)
    data=request.data
    pfchargeid=data['pfchargeid']
    try:
        pfchargeobj=PFChargesMaster.objects.filter(pf_charge_id__in=pfchargeid).values()
        if pfchargeobj:
            for i in range(0,len(pfchargeobj)):
                pfchargeobjget=PFChargesMaster.objects.get(pf_charge_id=pfchargeobj[i].get('pf_charge_id'))
                if pfchargeobjget.status=='Disabled':
                    pfchargeobjget.status='Active'
                    pfchargeobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status enabled'}, status=202)
            return Response({'status':200,'message':'PF Charges Master status changed to enabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['post'])
@permission_classes([AllowAny,])
def delete_pf_charge_master(request):
    # delete pf_charge_master by passing primary key(pfchargeid)
    data=request.data
    pfchargeid=data['pfchargeid']
    try:
        pfchargeobj = PFChargesMaster.objects.filter(pf_charge_id__in=pfchargeid).values()
        if pfchargeobj:
            for i in range(0, len(pfchargeobj)):
                pfchargeobjget = PFChargesMaster.objects.get(pf_charge_id=pfchargeobj[i].get('pf_charge_id'))
                if pfchargeobjget:
                    pfchargeobjget.delete()

            return Response({'status': 204, 'message': 'PF Charges Master data deleted'}, status=204)
        return Response({'status':200,'message':'PF Charges Master data not present or already deleted'},status=200)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['post'])
@permission_classes([AllowAny,])
def pf_charges_master_get_by_userid(request):
    data=request.data
    userid = data['userid']
    try:
        pfchargeobj = PFChargesMaster.objects.filter(updated_by=userid).values()
        pfchargeadmin=PFChargesMaster.objects.filter(admins=1).values()
        pfchargeval=list(chain(pfchargeobj,pfchargeadmin))
        if len(pfchargeobj)==0:
            return Response({'status': 200, 'message': 'pf charge admins datas', 'data': pfchargeadmin}, status=200)
        if len(pfchargeadmin) == 0:
            return Response({'status': 200, 'message': 'pf charge admins datas', 'data': pfchargeobj}, status=200)
        elif len(pfchargeobj)!=0 and len(pfchargeadmin)!=0:
            return Response({'status': 200, 'message': 'pf charge all datas', 'data': pfchargeval}, status=200)
        else:
            return Response({'status':204,'message':'noo'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes([AllowAny,])
def frieght_masters_user_id(request):
    data=request.data
    userid = data['userid']
    try:
        frieghtobj = FrieghtChargesMaster.objects.filter(updated_by=userid).values().order_by('frieght_id')
        freightadmin=FrieghtChargesMaster.objects.filter(admins=1).values().order_by('frieght_id')
        frieghtval=list(chain(frieghtobj,freightadmin))
        if len(frieghtobj)==0:
            return Response({'status': 200, 'message': 'frieght datas', 'data': freightadmin}, status=200)
        if len(freightadmin) == 0:
            return Response({'status': 200, 'message': 'freight admins datas', 'data': frieghtobj}, status=200)
        elif len(frieghtobj)!=0 and len(freightadmin)!=0:
            return Response({'status': 200, 'message': 'frieght all datas', 'data':frieghtval}, status=200)
        else:
            return Response({'status':204,'message':'noo'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
@permission_classes([AllowAny,])
def hsn_masters_user_id(request):
    data=request.data
    userid = data['userid']
    try:
        hsnobj = HSNMaster.objects.filter(updated_by=userid).values()
        hsnadmin=HSNMaster.objects.filter(admins=1).values()
        hsnval=list(chain(hsnobj,hsnadmin))
        if len(hsnobj)==0:
            return Response({'status': 200, 'message': 'hsn masters data', 'data': hsnadmin}, status=200)
        if len(hsnadmin) == 0:
            return Response({'status': 200, 'message': 'hsn master admins datas', 'data': hsnobj}, status=200)
        elif len(hsnobj)!=0 and len(hsnadmin)!=0:
            return Response({'status': 200, 'message': 'hsn master all datas', 'data':hsnval}, status=200)
        else:
            return Response({'status':204,'message':'noo'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
@permission_classes([AllowAny,])
def sac_masters_user_id(request):
    data=request.data
    userid = data['userid']
    try:
        sacobj = SACMaster.objects.filter(updated_by=userid).values()
        sacadmin=SACMaster.objects.filter(admins=1).values()
        sacval=list(chain(sacobj,sacadmin))
        if len(sacobj)==0:
            return Response({'status': 200, 'message': 'sac masters data', 'data': sacadmin}, status=200)
        if len(sacobj) == 0:
            return Response({'status': 200, 'message': 'sac masters admins datas', 'data': sacobj}, status=200)
        elif len(sacobj)!=0 and len(sacadmin)!=0:
            return Response({'status': 200, 'message': 'sac masters all datas', 'data':sacval}, status=200)
        else:
            return Response({'status':204,'message':'noo'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['put'])
@permission_classes([AllowAny,])
def disable_guarantee_master(request):
    # disable guarantee master by changing status from Active to Disabled by passing primary key(guaranteeid)
    data=request.data
    guaranteeid=data['guaranteeid']
    try:
        guaranteeobj=GuaranteeMaster.objects.filter(guarantee_id__in=guaranteeid).values()
        if guaranteeobj:
            for i in range(0,len(guaranteeobj)):
                guaranteeobjget=GuaranteeMaster.objects.get(guarantee_id=guaranteeobj[i].get('guarantee_id'))
                print(guaranteeobjget)
                if guaranteeobjget.status=='Active':
                    guaranteeobjget.status='Disabled'
                    guaranteeobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status disabled'}, status=202)
            return Response({'status':200,'message':'Guarantee Master status changed to disabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def enable_guarantee_master(request):
    # disable guarantee master by changing status from Active to Disabled by passing primary key(guaranteeid)
    data=request.data
    guaranteeid=data['guaranteeid']
    try:
        guaranteeobj=GuaranteeMaster.objects.filter(guarantee_id__in=guaranteeid).values()
        if guaranteeobj:
            for i in range(0,len(guaranteeobj)):
                guaranteeobjget=GuaranteeMaster.objects.get(guarantee_id=guaranteeobj[i].get('guarantee_id'))
                print(guaranteeobjget)
                if guaranteeobjget.status=='Disabled':
                    guaranteeobjget.status='Active'
                    guaranteeobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status enabled'}, status=202)
            return Response({'status':200,'message':'Guarantee Master status changed to enabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['post'])
@permission_classes([AllowAny,])
def delete_guarantee_master(request):
    # delete guarantee master by passing primary key(guaranteeid)
    data=request.data
    guaranteeid=data['guaranteeid']
    try:
        guaranteeobj = GuaranteeMaster.objects.filter(guarantee_id__in=guaranteeid).values()
        if guaranteeobj:
            for i in range(0, len(guaranteeobj)):
                guaranteeobjget = GuaranteeMaster.objects.get(guarantee_id=guaranteeobj[i].get('guarantee_id'))
                if guaranteeobjget:
                    guaranteeobjget.delete()

            return Response({'status': 204, 'message': 'Guarantee Master data deleted'}, status=204)
        return Response({'status':200,'message':'Guarantee Master data not present or already deleted'},status=200)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['post'])
@permission_classes([AllowAny,])
def guarantee_masters_user_id(request):
    data=request.data
    userid = data['userid']
    try:
        guaranteeobj = GuaranteeMaster.objects.filter(updated_by=userid).values()
        guaranteeadmin=GuaranteeMaster.objects.filter(admins=1).values()
        guarateeval=list(chain(guaranteeobj,guaranteeadmin))
        if len(guaranteeobj)==0:
            return Response({'status': 200, 'message': 'guarantee masters data', 'data': guaranteeadmin}, status=200)
        if len(guaranteeadmin) == 0:
            return Response({'status': 200, 'message': 'guarantee admins datas', 'data': guaranteeobj}, status=200)
        elif len(guaranteeobj)!=0 and len(guaranteeadmin)!=0:
            return Response({'status': 200, 'message': 'guarantee all datas', 'data':guarateeval}, status=200)
        else:
            return Response({'status':204,'message':'noo'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)







@api_view(['put'])
@permission_classes([AllowAny,])
def disable_designation_master(request):
    # disable designation master by changing status from Active to Disabled by passing primary key(designationid)
    data=request.data
    designationid=data['designationid']
    try:
        designationobj=DesignationMaster.objects.filter(designation_id__in=designationid).values()
        if designationobj:
            for i in range(0,len(designationobj)):
                designationobjget=DesignationMaster.objects.get(designation_id=designationobj[i].get('designation_id'))
                print(designationobjget)
                if designationobjget.status=='Active':
                    designationobjget.status='Disabled'
                    designationobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status disabled'},status=202)
            return Response({'status':200,'message':'Designation Master status changed to disabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def enable_designation_master(request):
    # enable designation master by changing status from Active to Disabled by passing primary key(designationid)
    data=request.data
    designationid=data['designationid']
    try:
        designationobj=DesignationMaster.objects.filter(designation_id__in=designationid).values()
        if designationobj:
            for i in range(0,len(designationobj)):
                designationobjget=DesignationMaster.objects.get(designation_id=designationobj[i].get('designation_id'))
                print(designationobjget)
                if designationobjget.status=='Disabled':
                    designationobjget.status='Active'
                    designationobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status enabled'}, status=202)
            return Response({'status':200,'message':'Designation Master status changed to enabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['post'])
@permission_classes([AllowAny,])
def delete_designation_master(request):
    # delete designation master by passing primary key(designationid)
    data=request.data
    designationid=data['designationid']
    try:
        designationobj = DesignationMaster.objects.filter(designation_id__in=designationid).values()
        if designationobj:
            for i in range(0, len(designationobj)):
                designationobjget = DesignationMaster.objects.get(designation_id=designationobj[i].get('designation_id'))
                print(designationobjget)
                if designationobjget:
                    designationobjget.delete()

            return Response({'status': 204, 'message': 'Designation Master data deleted'}, status=204)
        return Response({'status':200,'message':'Designation Master data not present or already deleted'},status=200)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)



@api_view(['post'])
@permission_classes([AllowAny,])
def designation_masters_user_id(request):
    data=request.data
    userid = data['userid']
    try:
        designationobj = DesignationMaster.objects.filter(updated_by=userid).values().order_by('designation_id')
        designationadmin=DesignationMaster.objects.filter(admins=1).values().order_by('designation_id')
        designationval=list(chain(designationobj,designationadmin))
        if len(designationobj)==0:
            return Response({'status': 200, 'message': 'Designation masters data', 'data': designationadmin}, status=200)
        if len(designationadmin) == 0:
            return Response({'status': 200, 'message': 'Designation admins datas', 'data': designationobj}, status=200)
        elif len(designationobj)!=0 and len(designationadmin)!=0:
            return Response({'status': 200, 'message': 'Designation all datas', 'data':designationval}, status=200)
        else:
            return Response({'status':204,'message':'noo'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


class TransitInsuranceMasterView(viewsets.ModelViewSet):
    # transit viewsets
    permission_classes = (AllowAny,)
    queryset = TransitInsuranceMaster.objects.all()
    serializer_class = TransitInsuranceMasterSerializer
    ordering_fields = ['transit_id']
    ordering = ['transit_id']

    # def get_queryset(self):
    #     # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
    #     transitmasterobj = TransitInsuranceMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by(
    #         'transit_id')
    #     if transitmasterobj:
    #         return  transitmasterobj
    #
    #     raise ValidationError({'message': 'Transit Master details not exist', 'status': 204})


@api_view(['put'])
@permission_classes([AllowAny,])
def disable_transit_insurance_master(request):
    # disable transit master by changing status from Active to Disabled by passing primary key(transitid)
    data=request.data
    transitid=data['transitid']
    try:
        transitobj=TransitInsuranceMaster.objects.filter(transit_id__in=transitid).values()
        if transitobj:
            for i in range(0,len(transitobj)):
                transitobjget=TransitInsuranceMaster.objects.get(transit_id=transitobj[i].get('transit_id'))
                if transitobjget.status=='Active':
                    transitobjget.status='Disabled'
                    transitobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status disabled'},status=202)
            return Response({'status':200,'message':'Transit Master status changed to disabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def enable_transit_insurance_master(request):
    # enable transit master by changing status from Active to Disabled by passing primary key(transitid)
    data=request.data
    transitid=data['transitid']
    try:
        transitobj=TransitInsuranceMaster.objects.filter(transit_id__in=transitid).values()
        if transitobj:
            for i in range(0,len(transitobj)):
                transitobjget=TransitInsuranceMaster.objects.get(transit_id=transitobj[i].get('transit_id'))
                if transitobjget.status=='Disabled':
                    transitobjget.status='Active'
                    transitobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status enabled'},status=202)
            return Response({'status':200,'message':'Transit Master status changed to enabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['post'])
@permission_classes([AllowAny,])
def delete_transit_insurance_master(request):
    # delete transit master by passing primary key(transitid)
    data=request.data
    transitid = data['transitid']
    try:
        transitobj = TransitInsuranceMaster.objects.filter(transit_id__in=transitid).values()
        if transitobj:
            for i in range(0, len(transitobj)):
                transitobjget = TransitInsuranceMaster.objects.get(transit_id=transitobj[i].get('transit_id'))
                if transitobjget:
                    transitobjget.delete()

            return Response({'status': 204, 'message': 'Transit Master data deleted'}, status=204)
        return Response({'status':200,'message':'Transit Master data not present or already deleted'},status=200)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['post'])
@permission_classes([AllowAny,])
def transit_insurance_master_user_id(request):
    data=request.data
    userid = data['userid']
    try:
        transitobj = TransitInsuranceMaster.objects.filter(updated_by=userid).values().order_by('transit_id')
        transitadmin=TransitInsuranceMaster.objects.filter(admins=1).values().order_by('transit_id')
        transitval=list(chain(transitobj,transitadmin))
        if len(transitobj)==0:
            return Response({'status': 200, 'message': 'Transit masters data', 'data': transitadmin}, status=200)
        if len(transitadmin) == 0:
            return Response({'status': 200, 'message': 'Transit admins datas', 'data': transitobj}, status=200)
        elif len(transitobj)!=0 and len(transitadmin)!=0:
            return Response({'status': 200, 'message': 'Transit all datas', 'data':transitval}, status=200)
        else:
            return Response({'status':204,'message':'noo'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




#----------------------------------------------------------------------------------------------
class PaymentMasterView(viewsets.ModelViewSet):
    # transit viewsets
    permission_classes = (AllowAny,)
    queryset = PaymentMaster.objects.all()
    serializer_class = PaymentMasterSerializer
    ordering_fields = ['payment_id']
    ordering = ['payment_id']

    # def get_queryset(self):
    #     # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
    #     paymentmasterobj = PaymentMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by(
    #         'payment_id')
    #     if paymentmasterobj:
    #         return paymentmasterobj
    #
    #     raise ValidationError({'message': 'Payment Master details not exist', 'status': 204})



@api_view(['put'])
@permission_classes([AllowAny,])
def disable_payment_master(request):
    # disable payment master by changing status from Active to Disabled by passing primary key(paymentid)
    data=request.data
    paymentid=data['paymentid']
    try:
        paymentobj=PaymentMaster.objects.filter(payment_id__in=paymentid).values()
        if paymentobj:
            for i in range(0,len(paymentobj)):
                paymentobjget=PaymentMaster.objects.get(payment_id=paymentobj[i].get('payment_id'))
                if paymentobjget.status=='Active':
                    paymentobjget.status='Disabled'
                    paymentobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status disabled'},status=202)
            return Response({'status':200,'message':'Payment Master status changed to disabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

@api_view(['put'])
@permission_classes([AllowAny,])
def enable_payment_master(request):
    # enable payment master by changing status from Active to Disabled by passing primary key(paymentid)
    data=request.data
    paymentid=data['paymentid']
    try:
        paymentobj=PaymentMaster.objects.filter(payment_id__in=paymentid).values()
        if paymentobj:
            for i in range(0,len(paymentobj)):
                paymentobjget=PaymentMaster.objects.get(payment_id=paymentobj[i].get('payment_id'))
                if paymentobjget.status=='Disabled':
                    paymentobjget.status='Active'
                    paymentobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status enabled'},status=202)
            return Response({'status':200,'message':'Payment Master status changed to enabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['post'])
@permission_classes([AllowAny,])
def delete_payment_master(request):
    # delete payment master by passing primary key(paymentid)
    data=request.data
    paymentid = data['paymentid']
    try:
        paymentobj = PaymentMaster.objects.filter(payment_id__in=paymentid).values()
        if paymentobj:
            for i in range(0, len(paymentobj)):
                paymentobjget = PaymentMaster.objects.get(payment_id=paymentobj[i].get('payment_id'))
                if paymentobjget:
                    paymentobjget.delete()

            return Response({'status': 204, 'message': 'Payment Master data deleted'}, status=204)
        return Response({'status':200,'message':'Payment Master data not present or already deleted'},status=200)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['post'])
@permission_classes([AllowAny,])
def payment_master_user_id(request):
    data=request.data
    userid = data['userid']
    try:
        paymentobj = PaymentMaster.objects.filter(updated_by=userid).values().order_by('payment_id')
        paymentadmin=PaymentMaster.objects.filter(admins=1).values().order_by('payment_id')
        paymentval=list(chain(paymentobj,paymentadmin))
        if len(paymentobj)==0:
            return Response({'status': 200, 'message': 'Payment masters data', 'data': paymentadmin}, status=200)
        if len(paymentadmin) == 0:
            return Response({'status': 200, 'message': 'Payment admins datas', 'data': paymentobj}, status=200)
        elif len(paymentobj)!=0 and len(paymentadmin)!=0:
            return Response({'status': 200, 'message': 'Payment all datas', 'data':paymentval}, status=200)
        else:
            return Response({'status':204,'message':'noo'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


#------------------------------------------------------------------------------------------------------------------------
class ValidityMasterView(viewsets.ModelViewSet):
    # validity viewsets
    permission_classes = (AllowAny,)
    queryset = ValidityMaster.objects.all().order_by('validity_id')
    serializer_class = ValidityMasterSerializer

    # def get_queryset(self):
    #     # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
    #     validitymasterobj = ValidityMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by(
    #         'validity_id')
    #     if validitymasterobj:
    #         return validitymasterobj
    #
    #     raise ValidationError({'message': 'Validity Master details not exist', 'status': 204})



@api_view(['put'])
@permission_classes([AllowAny,])
def disable_validity_master(request):
    # disable validity master by changing status from Active to Disabled by passing primary key(paymentid)
    data=request.data
    validityid=data['validityid']
    try:
        validityobj=ValidityMaster.objects.filter(validity_id__in=validityid).values()
        if validityobj:
            for i in range(0,len(validityobj)):
                validityobjget=ValidityMaster.objects.get(validity_id=validityobj[i].get('validity_id'))
                if validityobjget.status=='Active':
                    validityobjget.status='Disabled'
                    validityobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status disabled'},status=202)
            return Response({'status':200,'message':'Validity Master status changed to disabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def enable_validity_master(request):
    # enable validity master by changing status from Disabled to Active by passing primary key(paymentid)
    data=request.data
    validityid=data['validityid']
    try:
        validityobj=ValidityMaster.objects.filter(validity_id__in=validityid).values()
        if validityobj:
            for i in range(0,len(validityobj)):
                validityobjget=ValidityMaster.objects.get(validity_id=validityobj[i].get('validity_id'))
                if validityobjget.status=='Disabled':
                    validityobjget.status='Active'
                    validityobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status enabled'},status=202)
            return Response({'status':200,'message':'Validity Master status changed to enabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['post'])
@permission_classes([AllowAny,])
def delete_validity_master(request):
    # delete validity master by passing primary key(paymentid)
    data=request.data
    validityid = data['validityid']
    try:
        validityobj = ValidityMaster.objects.filter(validity_id__in=validityid).values()
        if validityobj:
            for i in range(0, len(validityobj)):
                validityobjget = ValidityMaster.objects.get(validity_id=validityobj[i].get('validity_id'))
                if validityobjget:
                    validityobjget.delete()

            return Response({'status': 204, 'message': 'Validity Master data deleted'}, status=204)
        return Response({'status':200,'message':'Validity Master data not present or already deleted'},status=200)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)



@api_view(['post'])
@permission_classes([AllowAny,])
def validity_master_user_id(request):
    data=request.data
    userid = data['userid']
    try:
        validityobj = ValidityMaster.objects.filter(updated_by=userid).values().order_by('validity_id')
        validityadmin=ValidityMaster.objects.filter(admins=1).values().order_by('validity_id')
        validityval=list(chain(validityobj,validityadmin))
        if len(validityobj)==0:
            return Response({'status': 200, 'message': 'Validity masters data', 'data': validityadmin}, status=200)
        if len(validityadmin) == 0:
            return Response({'status': 200, 'message': 'Validity admins datas', 'data': validityobj}, status=200)
        elif len(validityobj)!=0 and len(validityadmin)!=0:
            return Response({'status': 200, 'message': 'Validity all datas', 'data':validityval}, status=200)
        else:
            return Response({'status':204,'message':'noo'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

#------------------------------------------------------------------------------------------------------------------------

@api_view(['put'])
@permission_classes([AllowAny,])
def disable_delivery_master(request):
    # disable delivery master by changing status from Active to Disabled by passing primary key(deliveryid)
    data=request.data
    deliveryid=data['deliveryid']
    try:
        deliveryobj=DeliveryMaster.objects.filter(delivery_id__in=deliveryid).values()
        if deliveryobj:
            for i in range(0,len(deliveryobj)):
                deliveryobjget=DeliveryMaster.objects.get(delivery_id=deliveryobj[i].get('delivery_id'))
                if deliveryobjget.status=='Active':
                    deliveryobjget.status='Disabled'
                    deliveryobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status disabled'},status=202)
            return Response({'status':200,'message':'Delivery Master status changed to disabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def enable_delivery_master(request):
    # enable delivery master by changing status from Disabled to Active by passing primary key(deliveryid)
    data=request.data
    deliveryid=data['deliveryid']
    try:
        deliveryobj=DeliveryMaster.objects.filter(delivery_id__in=deliveryid).values()
        if deliveryobj:
            for i in range(0,len(deliveryobj)):
                deliveryobjget=DeliveryMaster.objects.get(delivery_id=deliveryobj[i].get('delivery_id'))
                if deliveryobjget.status=='Disabled':
                    deliveryobjget.status='Active'
                    deliveryobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status enabled'},status=202)
            return Response({'status':200,'message':'Delivery Master status changed to enabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['post'])
@permission_classes([AllowAny,])
def delete_delivery_master(request):
    # delete delivery master by passing primary key(paymentid)
    data=request.data
    deliveryid = data['deliveryid']
    try:
        deliveryobj = DeliveryMaster.objects.filter(delivery_id__in=deliveryid).values()
        if deliveryobj:
            for i in range(0, len(deliveryobj)):
                deliveryobjget = DeliveryMaster.objects.get(delivery_id=deliveryobj[i].get('delivery_id'))
                if deliveryobjget:
                    deliveryobjget.delete()

            return Response({'status': 204, 'message': 'Delivery Master data deleted'}, status=204)
        return Response({'status':200,'message':'Delivery Master data not present or already deleted'},status=200)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)




@api_view(['post'])
@permission_classes([AllowAny,])
def delivery_master_user_id(request):
    data=request.data
    userid = data['userid']
    try:
        deliveryobj = DeliveryMaster.objects.filter(updated_by=userid).values().order_by('delivery_id')
        deliveryadmin=DeliveryMaster.objects.filter(admins=1).values().order_by('delivery_id')
        deliveryval=list(chain(deliveryobj,deliveryadmin))
        if len(deliveryobj)==0:
            return Response({'status': 200, 'message': 'Delivery masters data', 'data': deliveryadmin}, status=200)
        if len(deliveryadmin) == 0:
            return Response({'status': 200, 'message': 'Delivery admins datas', 'data': deliveryobj}, status=200)
        elif len(deliveryobj)!=0 and len(deliveryadmin)!=0:
            return Response({'status': 200, 'message': 'Delivery all datas', 'data':deliveryval}, status=200)
        else:
            return Response({'status':204,'message':'noo'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)
#---------------------------------------------------------------------------------------------------


@api_view(['put'])
@permission_classes([AllowAny,])
def disable_country_master(request):
    # disable country master by changing status from Active to Disabled by passing primary key(deliveryid)
    data=request.data
    countryid=data['countryid']
    try:
        countryobj=CountryMaster.objects.filter(country_id__in=countryid).values()
        if countryobj:
            for i in range(0,len(countryobj)):
                countryobjget=CountryMaster.objects.get(country_id=countryobj[i].get('country_id'))
                if countryobjget.status=='Active':
                    countryobjget.status='Disabled'
                    countryobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status disabled'},status=202)
            return Response({'status':200,'message':'Country Master status changed to disabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def enable_country_master(request):
    # enable country master by changing status from Active to Disabled by passing primary key(deliveryid)
    data=request.data
    countryid=data['countryid']
    try:
        countryobj=CountryMaster.objects.filter(country_id__in=countryid).values()
        if countryobj:
            for i in range(0,len(countryobj)):
                countryobjget=CountryMaster.objects.get(country_id=countryobj[i].get('country_id'))
                if countryobjget.status=='Disabled':
                    countryobjget.status='Active'
                    countryobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status enabled'},status=202)
            return Response({'status':200,'message':'Country Master status changed to enabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['post'])
@permission_classes([AllowAny,])
def delete_country_master(request):
    # delete country master by passing primary key(paymentid)
    data=request.data
    countryid = data['countryid']
    try:
        countryobj = CountryMaster.objects.filter(country_id__in=countryid).values()
        if countryobj:
            for i in range(0, len(countryobj)):
                countryobjget = CountryMaster.objects.get(country_id=countryobj[i].get('country_id'))
                if countryobjget:
                    countryobjget.delete()

            return Response({'status': 204, 'message': 'Country Master data deleted'}, status=204)
        return Response({'status':200,'message':'Country Master data not present or already deleted'},status=200)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)




@api_view(['post'])
@permission_classes([AllowAny,])
def country_master_user_id(request):
    data=request.data
    userid = data['userid']
    try:
        countryobj = CountryMaster.objects.filter(updated_by=userid).values().order_by('country_id')
        countryadmin=CountryMaster.objects.filter(admins=1).values().order_by('country_id')
        countryval=list(chain(countryobj,countryadmin))
        if len(countryobj)==0:
            return Response({'status': 200, 'message': 'Country masters data', 'data': countryadmin}, status=200)
        if len(countryadmin) == 0:
            return Response({'status': 200, 'message': 'Country admins datas', 'data': countryobj}, status=200)
        elif len(countryobj)!=0 and len(countryadmin)!=0:
            return Response({'status': 200, 'message': 'Country all datas', 'data':countryval}, status=200)
        else:
            return Response({'status':204,'message':'noo'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

#-------------------------------------------------------------------------------------------------------
@api_view(['put'])
@permission_classes([AllowAny,])
def disable_tax_master(request):
    # disable tax master by changing status from Active to Disabled by passing primary key(taxid)
    data=request.data
    taxid=data['taxid']
    try:
        taxobj=TaxMaster.objects.filter(tax_id__in=taxid).values()
        if taxobj:
            for i in range(0,len(taxobj)):
                taxobjget=TaxMaster.objects.get(tax_id=taxobj[i].get('tax_id'))
                if taxobjget.status=='Active':
                    taxobjget.status='Disabled'
                    taxobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status disabled'},status=202)
            return Response({'status':200,'message':'Tax Master status changed to disabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def enable_tax_master(request):
    # enable tax master by changing status from Active to Disabled by passing primary key(taxid)
    data=request.data
    taxid=data['taxid']
    try:
        taxobj=TaxMaster.objects.filter(tax_id__in=taxid).values()
        if taxobj:
            for i in range(0,len(taxobj)):
                taxobjget=TaxMaster.objects.get(tax_id=taxobj[i].get('tax_id'))
                if taxobjget.status=='Disabled':
                    taxobjget.status='Active'
                    taxobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status enabled'},status=202)
            return Response({'status':200,'message':'Tax Master status changed to enabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['post'])
@permission_classes([AllowAny,])
def delete_tax_master(request):
    # delete tax master by passing primary key(taxid)
    data=request.data
    taxid = data['taxid']
    try:
        taxobj = TaxMaster.objects.filter(tax_id__in=taxid).values()
        if taxobj:
            for i in range(0, len(taxobj)):
                taxobjget = TaxMaster.objects.get(tax_id=taxobj[i].get('tax_id'))
                if taxobjget:
                    taxobjget.delete()

            return Response({'status': 204, 'message': 'Tax Master data deleted'}, status=204)
        return Response({'status':200,'message':'Tax Master data not present or already deleted'},status=200)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['post'])
@permission_classes([AllowAny,])
def tax_master_user_id(request):
    data=request.data
    userid = data['userid']
    try:
        taxobj = TaxMaster.objects.filter(updated_by=userid).values().order_by('tax_id')
        taxadmin=TaxMaster.objects.filter(admins=1).values().order_by('tax_id')
        taxval=list(chain(taxobj,taxadmin))
        if len(taxobj)==0:
            return Response({'status': 200, 'message': 'Tax masters data', 'data': taxadmin}, status=200)
        if len(taxadmin) == 0:
            return Response({'status': 200, 'message': 'Tax admins datas', 'data': taxobj}, status=200)
        elif len(taxobj)!=0 and len(taxadmin)!=0:
            return Response({'status': 200, 'message': 'Tax all datas', 'data':taxval}, status=200)
        else:
            return Response({'status':204,'message':'noo'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



#-------------------------------------------------------------------------------------------------------
@api_view(['put'])
@permission_classes([AllowAny,])
def disable_currency_master(request):
    # disable currency master by changing status from Active to Disabled by passing primary key(currencyid)
    data=request.data
    currencyid=data['currencyid']
    try:
        currencyobj=CurrencyMaster.objects.filter(currency_id__in=currencyid).values()
        if currencyobj:
            for i in range(0,len(currencyobj)):
                currencyobjget=CurrencyMaster.objects.get(currency_id=currencyobj[i].get('currency_id'))
                if currencyobjget.status=='Active':
                    currencyobjget.status='Disabled'
                    currencyobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status disabled'},status=202)
            return Response({'status':200,'message':'Currency Master status changed to disabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def enable_currency_master(request):
    # disable currency master by changing status from Disabled to Active by passing primary key(currencyid)
    data=request.data
    currencyid=data['currencyid']
    try:
        currencyobj=CurrencyMaster.objects.filter(currency_id__in=currencyid).values()
        if currencyobj:
            for i in range(0,len(currencyobj)):
                currencyobjget=CurrencyMaster.objects.get(currency_id=currencyobj[i].get('currency_id'))
                if currencyobjget.status=='Disabled':
                    currencyobjget.status='Active'
                    currencyobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status enabled'},status=202)
            return Response({'status':200,'message':'Currency Master status changed to enabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)



@api_view(['post'])
@permission_classes([AllowAny,])
def delete_currency_master(request):
    # delete currency master by passing primary key(taxid)
    data=request.data
    currencyid = data['currencyid']
    try:
        currencyobj = CurrencyMaster.objects.filter(currency_id__in=currencyid).values()
        if currencyobj:
            for i in range(0, len(currencyobj)):
                currencyobjget = CurrencyMaster.objects.get(currency_id=currencyobj[i].get('currency_id'))
                if currencyobjget:
                    currencyobjget.delete()

            return Response({'status': 204, 'message': 'Currency Master data deleted'}, status=204)
        return Response({'status':200,'message':'Currency Master data not present or already deleted'},status=200)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)




@api_view(['post'])
@permission_classes([AllowAny,])
def currency_master_user_id(request):
    data=request.data
    userid = data['userid']
    try:
        currencyobj = CurrencyMaster.objects.filter(updated_by=userid).values().order_by('currency_id')
        currencyadmin=CurrencyMaster.objects.filter(admins=1).values().order_by('currency_id')
        currencyval=list(chain(currencyobj,currencyadmin))
        if len(currencyobj)==0:
            return Response({'status': 200, 'message': 'Currency masters data', 'data': currencyadmin}, status=200)
        if len(currencyadmin) == 0:
            return Response({'status': 200, 'message': 'Currency admins datas', 'data': currencyobj}, status=200)
        elif len(currencyobj)!=0 and len(currencyadmin)!=0:
            return Response({'status': 200, 'message': 'Currency all datas', 'data':currencyval}, status=200)
        else:
            return Response({'status':204,'message':'noo'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

#--------------------------------------------------------------------------------------------------------------



@api_view(['post'])
@permission_classes([AllowAny,])
def uom_master_user_id(request):
    data=request.data
    userid = data['userid']
    try:
        uomobj = UOMMaster.objects.filter(updated_by=userid).values().order_by('uom_id')
        uomadmin=UOMMaster.objects.filter(admins=1).values().order_by('uom_id')
        uomval=list(chain(uomobj,uomadmin))
        if len(uomobj)==0:
            return Response({'status': 200, 'message': 'UOM masters data', 'data': uomadmin}, status=200)
        if len(uomadmin) == 0:
            return Response({'status': 200, 'message': 'UOM admins datas', 'data': uomobj}, status=200)
        elif len(uomobj)!=0 and len(uomadmin)!=0:
            return Response({'status': 200, 'message': 'UOM all datas', 'data':uomval}, status=200)
        else:
            return Response({'status':204,'message':'noo'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

#----------------------------------------------------------------------------------------------------
@api_view(['put'])
@permission_classes([AllowAny,])
def disable_department_master(request):
    # disable department master by changing status from Active to Disabled by passing primary key(departmentid)
    data=request.data
    departmentid=data['departmentid']
    try:
        departmentobj=DepartmentMaster.objects.filter(department_id__in=departmentid).values()
        if departmentobj:
            for i in range(0,len(departmentobj)):
                departmentobjget=DepartmentMaster.objects.get(department_id=departmentobj[i].get('department_id'))
                if departmentobjget.status=='Active':
                    departmentobjget.status='Disabled'
                    departmentobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status disabled'},status=202)
            return Response({'status':200,'message':'Department Master status changed to disabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['put'])
@permission_classes([AllowAny,])
def enable_department_master(request):
    # enable department master by changing status from Disabled to Active by passing primary key(departmentid)
    data=request.data
    departmentid=data['departmentid']
    try:
        departmentobj=DepartmentMaster.objects.filter(department_id__in=departmentid).values()
        if departmentobj:
            for i in range(0,len(departmentobj)):
                departmentobjget=DepartmentMaster.objects.get(department_id=departmentobj[i].get('department_id'))
                if departmentobjget.status=='Disabled':
                    departmentobjget.status='Active'
                    departmentobjget.save()
                else:
                    return Response({'status': 202, 'message': 'Already status enabled'},status=202)
            return Response({'status':200,'message':'Department Master status changed to enabled'},status=200)
        else:
            return Response({'status': 204, 'message': 'Not exist'}, status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)




@api_view(['post'])
@permission_classes([AllowAny,])
def delete_department_master(request):
    # delete department master by passing primary key(taxid)
    data=request.data
    departmentid = data['departmentid']
    try:
        departmentobj = DepartmentMaster.objects.filter(department_id__in=departmentid).values()
        if departmentobj:
            for i in range(0, len(departmentobj)):
                departmentobjget = DepartmentMaster.objects.get(department_id=departmentobj[i].get('department_id'))
                if departmentobjget:
                    departmentobjget.delete()

            return Response({'status': 204, 'message': 'Department Master data deleted'}, status=204)
        return Response({'status':200,'message':'Department Master data not present or already deleted'},status=200)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)




@api_view(['post'])
@permission_classes([AllowAny,])
def department_master_user_id(request):
    data=request.data
    userid=data['userid']
    try:
        departmentobj = DepartmentMaster.objects.filter(updated_by=userid).values().order_by('department_id')
        departmentadmin=DepartmentMaster.objects.filter(admins=1).values().order_by('department_id')
        departmentval=list(chain(departmentobj,departmentadmin))
        if len(departmentobj)==0:
            return Response({'status': 200, 'message': 'Department masters data', 'data': departmentadmin}, status=200)
        if len(departmentadmin) == 0:
            return Response({'status': 200, 'message': 'Department admins datas', 'data': departmentobj}, status=200)
        elif len(departmentobj)!=0 and len(departmentadmin)!=0:
            return Response({'status': 200, 'message': 'Department all datas', 'data':departmentval}, status=200)
        else:
            return Response({'status':204,'message':'noo'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


# class SubCategoryMasterPaginationView(viewsets.ModelViewSet):
#     # sub_category_master  viewsets
#     permission_classes = (AllowAny,)
#     queryset = SubCategoryMaster.objects.all()
#     serializer_class = SubcategoryMasterSerializer
#     ordering_fields = ['sub_category_id']
#     ordering = ['sub_category_id']
#     pagination_class = CustomPagination

class RfqCategoryMasterView(viewsets.ModelViewSet):
    # rfq_category master viewsets
    permission_classes = (AllowAny,)
    queryset = RfqCategoryMaster.objects.all().order_by('rfq_category_id')
    serializer_class = RfqCategoryMasterSerializer


class PriceBasisMasterView(viewsets.ModelViewSet):
    # price basis master viewsets
    permission_classes = (AllowAny,)
    queryset = PriceBasisMaster.objects.all().order_by('price_basis_id')
    serializer_class = PriceBasisMasterSerializer


class InspectionMasterView(viewsets.ModelViewSet):
    # inspection master viewsets
    permission_classes = (AllowAny,)
    queryset = InspectionMaster.objects.all().order_by('inspection_id')
    serializer_class = InspectionMasterSerializer

class LiquidatedDamageMasterView(viewsets.ModelViewSet):
    # liquidated master viewsets
    permission_classes = (AllowAny,)
    queryset = LiquidatedDamageMaster.objects.all().order_by('liquidated_id')
    serializer_class = LiquidatedDamageMasterSerializer

class TaxesAndDutiesMasterView(viewsets.ModelViewSet):
    # liquidated master viewsets
    permission_classes = (AllowAny,)
    queryset = TaxesAndDutiesMaster.objects.all().order_by('tax_duties_id')
    serializer_class = TaxesAndDutiesMasterSerializer


class TestAndQapMasterView(viewsets.ModelViewSet):
    # liquidated master viewsets
    permission_classes = (AllowAny,)
    queryset = TestAndQapMaster.objects.all().order_by('test_qap_id')
    serializer_class = TestAndQapMasterSerializer


class PerformanceGuaranteesMasterView(viewsets.ModelViewSet):
    # performance guarantee  master viewsets
    permission_classes = (AllowAny,)
    queryset = PerformanceGuaranteesMaster.objects.all().order_by('performance_id')
    serializer_class = PerformanceGuaranteesMasterSerializer


@api_view(['post'])
@permission_classes([AllowAny,])
def hsn_masters_user_id(request):
    data=request.data
    userid = data['userid']
    try:
        hsnobj = HSNMaster.objects.filter(updated_by=userid).values().order_by('hsn_id')
        hsnadmin=HSNMaster.objects.filter(admins=1).values().order_by('hsn_id')
        hsnval=list(chain(hsnobj,hsnadmin))
        if len(hsnobj)==0:
            return Response({'status': 200, 'message': 'HSN masters data', 'data': hsnadmin}, status=200)
        if len(hsnadmin) == 0:
            return Response({'status': 200, 'message': 'HSN admins datas', 'data': hsnobj}, status=200)
        elif len(hsnobj)!=0 and len(hsnadmin)!=0:
            return Response({'status': 200, 'message': 'HSN all datas', 'data':hsnval}, status=200)
        else:
            return Response({'status':204,'message':'No HSN data present'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes([AllowAny,])
def sac_masters_user_id(request):
    data=request.data
    userid = data['userid']
    try:
        sacobj = SACMaster.objects.filter(updated_by=userid).values().order_by('sac_id')
        sacadmin=SACMaster.objects.filter(admins=1).values().order_by('sac_id')
        sacval=list(chain(sacobj,sacadmin))
        if len(sacobj)==0:
            return Response({'status': 200, 'message': 'SAC masters data', 'data': sacadmin}, status=200)
        if len(sacadmin) == 0:
            return Response({'status': 200, 'message': 'SAC admins datas', 'data': sacobj}, status=200)
        elif len(sacobj)!=0 and len(sacadmin)!=0:
            return Response({'status': 200, 'message': 'SAC all datas', 'data':sacval}, status=200)
        else:
            return Response({'status':204,'message':'No HSN data present'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
# @permission_classes([AllowAny,])
def getfrightdeialswithvendorsindata(request):
    data=request.data
    userid=data['userid']
    try:
        frightobjuser=FrieghtChargesMaster.objects.filter(updated_by=userid).values()
        frightobjvendorsin=FrieghtChargesMaster.objects.filter(updated_by__isnull=True).values().order_by('frieght_id')
        finalres=list(chain(frightobjuser, frightobjvendorsin))

        return Response({'status': 200, 'message': 'ok','data':finalres}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
# @permission_classes([AllowAny,])
def getfrightbasedonid(request):
    data=request.data
    pid=data['pid']
    try:
        finalres=FrieghtChargesMaster.objects.filter(frieght_id=pid).values()
        return Response({'status': 200, 'message': 'ok', 'data': finalres}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

