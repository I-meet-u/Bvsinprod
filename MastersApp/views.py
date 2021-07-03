
from itertools import chain

from django.shortcuts import render
from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.views import View
import io, csv

from rest_framework.views import APIView

from AdminApp.models import AdminRegister
from .serializers import MainCoreMasterSerializer, CategoryMasterSerializer, SubcategoryMasterSerializer, \
    IndustryToServeMasterSerializer, \
    NatureOfBusinessMasterSerializer, SupplyCapabilitiesMasterSerializer, PincodeMasterSerializer, UOMMasterSerializer, \
    DepartmentMasterSerializer, DesignationMasterSerializer, TaxMasterSerializer, HSNMasterSerializer, \
    SACMasterSerializer, CurrencyMasterSerializer, PFChargesMasterSerializer, FrieghtChargesMasterSerializer, \
    DeliveryMasterSerializer, CountryMasterSerializer, WarrantyMasterSerializer, \
    GuaranteeMasterSerializer, ItemGroupMasterSerializer
from .models import MaincoreMaster, CategoryMaster, SubCategoryMaster, \
    IndustryToServeMaster, NatureOfBusinessMaster, SupplyCapabilitiesMaster, PincodeMaster, UOMMaster, DepartmentMaster, \
    DesignationMaster, TaxMaster, HSNMaster, SACMaster, CurrencyMaster, PFChargesMaster, FrieghtChargesMaster, \
    DeliveryMaster, CountryMaster, WarrantyMaster, GuaranteeMaster, ItemGroupMaster


# Create your views here.
# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 20
#     page_size_query_param = 'page_size'
#     max_page_size = 1000



class IndustryToServeMasterView(viewsets.ModelViewSet):
    # industry_servce master viewsets
    permission_classes = (AllowAny,)
    queryset = IndustryToServeMaster.objects.all()
    serializer_class = IndustryToServeMasterSerializer
    # pagination_class = StandardResultsSetPagination

class NatureOfBusinessMasterView(viewsets.ModelViewSet):
    # nature_of_business mster viewsets
    permission_classes = (AllowAny,)
    queryset = NatureOfBusinessMaster.objects.all()
    serializer_class =NatureOfBusinessMasterSerializer


class SupplyCapabilitiesMasterView(viewsets.ModelViewSet):
    # supply_capability  viewsets
    permission_classes = (AllowAny,)
    queryset = SupplyCapabilitiesMaster.objects.all()
    serializer_class =SupplyCapabilitiesMasterSerializer

class MaincoreMasterView(viewsets.ModelViewSet):
    # maincore_master  master viewsets
    permission_classes = (AllowAny,)
    queryset = MaincoreMaster.objects.all()
    serializer_class = MainCoreMasterSerializer

class CategoryMasterView(viewsets.ModelViewSet):
    # category_master  viewsets
    permission_classes = (AllowAny,)
    queryset =CategoryMaster.objects.all()
    serializer_class=CategoryMasterSerializer

class SubCategoryMasterView(viewsets.ModelViewSet):
    # sub_category_master  viewsets
    permission_classes = (AllowAny,)
    queryset = SubCategoryMaster.objects.all()
    serializer_class = SubcategoryMasterSerializer


class PincodeMasterView(viewsets.ModelViewSet):
    # pincode_master  viewsets
    permission_classes = (AllowAny,)
    queryset = PincodeMaster.objects.all()
    serializer_class = PincodeMasterSerializer

class UOMMasterView(viewsets.ModelViewSet):
    # UOM_master = viewsets
    permission_classes = (AllowAny,)
    queryset = UOMMaster.objects.all()
    serializer_class= UOMMasterSerializer

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        uommasterobj = UOMMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by('uom_id')
        uomotherdataobj=UOMMaster.objects.filter(admins=1).values().order_by('uom_id')
        uomvalue=list(chain(uommasterobj,uomotherdataobj))
        if uommasterobj and not uomotherdataobj:
            return uommasterobj
        elif not uommasterobj and uomotherdataobj:
            return uomotherdataobj

        elif uommasterobj and uomotherdataobj:
            return uomvalue

        raise ValidationError({'message': 'UOM Master details not exist', 'status': 204})


