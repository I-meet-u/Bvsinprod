from itertools import chain

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import MainCoreMasterSerializer, CategoryMasterSerializer, SubcategoryMasterSerializer, \
    IndustryToServeMasterSerializer, \
    NatureOfBusinessMasterSerializer, SupplyCapabilitiesMasterSerializer, PincodeMasterSerializer, UOMMasterSerializer, \
    DepartmentMasterSerializer, DesignationMasterSerializer, TaxMasterSerializer, HSNMasterSerializer, \
    SACMasterSerializer, CurrencyMasterSerializer, PFChargesMasterSerializer, FrieghtChargesMasterSerializer, \
    WarrantyGuaranteeMasterSerializer, DeliveryMasterSerializer
from .models import MaincoreMaster, CategoryMaster, SubCategoryMaster, \
    IndustryToServeMaster, NatureOfBusinessMaster, SupplyCapabilitiesMaster, PincodeMaster, UOMMaster, DepartmentMaster, \
    DesignationMaster, TaxMaster, HSNMaster, SACMaster, CurrencyMaster, PFChargesMaster, FrieghtChargesMaster, \
    WarrantyGuaranteeMaster, DeliveryMaster


# Create your views here.
class IndustryToServeMasterView(viewsets.ModelViewSet):
    # industry_servce master viewsets
    permission_classes = (AllowAny,)
    queryset = IndustryToServeMaster.objects.all()
    serializer_class = IndustryToServeMasterSerializer

class NatureOfBusinessMasterView(viewsets.ModelViewSet):
    # nature_of_business mster viewsets
    permission_classes = (AllowAny,)
    queryset = NatureOfBusinessMaster.objects.all()
    serializer_class =NatureOfBusinessMasterSerializer


class SupplyCapabilitiesMasterView(viewsets.ModelViewSet):
    # supply_capability  viewsets
    queryset = SupplyCapabilitiesMaster.objects.all()
    serializer_class =SupplyCapabilitiesMasterSerializer

class MaincoreMasterView(viewsets.ModelViewSet):
    # maincore_master  master viewsets
    queryset = MaincoreMaster.objects.all()
    serializer_class = MainCoreMasterSerializer

class CategoryMasterView(viewsets.ModelViewSet):
    # category_master  viewsets
    queryset =CategoryMaster.objects.all()
    serializer_class=CategoryMasterSerializer

class SubCategoryMasterView(viewsets.ModelViewSet):
    # sub_category_master  viewsets
    queryset = SubCategoryMaster.objects.all()
    serializer_class = SubcategoryMasterSerializer


class PincodeMasterView(viewsets.ModelViewSet):
    # pincode_master  viewsets
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
        uomotherdataobj=UOMMaster.objects.filter().values().order_by('uom_id')
        uomvalue=list(chain(uommasterobj,uomotherdataobj))
        if uommasterobj:
            return uomvalue
        raise ValidationError({'message': 'UOM Master details not exist','status': 204})



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
        if not departmentmasterobj:
            raise ValidationError({'message': 'Department Master details not exist', 'status': 204})
        return departmentvalue


class DesignationMasterView(viewsets.ModelViewSet):
    # designation_master viewsets
    permission_classes = (AllowAny,)
    queryset = DesignationMaster.objects.all()
    serializer_class = DesignationMasterSerializer


class TaxMasterView(viewsets.ModelViewSet):
    # tax_master  viewsets
    permission_classes = (AllowAny,)
    queryset = TaxMaster.objects.all()
    serializer_class = TaxMasterSerializer



class HSNMasterSerializerView(viewsets.ModelViewSet):
    # hsn_master  viewsets
    permission_classes = (AllowAny,)
    queryset = HSNMaster.objects.all()
    serializer_class = HSNMasterSerializer


class SACMasterView(viewsets.ModelViewSet):
    # sac_master  viewsets
    permission_classes = (AllowAny,)
    queryset = SACMaster.objects.all()
    serializer_class = SACMasterSerializer



class CurrencyMasterView(viewsets.ModelViewSet):
    # currency_master viewsets
    permission_classes = (AllowAny,)
    queryset = CurrencyMaster.objects.all()
    serializer_class = CurrencyMasterSerializer


class PFChargesMasterView(viewsets.ModelViewSet):
    # pf_charges master viewsets
    permission_classes = (AllowAny,)
    queryset = PFChargesMaster.objects.all()
    serializer_class = PFChargesMasterSerializer

class FrieghtChargesMasterView(viewsets.ModelViewSet):
    # frieght_charges master viewsets
    permission_classes = (AllowAny,)
    queryset = FrieghtChargesMaster.objects.all()
    serializer_class = FrieghtChargesMasterSerializer

class WarrantyGuaranteeMasterView(viewsets.ModelViewSet):
    # warranty_master viewsets
    permission_classes = (AllowAny,)
    queryset = WarrantyGuaranteeMaster.objects.all()
    serializer_class = WarrantyGuaranteeMasterSerializer

class DeliveryMasterView(viewsets.ModelViewSet):
    # delivery_master viewsets
    permission_classes = (AllowAny,)
    queryset = DeliveryMaster.objects.all()
    serializer_class = DeliveryMasterSerializer



@api_view(['post'])
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
def disable_nature_of_business(request):
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
def disable_supply_capabilities(request):
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
def disable_industry_serve(request):
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
                    uomget.status='Enabled'
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
        warrantymasterobj = WarrantyGuaranteeMaster.objects.filter().values()
        if warrantymasterobj:
            masterslist.append({'warranty_master': warrantymasterobj})
        deliverymasterobj = DeliveryMaster.objects.filter().values()
        if deliverymasterobj:
            masterslist.append({'delivery_master': deliverymasterobj})
        return Response({'status': 200, 'message': 'Masters List','data':masterslist}, status=200)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



