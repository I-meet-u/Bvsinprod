import math
from itertools import chain

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import api_view, permission_classes, action, parser_classes
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
# Create your views here.
from BiddingApp.models import SourcePublish, SourceList_CreateItems, BuyerProductBidding, BiddingBuyerProductDetails, \
    SelectVendorsForBiddingProduct, VendorProductBidding, VendorBiddingBuyerProductDetails
from DashboardApp.models import InternalVendor, TrailVendors, BusinessRequest, InternalBuyer
from LandingPageApp.models import CompanyReviewAndRating, Message
from LandingPageApp.serializers import CompanyReviewSerializer, MessageSerializer
from MastersApp.models import MaincoreMaster, CategoryMaster, SubCategoryMaster
from MaterialApp.models import VendorProduct_BasicDetails, LandingPageBidding, BuyerProduct_Requirements
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
                                      'category_name': catobj[i].get('category_name'),
                                      'category_image':catobj[i].get('category_image'),
                                      })
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
    rating_ccode=[]
    average=0
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
            basicobj=BasicCompanyDetails.objects.filter(company_code=supplyobj[i].get('company_code_id')).values()
            billingobj=BillingAddress.objects.filter(company_code=supplyobj[i].get('company_code_id')).values()
            regobj=SelfRegistration.objects.filter(id=supplyobj[i].get('updated_by_id')).values()
            industryobj=IndustrialHierarchy.objects.filter(company_code_id=supplyobj[i].get('company_code_id')).values()
            # ratingobj=CompanyReviewAndRating.objects.filter(company_code_id=supplyobj[0].get('company_code_id')).values()

            reviewobj = CompanyReviewAndRating.objects.filter(company_code_id=supplyobj[i].get('company_code_id')).values()
            sum = 0
            for rating in reviewobj:
                sum = sum + rating['rating']
                if len(reviewobj) > 0:
                    average = sum / len(reviewobj)
                else:
                    average = 0
            print(average)

            basicdatavalues.append({'company_code': basicobj[0].get('company_code'),
                                    'company_name': basicobj[0].get('company_name'),
                                    'company_type': basicobj[0].get('company_type'),
                                    'listing_date': basicobj[0].get('listing_date'),
                                    'pan_number': basicobj[0].get('pan_number'),
                                    'tax_payer_type': basicobj[0].get('tax_payer_type'),
                                    'msme_registered': basicobj[0].get('msme_registered'),
                                    'company_established': basicobj[0].get('company_established'),
                                    'updated_by': basicobj[0].get('updated_by_id'),
                                    'gst_no': basicobj[0].get('gst_number'),
                                    'billing_address': billingobj[0].get('bill_address'),
                                    'nature_of_business': regobj[0].get('nature_of_business'),
                                    'profile_image': regobj[0].get('profile_cover_photo'),
                                    'maincore': industryobj[0].get('maincore'),
                                    'category': industryobj[0].get('category'),
                                    'subcategory': industryobj[0].get('subcategory'),
                                    'usertype': regobj[0].get('user_type'),
                                    'bill_city': billingobj[0].get('bill_city'),
                                    'industrial_scale': basicobj[0].get('industrial_scale'),
                                    'email': regobj[0].get('username'),
                                    'phone': regobj[0].get('phone_number'),
                                    'registered_date': regobj[0].get('created_on'),
                                    'rating':round(average)
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
        subcategoryobj = SubCategoryMaster.objects.filter(category_id__in=categoryid).values()
        if len(subcategoryobj)>0:
            for i in range(0,len(subcategoryobj)):
                subcatnamearrayofarray.append({'sub_category_name':subcategoryobj[i].get('sub_category_name'),
                                               'sub_category_id':subcategoryobj[i].get('sub_category_id'),
                                               'sub_category_image': subcategoryobj[i].get('sub_category_image')
                                               })
                subcategoryarray.append({subcategoryobj[i].get('sub_category_name')})
                supobj=IndustrialHierarchy.objects.filter(subcategory__icontains=subcategoryobj[i].get('sub_category_name')).values()
                if len(supobj)>0:
                    for j in range(0,len(supobj)):
                        basicinfoobj = BasicCompanyDetails.objects.filter(company_code=supobj[j].get('company_code_id')).values()
                        bill_obj = BillingAddress.objects.filter(
                            company_code_id=supobj[j].get('company_code_id')).values()
                        if basicinfoobj and  bill_obj:
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

                else:
                    # compcodearray.append()
                    subcatnamearrayofarray[i].__setitem__('compcodearray', compcodearray)
                    compcodearray = []
            return Response({'status': 200, 'message': 'ok','data':subcatnamearrayofarray}, status=200)
        else:
            print('nooooooooo')
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
    queryset = CompanyReviewAndRating.objects.all()
    serializer_class = CompanyReviewSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', None)
        company_code = request.data.get('company_code', None)
        review = request.data.get('review', None),
        rating = request.data.get('rating', None)
        full_name = SelfRegistration.objects.filter(id=user_id).values()
        if len(full_name)>0:
            name = full_name[0].get('contact_person')
        basicobj = BasicCompanyDetails.objects.filter(company_code=company_code).values()
        request.data['company_name'] = basicobj[0].get('company_name')
        request.data['name'] = name
        return super().create(request, *args, **kwargs)
    # def create(self, request, *args, **kwargs):
    #     user_id=request.data.get('user_id',None)
    #     name=request.data.get('name',None)
    #     company_code=request.data.get('company_code',None)
    #     review=request.data.get('review',None),
    #     rating=request.data.get('rating',None)
    #
    #     basicobj=BasicCompanyDetails.objects.filter(company_code=company_code).values()
    #     request.data['company_name']=basicobj[0].get('company_name')
    #     return super().create(request, *args, **kwargs)


@api_view(['post'])
@permission_classes((AllowAny,))
def average_rating(request):
    data=request.data
    # user_id=data['user_id']
    company_code=data['company_code']
    user_array=[]
    average=0
    try:
        reviewobj=CompanyReviewAndRating.objects.filter(company_code=company_code).values()
        sum=0
        for rating in reviewobj:
            sum=sum+rating['rating']
            if len(reviewobj)>0:
                average=sum/len(reviewobj)
            else:
                average=0
        showallreview=CompanyReviewAndRating.objects.filter(company_code=company_code).values().order_by('-id')

        user_array.append({'total_ratings':sum,
                           'average_ratings':average,
                           'company_code':reviewobj[0].get('company_code_id'),
                           'company_name':reviewobj[0].get('company_name')
                           })

        return Response({'status': 200, 'message': 'Rating List', 'data': user_array,'reviewlist':showallreview}, status=200)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

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


#
# @api_view(['post'])
# @permission_classes((AllowAny,))
# def get_all_company_products_services(request):
#     search_type=request.data['search_type']
#     getarray=[]
#     useridarray=[]
#     try:
#         SelfRegistrationobj = SelfRegistration.objects.filter(admin_approve='Approved').values()
#         for i in range(len(SelfRegistrationobj)):
#             useridarray.append(SelfRegistrationobj[i].get('id'))
#
#         if search_type=='Companies':
#             basicobj=BasicCompanyDetails.objects.filter(updated_by_id__in=useridarray).values()
#             if len(basicobj)>0:
#                 for i in range(0,len(basicobj)):
#                     getarray.append({'name':basicobj[i].get('company_name'),
#                                      'ccode':basicobj[i].get('company_code')
#                                      })
#
#                 return Response({'status':200,'message':'Companies List','data':getarray},status=200)
#             else:
#                 return Response({'status': 204, 'message': 'Companies datas are Not Present'}, status=204)
#         elif search_type=='Products':
#             productobj=VendorProduct_BasicDetails.objects.filter(item_type='Product').values()
#             if len(productobj)>0:
#                 for i in range(0,len(productobj)):
#                     maincorevalue = MaincoreMaster.objects.filter(maincore_name=productobj[i].
#                                                                   get('core_sector')).values()
#                     Categorydetails=CategoryMaster.objects.filter(maincore=maincorevalue[0].get('maincore_id')).values()
#                     getarray.append({'name':productobj[i].get('item_name'),
#                                      'product_code': productobj[i].get('item_code'),
#                                      'maincore':productobj[i].get('core_sector'),
#                                      'category':Categorydetails[0].get('category_id'),
#                                      'subcategory':productobj[i].get('sub_category'),
#                                      })
#                 return Response({'status': 200, 'message': 'Vendor Product List', 'data': getarray}, status=200)
#             else:
#                 return Response({'status': 204, 'message': 'Vendor Product Lists are Not Present'}, status=204)
#         elif search_type == 'All':
#             itemtypearr=['Product','Service']
#             productobj = VendorProduct_BasicDetails.objects.filter(item_type__in=itemtypearr).values()
#             if len(productobj) > 0:
#                 for i in range(0, len(productobj)):
#                     maincorevalue = MaincoreMaster.objects.filter(maincore_name=productobj[i].
#                                                                   get('core_sector')).values()
#                     Categorydetails = CategoryMaster.objects.filter(
#                         maincore=maincorevalue[0].get('maincore_id')).values()
#                     getarray.append({'name': productobj[i].get('item_name'),
#                                      'product_code': productobj[i].get('item_code'),
#                                      'maincore': productobj[i].get('core_sector'),
#                                      'category': Categorydetails[0].get('category_id'),
#                                      'subcategory': productobj[i].get('sub_category'),
#                                      })
#
#                 return Response({'status': 200, 'message': 'Vendor All List', 'data': getarray}, status=200)
#             else:
#                 return Response({'status': 204, 'message': 'Vendor All Lists are Not Present'}, status=204)
#         elif search_type == 'Services':
#             productobj = VendorProduct_BasicDetails.objects.filter(item_type='Service').values()
#             if len(productobj) > 0:
#                 for i in range(0, len(productobj)):
#                     maincorevalue = MaincoreMaster.objects.filter(maincore_name=productobj[i].
#                                                                   get('core_sector')).values()
#                     Categorydetails = CategoryMaster.objects.filter(
#                         maincore=maincorevalue[0].get('maincore_id')).values()
#                     getarray.append({'name': productobj[i].get('item_name'),
#                                      'product_code': productobj[i].get('item_code'),
#                                      'maincore': productobj[i].get('core_sector'),
#                                      'category': Categorydetails[0].get('category_id'),
#                                      'subcategory': productobj[i].get('sub_category'),
#                                      })
#                 return Response({'status': 200, 'message': 'Vendor Product List', 'data': getarray}, status=200)
#             else:
#                 return Response({'status': 204, 'message': 'Vendor Product Lists are Not Present'}, status=204)
#
#         else:
#             return Response({'status': 204, 'message': 'search type value is mis-spelled or not present'}, status=204)
#
#
#     except Exception as e:
#         return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
@permission_classes((AllowAny,))
def get_all_company_products_services(request):
    search_type=request.data['search_type']
    getarray=[]
    useridarray=[]
    try:
        SelfRegistrationobj = SelfRegistration.objects.filter(admin_approve='Approved').values()
        for i in range(len(SelfRegistrationobj)):
            useridarray.append(SelfRegistrationobj[i].get('id'))

        if search_type=='Companies':
            basicobj=BasicCompanyDetails.objects.filter(updated_by_id__in=useridarray).values()
            if len(basicobj)>0:
                for i in range(0,len(basicobj)):
                    getarray.append({'name':basicobj[i].get('company_name'),
                                     'ccode':basicobj[i].get('company_code')
                                     })

                return Response({'status':200,'message':'Companies List','data':getarray},status=200)
            else:
                return Response({'status': 204, 'message': 'Companies datas are Not Present','data':getarray}, status=204)
        elif search_type=='Products':
            productobj=VendorProduct_BasicDetails.objects.filter(item_type='Product').values()
            if len(productobj)>0:
                for i in range(0,len(productobj)):
                    maincorevalue = MaincoreMaster.objects.filter(maincore_name__icontains=productobj[i].
                                                                  get('core_sector')).values()
                    if maincorevalue:
                        Categorydetails=CategoryMaster.objects.filter(maincore=maincorevalue[0].get('maincore_id')).values()
                        if Categorydetails:
                            getarray.append({'name':productobj[i].get('item_name'),
                                             'product_code': productobj[i].get('item_code'),
                                             'maincore':productobj[i].get('core_sector'),
                                             'category':Categorydetails[0].get('category_id'),
                                             'subcategory':productobj[i].get('sub_category'),
                                             'itemtype':productobj[i].get('item_type')
                                             })
                        else:
                            getarray.append({'name': productobj[i].get('item_name'),
                                             'product_code': productobj[i].get('item_code'),
                                             'maincore': productobj[i].get('core_sector'),
                                             'category':"",
                                             'subcategory': productobj[i].get('sub_category'),
                                             'itemtype': productobj[i].get('item_type')
                                             })
                return Response({'status': 200, 'message': 'Vendor Product List', 'data': getarray}, status=200)
            else:
                return Response({'status': 204, 'message': 'Vendor Product Lists are Not Present','data':getarray}, status=204)
        elif search_type == 'All':
            itemtypearr=['Product','Service']
            # alldata = VendorProduct_BasicDetails.objects.filter(item_type__in=itemtypearr).values()
            alldata = VendorProduct_BasicDetails.objects.filter(item_type__in=itemtypearr).values()


            if len(alldata) > 0:
                for i in range(0, len(alldata)):
                    print(alldata[i].get('item_name'))
                    Maaincoreid=MaincoreMaster.objects.filter(maincore_name=alldata[i].get('core_sector')).values()
                    if Maaincoreid:
                        Categoryid=CategoryMaster.objects.filter(category_name=alldata[i].get('category')).values()
                        if Categoryid:
                            print("maincore =====================================")
                            print(Maaincoreid)
                            print("category =====================================")
                            print(alldata[i].get('category'))
                            print(Categoryid)

                            getarray.append({'name': alldata[i].get('item_name'),
                                             'product_code':alldata[i].get('item_code'),
                                             'maincore':Maaincoreid[0].get('maincore_id'),
                                             'category':Categoryid[0].get('category_id'),
                                             'subcategory':alldata[i].get('sub_category'),
                                             'itemtype':alldata[i].get('item_type')
                                             })
                        else:
                            getarray.append({'name': alldata[i].get('item_name'),
                                             'product_code': alldata[i].get('item_code'),
                                             'maincore': Maaincoreid[0].get('maincore_id'),
                                             'category': "",
                                             'subcategory': alldata[i].get('sub_category'),
                                             'itemtype': alldata[i].get('item_type')
                                             })

            basicobj = BasicCompanyDetails.objects.filter().values()
            if len(basicobj) > 0:
                for i in range(0, len(basicobj)):
                    getarray.append({'name': basicobj[i].get('company_name'),
                                     'ccode': basicobj[i].get('company_code')
                                     })
                return Response({'status': 200, 'message': 'Vendor All List', 'data': getarray}, status=200)
            else:
                return Response({'status': 204, 'message': 'Vendor All Lists are Not Present','data':getarray}, status=204)
        elif search_type == 'Services':
            productobj = VendorProduct_BasicDetails.objects.filter(item_type='Service').values()
            if len(productobj) > 0:
                for i in range(0, len(productobj)):
                    maincorevalue = MaincoreMaster.objects.filter(maincore_name=productobj[i].
                                                                  get('core_sector')).values()
                    if maincorevalue:
                        Categorydetails = CategoryMaster.objects.filter(
                            maincore=maincorevalue[0].get('maincore_id')).values()
                        if Categorydetails:
                            getarray.append({'name': productobj[i].get('item_name'),
                                             'product_code': productobj[i].get('item_code'),
                                             'maincore': productobj[i].get('core_sector'),
                                             'category': "",
                                             'subcategory': productobj[i].get('sub_category'),
                                             'itemtype': productobj[i].get('item_type')
                                             })
                        else:
                            getarray.append({'name': productobj[i].get('item_name'),
                                             'product_code': productobj[i].get('item_code'),
                                             'maincore': productobj[i].get('core_sector'),
                                             'category': "",
                                             'subcategory': productobj[i].get('sub_category'),
                                             'itemtype': productobj[i].get('item_type')
                                             })
                return Response({'status': 200, 'message': 'Vendor Service List', 'data': getarray}, status=200)
            else:
                return Response({'status': 204, 'message': 'Vendor Service Lists are Not Present','data':getarray}, status=204)

        else:
            return Response({'status': 204, 'message': 'search type value is mis-spelled or not present'}, status=204)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


# @api_view(['post'])
# @permission_classes((AllowAny,))
# def get_all_company_products_services(request):
#     search_type=request.data['search_type']
#     getarray=[]
#     try:
#         if search_type=='Companies':
#             basicobj=BasicCompanyDetails.objects.filter().values()
#             if len(basicobj)>0:
#                 for i in range(0,len(basicobj)):
#                     getarray.append({'name':basicobj[i].get('company_name'),
#                                      'ccode':basicobj[i].get('company_code')
#                                      })
#
#                 return Response({'status':200,'message':'Companies List','data':getarray},status=200)
#             else:
#                 return Response({'status': 204, 'message': 'Companies datas are Not Present'}, status=204)
#         elif search_type=='Products':
#             productobj=VendorProduct_BasicDetails.objects.filter(item_type='Product').values()
#             if len(productobj)>0:
#                 for i in range(0,len(productobj)):
#                     getarray.append({'name':productobj[i].get('item_name'),
#                                      'product_code': productobj[i].get('item_code')
#                                      })
#                 return Response({'status': 200, 'message': 'Vendor Product List', 'data': getarray}, status=200)
#             else:
#                 return Response({'status': 204, 'message': 'Vendor Product Lists are Not Present'}, status=204)
#         elif search_type == 'All':
#             alldata = VendorProduct_BasicDetails.objects.filter(item_type='Product').values()
#             if len(alldata) > 0:
#                 for i in range(0, len(alldata)):
#                     getarray.append({'name': alldata[i].get('item_name'),
#                                      'product_code':alldata[i].get('item_code')
#                                      })
#             basicobj = BasicCompanyDetails.objects.filter().values()
#             if len(basicobj) > 0:
#                 for i in range(0, len(basicobj)):
#                     getarray.append({'name': basicobj[i].get('company_name'),
#                                      'ccode': basicobj[i].get('company_code')
#                                      })
#
#                 return Response({'status': 200, 'message': 'Vendor All List', 'data': getarray}, status=200)
#             else:
#                 return Response({'status': 204, 'message': 'Vendor All Lists are Not Present'}, status=204)
#         else:
#             return Response({'status': 204, 'message': 'search type value is mis-spelled or not present'}, status=204)
#
#
#     except Exception as e:
#         return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['get'])
def get_approved_companies_list(request):
    basicarray=[]
    try:
        regobj=SelfRegistration.objects.filter(admin_approve='Approved').values().order_by('id')
        if len(regobj)>0:
            for i in range(0,len(regobj)):
                print(regobj[i].get('id'))
                basicobj = BasicCompanyDetails.objects.filter(updated_by_id=regobj[i].get('id')).values()
                if len(basicobj)>0:
                    billobj = BillingAddress.objects.filter(updated_by_id=basicobj[0].get('updated_by_id')).values().order_by('company_code')
                    if billobj:
                        basicarray.append({'company_code':basicobj[0].get('company_code'),
                                       'gst_number':basicobj[0].get('gst_number'),
                                       'name':basicobj[0].get('company_name'),
                                       'company_type':basicobj[0].get('company_type'),
                                       'listing_date':basicobj[0].get('listing_date'),
                                       'pan_number':basicobj[0].get('pan_number'),
                                       'tax_payer_type':basicobj[0].get('tax_payer_type'),
                                       'msme_registered':basicobj[0].get('msme_registered'),
                                       'company_established':basicobj[0].get('company_established'),
                                       'registered_iec':basicobj[0].get('registered_iec'),
                                       'industrial_scale':basicobj[0].get('industrial_scale'),
                                       'updated_by':basicobj[0].get('updated_by_id'),
                                       'billing_address':billobj[0].get('bill_address'),
                                       'email':regobj[i].get('username'),
                                       'phone_number':regobj[i].get('phone_number'),
                                       'profile_photo':regobj[i].get('profile_cover_photo')
                                       })
                else:
                    pass
            return Response({'status': 200, 'message': 'Approved Companies List', 'data': basicarray}, status=200)
        else:
            return Response({'status': 204, 'message': 'Approved Companies Are Not Present'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['get'])
@permission_classes((AllowAny,))
def get_all_vendor_product_details(request):
    try:
        vendorobj=VendorProduct_BasicDetails.objects.filter().values().order_by('vendor_product_id')
        if len(vendorobj)>0:
            return Response({'status':200,'message':'Vendor Product List','data':vendorobj},status=200)
        else:
            return Response({'status':204,'message':'Not Present'},status=204)

    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


# @api_view(['post'])
# @permission_classes((AllowAny,))
# def search_texts(request):
#     search_type=request.data['search_type']
#     search_text=request.data['search_text']
#     try:
#         if search_type=='Companies':
#             basicobj=BasicCompanyDetails.objects.filter(company_name__icontains=search_text).values()
#             if len(basicobj)>0:
#
#                 return Response({'status':200,'message':'Companies List','data':basicobj},status=200)
#             else:
#                 return Response({'status': 204, 'message': 'Companies datas are Not Present','data':basicobj}, status=204)
#         elif search_type=='Products':
#             productobj=VendorProduct_BasicDetails.objects.filter(item_type='Product',item_name__icontains=search_text).values()
#             if len(productobj)>0:
#                 return Response({'status': 200, 'message': 'Vendor Product List', 'data': productobj}, status=200)
#             else:
#                 return Response({'status': 204, 'message': 'Vendor Product Lists are Not Present','data':productobj}, status=204)
#
#         elif search_type=='Service':
#             productobj=VendorProduct_BasicDetails.objects.filter(item_type='Service',item_name__icontains=search_text).values()
#             if len(productobj)>0:
#                 return Response({'status': 200, 'message': 'Vendor Service List', 'data': productobj}, status=200)
#             else:
#                 return Response({'status': 204, 'message': 'Vendor Service Lists are Not Present','data':productobj}, status=204)
#         elif search_type == 'All':
#             alldata = VendorProduct_BasicDetails.objects.filter(item_type='Product',item_name__icontains=search_text).values()
#
#             alldata1 = VendorProduct_BasicDetails.objects.filter(item_type='Service',
#                                                                  item_name__icontains=search_text).values()
#             basicobj = BasicCompanyDetails.objects.filter(company_name__icontains=search_text).values()
#             return Response({'status': 200, 'message': 'Vendor All List', 'data_basic_info':basicobj,'vendor_product_data':alldata,'vendor_service_data':alldata1}, status=200)
#         else:
#             return Response({'status': 204, 'message': 'search type value is mis-spelled or not present'}, status=204)
#
#
#     except Exception as e:
#         return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def search_texts(request):
    search_type=request.data['search_type']
    search_text=request.data['search_text']
    getarray=[]
    try:
        if search_type=='Companies':
            basicobj=BasicCompanyDetails.objects.filter(company_name__icontains=search_text).values()
            print(basicobj)
            if len(basicobj)>0:
                for i in range(0,len(basicobj)):
                    regobj=SelfRegistration.objects.filter(id=basicobj[i].get('updated_by_id')).values()
                    billobj=BillingAddress.objects.filter(updated_by_id=basicobj[i].get('updated_by_id')).values()
                    hierarchyobj=IndustrialHierarchy.objects.filter(updated_by_id=basicobj[i].get('updated_by_id')).values()
                    if regobj:
                        if basicobj:
                            if billobj:
                                if hierarchyobj:
                                    getarray.append({'company_code': basicobj[i].get('company_code'),
                                                     'company_name': basicobj[i].get('company_name'),
                                                     'gst_number': basicobj[i].get('gst_number'),
                                                     'user_type': regobj[0].get('user_type'),
                                                     'email': regobj[0].get('username'),
                                                     'phone_number': regobj[0].get('phone_number'),
                                                     'profile_photo': regobj[0].get('profile_cover_photo'),
                                                     'nature_of_business': regobj[0].get('nature_of_business'),
                                                     'bill_city': billobj[0].get('bill_city'),
                                                     'bill_address': billobj[0].get('bill_address'),
                                                     'maincore': hierarchyobj[0].get('maincore'),
                                                     'category': hierarchyobj[0].get('category'),
                                                     'subcategory': hierarchyobj[0].get('subcategory'),
                                                     'industrial_scale': basicobj[i].get('industrial_scale'),
                                                     'registered_date': regobj[0].get('created_on')
                                                     })
                                else:
                                    getarray.append({'company_code': basicobj[i].get('company_code'),
                                                     'company_name': basicobj[i].get('company_name'),
                                                     'gst_number': basicobj[i].get('gst_number'),
                                                     'user_type': regobj[0].get('user_type'),
                                                     'email': regobj[0].get('username'),
                                                     'phone_number': regobj[0].get('phone_number'),
                                                     'profile_photo': regobj[0].get('profile_cover_photo'),
                                                     'nature_of_business': regobj[0].get('nature_of_business'),
                                                     'bill_city': billobj[0].get('bill_city'),
                                                     'bill_address': billobj[0].get('bill_address'),
                                                     'maincore': 'Not Available',
                                                     'category': 'Not Available',
                                                     'subcategory': 'Not Available',
                                                     'industrial_scale': basicobj[i].get('industrial_scale'),
                                                     'registered_date': regobj[0].get('created_on')
                                                     })
                return Response({'status':200,'message':'Companies List','data':getarray},status=200)
            else:
                return Response({'status': 204, 'message': 'Companies datas are Not Present','data':basicobj}, status=204)
        elif search_type=='Products':
            productobj=VendorProduct_BasicDetails.objects.filter(item_type='Product',item_name__icontains=search_text).values()
            if len(productobj)>0:
                return Response({'status': 200, 'message': 'Vendor Product List', 'data': productobj}, status=200)
            else:
                return Response({'status': 204, 'message': 'Vendor Product Lists are Not Present','data':productobj}, status=204)

        elif search_type=='Service':
            productobj=VendorProduct_BasicDetails.objects.filter(item_type='Service',item_name__icontains=search_text).values()
            if len(productobj)>0:
                return Response({'status': 200, 'message': 'Vendor Service List', 'data': productobj}, status=200)
            else:
                return Response({'status': 204, 'message': 'Vendor Service Lists are Not Present','data':productobj}, status=204)
        elif search_type == 'All':
            alldata = VendorProduct_BasicDetails.objects.filter(item_type='Product',item_name__icontains=search_text).values()
            alldata1 = VendorProduct_BasicDetails.objects.filter(item_type='Service',
                                                                 item_name__icontains=search_text).values()
            basicobj = BasicCompanyDetails.objects.filter(company_name__icontains=search_text).values()
            print("basicobj ",basicobj)
            for i in range(0,len(basicobj)):
                print("inside for loop")
                regobj=SelfRegistration.objects.filter(id=basicobj[i].get('updated_by_id')).values()
                billobj=BillingAddress.objects.filter(updated_by_id=basicobj[i].get('updated_by_id')).values()
                hierarchyobj=IndustrialHierarchy.objects.filter(updated_by_id=basicobj[i].get('updated_by_id')).values()
                if regobj:
                    if basicobj:
                        if billobj:
                            if hierarchyobj:
                                getarray.append({'company_code':basicobj[i].get('company_code'),
                                                 'company_name':basicobj[i].get('company_name'),
                                                 'gst_number':basicobj[i].get('gst_number'),
                                                 'user_type':regobj[0].get('user_type'),
                                                 'email':regobj[0].get('username'),
                                                 'phone_number':regobj[0].get('phone_number'),
                                                 'profile_photo': regobj[0].get('profile_cover_photo'),
                                                 'nature_of_business':regobj[0].get('nature_of_business'),
                                                 'bill_city':billobj[0].get('bill_city'),
                                                 'bill_address':billobj[0].get('bill_address'),
                                                 'maincore':hierarchyobj[0].get('maincore'),
                                                 'category':hierarchyobj[0].get('category'),
                                                 'subcategory':hierarchyobj[0].get('subcategory'),
                                                 'industrial_scale': basicobj[i].get('industrial_scale'),
                                                 'registered_date': regobj[0].get('created_on')
                                                 })
                            else:
                                getarray.append({'company_code': basicobj[i].get('company_code'),
                                                 'company_name': basicobj[i].get('company_name'),
                                                 'gst_number': basicobj[i].get('gst_number'),
                                                 'user_type': regobj[0].get('user_type'),
                                                 'email': regobj[0].get('username'),
                                                 'phone_number': regobj[0].get('phone_number'),
                                                 'profile_photo': regobj[0].get('profile_cover_photo'),
                                                 'nature_of_business': regobj[0].get('nature_of_business'),
                                                 'bill_city': billobj[0].get('bill_city'),
                                                 'bill_address': billobj[0].get('bill_address'),
                                                 'maincore': 'Not Available',
                                                 'category': 'Not Available',
                                                 'subcategory': 'Not Available',
                                                 'industrial_scale': basicobj[i].get('industrial_scale'),
                                                 'registered_date': regobj[0].get('created_on')
                                                 })
            return Response({'status': 200, 'message': 'Vendor All List', 'data_basic_info':getarray,'vendor_product_data':alldata,'vendor_service_data':alldata1}, status=200)
        else:
            return Response({'status': 204, 'message': 'search type value is mis-spelled or not present'}, status=204)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes([AllowAny],)
def getproductbymaincore(request):
    try:
        data=request.data
        maincoreproducts=""
        if data['key']=="vsinadmindb":
            MaincoreMasterobj=MaincoreMaster.objects.filter(maincore_id=data['mid']).values()
            if MaincoreMasterobj:
                maincoreproducts=VendorProduct_BasicDetails.objects.filter(core_sector=MaincoreMasterobj[0].get('maincore_name')).values()
                if maincoreproducts:
                    return Response({'status': 200, 'message': 'product list','products':maincoreproducts},status=200)
            return Response({'status': 202, 'message': 'product list', 'products': maincoreproducts}, status=202)
        else:
            return Response({'status':400,'message':'Bad Request'},status=400)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['post'])
@permission_classes([AllowAny])
def company_details_by_maincore_id(request):
    data=request.data
    key = data['key']
    maincore_id=data['maincore_id']
    companycodearray=[]
    maincorearray=[]
    basicdatavalues=[]
    average=0
    try:
        if key=="vsinadmindb":
            maincoreobj=MaincoreMaster.objects.filter(maincore_id=maincore_id).values()
            for i in range(0, len(maincoreobj)):
                maincorearray.append(maincoreobj[i].get('maincore_name'))
            companycodearray.append(maincorearray)
            supplyobj = IndustrialHierarchy.objects.filter(maincore__overlap=maincorearray).values()


            for i  in range(0,len(supplyobj)):
                basicobj=BasicCompanyDetails.objects.filter(company_code=supplyobj[i].get('company_code_id')).values()
                billingobj=BillingAddress.objects.filter(company_code=supplyobj[i].get('company_code_id')).values()
                regobj=SelfRegistration.objects.filter(id=supplyobj[i].get('updated_by_id')).values()
                industryobj=IndustrialHierarchy.objects.filter(company_code_id=supplyobj[i].get('company_code_id')).values()

                reviewobj = CompanyReviewAndRating.objects.filter(company_code_id=supplyobj[i].get('company_code_id')).values()
                sum = 0
                for rating in reviewobj:
                    sum = sum + rating['rating']
                    if len(reviewobj) > 0:
                        average = sum / len(reviewobj)
                    else:
                        average = 0
                print(average)

                basicdatavalues.append({'company_code': basicobj[0].get('company_code'),
                                        'company_name': basicobj[0].get('company_name'),
                                        'company_type': basicobj[0].get('company_type'),
                                        'listing_date': basicobj[0].get('listing_date'),
                                        'pan_number': basicobj[0].get('pan_number'),
                                        'tax_payer_type': basicobj[0].get('tax_payer_type'),
                                        'msme_registered': basicobj[0].get('msme_registered'),
                                        'company_established': basicobj[0].get('company_established'),
                                        'updated_by': basicobj[0].get('updated_by_id'),
                                        'gst_no': basicobj[0].get('gst_number'),
                                        'billing_address': billingobj[0].get('bill_address'),
                                        'nature_of_business': regobj[0].get('nature_of_business'),
                                        'profile_image': regobj[0].get('profile_cover_photo'),
                                        'maincore': industryobj[0].get('maincore'),
                                        'category': industryobj[0].get('category'),
                                        'subcategory': industryobj[0].get('subcategory'),
                                        'usertype': regobj[0].get('user_type'),
                                        'bill_city': billingobj[0].get('bill_city'),
                                        'industrial_scale': basicobj[0].get('industrial_scale'),
                                        'email': regobj[0].get('username'),
                                        'phone': regobj[0].get('phone_number'),
                                        'registered_date': regobj[0].get('created_on'),
                                        'rating':round(average)
                                        })

            return Response({'status':200,'message':'ok','data':basicdatavalues},status=200)
        else:
            return Response({'status': 401, 'message': 'UnAuthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)




@api_view(['post'])
@permission_classes([AllowAny])
def company_details_by_maincore_id_cat_id(request):
    data=request.data
    key = data['key']
    maincore_id=data['maincore_id']
    category_id = data['category_id']
    companycodearray=[]
    maincorearray=[]
    categoryarray=[]
    basicdatavalues=[]
    average=0
    try:
        if key=="vsinadmindb":
            maincoreobj=MaincoreMaster.objects.filter(maincore_id=maincore_id).values()
            for i in range(0, len(maincoreobj)):
                maincorearray.append(maincoreobj[i].get('maincore_name'))

            categoryobj = CategoryMaster.objects.filter(category_id=category_id).values()
            for i in range(0, len(categoryobj)):
                categoryarray.append(categoryobj[i].get('category_name'))
            supplyobj = IndustrialHierarchy.objects.filter(maincore__overlap=maincorearray,category__overlap=categoryarray).values()


            for i  in range(0,len(supplyobj)):
                basicobj=BasicCompanyDetails.objects.filter(company_code=supplyobj[i].get('company_code_id')).values()
                billingobj=BillingAddress.objects.filter(company_code=supplyobj[i].get('company_code_id')).values()
                regobj=SelfRegistration.objects.filter(id=supplyobj[i].get('updated_by_id')).values()
                industryobj=IndustrialHierarchy.objects.filter(company_code_id=supplyobj[i].get('company_code_id')).values()

                reviewobj = CompanyReviewAndRating.objects.filter(company_code_id=supplyobj[i].get('company_code_id')).values()
                sum = 0
                for rating in reviewobj:
                    sum = sum + rating['rating']
                    if len(reviewobj) > 0:
                        average = sum / len(reviewobj)
                    else:
                        average = 0
                print(average)

                basicdatavalues.append({'company_code': basicobj[0].get('company_code'),
                                        'company_name': basicobj[0].get('company_name'),
                                        'company_type': basicobj[0].get('company_type'),
                                        'listing_date': basicobj[0].get('listing_date'),
                                        'pan_number': basicobj[0].get('pan_number'),
                                        'tax_payer_type': basicobj[0].get('tax_payer_type'),
                                        'msme_registered': basicobj[0].get('msme_registered'),
                                        'company_established': basicobj[0].get('company_established'),
                                        'updated_by': basicobj[0].get('updated_by_id'),
                                        'gst_no': basicobj[0].get('gst_number'),
                                        'billing_address': billingobj[0].get('bill_address'),
                                        'nature_of_business': regobj[0].get('nature_of_business'),
                                        'profile_image': regobj[0].get('profile_cover_photo'),
                                        'maincore': industryobj[0].get('maincore'),
                                        'category': industryobj[0].get('category'),
                                        'subcategory': industryobj[0].get('subcategory'),
                                        'usertype': regobj[0].get('user_type'),
                                        'bill_city': billingobj[0].get('bill_city'),
                                        'industrial_scale': basicobj[0].get('industrial_scale'),
                                        'email': regobj[0].get('username'),
                                        'phone': regobj[0].get('phone_number'),
                                        'registered_date': regobj[0].get('created_on'),
                                        'rating':round(average)
                                        })

            return Response({'status':200,'message':'ok','data':basicdatavalues},status=200)
        else:
            return Response({'status': 401, 'message': 'UnAuthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['GET','POST'])
@permission_classes((AllowAny,))
# @parser_classes([MultiPartParser])
def messages_lists(request,sender=None,receiver=None):
    try:

        # if request.data['key']=='vsinadmindb':
        if request.method=='GET':
            messages=Message.objects.filter(sender_id=sender,receiver_id=receiver)
            serializer=MessageSerializer(messages,many=True)
            # for msg in messages:
            #     if msg.is_read==False:
            #         msg.is_read=True
            #         msg.save()
            return Response(serializer.data)
        elif(request.method=='POST'):
            if request.data['key'] == 'vsinadmindb':
                serializer=MessageSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_201_CREATED)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status':401,'message':'UnAuthorized'},status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes((AllowAny,))
def receiver_sender_messages(request,sender=None,receiver=None):
    try:
        if request.method == 'GET':
            messages = Message.objects.filter(sender_id=sender, receiver_id=receiver)
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes((AllowAny,))
def messages_user_list(request):
    data=request.data
    sender=data['sender']
    message_list=[]
    try:
        msgobj=Message.objects.filter(sender_id=sender).values().order_by('created_time')
        if len(msgobj)>0:
            for i in range(0,len(msgobj)):
                regobj1=SelfRegistration.objects.filter(id=msgobj[i].get('sender_id')).values()
                regobj2 = SelfRegistration.objects.filter(id=msgobj[i].get('receiver_id')).values()
                sender_addressobj=BillingAddress.objects.filter(updated_by_id=regobj1[0].get('id')).values()
                if sender_addressobj:
                    receiver_addressobj=BillingAddress.objects.filter(updated_by_id=regobj2[0].get('id')).values()
                    if receiver_addressobj:
                        message_list.append({'sender_name':msgobj[i].get('sender_name'),
                                             'receiver_name':msgobj[i].get('receiver_name'),
                                             'created_time': msgobj[i].get('created_time'),
                                             'sender_id': msgobj[i].get('sender_id'),
                                             'receiver_id': msgobj[i].get('receiver_id'),
                                             'sender_email_id':regobj1[0].get('username'),
                                             'receiver_email_id': regobj2[0].get('username'),
                                             'messages':msgobj[i].get('messages'),
                                             'sender_city':sender_addressobj[0].get('bill_city'),
                                             'sender_state': sender_addressobj[0].get('bill_state'),
                                             'sender_country': sender_addressobj[0].get('bill_country'),
                                             'receiver_city': receiver_addressobj[0].get('bill_city'),
                                             'receiver_state': receiver_addressobj[0].get('bill_state'),
                                             'receiver_country': receiver_addressobj[0].get('bill_country'),
                                             'company_logo_sender':regobj1[0].get('profile_cover_photo'),
                                             'company_logo_receiver': regobj2[0].get('profile_cover_photo'),
                                             'company_name_sender':msgobj[i].get('company_name_sender'),
                                             'company_name_receiver':msgobj[i].get('company_name_receiver'),
                                             'vendor_product_pk':msgobj[i].get('vendor_product_pk_id'),
                                             'source':msgobj[i].get('source'),
                                             'get_vendor': msgobj[i].get('get_vendor'),
                                             'rfq': msgobj[i].get('rfq'),
                                             'enquiry':msgobj[i].get('enquiry')

                                             })
                    else:
                        message_list.append({'sender_name': msgobj[i].get('sender_name'),
                                             'receiver_name': msgobj[i].get('receiver_name'),
                                             'created_time': msgobj[i].get('created_time'),
                                             'sender_id': msgobj[i].get('sender_id'),
                                             'receiver_id': msgobj[i].get('receiver_id'),
                                             'sender_email_id': regobj1[0].get('username'),
                                             'receiver_email_id': regobj2[0].get('username'),
                                             'messages': msgobj[i].get('messages'),
                                             'sender_city': sender_addressobj[0].get('bill_city'),
                                             'sender_state': sender_addressobj[0].get('bill_state'),
                                             'sender_country': sender_addressobj[0].get('bill_country'),
                                             'receiver_city': "",
                                             'receiver_state': "",
                                             'receiver_country': "",
                                             'company_logo_sender': regobj1[0].get('profile_cover_photo'),
                                             'company_logo_receiver': regobj2[0].get('profile_cover_photo'),
                                             'company_name_sender': msgobj[i].get('company_name_sender'),
                                             'company_name_receiver': msgobj[i].get('company_name_receiver'),
                                             'vendor_product_pk': msgobj[i].get('vendor_product_pk_id'),
                                             'source': msgobj[i].get('source'),
                                             'get_vendor': msgobj[i].get('get_vendor'),
                                             'rfq': msgobj[i].get('rfq'),
                                             'enquiry': msgobj[i].get('enquiry')

                                             })
            return Response({'status':200,'message':'Users List','data':message_list},status=200)
        else:
            return Response({'status':204,'message':'Users Not Present','data':msgobj},status=200)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

# @api_view(['post'])
# @permission_classes((AllowAny,))
# def internal_external_trail_buyers_users_list(request):
#     users=request.data['users']
#     external_list=[]
#     buyer_list=[]
#     internal_list=[]
#     trail_list=[]
#     business_network=[]
#     try:
#         if users=='external_user':
#             regobjdata = SelfRegistration.objects.filter(Q(user_type='Vendor') | Q(user_type='Both'),
#                                                          admin_approve='Approved').values().order_by('id')
#             if len(regobjdata)>0:
#                 for i in range(0, len(regobjdata)):
#                     basicobj = BasicCompanyDetails.objects.get(updated_by_id=regobjdata[i].get('id'))
#                     if basicobj:
#                         external_list.append({'company_code': basicobj.company_code,
#                                               'company_name': basicobj.company_name,
#                                               'phone_no': regobjdata[i].get('phone_number'),
#                                               'email_id': regobjdata[i].get('username'),
#                                               'user_name':regobjdata[i].get('contact_person'),
#                                               'user_id':regobjdata[i].get('id'),
#                                               'profile_cover_photo':regobjdata[i].get('profile_cover_photo')
#                                               })
#                     else:
#                         external_list.append({'company_code': "",
#                                               'company_name': "",
#                                               'phone_no': regobjdata[i].get('phone_number'),
#                                               'email_id': regobjdata[i].get('username'),
#                                               'user_name': regobjdata[i].get('contact_person'),
#                                               'user_id': regobjdata[i].get('id'),
#                                               'profile_cover_photo': regobjdata[i].get('profile_cover_photo')
#                                               })
#
#                 return Response({'status':200,'message':'External Users List','data':external_list},status=200)
#             else:
#                 return Response({'status': 204, 'message': 'Not Present'}, status=204)
#         elif users=='buyer':
#             regobjdata = SelfRegistration.objects.filter(user_type='Buyer',admin_approve='Approved').values().order_by('id')
#             if len(regobjdata) > 0:
#                 for i in range(0, len(regobjdata)):
#                     basicobj = BasicCompanyDetails.objects.get(updated_by_id=regobjdata[i].get('id'))
#                     if basicobj:
#                         buyer_list.append({'company_code': basicobj.company_code,
#                                           'company_name': basicobj.company_name,
#                                           'phone_no': regobjdata[i].get('phone_number'),
#                                           'email_id': regobjdata[i].get('username'),
#                                           'user_name': regobjdata[i].get('contact_person'),
#                                           'user_id': regobjdata[i].get('id'),
#                                            'profile_cover_photo': regobjdata[i].get('profile_cover_photo')
#                                             })
#                     else:
#                         buyer_list.append({'company_code': "",
#                                            'company_name': "",
#                                            'phone_no': regobjdata[i].get('phone_number'),
#                                            'email_id': regobjdata[i].get('username'),
#                                            'user_name': regobjdata[i].get('contact_person'),
#                                            'user_id': regobjdata[i].get('id'),
#                                            'profile_cover_photo': regobjdata[i].get('profile_cover_photo')
#                                            })
#                 return Response({'status': 200, 'message': 'Buyers List', 'data': buyer_list}, status=200)
#             else:
#                 return Response({'status': 204, 'message': 'Not Present'}, status=204)
#
#         elif users == 'internal_user':
#             internalobj = InternalVendor.objects.filter().values().order_by('internal_vendor_id')
#             if len(internalobj)>0:
#                 for i in range(len(internalobj)):
#                     regobj=SelfRegistration.objects.filter(username=internalobj[i].get('email_id')).values()
#                     if len(regobj)>0:
#                         internal_list.append({'company_code': internalobj[i].get('company_code'),
#                                               'company_name': internalobj[i].get('company_name'),
#                                               'phone_no': internalobj[i].get('phone_number'),
#                                               'email_id':internalobj[i].get('email_id'),
#                                               'user_name': regobj[0].get('contact_person'),
#                                               'user_id': regobj[0].get('id'),
#                                               'profile_cover_photo': regobj[0].get('profile_cover_photo')
#                                                   })
#                     else:
#                         internal_list.append({'company_code': internalobj[i].get('company_code'),
#                                               'company_name': internalobj[i].get('company_name'),
#                                               'phone_no': "",
#                                               'email_id': "",
#                                               'user_name':"",
#                                               'user_id': "",
#                                               'profile_cover_photo': ""
#                                               })
#
#                 return Response({'status': 200, 'message': 'Internal Users List', 'data': internal_list},
#                                 status=200)
#             else:
#                 return Response({'status': 204, 'message': 'Not Present'}, status=204)
#         elif users=='trail_user':
#             trailobj=TrailVendors.objects.filter().values().order_by('id')
#             if len(trailobj)>0:
#                 for i in range(0,len(trailobj)):
#                     basicobj = BasicCompanyDetails.objects.filter(
#                         company_code=trailobj[i].get('company_code_id')).values()
#                     if len(basicobj) > 0:
#                         regobj=SelfRegistration.objects.filter(id=basicobj[0].get('updated_by_id')).values()
#                         if len(regobj)>0:
#                                 trail_list.append({'company_code': basicobj[0].get('company_code'),
#                                                       'company_name': basicobj[0].get('company_name'),
#                                                       'phone_no': regobj[0].get('phone_number'),
#                                                       'email_id': regobj[0].get('username'),
#                                                       'user_name':regobj[0].get('contact_person'),
#                                                       'user_id': regobj[0].get('id'),
#                                                       'profile_cover_photo': regobj[0].get('profile_cover_photo')
#                                                       })
#                         else:
#                             trail_list.append({'company_code': basicobj[0].get('company_code'),
#                                                'company_name': basicobj[0].get('company_name'),
#                                                'phone_no': "",
#                                                'email_id': "",
#                                                'user_name': "",
#                                                'user_id': "",
#                                                'profile_cover_photo': "",
#                                                })
#                 return Response({'status': 200, 'message': 'Trail Users List', 'data': trail_list},
#                                 status=200)
#             else:
#                 return Response({'status': 204, 'message': 'Not Present'}, status=204)
#         elif users=='business_network':
#             businessacceptobj = BusinessRequest.objects.filter(send_status='Accept').values().order_by('id')
#             if len(businessacceptobj) > 0:
#                 for i in range(0, len(businessacceptobj)):
#                     regobj=SelfRegistration.objects.filter(id=businessacceptobj[i].get('updated_by_id')).values().order_by('id')
#                     if regobj:
#                         basicobj = BasicCompanyDetails.objects.filter(
#                             updated_by_id=regobj[0].get('id')).values()
#                         if basicobj:
#                             business_network.append({'company_code': basicobj[0].get('company_code'),
#                                                       'company_name': basicobj[0].get('company_name'),
#                                                       'phone_no': regobj[0].get('phone_number'),
#                                                       'email_id': regobj[0].get('username'),
#                                                       'user_name':regobj[0].get('contact_person'),
#                                                       'user_id': regobj[0].get('id'),
#                                                       'profile_cover_photo': regobj[0].get('profile_cover_photo')})
#                         else:
#                             business_network.append({'company_code': "",
#                                                      'company_name': "",
#                                                      'phone_no': regobj[0].get('phone_number'),
#                                                      'email_id': regobj[0].get('username'),
#                                                      'user_name': regobj[0].get('contact_person'),
#                                                      'user_id': regobj[0].get('id'),
#                                                      'profile_cover_photo': regobj[0].get('profile_cover_photo')})
#
#                 return Response({'status': 200, 'message': 'Business Network Users List', 'data': business_network},
#                                 status=200)
#             else:
#                 return Response({'status': 204, 'message': 'Not Present'}, status=204)
#         else:
#             return Response({'status': 202, 'message': 'Users Name is not correct or mis-spelled'}, status=202)
#
#
#     except Exception as e:
#         return Response({'status': 500, 'error': str(e)}, status=500)



# @api_view(['post'])
# @permission_classes((AllowAny,))
# def post_listings(request):
#     data = request.data
#     product_name = data['product_name']
#     prodarray = []
#     try:
#         biddingobj = LandingPageBidding.objects.filter(product_name=product_name).values()
#         if len(biddingobj) > 0:
#             for i in range(len(biddingobj)):
#                 print(biddingobj[i].get('publish_date'))
#                 productobj = VendorProduct_BasicDetails.objects.filter(
#                     vendor_product_id=biddingobj[i].get('vendor_product_pk')).values()
#                 userobj = SelfRegistration.objects.filter(id=productobj[0].get('updated_by_id')).values()
#                 cmpobj = BasicCompanyDetails.objects.filter(updated_by_id=productobj[0].get('updated_by_id')).values()
#                 locationobj = BillingAddress.objects.filter(updated_by_id=userobj[0].get('id')).values()
#                 if locationobj:
#                     prodarray.append({'product': biddingobj[i].get('product_name'),
#                                       'company_name': cmpobj[0].get('company_name'),
#                                       'contact_person': userobj[0].get('contact_person'),
#                                       'uom': productobj[i].get('uom'),
#                                       'date_time': productobj[i].get('created_on'),
#                                       'publish_date': biddingobj[i].get('publish_date'),
#                                       'deadline_date': biddingobj[i].get('deadline_date'),
#                                       'location': locationobj[0].get('bill_location'),
#                                       'product_id':biddingobj[i].get('id')
#                                       })
#                 else:
#                     prodarray.append({'product': biddingobj[i].get('product_name'),
#                                       'company_name': cmpobj[0].get('company_name'),
#                                       'contact_person': userobj[0].get('contact_person'),
#                                       'uom': productobj[i].get('uom'),
#                                       'date_time': productobj[i].get('created_on'),
#                                       'publish_date': biddingobj[i].get('publish_date'),
#                                       'deadline_date': biddingobj[i].get('deadline_date'),
#                                       'location': "",
#                                       'product_id': biddingobj[i].get('id')
#                                       })
#                 return Response({'status': 200, 'message': 'product List', 'data': prodarray},
#                                 status=status.HTTP_200_OK)
#         else:
#             return Response({'status': 204, 'message': 'product details are not exist'},
#                             status=status.HTTP_204_NO_CONTENT)
#     except Exception as e:
#         return Response({'status': 500, 'error': str(e)}, status=500)
#     # data=request.data
#     # product_name=data['product_name']
#     # product_list=[]
#     # try:
#     #     vendorobj=VendorProduct_BasicDetails.objects.filter(item_name=product_name).values()
#     #     if len(vendorobj)>0:
#     #         for i in range(0,len(vendorobj)):
#     #             regobj=SelfRegistration.objects.filter(id=vendorobj[i].get('updated_by_id')).values()
#     #             if regobj:
#     #                 basicobj=BasicCompanyDetails.objects.filter(updated_by_id=regobj[0].get('id')).values()
#     #                 product_list.append({'product_name':vendorobj[i].get('item_name'),
#     #                                      'company_name':basicobj[0].get('company_name'),
#     #                                      'company_code':basicobj[0].get('company_code'),
#     #                                      'username':regobj[0].get('conact_person'),
#     #                                      'email_id':regobj[0].get('username'),
#     #                                      'profile_cover_photo':regobj[0].get('profile_cover_photo'),
#     #                                      'user_id':regobj[0].get('id')
#     #                                      })
#     #         return Response({'status': 200, 'message': 'Listing Data','data':product_list},
#     #                         status=200)
#     #     else:
#     #         return Response({'status': 204, 'message': 'Product Details are not present'},
#     #                         status=204)
#     #
#     # except Exception as e:
#     #     return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def messages_user_list_receiver(request):
    data=request.data
    receiver=data['receiver']
    message_list=[]
    try:
        msgobj=Message.objects.filter(receiver_id=receiver).values().order_by('created_time')
        if len(msgobj)>0:
            for i in range(0,len(msgobj)):
                regobj1=SelfRegistration.objects.filter(id=msgobj[i].get('sender_id')).values()
                regobj2 = SelfRegistration.objects.filter(id=msgobj[i].get('receiver_id')).values()
                sender_addressobj=BillingAddress.objects.filter(updated_by_id=regobj1[0].get('id')).values()
                if sender_addressobj:
                    receiver_addressobj=BillingAddress.objects.filter(updated_by_id=regobj2[0].get('id')).values()
                    if receiver_addressobj:
                        message_list.append({'sender_name':msgobj[i].get('sender_name'),
                                             'receiver_name':msgobj[i].get('receiver_name'),
                                             'created_time': msgobj[i].get('created_time'),
                                             'sender_id': msgobj[i].get('sender_id'),
                                             'receiver_id': msgobj[i].get('receiver_id'),
                                             'sender_email_id':regobj1[0].get('username'),
                                             'receiver_email_id': regobj2[0].get('username'),
                                             'messages':msgobj[i].get('messages'),
                                             'sender_city':sender_addressobj[0].get('bill_city'),
                                             'sender_state': sender_addressobj[0].get('bill_state'),
                                             'sender_country': sender_addressobj[0].get('bill_country'),
                                             'receiver_city': receiver_addressobj[0].get('bill_city'),
                                             'receiver_state': receiver_addressobj[0].get('bill_state'),
                                             'receiver_country': receiver_addressobj[0].get('bill_country'),
                                             'company_logo_sender':regobj1[0].get('profile_cover_photo'),
                                             'company_logo_receiver': regobj2[0].get('profile_cover_photo'),
                                             'company_name_sender':msgobj[i].get('company_name_sender'),
                                             'company_name_receiver':msgobj[i].get('company_name_receiver'),
                                             'vendor_product_pk': msgobj[i].get('vendor_product_pk_id'),
                                             'source': msgobj[i].get('source'),
                                             'get_vendor': msgobj[i].get('get_vendor'),
                                             'rfq': msgobj[i].get('rfq'),
                                             'enquiry': msgobj[i].get('enquiry')

                                             })
                    else:
                        message_list.append({'sender_name': msgobj[i].get('sender_name'),
                                             'receiver_name': msgobj[i].get('receiver_name'),
                                             'created_time': msgobj[i].get('created_time'),
                                             'sender_id': msgobj[i].get('sender_id'),
                                             'receiver_id': msgobj[i].get('receiver_id'),
                                             'sender_email_id': regobj1[0].get('username'),
                                             'receiver_email_id': regobj2[0].get('username'),
                                             'messages': msgobj[i].get('messages'),
                                             'sender_city': sender_addressobj[0].get('bill_city'),
                                             'sender_state': sender_addressobj[0].get('bill_state'),
                                             'sender_country': sender_addressobj[0].get('bill_country'),
                                             'receiver_city': "",
                                             'receiver_state': "",
                                             'receiver_country': "",
                                             'company_logo_sender': regobj1[0].get('profile_cover_photo'),
                                             'company_logo_receiver': regobj2[0].get('profile_cover_photo'),
                                             'company_name_sender': msgobj[i].get('company_name_sender'),
                                             'company_name_receiver': msgobj[i].get('company_name_receiver'),
                                             'vendor_product_pk': msgobj[i].get('vendor_product_pk_id'),
                                             'source': msgobj[i].get('source'),
                                             'get_vendor': msgobj[i].get('get_vendor'),
                                             'rfq': msgobj[i].get('rfq'),
                                             'enquiry': msgobj[i].get('enquiry')

                                             })
            return Response({'status':200,'message':'Receiver Users List','data':message_list},status=200)
        else:
            return Response({'status':204,'message':'Users Not Present','data':msgobj},status=200)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def internal_external_trail_buyers_users_list(request):
    users=request.data['users']
    user_id=request.data['user_id']
    external_list=[]
    buyer_list=[]
    internal_list=[]
    trail_list=[]
    business_network=[]
    internalarray=[]
    internalbuyerarray=[]
    try:
        if users=='external_user':
            regobjdata = SelfRegistration.objects.filter(Q(user_type='Vendor') | Q(user_type='Both'),
                                                         admin_approve='Approved').values().order_by('id')
            if len(regobjdata)>0:
                internalobj = InternalVendor.objects.filter(updated_by_id=user_id).values()
                for i in range(0, len(internalobj)):
                    internalarray.append(internalobj[i].get('company_code'))
                internalbuyer = InternalBuyer.objects.filter(updated_by_id=user_id).values()
                for i in range(0, len(internalbuyer)):
                    internalbuyerarray.append(internalbuyer[i].get('company_code'))
                for i in range(0, len(regobjdata)):
                    basicobj = BasicCompanyDetails.objects.get(updated_by_id=regobjdata[i].get('id'))
                    if basicobj:
                        billobj=BillingAddress.objects.filter(updated_by_id=basicobj.updated_by_id).values()
                        if billobj:
                            if basicobj.company_code not in internalarray or basicobj.company_code not in internalbuyerarray:
                                external_list.append({'company_code': basicobj.company_code,
                                                      'company_name': basicobj.company_name,
                                                      'phone_no': regobjdata[i].get('phone_number'),
                                                      'email_id': regobjdata[i].get('username'),
                                                      'user_name':regobjdata[i].get('contact_person'),
                                                      'user_id':regobjdata[i].get('id'),
                                                      'profile_cover_photo':regobjdata[i].get('profile_cover_photo'),
                                                      'bill_city':billobj[0].get('bill_city'),
                                                      'bill_state': billobj[0].get('bill_state'),
                                                      'bill_country': billobj[0].get('bill_country'),
                                                      })
                            else:
                                external_list.append({'company_code': basicobj.company_code,
                                                      'company_name': basicobj.company_name,
                                                      'phone_no': regobjdata[i].get('phone_number'),
                                                      'email_id': regobjdata[i].get('username'),
                                                      'user_name': regobjdata[i].get('contact_person'),
                                                      'user_id': regobjdata[i].get('id'),
                                                      'profile_cover_photo': regobjdata[i].get('profile_cover_photo'),
                                                      'bill_city':"",
                                                      'bill_state': "",
                                                      'bill_country': "",
                                                      })

                return Response({'status':200,'message':'External Users List','data':external_list},status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)
        elif users=='buyer':
            internalbuyer = InternalBuyer.objects.filter(updated_by_id=user_id).values().order_by('internal_buyer_id')
            print(len(internalbuyer))
            if len(internalbuyer):
                for i in range(0,len(internalbuyer)):
                    regobj=SelfRegistration.objects.filter(username=internalbuyer[i].get('email_id')).values()
                    if regobj:
                        billobj = BillingAddress.objects.filter(updated_by_id=regobj[0].get('updated_by_id')).values()
                        if billobj:
                            buyer_list.append({'company_code': internalbuyer[i].get('company_code'),
                                               'company_name': internalbuyer[i].get('company_name'),
                                               'phone_no': internalbuyer[i].get('phone_number'),
                                               'email_id': internalbuyer[i].get('email_id'),
                                               'user_name': regobj[0].get('contact_person'),
                                               'user_id': regobj[0].get('id'),
                                               'profile_cover_photo': regobj[0].get('profile_cover_photo'),
                                               'bill_city': internalbuyer[i].get('city'),
                                               'bill_state': internalbuyer[i].get('state'),
                                               'bill_country': billobj[0].get('bill_country'),
                                               })
                        else:
                            buyer_list.append({'company_code': internalbuyer[i].get('company_code'),
                                               'company_name': internalbuyer[i].get('company_name'),
                                               'phone_no': internalbuyer[i].get('phone_number'),
                                               'email_id': internalbuyer[i].get('email_id'),
                                               'user_name': regobj[0].get('contact_person'),
                                               'user_id': regobj[0].get('id'),
                                               'profile_cover_photo': regobj[0].get('profile_cover_photo'),
                                               'bill_city': internalbuyer[i].get('city'),
                                               'bill_state': internalbuyer[i].get('state'),
                                               'bill_country': "",
                                               })

                return Response({'status': 200, 'message': 'Buyers List', 'data': buyer_list}, status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)

            # regobjdata = SelfRegistration.objects.filter(user_type='Buyer',admin_approve='Approved').values().order_by('id')
            # print(len(regobjdata))
            # if len(regobjdata) > 0:
            #     internalbuyer = InternalBuyer.objects.filter(updated_by_id=user_id).values()
            #     for i in range(0, len(internalbuyer)):
            #         internalbuyerarray.append(internalbuyer[i].get('company_code'))
            #     for i in range(0, len(regobjdata)):
            #         basicobj = BasicCompanyDetails.objects.get(updated_by_id=regobjdata[i].get('id'))
            #         if basicobj:
            #             billobj = BillingAddress.objects.filter(updated_by_id=basicobj.updated_by_id).values()
            #             if billobj:
            #                 if basicobj.company_code not in internalarray or basicobj.company_code not in internalbuyerarray:
            #                     buyer_list.append({'company_code': basicobj.company_code,
            #                                       'company_name': basicobj.company_name,
            #                                       'phone_no': regobjdata[i].get('phone_number'),
            #                                       'email_id': regobjdata[i].get('username'),
            #                                       'user_name': regobjdata[i].get('contact_person'),
            #                                       'user_id': regobjdata[i].get('id'),
            #                                       'profile_cover_photo': regobjdata[i].get('profile_cover_photo'),
            #                                        'bill_city': billobj[0].get('bill_city'),
            #                                        'bill_state': billobj[0].get('bill_state'),
            #                                        'bill_country': billobj[0].get('bill_country'),
            #                                         })
            #                 else:
            #                     buyer_list.append({'company_code': basicobj.company_code,
            #                                        'company_name': basicobj.company_name,
            #                                        'phone_no': regobjdata[i].get('phone_number'),
            #                                        'email_id': regobjdata[i].get('username'),
            #                                        'user_name': regobjdata[i].get('contact_person'),
            #                                        'user_id': regobjdata[i].get('id'),
            #                                        'profile_cover_photo': regobjdata[i].get('profile_cover_photo'),
            #                                        'bill_city': "",
            #                                        'bill_state': "",
            #                                        'bill_country': "",
            #                                        })
            #     return Response({'status': 200, 'message': 'Buyers List', 'data': buyer_list}, status=200)
            # else:
            #     return Response({'status': 204, 'message': 'Not Present'}, status=204)

        elif users == 'internal_user':
            internalobj = InternalVendor.objects.filter(updated_by_id=user_id).values().order_by('internal_vendor_id')
            if len(internalobj)>0:
                for i in range(len(internalobj)):
                    regobj=SelfRegistration.objects.filter(username=internalobj[i].get('email_id')).values()
                    if len(regobj)>0:
                        billobj=BillingAddress.objects.filter(updated_by_id=regobj[0].get('id')).values()
                        if billobj:
                            internal_list.append({'company_code': internalobj[i].get('company_code'),
                                                  'company_name': internalobj[i].get('company_name'),
                                                  'phone_no': internalobj[i].get('phone_number'),
                                                  'email_id':internalobj[i].get('email_id'),
                                                  'user_name': regobj[0].get('contact_person'),
                                                  'user_id': regobj[0].get('id'),
                                                  'profile_cover_photo': regobj[0].get('profile_cover_photo'),
                                                  'bill_city':billobj[0].get('bill_city'),
                                                  'bill_state': billobj[0].get('bill_state'),
                                                  'bill_country': billobj[0].get('bill_country'),
                                                      })
                        else:
                            internal_list.append({'company_code': internalobj[i].get('company_code'),
                                                  'company_name': internalobj[i].get('company_name'),
                                                   'phone_no': internalobj[i].get('phone_number'),
                                                  'email_id':internalobj[i].get('email_id'),
                                                  'user_name': regobj[0].get('contact_person'),
                                                  'user_id': regobj[0].get('id'),
                                                  'profile_cover_photo': regobj[0].get('profile_cover_photo'),
                                                  'bill_city': "",
                                                  'bill_state': "",
                                                  'bill_country':"",
                                                  })

                return Response({'status': 200, 'message': 'Internal Users List', 'data': internal_list},
                                status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)
        elif users=='trail_user':
            trailobj=TrailVendors.objects.filter(updated_by_id=user_id).values().order_by('id')
            if len(trailobj)>0:
                for i in range(0,len(trailobj)):
                    basicobj = BasicCompanyDetails.objects.filter(
                        company_code=trailobj[i].get('company_code_id')).values()
                    if len(basicobj) > 0:
                        regobj=SelfRegistration.objects.filter(id=basicobj[0].get('updated_by_id')).values()
                        if len(regobj)>0:
                            billobj=BillingAddress.objects.filter(updated_by_id=regobj[0].get('id')).values()
                            if billobj:
                                    trail_list.append({'company_code': basicobj[0].get('company_code'),
                                                          'company_name': basicobj[0].get('company_name'),
                                                          'phone_no': regobj[0].get('phone_number'),
                                                          'email_id': regobj[0].get('username'),
                                                          'user_name':regobj[0].get('contact_person'),
                                                          'user_id': regobj[0].get('id'),
                                                          'profile_cover_photo': regobj[0].get('profile_cover_photo'),
                                                           'bill_city': billobj[0].get('bill_city'),
                                                           'bill_state': billobj[0].get('bill_state'),
                                                           'bill_country': billobj[0].get('bill_country'),
                                                          })
                            else:
                                trail_list.append({'company_code': basicobj[0].get('company_code'),
                                                   'company_name': basicobj[0].get('company_name'),
                                                    'phone_no': regobj[0].get('phone_number'),
                                                    'email_id': regobj[0].get('username'),
                                                    'user_name':regobj[0].get('contact_person'),
                                                    'user_id': regobj[0].get('id'),
                                                    'profile_cover_photo': regobj[0].get('profile_cover_photo'),
                                                    'bill_city': "",
                                                    'bill_state': "",
                                                    'bill_country': "",
                                                   })
                return Response({'status': 200, 'message': 'Trail Users List', 'data': trail_list},
                                status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)
        elif users=='business_network':
            businessacceptobj = BusinessRequest.objects.filter(send_status='Accept',updated_by_id=user_id).values().order_by('id')
            if len(businessacceptobj) > 0:
                for i in range(0, len(businessacceptobj)):
                    regobj=SelfRegistration.objects.filter(id=businessacceptobj[i].get('updated_by_id')).values().order_by('id')
                    if regobj:
                        basicobj = BasicCompanyDetails.objects.filter(
                            updated_by_id=regobj[0].get('id')).values()
                        if basicobj:
                            business_network.append({'company_code': basicobj[0].get('company_code'),
                                                      'company_name': basicobj[0].get('company_name'),
                                                      'phone_no': regobj[0].get('phone_number'),
                                                      'email_id': regobj[0].get('username'),
                                                      'user_name':regobj[0].get('contact_person'),
                                                      'user_id': regobj[0].get('id'),
                                                      'profile_cover_photo': regobj[0].get('profile_cover_photo')})
                        else:
                            business_network.append({'company_code': "",
                                                     'company_name': "",
                                                     'phone_no': regobj[0].get('phone_number'),
                                                     'email_id': regobj[0].get('username'),
                                                     'user_name': regobj[0].get('contact_person'),
                                                     'user_id': regobj[0].get('id'),
                                                     'profile_cover_photo': regobj[0].get('profile_cover_photo')})

                return Response({'status': 200, 'message': 'Business Network Users List', 'data': business_network},
                                status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)
        else:
            return Response({'status': 202, 'message': 'Users Name is not correct or mis-spelled'}, status=202)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def post_listings(request):
    data = request.data
    sub_cat=data['sub_cat']
    prodarray = []
    try:
        subcatproobj=VendorProduct_BasicDetails.objects.filter(sub_category=sub_cat).values()
        print(len(subcatproobj))
        if len(subcatproobj)>0:
            for i in range(len(subcatproobj)):
                biddingobj = LandingPageBidding.objects.filter(product_name=subcatproobj[i].get('item_name')).values()
                # print(biddingobj)
                if len(biddingobj) > 0:
                    productobj = VendorProduct_BasicDetails.objects.filter(vendor_product_id=biddingobj[0].get('vendor_product_pk')).values()
                    userobj = SelfRegistration.objects.filter(id=productobj[0].get('updated_by_id')).values()
                    cmpobj = BasicCompanyDetails.objects.filter(updated_by_id=productobj[0].get('updated_by_id')).values()
                    locationobj = BillingAddress.objects.filter(updated_by_id=userobj[0].get('id')).values()
                    if locationobj:
                        prodarray.append({'product': biddingobj[0].get('product_name'),
                                          'company_name': cmpobj[0].get('company_name'),
                                          'company_code':cmpobj[0].get('company_code'),
                                          'contact_person': userobj[0].get('contact_person'),
                                          'uom': productobj[0].get('uom'),
                                          'date_time': productobj[0].get('created_on'),
                                          'publish_date': biddingobj[0].get('publish_date'),
                                          'deadline_date': biddingobj[0].get('deadline_date'),
                                          'location': locationobj[0].get('bill_location'),
                                          'landing_page_pk': biddingobj[0].get('id'),
                                          'userid':userobj[0].get('id'),
                                          'vendor_product_pk':productobj[0].get('vendor_product_id'),
                                          'email_id':userobj[0].get('username')
                                          })
                    else:
                        prodarray.append({'product': biddingobj[0].get('product_name'),
                                          'company_name': cmpobj[0].get('company_name'),
                                          'company_code': cmpobj[0].get('company_code'),
                                          'contact_person': userobj[0].get('contact_person'),
                                          'uom': productobj[0].get('uom'),
                                          'date_time': productobj[0].get('created_on'),
                                          'publish_date': biddingobj[0].get('publish_date'),
                                          'deadline_date': biddingobj[0].get('deadline_date'),
                                          'location': "",
                                          'landing_page_pk': biddingobj[0].get('id'),
                                          'userid': userobj[0].get('id'),
                                          'vendor_product_pk': productobj[0].get('vendor_product_id'),
                                          'email_id': userobj[0].get('username')
                                          })
            return Response({'status': 200, 'message': 'product List', 'data': prodarray},
                                        status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'product details are not exist'},
                                    status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def get_buyer_requirements_for_same_subcategories(request):
    data=request.data
    vendor_pk=data['vendor_pk']
    try:
        buyerrequirementobj=BuyerProduct_Requirements.objects.filter(vendor_product_basic_pk__in=vendor_pk).values()
        if len(buyerrequirementobj)>0:
            return Response({'status': 200, 'message': 'Buyer Product Requirement List' ,'data':buyerrequirementobj},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'Not Present'},
                            status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def source_listings(request):
    data = request.data
    user_id = data['user_id']
    prodarray = []
    try:
        subcatproobj = SourcePublish.objects.filter(updated_by_id=user_id).values()
        print(len(subcatproobj))
        if len(subcatproobj) > 0:
            for i in range(len(subcatproobj)):
                sourceobj = SourceList_CreateItems.objects.filter(item_name=subcatproobj[i].get('source_item_name')).values()
                userobj = SelfRegistration.objects.filter(id=sourceobj[0].get('updated_by_id')).values()
                cmpobj = BasicCompanyDetails.objects.filter(updated_by_id=sourceobj[0].get('updated_by_id')).values()
                locationobj = BillingAddress.objects.filter(updated_by_id=userobj[0].get('id')).values()
                if locationobj:
                    prodarray.append({'product': subcatproobj[0].get('source_item_name'),
                                      'source_item_type': subcatproobj[0].get('source_item_type'),
                                      'source_quantity': subcatproobj[0].get('source_quantity'),
                                      'source_item_description': subcatproobj[0].get('source_item_description'),
                                      'company_name': cmpobj[0].get('company_name'),
                                      'company_code':cmpobj[0].get('company_code'),
                                      'contact_person': userobj[0].get('contact_person'),
                                      'source_uom': subcatproobj[0].get('source_uom'),
                                      'date_time': subcatproobj[0].get('created_on'),
                                      'publish_date': sourceobj[0].get('publish_date'),
                                      'deadline_date': sourceobj[0].get('deadline_date'),
                                      'location': locationobj[0].get('bill_location'),
                                      'userid':userobj[0].get('id'),
                                      'email_id':userobj[0].get('username')
                                      })
                # else:
                #     prodarray.append({'product': biddingobj[0].get('product_name'),
                #                       'source_item_type': subcatproobj[0].get('source_item_type'),
                #                       'source_quantity': subcatproobj[0].get('source_quantity'),
                #                       'source_item_description': subcatproobj[0].get('source_item_description'),
                #                       'company_name': cmpobj[0].get('company_name'),
                #                       'company_code': cmpobj[0].get('company_code'),
                #                       'contact_person': userobj[0].get('contact_person'),
                #                       'uom': productobj[0].get('uom'),
                #                       'date_time': productobj[0].get('created_on'),
                #                       'publish_date': biddingobj[0].get('publish_date'),
                #                       'deadline_date': biddingobj[0].get('deadline_date'),
                #                       'location': "",
                #                       'landing_page_pk': biddingobj[0].get('id'),
                #                       'userid': userobj[0].get('id'),
                #                       'vendor_product_pk': productobj[0].get('vendor_product_id'),
                #                       'email_id': userobj[0].get('username')
                #                       })
            return Response({'status': 200, 'message': 'source List', 'data': prodarray},
                                    status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'source details are not exist'},
                                    status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
@permission_classes((AllowAny,))
def source_listings_for_invite_vendors(request):
    data = request.data
    userid=data['userid']
    prodarray = []
    try:
        sourcepublishobj = SourcePublish.objects.filter(source_user_id=userid).values()
        if len(sourcepublishobj) > 0:
            for i in range(0, len(sourcepublishobj)):
                sourceobj = SourceList_CreateItems.objects.filter(id=sourcepublishobj[i].get('source_id'),
                                                                  get_vendors='False').values()
                if sourceobj:
                    userobj = SelfRegistration.objects.filter(id=sourcepublishobj[i].get('updated_by_id')).values()
                    if userobj:
                        cmpobj = BasicCompanyDetails.objects.filter(updated_by_id=userobj[0].get('id')).values()
                        if cmpobj:
                            locationobj = BillingAddress.objects.filter(
                                updated_by_id=cmpobj[0].get('updated_by_id')).values()
                            if locationobj:
                                prodarray.append({'source_id': sourcepublishobj[i].get('source_id'),
                                                  'source_item_type': sourceobj[0].get('item_type'),
                                                  'source_code': sourceobj[0].get('source_code'),
                                                  'source': sourceobj[0].get('source'),
                                                  'item_name': sourceobj[0].get('item_name'),
                                                  'item_code': sourceobj[0].get('item_code'),
                                                  'item_description': sourceobj[0].get('item_description'),
                                                  'uom': sourceobj[0].get('uom'),
                                                  'department': sourceobj[0].get('department'),
                                                  'quantity': sourceobj[0].get('quantity'),
                                                  'deadline_date': sourceobj[0].get('deadline_date'),
                                                  'publish_date': sourceobj[0].get('publish_date'),
                                                  'source_required_city': sourceobj[0].get('source_required_city'),
                                                  'source_vendors': sourceobj[0].get('source_vendors'),
                                                  'updated_by': sourcepublishobj[i].get('updated_by_id'),
                                                  'created_by': sourcepublishobj[i].get('created_by'),
                                                  'admins': sourceobj[0].get('admins_id'),
                                                  'buyer_user_id': sourcepublishobj[i].get('source_user_id'),
                                                  'publish_pk': sourcepublishobj[i].get('id'),
                                                  'unit_rate': sourcepublishobj[i].get('source_unit_rate'),
                                                  'tax': sourcepublishobj[i].get('source_tax'),
                                                  'discount': sourcepublishobj[i].get('source_discount'),
                                                  'total_amount': sourcepublishobj[i].get('source_total_amount'),
                                                  'maincore': sourceobj[0].get('maincore'),
                                                  'category': sourceobj[0].get('category'),
                                                  'company_code': cmpobj[0].get('company_code'),
                                                  'company_name': cmpobj[0].get('company_name'),
                                                  'email_id': userobj[0].get('username'),
                                                  'user_name': userobj[0].get('contact_person'),
                                                  'bill_city': locationobj[0].get('bill_city'),
                                                  'get_vendors': sourceobj[0].get('get_vendors'),
                                                  })
                            else:
                                prodarray.append({'source_id': sourceobj[0].get('source_id'),
                                                  'source_item_type': sourceobj[0].get('item_type'),
                                                  'source_code': sourceobj[0].get('source_code'),
                                                  'source': sourceobj[0].get('source'),
                                                  'item_name': sourceobj[0].get('item_name'),
                                                  'item_code': sourceobj[0].get('item_code'),
                                                  'item_description': sourceobj[0].get('item_description'),
                                                  'uom': sourceobj[0].get('uom'),
                                                  'department': sourceobj[0].get('department'),
                                                  'quantity': sourceobj[0].get('quantity'),
                                                  'deadline_date': sourceobj[0].get('deadline_date'),
                                                  'publish_date': sourceobj[0].get('publish_date'),
                                                  'source_required_city': sourceobj[0].get('source_required_city'),
                                                  'source_vendors': sourceobj[0].get('source_vendors'),
                                                  'updated_by': sourcepublishobj[i].get('updated_by_id'),
                                                  'created_by': sourcepublishobj[i].get('created_by'),
                                                  'admins': sourceobj[0].get('admins_id'),
                                                  'buyer_user_id': sourcepublishobj[i].get('source_user_id'),
                                                  'publish_pk': sourcepublishobj[i].get('id'),
                                                  'unit_rate': sourcepublishobj[i].get('source_unit_rate'),
                                                  'tax': sourcepublishobj[i].get('source_tax'),
                                                  'discount': sourcepublishobj[i].get('source_discount'),
                                                  'total_amount': sourcepublishobj[i].get('source_total_amount'),
                                                  'maincore': sourceobj[0].get('maincore'),
                                                  'category': sourceobj[0].get('category'),
                                                  'company_code': cmpobj[0].get('company_code'),
                                                  'company_name': cmpobj[0].get('company_name'),
                                                  'email_id': userobj[0].get('username'),
                                                  'user_name': userobj[0].get('contact_person'),
                                                  'bill_city': locationobj[0].get('bill_city'),
                                                  'get_vendors': sourceobj[0].get('get_vendors')
                                                  })

            return Response({'status': 200, 'message': 'Get Vendors Source List', 'data': prodarray},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'source details are not exist'},
                            status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def get_buyer_data_to_show_to_invite_vendors(request):
    data = request.data
    vendor_user_id=data['vendor_user_id']
    code_list = []
    source_list=[]
    try:

        sourcepublishobj = SourcePublish.objects.filter(updated_by_id__in=vendor_user_id).values()
        print(len(sourcepublishobj),'ok')
        if sourcepublishobj:
            for i in range(0,len(sourcepublishobj)):
                code_list.append(sourcepublishobj[i].get('source_id'))
            sourceobj = SourceList_CreateItems.objects.filter(id__in=code_list).values()
            if len(sourceobj)>0:
                for i in range(0,len(sourceobj)):
                    source_list.append({'source_id': sourceobj[i].get('id'),
                                      'source_code': sourceobj[i].get('source_code'),
                                      'source': sourceobj[i].get('source'),
                                      'item_name': sourceobj[i].get('item_name'),
                                      'item_code': sourceobj[i].get('item_code'),
                                      'item_description': sourceobj[i].get('item_description'),
                                      'uom': sourceobj[i].get('uom'),
                                      'quantity': sourceobj[i].get('quantity'),
                                      'deadline_date': sourceobj[i].get('deadline_date'),
                                      'publish_date': sourceobj[i].get('publish_date'),
                                      'updated_by': sourceobj[i].get('updated_by_id'),
                                      'created_by': sourceobj[i].get('created_by')
                                            })
            else:
                source_list=[]



            return Response({'status': 200, 'message': 'Source Buyer Details List For invite vendors', 'data': source_list},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'source details are not exist'},
                            status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
@permission_classes((AllowAny,))
def source_listings_based_on_category_for_get_vendors(request):
    data = request.data
    userid=data['userid']
    code_list = []
    source_list=[]
    hierarchy_list=[]
    try:
        sourcepub1 = SourcePublish.objects.filter(source_user_id=userid).values()
        if len(sourcepub1) > 0:
            for i in range(0, len(sourcepub1)):
                code_list.append(sourcepub1[i].get('source_id'))
            sourceobj1 = SourceList_CreateItems.objects.filter(id__in=code_list,
                                                              get_vendors='True').values()
            if sourceobj1:
                industryobj=IndustrialHierarchy.objects.filter(category__icontains=sourceobj1[0].get('category')).values()
                for i in range(0,len(industryobj)):
                    hierarchy_list.append(industryobj[i].get('updated_by_id'))
                sourcepublishobj=SourcePublish.objects.filter(updated_by_id__in=hierarchy_list).values()
                for i in range(0,len(sourcepublishobj)):
                    sourceobj = SourceList_CreateItems.objects.filter(id__in=code_list,
                                                                      get_vendors='True').values()
                    if sourceobj:
                        userobj = SelfRegistration.objects.filter(
                            id=sourcepublishobj[i].get('updated_by_id')).values()
                        if userobj:
                            cmpobj = BasicCompanyDetails.objects.filter(updated_by_id=userobj[0].get('id')).values()
                            if cmpobj:
                                locationobj = BillingAddress.objects.filter(
                                    updated_by_id=cmpobj[0].get('updated_by_id')).values()
                                if locationobj:
                                    source_list.append({'source_id': sourcepublishobj[i].get('source_id'),
                                                        'source_item_type': sourceobj[0].get('item_type'),
                                                        'source_code': sourceobj[0].get('source_code'),
                                                        'source': sourceobj[0].get('source'),
                                                        'item_name': sourceobj[0].get('item_name'),
                                                        'item_code': sourceobj[0].get('item_code'),
                                                        'item_description': sourceobj[0].get('item_description'),
                                                        'uom': sourceobj[0].get('uom'),
                                                        'department': sourceobj[0].get('department'),
                                                        'quantity': sourceobj[0].get('quantity'),
                                                        'deadline_date': sourceobj[0].get('deadline_date'),
                                                        'publish_date': sourceobj[0].get('publish_date'),
                                                        'source_required_city': sourceobj[0].get(
                                                            'source_required_city'),
                                                        'source_vendors': sourceobj[0].get('source_vendors'),
                                                        'updated_by': sourcepublishobj[i].get('updated_by_id'),
                                                        'created_by': sourcepublishobj[i].get('created_by'),
                                                        'admins': sourceobj[0].get('admins_id'),
                                                        'buyer_user_id': sourcepublishobj[i].get('source_user_id'),
                                                        'publish_pk': sourcepublishobj[i].get('id'),
                                                        'unit_rate': sourcepublishobj[i].get('source_unit_rate'),
                                                        'tax': sourcepublishobj[i].get('source_tax'),
                                                        'discount': sourcepublishobj[i].get('source_discount'),
                                                        'total_amount': sourcepublishobj[i].get('source_total_amount'),
                                                        'maincore': sourceobj[0].get('maincore'),
                                                        'category': sourceobj[0].get('category'),
                                                        'company_code': cmpobj[0].get('company_code'),
                                                        'company_name': cmpobj[0].get('company_name'),
                                                        'email_id': userobj[0].get('username'),
                                                        'user_name': userobj[0].get('contact_person'),
                                                        'bill_city': locationobj[0].get('bill_city'),
                                                        'get_vendors': sourceobj[0].get('get_vendors')
                                                        })
                                else:
                                    source_list.append({'source_id': sourceobj[0].get('source_id'),
                                                        'source_item_type': sourceobj[0].get('item_type'),
                                                        'source_code': sourceobj[0].get('source_code'),
                                                        'source': sourceobj[0].get('source'),
                                                        'item_name': sourceobj[0].get('item_name'),
                                                        'item_code': sourceobj[0].get('item_code'),
                                                        'item_description': sourceobj[0].get('item_description'),
                                                        'uom': sourceobj[0].get('uom'),
                                                        'department': sourceobj[0].get('department'),
                                                        'quantity': sourceobj[0].get('quantity'),
                                                        'deadline_date': sourceobj[0].get('deadline_date'),
                                                        'publish_date': sourceobj[0].get('publish_date'),
                                                        'source_required_city': sourceobj[0].get(
                                                            'source_required_city'),
                                                        'source_vendors': sourceobj[0].get('source_vendors'),
                                                        'updated_by': sourcepublishobj[i].get('updated_by_id'),
                                                        'created_by': sourcepublishobj[i].get('created_by'),
                                                        'admins': sourceobj[0].get('admins_id'),
                                                        'buyer_user_id': sourcepublishobj[i].get('source_user_id'),
                                                        'publish_pk': sourcepublishobj[i].get('id'),
                                                        'unit_rate': sourcepublishobj[i].get('source_unit_rate'),
                                                        'tax': sourcepublishobj[i].get('source_tax'),
                                                        'discount': sourcepublishobj[i].get('source_discount'),
                                                        'total_amount': sourcepublishobj[i].get('source_total_amount'),
                                                        'maincore': sourceobj[0].get('maincore'),
                                                        'category': sourceobj[0].get('category'),
                                                        'company_code': cmpobj[0].get('company_code'),
                                                        'company_name': cmpobj[0].get('company_name'),
                                                        'email_id': userobj[0].get('username'),
                                                        'user_name': userobj[0].get('contact_person'),
                                                        'bill_city': "",
                                                        'get_vendors': sourceobj[0].get('get_vendors')
                                                        })


            return Response({'status': 200, 'message': 'Source Buyer Details List For get vendors', 'data': source_list},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'source details are not exist'},
                            status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes((AllowAny,))
def buyer_bidding_rfq(request):
    data = request.data
    user_id = data['user_id']
    prodarray = []
    try:
        biddingobj = BuyerProductBidding.objects.filter(updated_by_id=user_id,get_vendors='False').values()
        print(len(biddingobj))
        if len(biddingobj) > 0:
            for i in range(len(biddingobj)):
                userobj = SelfRegistration.objects.filter(id=biddingobj[i].get('updated_by_id')).values()
                buyproobj = BiddingBuyerProductDetails.objects.filter(updated_by=biddingobj[i].get('updated_by_id')).values()
                cmpobj = BasicCompanyDetails.objects.filter(updated_by_id=biddingobj[i].get('updated_by_id')).values()
                locationobj = BillingAddress.objects.filter(updated_by_id=biddingobj[i].get('updated_by_id')).values()
                if locationobj:
                    prodarray.append({'buyer_item_name': buyproobj[0].get('buyer_item_name'),
                                      'buyer_item_type': buyproobj[0].get('buyer_item_type'),
                                      'buyer_quantity': buyproobj[0].get('buyer_quantity'),
                                      'buyer_item_description': buyproobj[0].get('buyer_item_description'),
                                      'company_name': cmpobj[0].get('company_name'),
                                      'company_code':cmpobj[0].get('company_code'),
                                      'contact_name': biddingobj[0].get('contact_name'),
                                      'buyer_uom': buyproobj[0].get('buyer_uom'),
                                      'date_time': biddingobj[i].get('created_on'),
                                      'publish_date': biddingobj[i].get('product_publish_date'),
                                      'deadline_date': biddingobj[i].get('product_deadline_date'),
                                      'location': locationobj[0].get('bill_location'),
                                      'userid':userobj[0].get('id'),
                                      'email_id':userobj[0].get('username')
                                      })
                return Response({'status': 200, 'message': 'Bidding List', 'data': prodarray},
                    status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'Bidding details are not exist'},
                    status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['post'])
@permission_classes((AllowAny,))
def bidding_invite_vendor(request):
    data = request.data
    user_id = data['user_id']
    prodarray = []
    bidlist=[]
    try:
        biddingobj = BuyerProductBidding.objects.filter(updated_by_id=user_id,get_vendors='False').values()
        if biddingobj:
            for i in range(0,len(biddingobj)):
                bidlist.append(biddingobj[i].get('product_rfq_number'))

            selectobj=SelectVendorsForBiddingProduct.objects.filter(rfq_number__in=bidlist,updated_by_id=user_id).values()
            if len(selectobj) > 0:
                for i in range(len(selectobj)):
                    bidobj=BuyerProductBidding.objects.filter(updated_by_id=user_id,product_rfq_number=selectobj[i].get('rfq_number'),get_vendors='False').values()
                    if bidobj:
                        basicobj=BasicCompanyDetails.objects.filter(company_code=selectobj[i].get('vendor_code')).values()
                        if basicobj:
                            regobj=SelfRegistration.objects.filter(id=basicobj[0].get('updated_by_id')).values()
                            if regobj:
                                locationobj = BillingAddress.objects.filter(updated_by_id=regobj[0].get('id')).values()
                                if locationobj:
                                    prodarray.append({'company_name': basicobj[0].get('company_name'),
                                                      'company_code':basicobj[0].get('company_code'),
                                                      'contact_name': regobj[0].get('contact_name'),
                                                      'location': locationobj[0].get('bill_location'),
                                                      'userid':regobj[0].get('id'),
                                                      'email_id':regobj[0].get('username'),
                                                      'vendor_status': selectobj[i].get('vendor_status'),
                                                      'rfq_number': selectobj[i].get('rfq_number'),
                                                      'buyer_user_id':user_id,
                                                      'get_vendors': bidobj[0].get('get_vendors'),
                                                      'maincore': bidobj[0].get('maincore'),
                                                      'category': bidobj[0].get('category'),
                                                      'sub_category': bidobj[0].get('sub_category'),
                                                      })
                                else:
                                    prodarray.append({'company_name': basicobj[0].get('company_name'),
                                                      'company_code': basicobj[0].get('company_code'),
                                                      'contact_name': regobj[0].get('contact_name'),
                                                      'location': "",
                                                      'userid': regobj[0].get('id'),
                                                      'email_id': regobj[0].get('username'),
                                                      'vendor_status': selectobj[i].get('vendor_status'),
                                                      'rfq_number': selectobj[i].get('rfq_number'),
                                                      'buyer_user_id': user_id,
                                                      'get_vendors': bidobj[0].get('get_vendors'),
                                                      'maincore': bidobj[0].get('maincore'),
                                                      'category': bidobj[0].get('category'),
                                                      'sub_category': bidobj[0].get('sub_category'),
                                                      })

            return Response({'status': 200, 'message': 'Vendors List', 'data': prodarray},
                    status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'Bidding details are not exist'},
                    status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes((AllowAny,))
def bidding_get_vendor(request):
    data = request.data
    user_id = data['user_id']
    prodarray = []
    bidlist=[]
    industry=[]
    try:
        biddingobj = BuyerProductBidding.objects.filter(updated_by_id=user_id,get_vendors='True').values()
        if biddingobj:
            for i in range(0,len(biddingobj)):
                heirarchyobj=IndustrialHierarchy.objects.filter(category__icontains=biddingobj[i].get('category')).values()
                industry.append(heirarchyobj[0].get('updated_by_id'))
                basicobj=BasicCompanyDetails.objects.filter(updated_by_id=heirarchyobj[0].get('updated_by_id')).values()
                if basicobj:
                    bidobj = BuyerProductBidding.objects.filter(category__in=heirarchyobj[0].get('category')).values()
                    if bidobj:
                        regobj=SelfRegistration.objects.filter(id=basicobj[0].get('updated_by_id')).values()
                        if regobj:
                            locationobj = BillingAddress.objects.filter(updated_by_id=regobj[0].get('id')).values()
                            if locationobj:
                                prodarray.append({'company_name': basicobj[0].get('company_name'),
                                                  'company_code':basicobj[0].get('company_code'),
                                                  'contact_name': regobj[0].get('contact_name'),
                                                  'location': locationobj[0].get('bill_location'),
                                                  'userid':regobj[0].get('id'),
                                                  'email_id':regobj[0].get('username'),
                                                  'buyer_user_id':user_id,
                                                  'get_vendors':'True',
                                                  'maincore':bidobj[0].get('maincore'),
                                                  'category':bidobj[0].get('category'),
                                                  'subcategory':bidobj[0].get('subcategory')
                                                  })
                            else:
                                prodarray.append({'company_name': basicobj[0].get('company_name'),
                                                  'company_code': basicobj[0].get('company_code'),
                                                  'contact_name': regobj[0].get('contact_name'),
                                                  'location': "",
                                                  'userid': regobj[0].get('id'),
                                                  'email_id': regobj[0].get('username'),
                                                  'buyer_user_id': user_id,
                                                  'get_vendors':'True',
                                                   'maincore':bidobj[0].get('maincore'),
                                                  'category':bidobj[0].get('category'),
                                                  'subcategory':bidobj[0].get('subcategory')
                                                  })

            return Response({'status': 200, 'message': ' Get Vendors List', 'data': prodarray},
                    status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'Bidding details are not exist'},
                    status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def vendors_list_based_on_rfq_Code(request):
    data = request.data
    rfq_code = data['rfq_code']
    try:
        vendorobj = VendorProductBidding.objects.filter(vendor_product_rfq_number=rfq_code).values().order_by('vendor_product_bidding_id')
        if len(vendorobj)>0:
            return Response({'status': 201, 'message': 'OK','data':vendorobj}, status=201)
        else:
            return Response({'status': 204, 'message': 'Not Present','data':vendorobj}, status=204)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def buyer_data_based_on_vendor_code_and_vendor_rfq(request):
    data = request.data
    vendor_code = data['vendor_code']
    vendor_rfq=data['vendor_rfq']
    buyerarray = []
    try:
        vendorobj = VendorProductBidding.objects.filter(vendor_code__in=vendor_code,
                                                        vendor_product_rfq_number=vendor_rfq).values()
        if len(vendorobj) > 0:
            for i in range(0,len(vendorobj)):
                buyerobj = BuyerProductBidding.objects.filter(product_rfq_number=vendorobj[i].get('vendor_product_rfq_number')).values()
                if buyerobj:
                    userobj = SelfRegistration.objects.filter(id=buyerobj[0].get('updated_by_id')).values()
                    if userobj:
                        cmpobj = BasicCompanyDetails.objects.filter(updated_by_id=userobj[0].get('id')).values()
                        if cmpobj:
                            locationobj = BillingAddress.objects.filter(updated_by_id=cmpobj[0].get('updated_by_id')).values()
                            if locationobj:
                                buyerarray.append({'company_name': cmpobj[0].get('company_name'),
                                                   'company_code': cmpobj[0].get('company_code'),
                                                   'contact_name': userobj[0].get('contact_name'),
                                                   'product_publish_date': buyerobj[0].get('product_publish_date'),
                                                   'product_deadline_date': buyerobj[0].get('product_deadline_date'),
                                                   'location': locationobj[0].get('bill_location'),
                                                   'city':locationobj[0].get('bill_city'),
                                                   'userid': userobj[0].get('id'),
                                                   'email_id': userobj[0].get('username'),
                                                   'buyer_rfq_number':buyerobj[0].get('product_rfq_number'),
                                                   'buyer_user_id':buyerobj[0].get('updated_by_id')
                                                   })
                            else:
                                buyerarray.append({'company_name': cmpobj[0].get('company_name'),
                                                   'company_code': cmpobj[0].get('company_code'),
                                                   'contact_name': userobj[0].get('contact_name'),
                                                   'product_publish_date': buyerobj[0].get('product_publish_date'),
                                                   'product_deadline_date': buyerobj[0].get('product_deadline_date'),
                                                   'location':"",
                                                   'city':"",
                                                   'userid': userobj[0].get('id'),
                                                   'email_id': userobj[0].get('username'),
                                                   'buyer_rfq_number': buyerobj[0].get('product_rfq_number'),
                                                   'buyer_user_id': buyerobj[0].get('updated_by_id')
                                                   })

                return Response({'status': 200, 'message': 'Buyer Rfq List', 'data': buyerarray}, status=200)
        else:
            return Response({'status': 202, 'message': 'No Data Found', 'data': vendorobj}, status=202)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes((AllowAny,))
def vendors_details_to_show_buyer(request):
    data = request.data
    vendor_code = data['vendor_code']
    vendor_rfq=data['vendor_rfq']
    buyerarray = []
    quantity=0
    total_unit_price=0
    total_tax=0.00
    total_discount=0
    total_amount=0.0
    try:
        vendorobj = VendorProductBidding.objects.filter(vendor_code__in=vendor_code,
                                                        vendor_product_rfq_number=vendor_rfq).values()
        if len(vendorobj) > 0:
            for i in range(0,len(vendorobj)):
                vendorproductobj = VendorBiddingBuyerProductDetails.objects.filter(
                    vendor_rfq_number=vendorobj[i].get('vendor_product_rfq_number'),
                    vendor_code=vendorobj[i].get('vendor_code')).values()
                if vendorproductobj:
                    quantity = quantity + int(vendorproductobj[0].get('vendor_quantity'))
                    total_unit_price = total_unit_price + int(vendorproductobj[0].get('vendor_rate'))
                    val = vendorproductobj[0].get('vendor_tax')
                    taxval = val.split('%')
                    total_tax = total_tax + float(taxval[0])
                    total_discount = total_discount + int(vendorproductobj[0].get('vendor_discount'))
                    total_amount = total_amount + float(vendorproductobj[0].get('vendor_total_amount'))
                    userobj = SelfRegistration.objects.filter(id=vendorobj[i].get('updated_by_id')).values()
                    if userobj:
                        cmpobj = BasicCompanyDetails.objects.filter(updated_by_id=userobj[0].get('id')).values()
                        if cmpobj:
                            locationobj = BillingAddress.objects.filter(updated_by_id=cmpobj[0].get('updated_by_id')).values()
                            if locationobj:
                                buyerarray.append({'company_name': cmpobj[0].get('company_name'),
                                                   'company_code': cmpobj[0].get('company_code'),
                                                   'contact_name': userobj[0].get('contact_name'),
                                                   'product_publish_date': vendorobj[i].get('vendor_product_publish_date'),
                                                   'product_deadline_date': vendorobj[i].get('vendor_product_deadline_date'),
                                                   'location': locationobj[0].get('bill_location'),
                                                   'city':locationobj[0].get('bill_city'),
                                                   'userid': userobj[0].get('id'),
                                                   'email_id': userobj[0].get('username'),
                                                   'vendor_rfq_number':vendorobj[i].get('vendor_product_rfq_number'),
                                                   'vendor_rfq_title':vendorobj[i].get('vendor_product_rfq_title'),
                                                   'no_of_items':len(vendorproductobj),
                                                   'no_of_quantity':quantity,
                                                   'no_of_unit_price':total_unit_price,
                                                   'no_of_tax':total_tax,
                                                   'no_of_discount':total_discount,
                                                   'no_of_amount':total_amount

                                                   })
                            else:
                                buyerarray.append({'company_name': cmpobj[0].get('company_name'),
                                                   'company_code': cmpobj[0].get('company_code'),
                                                   'contact_name': userobj[0].get('contact_name'),
                                                   'product_publish_date': vendorobj[i].get(
                                                       'vendor_product_publish_date'),
                                                   'product_deadline_date': vendorobj[i].get(
                                                       'vendor_product_deadline_date'),
                                                   'location': locationobj[0].get('bill_location'),
                                                   'city': locationobj[0].get('bill_city'),
                                                   'userid': userobj[0].get('id'),
                                                   'email_id': userobj[0].get('username'),
                                                   'vendor_rfq_number': vendorobj[i].get('vendor_product_rfq_number'),
                                                   'vendor_rfq_title': vendorobj[i].get('vendor_product_rfq_title'),
                                                   'no_of_items': len(vendorproductobj),
                                                   'no_of_quantity': quantity,
                                                   'no_of_unit_price': total_unit_price,
                                                   'no_of_tax': total_tax,
                                                   'no_of_discount': total_discount,
                                                   'no_of_amount': total_amount

                                                   })



                return Response({'status': 200, 'message': 'Vendr Details List', 'data': buyerarray}, status=200)
        else:
            return Response({'status': 202, 'message': 'No Data Found', 'data': vendorobj}, status=202)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes((AllowAny,))
def get_all_message_list(request):
    key=request.data['key']
    try:
        if key=='vsinadmindb':
            msgobj=Message.objects.filter().values().order_by('id')
            if len(msgobj)>0:
                return Response({'status':200,'message':'Message List','data':msgobj},status=200)
            else:
                return Response({'status': 204, 'message': 'No Data Found'}, status=204)
        else:
            return Response({'status':401,'message':'UnAuthorized'},status=401)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['put'])
@permission_classes((AllowAny,))
def update_message_data(request):
    id=request.data['id']
    try:
        msgobj=Message.objects.filter(id=id).values()
        if len(msgobj)>0:
            msgval=Message.objects.get(id=msgobj[0].get('id'))
            if msgval.is_read==False:
                msgval.is_read=True
                msgval.save()
                return Response({'status':202,'message':'Updated','data':msgval.is_read},status=202)
            else:
                return Response({'status': 200, 'message': ' Already Updated'}, status=200)
        else:
            return Response({'status': 204, 'message': 'No Data Found'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)