class DepartmentMasterView(viewsets.ModelViewSet):
    # department_master  viewsets
    permission_classes = (AllowAny,)
    queryset = DepartmentMaster.objects.all()
    serializer_class = DepartmentMasterSerializer

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        departmentmasterobj = DepartmentMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by('department_id')
        departmentotherdataobj = DepartmentMaster.objects.filter(admins=1).order_by('department_id')
        departmentvalue = list(chain(departmentmasterobj, departmentotherdataobj))
        if departmentmasterobj and not departmentotherdataobj:
            return departmentmasterobj
        elif not departmentmasterobj and departmentotherdataobj:
            return departmentotherdataobj

        elif departmentmasterobj and departmentotherdataobj:
            return departmentvalue

        raise ValidationError({'message': 'Department Master details not exist', 'status': 204})

class DesignationMasterView(viewsets.ModelViewSet):
    # designation_master viewsets
    permission_classes = (AllowAny,)
    queryset = DesignationMaster.objects.all()
    serializer_class = DesignationMasterSerializer

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        designationmasterobj = DesignationMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by(
            'designation_id')
        designationotherdataobj = DesignationMaster.objects.filter(admins=1).order_by('designation_id')
        designationval = list(chain(designationmasterobj, designationotherdataobj))
        if designationmasterobj and not designationotherdataobj:
            return designationmasterobj
        elif not designationmasterobj and designationotherdataobj:
            return designationotherdataobj

        elif designationmasterobj and designationotherdataobj:
            return designationval

        raise ValidationError({'message': 'Designation Master details not exist', 'status': 204})

class TaxMasterView(viewsets.ModelViewSet):
    # tax_master  viewsets
    permission_classes = (AllowAny,)
    queryset = TaxMaster.objects.all()
    serializer_class = TaxMasterSerializer

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        taxmasterobj = TaxMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by(
            'tax_id')
        taxotherdataobj = TaxMaster.objects.filter(admins=1).order_by('tax_id')
        taxvalue = list(chain(taxmasterobj, taxotherdataobj))
        if taxmasterobj and not taxotherdataobj:
            return taxmasterobj
        elif not taxmasterobj and taxotherdataobj:
            return taxotherdataobj

        elif taxmasterobj and taxotherdataobj:
            return taxvalue

        raise ValidationError({'message': 'Tax Master details not exist', 'status': 204})


class HSNMasterSerializerView(viewsets.ModelViewSet):
    # hsn_master  viewsets
    permission_classes = (AllowAny,)
    queryset = HSNMaster.objects.all()
    serializer_class = HSNMasterSerializer

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        hsnmasterobj = HSNMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by('hsn_id')
        hsnotherdataobj = HSNMaster.objects.filter(admins=1).order_by('hsn_id')
        hsnvalue = list(chain(hsnmasterobj, hsnotherdataobj))
        if hsnmasterobj:
            return hsnvalue

        raise ValidationError({'message': 'HSN Master details not exist', 'status': 204})


class SACMasterView(viewsets.ModelViewSet):
    # sac_master  viewsets
    permission_classes = (AllowAny,)
    queryset = SACMaster.objects.all()
    serializer_class = SACMasterSerializer

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        sacmasterobj = SACMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by('sac_id')
        sacotherdataobj = SACMaster.objects.filter(admins=1).order_by('sac_id')
        sacvalue = list(chain(sacmasterobj,sacotherdataobj))
        if sacmasterobj:
            return sacvalue

        raise ValidationError({'message': 'SAC Master details not exist', 'status': 204})

