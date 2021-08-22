from itertools import chain

from django.shortcuts import render
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
# Create your views here.
from LandingPageApp.models import CompanyReview, CompanyRating
from LandingPageApp.serializers import CompanyReviewSerializer, CompanyRatingSerializer
from MastersApp.models import MaincoreMaster, CategoryMaster, SubCategoryMaster
from MaterialApp.models import VendorProduct_BasicDetails
from RegistrationApp.models import SelfRegistration, BasicCompanyDetails, IndustrialHierarchy, BillingAddress, \
    IndustrialInfo


@api_view(['get'])
@permission_classes([AllowAny])
def maincore_all_list(request):
    # maincore master all data by using filter
    try:
        maincoreobj=MaincoreMaster.objects.filter().values()
        if maincoreobj:
            return Response({'status': 200, 'message': 'maincore full list', 'data': maincoreobj}, status=200)
        else:
            return Response({'status': 204, 'message': 'not found'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes([AllowAny])
def maincore_list(request):
    # maincore master all data by using filter and passing maincore_id and maincore_name
    data=request.data
    maincore_id=data['maincore_id']
    maincore_name=data['maincore_name']
    try:
        mainobj = MaincoreMaster.objects.filter(maincore_id=maincore_id,maincore_name=maincore_name).values()
        if mainobj:
            return Response({'status':200, 'message':'maincore list','data':mainobj}, status=200)
        else:
            return Response({'status':204, 'message':'not found'}, status=204)
    except Exception as e:
        return Response({'status':500, 'error':str(e)}, status=500)

@api_view(['post'])
@permission_classes([AllowAny])
def category_list(request):
    # category master all data by using filter and passing maincore_id
    data = request.data
    maincoreid = data['maincoreid']
    categoryarray=[]
    subcatarray=[]
    subcategoryarray = []
    try:
        catobj = CategoryMaster.objects.filter(maincore=maincoreid).order_by('category_name').values()
        print(len(catobj))
        if catobj:
            for i in range(0, len(catobj)):
                categoryarray.append({'category_id': catobj[i].get('category_id'),
                                      'category_name': catobj[i].get('category_name')})
                subcat = SubCategoryMaster.objects.filter(category_id=catobj[i].get('category_id')).values()
                for j in range(0,len(subcat)):
                    subcatarray.append({'subcatname',subcat[j].get('sub_category_name')})

                categoryarray[i].setdefault('subcatdata',subcat)
            return Response({'status': 200, 'message': 'category list', 'data': categoryarray}, status=200)

        else:
            return Response({'status': 204, 'message': 'not found'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes([AllowAny])
def subcategory_list(request):
    # sub_category master all data by using filter and passing category
    data = request.data
    category = data['category']
    try:
        subobj = SubCategoryMaster.objects.filter(category=category).values()
        if subobj:
            return Response({'status': 200, 'message': 'subcategory list', 'data': subobj}, status=200)
        else:
            return Response({'status': 204, 'message': 'not found'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes([AllowAny])
def subcategory_list_category_in_array(request):
    # sub_category master all data by using filter and passing category in array format. example: category[1,2,3]
    data = request.data
    category = data['category']
    try:
        subobj = SubCategoryMaster.objects.filter(category__in=category).values()
        if subobj:
            return Response({'status': 200, 'message': 'subcategory list', 'data': subobj}, status=200)
        else:
            return Response({'status': 204, 'message': 'not found'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['post'])
@permission_classes([AllowAny])
def company_name_search(request):
    # company_name search by passing company names to basic_info and using icontains
    data=request.data
    try:
        regobj =BasicCompanyDetails.objects.filter(company_name__icontains=data['company_name']).values()
        if regobj:
            return Response({'status':200, 'data':regobj}, status=200)
        else:
            return Response({'status':204, 'message':'Company name not found'}, status=204)
    except Exception as e:
        return Response({'status':500, 'error':str(e)}, status=500)


@api_view(['post'])
@permission_classes([AllowAny])
def sub_category_search_by_name(request):
    # sub_category name search by passing sub_category_names to sub_category_master and using icontains
    data = request.data

    try:
        subcatobj = SubCategoryMaster.objects.filter(sub_category_name__icontains=data['sub_category_name']).values()
        if subcatobj:
            return Response({'status': 200, 'message': 'subcategory list', 'data': subcatobj}, status=200)
        else:
            return Response({'status': 204, 'message': 'not found'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
@permission_classes([AllowAny])
def category_search_by_name(request):
    # category_name master search by passing category_name to category_master and using icontains
    data=request.data
    category_name = data['category_name']
    array=[]
    subcatarray=[]
    try:
        catobj = CategoryMaster.objects.filter(category_name__icontains=category_name).values()
        print(catobj)
        if catobj:
            for i in range(0, len(catobj)):
                array.append({'category_id': catobj[i].get('category_id'),
                              'category_name': catobj[i].get('category_name')})
                subcatobj = SubCategoryMaster.objects.filter(category_id=catobj[i].get('category_id')).values()
                for j in range(0, len(subcatobj)):
                    subcatarray.append({'subcatname', subcatobj[j].get('sub_category_name')})
                array[i].setdefault('subcatdata', subcatobj)
            return Response({'status': 200, 'message': 'category list', 'data': array}, status=200)
        else:
            return Response({'status': 204, 'message': 'not found'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['get'])
@permission_classes([AllowAny])
def get_all_billing_cities(request):
    # getting bill_city by using filter from Billing Address
    try:
        cityobj=BillingAddress.objects.filter().values('bill_city')
        if cityobj:
            return Response({'status': 200, 'message': 'City List', 'data': cityobj}, status=200)
        else:
            return Response({'status': 204, 'message': 'No Cities Found'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes([AllowAny])
def get_all_company_details_company_code(request):
    # get all basic-info details by passing company_code
    data=request.data
    companycode=data['companycode']
    try:
        companyobj=BasicCompanyDetails.objects.filter(company_code=companycode).values()
        if companyobj:
            return Response({'status': 200, 'message': 'Company List', 'data': companyobj}, status=200)
        else:
            return Response({'status': 204, 'message': 'No Data Found'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes([AllowAny])
def company_details_by_subcategory_id(request):
    # get company details by passing sub_category_id to sub_category and also fetching basic details and industry hierarchy
    data=request.data
    sub_category_id=data['sub_category_id']
    companycodearray=[]
    subcatnamearrayofarray=[]
    basicdatavalues=[]
    try:
        subobj=SubCategoryMaster.objects.filter(sub_category_id=sub_category_id).values()
        for i in range(0, len(subobj)):
            subcatnamearrayofarray.append(subobj[i].get('sub_category_name'))
        print(subcatnamearrayofarray)
        companycodearray.append(subcatnamearrayofarray)
        print(companycodearray)
        supplyobj = IndustrialHierarchy.objects.filter(subcategory__overlap=subcatnamearrayofarray).values()
            # subcatnamearrayofarray.append({'sub_category_name': subobj[i].get('sub_category_name')})

        for i  in range(0,len(supplyobj)):
            basicobj=BasicCompanyDetails.objects.get(company_code=supplyobj[i].get('company_code_id'))
            basicdatavalues.append({'company_code':basicobj.company_code,
                                    'company_name':basicobj.company_name,
                                    'company_type':basicobj.company_type,
                                    'listing_date':basicobj.listing_date,
                                    'pan_number':basicobj.pan_number,
                                    'tax_payer_type':basicobj.tax_payer_type,
                                    'msme_registered':basicobj.msme_registered,
                                    'company_established':basicobj.company_established,
                                    'updated_by':basicobj.updated_by_id

                                    })

        return Response({'status':200,'message':'ok','data':basicdatavalues},status=200)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['post'])
@permission_classes([AllowAny])
def category_list_by_maincore(request):
    # category master all data by using filter and passing maincore_id
    data = request.data
    maincoreid = data['maincoreid']
    try:
        catobj = CategoryMaster.objects.filter(maincore__in=maincoreid).values()
        print(len(catobj))
        if catobj:
            return Response({'status': 200, 'message': 'category list', 'data': catobj}, status=200)
        else:
            return Response({'status': 204, 'message': 'not found'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['post'])
@permission_classes([AllowAny])
def company_details_by_category_id(request):
    # get company details by passing category_id to sub_category and also fetching basic details and industry hierarchy

    data = request.data
    categoryid = data['categoryid']
    subcategoryarray =[]
    compcodearray=[]
    subcatnamearrayofarray=[]
    try:
        subcategoryobj = SubCategoryMaster.objects.filter(category__in=categoryid).values()
        for i in range(0,len(subcategoryobj)):
            subcatnamearrayofarray.append({'sub_category_name':subcategoryobj[i].get('sub_category_name'),
                                           'sub_category_id':subcategoryobj[i].get('sub_category_id')})
            subcategoryarray.append({subcategoryobj[i].get('sub_category_name')})
            supobj=IndustrialHierarchy.objects.filter(subcategory__icontains=subcategoryobj[i].get('sub_category_name')).values()
            for j in range(0,len(supobj)):
                basicinfoobj = BasicCompanyDetails.objects.filter(company_code=supobj[j].get('company_code_id')).values()
                bill_obj=BillingAddress.objects.filter(company_code_id=supobj[j].get('company_code_id')).values()
                compcodearray.append({'compcode':supobj[j].get('company_code_id'),
                                      'cname':basicinfoobj[0].get('company_name'),
                                      'GST':basicinfoobj[0].get('gst_number'),
                                      'city': bill_obj[0].get('bill_city'),
                                      'state': bill_obj[0].get('bill_state'),
                                      'country': bill_obj[0].get('bill_country'),
                                      'maincore':supobj[j].get('maincore'),
                                      'category':supobj[j].get('category'),
                                      'subcategory':supobj[j].get('subcategory')
                                      })
            subcatnamearrayofarray[i].__setitem__('compcodearray',compcodearray)
            compcodearray=[]
        return Response({'status': 200, 'message': 'ok','data':subcatnamearrayofarray}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes([AllowAny])
def basic_details_by_company_name(request):
    data=request.data
    company_code=data['company_code']
    basicarray=[]
    try:
        basicobj=BasicCompanyDetails.objects.filter(company_code__icontains=company_code).values().order_by('company_code')
        for i in range(0,len(basicobj)):

            basicarray.append(basicobj[i].get('company_code'))
        if len(basicobj)!=0:
            regobj=SelfRegistration.objects.filter(id=basicobj[0].get('updated_by_id')).order_by('id').values('profile_cover_photo')
            industryinfoobj=IndustrialInfo.objects.filter(company_code__in=basicarray).values().order_by('company_code')
            industryhierarchyobj = IndustrialHierarchy.objects.filter(company_code__in=basicarray).values().order_by('company_code')
            basicdetailsall = chain(regobj,basicobj,industryinfoobj, industryhierarchyobj)
            return Response({'status': 200, 'message': 'company list', 'data': basicdetailsall}, status=200)
        else:
            return Response({'status': 204, 'message': 'basic company details not present for this company name'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes([AllowAny])
def maincore_by_id(request):
    data=request.data
    maincore_id=data['maincore_id']
    # maincore master all data by using filter and passig maincore id
    try:
        maincoreobj=MaincoreMaster.objects.filter(maincore_id=maincore_id).values('maincore_name')
        if len(maincoreobj)>0:
            return Response({'status': 200, 'message': 'Maincore List', 'data': maincoreobj}, status=200)
        else:
            return Response({'status': 204, 'message': 'Maincore details not found for this id'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



class CompanyReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = CompanyReview.objects.all()
    serializer_class = CompanyReviewSerializer

    @action(detail=True,methods=['POST'])
    def rate_movie(self,request,pk=None):
        if 'stars' in request.data:
            reviews=CompanyReview.objects.get(id=pk)
            stars=request.data['stars']
            user=SelfRegistration.objects.get(id=request.data('user',None))

            try:
                ratingobj=CompanyRating.objects.get(user=user.id,movie=reviews.id)
                ratingobj.stars=stars
                ratingobj.save()
                serailizer=CompanyRatingSerializer(ratingobj,many=False)
                response={'message':'Rating Updated','result':serailizer.data}
                return Response(response,status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'status': 500, 'error': str(e)}, status=500)

class CompanyRatingViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = CompanyRating.objects.all()
    serializer_class = CompanyRatingSerializer


@api_view(['post'])
@permission_classes((AllowAny,))
def get_all_company_products_services(request):
    search_type=request.data['search_type']
    getarray=[]
    try:
        if search_type=='Companies':
            basicobj=BasicCompanyDetails.objects.filter().values()
            if len(basicobj)>0:
                for i in range(0,len(basicobj)):
                    getarray.append({'name':basicobj[i].get('company_name'),
                                     'ccode':basicobj[i].get('company_code')
                                     })

                return Response({'status':200,'message':'Companies List','data':getarray},status=200)
            else:
                return Response({'status': 204, 'message': 'Companies datas are Not Present'}, status=204)
        elif search_type=='Products':
            productobj=VendorProduct_BasicDetails.objects.filter(item_type='Product').values()
            if len(productobj)>0:
                for i in range(0,len(productobj)):
                    getarray.append({'name':productobj[i].get('item_name'),
                                     'product_code': productobj[i].get('item_code')
                                     })
                return Response({'status': 200, 'message': 'Vendor Product List', 'data': getarray}, status=200)
            else:
                return Response({'status': 204, 'message': 'Vendor Product Lists are Not Present'}, status=204)
        elif search_type == 'All':
            alldata = VendorProduct_BasicDetails.objects.filter(item_type='Product').values()
            if len(alldata) > 0:
                for i in range(0, len(alldata)):
                    getarray.append({'name': alldata[i].get('item_name'),
                                     'product_code':alldata[i].get('item_code')
                                     })
            basicobj = BasicCompanyDetails.objects.filter().values()
            if len(basicobj) > 0:
                for i in range(0, len(basicobj)):
                    getarray.append({'name': basicobj[i].get('company_name'),
                                     'ccode': basicobj[i].get('company_code')
                                     })

                return Response({'status': 200, 'message': 'Vendor All List', 'data': getarray}, status=200)
            else:
                return Response({'status': 204, 'message': 'Vendor All Lists are Not Present'}, status=204)
        else:
            return Response({'status': 204, 'message': 'search type value is mis-spelled or not present'}, status=204)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)
