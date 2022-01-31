import math
from itertools import chain

from django.shortcuts import render
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
# Create your views here.
from LandingPageApp.models import CompanyReviewAndRating
from LandingPageApp.serializers import CompanyReviewSerializer
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
        subcategoryobj = SubCategoryMaster.objects.filter(category__in=categoryid).values()
        for i in range(0,len(subcategoryobj)):
            subcatnamearrayofarray.append({'sub_category_name':subcategoryobj[i].get('sub_category_name'),
                                           'sub_category_id':subcategoryobj[i].get('sub_category_id'),
                                           'sub_category_image': subcategoryobj[i].get('sub_category_image')
                                           })
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
                    maincorevalue = MaincoreMaster.objects.filter(maincore_name=productobj[i].
                                                                  get('core_sector')).values()
                    Categorydetails=CategoryMaster.objects.filter(maincore=maincorevalue[0].get('maincore_id')).values()
                    getarray.append({'name':productobj[i].get('item_name'),
                                     'product_code': productobj[i].get('item_code'),
                                     'maincore':productobj[i].get('core_sector'),
                                     'category':Categorydetails[0].get('category_id'),
                                     'subcategory':productobj[i].get('sub_category'),
                                     'itemtype':productobj[i].get('item_type')
                                     })
                return Response({'status': 200, 'message': 'Vendor Product List', 'data': getarray}, status=200)
            else:
                return Response({'status': 204, 'message': 'Vendor Product Lists are Not Present','data':getarray}, status=204)
        elif search_type == 'All':
            itemtypearr=['Product','Service']
            alldata = VendorProduct_BasicDetails.objects.filter(item_type__in=itemtypearr).values()
            if len(alldata) > 0:
                for i in range(0, len(alldata)):
                    Maaincoreid=MaincoreMaster.objects.filter(maincore_name=alldata[i].get('core_sector')).values()
                    Categoryid=CategoryMaster.objects.filter(category_name=alldata[i].get('category')).values()
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
                    Categorydetails = CategoryMaster.objects.filter(
                        maincore=maincorevalue[0].get('maincore_id')).values()
                    getarray.append({'name': productobj[i].get('item_name'),
                                     'product_code': productobj[i].get('item_code'),
                                     'maincore': productobj[i].get('core_sector'),
                                     'category': Categorydetails[0].get('category_id'),
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
            if len(basicobj)>0:
                for i in range(0,len(basicobj)):
                    print(basicobj[i].get('updated_by_id'))
                    regobj=SelfRegistration.objects.filter(id=basicobj[i].get('updated_by_id')).values()
                    print(len(regobj),regobj[0].get('user_type'))
                    billobj=BillingAddress.objects.filter(updated_by_id=basicobj[i].get('updated_by_id')).values()
                    print(len(billobj), billobj[0].get('bill_city'))
                    hierarchyobj=IndustrialHierarchy.objects.filter(updated_by_id=basicobj[i].get('updated_by_id')).values()
                    print(len(hierarchyobj),hierarchyobj[0].get('maincore'))
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
                    #
                    #
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
            for i in range(0,len(basicobj)):
                regobj=SelfRegistration.objects.filter(id=basicobj[i].get('updated_by_id')).values()
                billobj=BillingAddress.objects.filter(updated_by_id=basicobj[i].get('updated_by_id')).values()
                hierarchyobj=IndustrialHierarchy.objects.filter(updated_by_id=basicobj[i].get('updated_by_id')).values()
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