class CurrencyMasterView(viewsets.ModelViewSet):
    # currency_master viewsets
    permission_classes = (AllowAny,)
    queryset = CurrencyMaster.objects.all()
    serializer_class = CurrencyMasterSerializer

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        currencymasterobj = CurrencyMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by(
            'currency_id')
        currencyotherdataobj = CurrencyMaster.objects.filter(admins=1).order_by('currency_id')
        currencyval = list(chain(currencymasterobj, currencyotherdataobj))
        if currencymasterobj and currencyotherdataobj:
            return currencyval

        raise ValidationError({'message': 'Currency Master details not exist', 'status': 204})

class PFChargesMasterView(viewsets.ModelViewSet):
    # pf_charges master viewsets
    permission_classes = (AllowAny,)
    queryset = PFChargesMaster.objects.all()
    serializer_class = PFChargesMasterSerializer

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        pfmasterobj = PFChargesMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by(
            'pf_charge_id')
        pfmasterotherobj = PFChargesMaster.objects.filter(admins=1).order_by('pf_charge_id')
        pfval = list(chain(pfmasterobj, pfmasterotherobj))
        if pfmasterobj and pfmasterotherobj:
            return pfval

        raise ValidationError({'message': 'PF Charges Master details not exist', 'status': 204})

class FrieghtChargesMasterView(viewsets.ModelViewSet):
    # frieght_charges master viewsets
    permission_classes = (AllowAny,)
    queryset = FrieghtChargesMaster.objects.all()
    serializer_class = FrieghtChargesMasterSerializer

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        frieghtmasterobj = FrieghtChargesMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by(
            'frieght_id')
        frieghtmasterotherobj = FrieghtChargesMaster.objects.filter(admins=1).order_by('frieght_id')
        frieghtval = list(chain(frieghtmasterobj, frieghtmasterotherobj))
        if frieghtmasterobj and frieghtmasterotherobj:
            return frieghtval

        raise ValidationError({'message': 'Frieght Master details not exist', 'status': 204})

class WarrantyMasterView(viewsets.ModelViewSet):
    # warranty_master viewsets
    permission_classes = (AllowAny,)
    queryset = WarrantyMaster.objects.all()
    serializer_class = WarrantyMasterSerializer

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        warrantymasterobj = WarrantyMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by(
            'warranty_id')
        warrantyotherobj = WarrantyMaster.objects.filter(admins=1).order_by('warranty_id')
        warrantyval = list(chain(warrantymasterobj, warrantyotherobj))
        if warrantymasterobj and warrantyotherobj:
            return warrantyval

        raise ValidationError({'message': 'Warranty Master details not exist', 'status': 204})

class GuaranteeMasterView(viewsets.ModelViewSet):
    # warranty_master viewsets
    permission_classes = (AllowAny,)
    queryset = GuaranteeMaster.objects.all()
    serializer_class =GuaranteeMasterSerializer

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        guaranteemasterobj = GuaranteeMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by(
            'guarantee_id')
        guaranteeotherobj = GuaranteeMaster.objects.filter(admins=1).order_by('guarantee_id')
        guaranteeval = list(chain(guaranteemasterobj, guaranteeotherobj))
        if guaranteemasterobj and not guaranteeotherobj:
            return guaranteemasterobj
        elif not guaranteemasterobj and guaranteeotherobj:
            return guaranteeotherobj

        elif guaranteemasterobj and guaranteeotherobj:
            return guaranteeval

        raise ValidationError({'message': 'Guarantee Master details not exist', 'status': 204})

class DeliveryMasterView(viewsets.ModelViewSet):
    # delivery_master viewsets
    permission_classes = (AllowAny,)
    queryset = DeliveryMaster.objects.all()
    serializer_class = DeliveryMasterSerializer

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        deliverymasterobj = DeliveryMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by(
            'delivery_id')
        deliveryotherobj = DeliveryMaster.objects.filter(admins=1).order_by('delivery_id')
        deliveryval = list(chain(deliverymasterobj, deliveryotherobj))
        if deliverymasterobj and not deliveryotherobj:
            return deliverymasterobj
        elif not deliverymasterobj and deliveryotherobj:
            return deliveryotherobj

        elif deliverymasterobj and deliveryotherobj:
            return deliveryval

        raise ValidationError({'message': 'Delivery Master details not exist', 'status': 204})

class CountryMasterView(viewsets.ModelViewSet):
    # country_master viewsets
    permission_classes = (AllowAny,)
    queryset = CountryMaster.objects.all()
    serializer_class = CountryMasterSerializer

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        countrymasterobj = CountryMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by(
            'country_id')
        countryotherobj = DepartmentMaster.objects.filter(admins=1).order_by('department_id')
        countryval = list(chain(countrymasterobj, countryotherobj))
        if countrymasterobj and not countryotherobj:
            return countrymasterobj
        elif not countrymasterobj and countryotherobj:
            return countryotherobj

        elif countrymasterobj and countryotherobj:
            return countryval

        raise ValidationError({'message': 'Country Master details not exist', 'status': 204})


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
    userid = data['userid']
    try:
        uomobj=UOMMaster.objects.filter(uom_id__in=uomid,updated_by=userid).values()
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
    userid=data['userid']
    try:
        uomobj=UOMMaster.objects.filter(uom_id__in=uomid,updated_by=userid).values()
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
    userid = data['userid']
    try:
        uomobj=UOMMaster.objects.filter(uom_id__in=uomid,updated_by=userid).values()
        if len(uomobj)>0:
            for i in range(0,len(uomobj)):
                uomget=UOMMaster.objects.get(uom_id=uomobj[i].get('uom_id'))
                if uomget.status=='Disabled':
                    uomget.status='Active'
                    uomget.save()
                else:
                    return Response({'status':202,'message':'UOM masters already enabled or it is not in disable state'},status=202)
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
        itemgroupmasterobj = ItemGroupMaster.objects.filter().values()
        if itemgroupmasterobj:
            masterslist.append({'item_group_master': itemgroupmasterobj})
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


@api_view(['get'])
@permission_classes([AllowAny,])
def industry_to_serve_master_history(request):
    try:
        industrytoservehistoryobj=IndustryToServeMaster.history.filter().values()
        return Response({'status':200,'message':'Industry to Serve Master history','data':industrytoservehistoryobj},status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['get'])
@permission_classes([AllowAny,])
def nature_of_business_master_history(request):
    try:
        natureofbusinesshistoryobj=NatureOfBusinessMaster.history.filter().values()
        return Response({'status':200,'message':'Nature of business Master history','data':natureofbusinesshistoryobj},status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['get'])
@permission_classes([AllowAny,])
def supply_capabilites_master_history(request):
    try:
        supplycapabiliteshistoryobj=SupplyCapabilitiesMaster.history.filter().values()
        return Response({'status':200,'message':'Supply Capabilities Master history','data':supplycapabiliteshistoryobj},status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['get'])
@permission_classes([AllowAny,])
def maincore_master_history(request):
    try:
        maincorehisotryobj=MaincoreMaster.history.filter().values()
        return Response({'status':200,'message':'Maincore Master history','data':maincorehisotryobj},status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['get'])
@permission_classes([AllowAny,])
def category_master_history(request):
    try:
        categoryhistoryobj=CategoryMaster.history.filter().values()
        return Response({'status':200,'message':'Category Master history','data':categoryhistoryobj},status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['get'])
@permission_classes([AllowAny,])
def sub_category_master_history(request):
    try:
        subcategoryhistoryobj=SubCategoryMaster.history.filter().values()
        return Response({'status':200,'message':'Sub Category Master history','data':subcategoryhistoryobj},status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)






#
# class IndustryServeUploadView(APIView):
#     permission_classes=(AllowAny,)
#     def post(self, request):
#         rowdata=[]
#         newdata=[]
#         newval=[]
#         paramFile =request.data['csv_industry_file']
#         # portfolio1 = csv.DictReader(paramFile)
#         # list_of_dict = list(portfolio1)
#         decoded_file = paramFile.read().decode()
#         # upload_products_csv.delay(decoded_file, request.user.pk)
#         io_string = io.StringIO(decoded_file)
#         list_of_dict = csv.DictReader(io_string)
#         try:
#             industryobj = IndustryToServeMaster.objects.filter().values()
#             for i in range(0,len(industryobj)):
#                 rowdata.append(industryobj[i].get('industry_name'))
#             for row in list_of_dict:
#                 newval.append(row['industry_name'])
#                 # if row['industry_name']  in  rowdata:
#                 #     print('already present')
#                 #     newdata.append(row['industry_name'])
#                 # else:
#                 #     print('not  present')
#                 #     return Response({'status': 202, 'message': 'already present'}, status=202)
#                 #     objs = [
#                 #             IndustryToServeMaster(
#                 #                 industry_name=row['industry_name'],
#                 #                 csv_industry=paramFile
#                 #
#                 #             )
#                 #
#                 #
#                 #         ]
#                 #     msg = IndustryToServeMaster.objects.bulk_create(objs)
#                 # else:
#                 #     print('alreafy present')
#                 #     newdata.append(row['industry_name'])
#                 #     return Response({'status':202,'message':'already present'},status=202)
#             return Response({'status':200,'message':'ok','data':newval},status=200)
#         except Exception as e:
#             return Response({'status': 500, 'error': str(e)}, status=500)
#         #     returnmsg = {"status_code": 200}
#         #     print('imported successfully')
#         # except Exception as e:
#         #     print('Error While Importing Data: ',)
#         #     returnmsg = {"status_code": 500,'message':str(e)}
#
#         # return JsonResponse(returnmsg)


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

    def get_queryset(self):
        # overriding get_queryset by passing user_id. Here user_id is nothing but updated_by
        itemgroupobj = ItemGroupMaster.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by('item_group_id')
        itemgroupdataobj=ItemGroupMaster.objects.filter(admins=1).values().order_by('item_group_id')
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

@api_view(['get'])
@permission_classes([AllowAny,])
def item_group_master_history(request):
    try:
        itemgroupmasterobj=ItemGroupMaster.history.filter().values()
        if itemgroupmasterobj:
            return Response({'status':200,'message':'Item group Master history','data':itemgroupmasterobj},status=200)
        else:
            return Response({'status': 204, 'message': 'Item group Master data not persent'},
                            status=204)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



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

@api_view(['get'])
@permission_classes([AllowAny,])
def hsn_master_history(request):
    try:
        hsnmasterobj=HSNMaster.history.filter().values()
        if hsnmasterobj:
            return Response({'status':200,'message':'HSN Master history','data':hsnmasterobj},status=200)
        else:
            return Response({'status': 204, 'message': 'HSN Master history data not persent'},
                            status=204)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



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

@api_view(['get'])
@permission_classes([AllowAny,])
def sac_master_history(request):
    try:
        sacmasterobj=SACMaster.history.filter().values()
        if sacmasterobj:
            return Response({'status':200,'message':'SAC Master history','data':sacmasterobj},status=200)
        else:
            return Response({'status': 204, 'message': 'SAC Master data not persent'},
                            status=204)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




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

@api_view(['get'])
@permission_classes([AllowAny,])
def currency_master_history(request):
    try:
        currencyhistoryobj=CurrencyMaster.history.filter().values()
        if currencyhistoryobj:
            return Response({'status':200,'message':'Currency Master history','data':currencyhistoryobj},status=200)
        else:
            return Response({'status': 204, 'message': 'Currency History Master data not persent'},
                            status=204)

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
def delete_currency_master(request):
    # delete pf_charge_master by passing primary key(pfchargeid)
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

@api_view(['get'])
@permission_classes([AllowAny,])
def currency_master_history(request):
    try:
        currencyhistoryobj=CurrencyMaster.history.filter().values()
        if currencyhistoryobj:
            return Response({'status':200,'message':'Currency Master history','data':currencyhistoryobj},status=200)
        else:
            return Response({'status': 204, 'message': 'Currency History Master data not persent'},
                            status=204)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)