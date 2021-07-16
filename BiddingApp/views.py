from datetime import date
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from MaterialApp.models import BuyerProductDetails
from RegistrationApp.models import BasicCompanyDetails
from .serializers import *

from .models import *

# Create your views here.
class BuyerProductBiddingView(viewsets.ModelViewSet):
    queryset = BuyerProductBidding.objects.all()
    serializer_class = BuyerProductBiddingSerializer
    permission_classes = [permissions.AllowAny]
    ordering_fields = ['product_bidding_id']
    ordering = ['product_bidding_id']

    def create(self, request, *args, **kwargs):
        created_by = request.data.get('created_by',None)
        updated_by = request.data.get('updated_by', None)
        product_rfq_type=request.data.get('product_rfq_type',None)
        product_publish_date=request.data.get('product_publish_date',None)
        product_deadline_date=request.data.get('product_deadline_date',None)
        product_delivery_date=request.data.get('product_delivery_date',None)
        product_department=request.data.get('product_department',None)
        product_rfq_currency = request.data.get('product_rfq_currency', None)
        product_rfq_category = request.data.get('product_rfq_category', None)
        product_bill_address=request.data.get('product_bill_address',None)
        product_ship_address=request.data.get('product_ship_address',None)
        product_rfq_title=request.data.get('product_rfq_title',None)
        rfqcodesettingsobj = RfqCodeSettings.objects.filter(updated_by=updated_by).order_by('-id').values()
        print(rfqcodesettingsobj)
        print(len(rfqcodesettingsobj))

        if len(rfqcodesettingsobj)>0:

            buyerbid = BuyerProductBidding.objects.filter(updated_by=updated_by).values()
            if len(buyerbid)==0:
                request.data['user_prefix'] = rfqcodesettingsobj[0].get('prefix')
                request.data['user_rfq_number'] =rfqcodesettingsobj[0].get('prefix')+str(int(rfqcodesettingsobj[0].get('numeric')))
                request.data['user_bidding_numeric'] = int(rfqcodesettingsobj[0].get('numeric'))+1
            else:
                buyerbid = BuyerProductBidding.objects.filter(updated_by=updated_by).order_by('-product_bidding_id').values()
                print(buyerbid)
                request.data['user_prefix'] = buyerbid[0].get('user_prefix')
                bidding_numeric =int(buyerbid[0].get('user_bidding_numeric'))+1
                user_rfq_number =buyerbid[0].get('user_prefix')+str(int(buyerbid[0].get('user_bidding_numeric')))
                request.data['user_rfq_number'] = user_rfq_number
                request.data['user_bidding_numeric'] = bidding_numeric


            return super().create(request, *args, **kwargs)
        else:
            return Response({'status':204,'message':'Rfq Code Settings Not Present,Please Create Rfq in Settings'},status=204)

    def get_queryset(self):
        buyerproductbiddingobj=BuyerProductBidding.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if buyerproductbiddingobj:
            return buyerproductbiddingobj
        raise ValidationError({'message':'Buyer Product Bidding details of particular user id is not exist','status':204})


class BiddingBuyerProductDetailsView(viewsets.ModelViewSet):
    queryset = BiddingBuyerProductDetails.objects.all()
    serializer_class = BiddingBuyerProductDetailsSerializer
    permission_classes = [permissions.AllowAny]
    ordering_fields = ['id']
    ordering = ['id']

    def create(self, request, *args, **kwargs):
        productdetails = request.data['productdetails']
        buyer_rfq_number = request.data.get('buyer_rfq_number', None)
        userid = request.data.get('userid', None)
        try:
            for i in range(0, len(productdetails)):
                BiddingBuyerProductDetails.objects.create(buyer_rfq_number=buyer_rfq_number,
                                                          buyer_item_code=productdetails[i].get('buyer_item_code'),
                                                          buyer_item_name=productdetails[i].get('buyer_item_name'),
                                                          buyer_item_description=productdetails[i].get(
                                                              'buyer_item_description'),
                                                          buyer_uom=productdetails[i].get('buyer_uom'),
                                                          buyer_category=productdetails[i].get('buyer_category'),
                                                          buyer_quantity=productdetails[i].get('buyer_quantity'),
                                                          buyer_document=productdetails[i].get('buyer_document'),
                                                          updated_by=SelfRegistration.objects.get(id=userid),
                                                          created_by=userid)

            return Response({'status': 200, 'message': 'Product Details Are Added'}, status=200)
        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)

    def get_queryset(self):
        buyerproductdetailsobj = BiddingBuyerProductDetails.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if buyerproductdetailsobj:
            return buyerproductdetailsobj
        raise ValidationError(
            {'message': 'Buyer Bidding Product details of particular user id is not exist', 'status': 204})

class RfqCodeSettingsView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = RfqCodeSettings.objects.all()
    serializer_class = RfqCodeSettingsSerializer
    ordering_fields = ['id']
    ordering = ['id']

    def create(self, request, *args, **kwargs):
        prefix = request.data.get('prefix',None)
        numeric = request.data.get('numeric',None)
        suffix = request.data.get('suffix',None)
        try:
            rfq_number=prefix+suffix+numeric
            request.data['rfq_number']=rfq_number
            return super().create(request, *args, **kwargs)

        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)

    def get_queryset(self):
        rfqnumberobj=RfqCodeSettings.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if rfqnumberobj:
            return rfqnumberobj
        raise ValidationError({'message':'Rfq Number details of particular user id is not exist','status':204})


@api_view(['post'])
@permission_classes((AllowAny,))
def get_buyer_product_based_on_userid_pk(request):
    data=request.data
    buyerproductid=data['buyerproductid']
    userid=data['userid']
    try:
        buyerproductobj=BuyerProductDetails.objects.filter(buyer_product_id__in=buyerproductid,updated_by=userid).values()
        if len(buyerproductobj)>0:
            return Response({'status':200,'message':'Buyer Product List','data':buyerproductobj},status=200)
        else:
            return Response({'status':204,'message':'Buyer Product Details Not Present'},status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)


@api_view(['put'])
@permission_classes((AllowAny,))
def updated_rfq_code_settings_and_rfq_number(request):
    data=request.data
    userid=data['userid']
    prefix=data['prefix']
    suffix=data['suffix']
    numeric=data['numeric']
    try:
        rfqcodesettingsobj=RfqCodeSettings.objects.filter(updated_by=userid).order_by('-id').values()
        if len(rfqcodesettingsobj)>0:
            rfqcodeobj=RfqCodeSettings.objects.get(updated_by=userid,id=rfqcodesettingsobj[0].get('id'))
            if rfqcodeobj.prefix !=prefix:
                rfqcodeobj.prefix=prefix
                rfqcodeobj.save()
            if rfqcodeobj.suffix!=suffix:
                rfqcodeobj.suffix=suffix
                rfqcodeobj.save()

            if rfqcodeobj.numeric!=numeric:
                rfqcodeobj.numeric=numeric
                rfqcodeobj.save()

                value=rfqcodeobj.prefix+rfqcodeobj.suffix+rfqcodeobj.numeric
                rfqcodeobj.rfq_number=value
                rfqcodeobj.save()

            rfqbid=BuyerProductBidding.objects.filter(updated_by_id=userid).order_by('-product_bidding_id').values()
            if len(rfqbid)>0:
                rfqval=BuyerProductBidding.objects.get(product_bidding_id=rfqbid[0].get('product_bidding_id'),updated_by_id=rfqbid[0].get('updated_by_id'))
                print(rfqval.product_bidding_id)
                if rfqval.user_rfq_number!=rfqcodeobj.rfq_number:
                    rfqval.user_rfq_number=rfqcodeobj.rfq_number
                    rfqval.save()
                if rfqval.user_bidding_numeric!=rfqcodeobj.numeric:
                    rfqval.user_bidding_numeric=int(rfqcodeobj.numeric)+1
                    rfqval.save()

                if rfqval.user_prefix !=rfqcodeobj.prefix:
                    rfqval.user_prefix=rfqcodeobj.prefix
                    rfqval.save()

                return Response({'status':202,'message':'Buyer Product Bidding and Rfq Code Settings Upadted'},status=202)

            else:
                return Response({'status': 200, 'message': 'Buyer Product Bidding Not Present'}, status=200)

        else:
            return Response({'status':204,'message':'Rfq Code Settigs data for this user id is not present'},status=204)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)

class RfqTermsDescriptionView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = RfqTermsDescription.objects.all()
    serializer_class = RfqTermsDescriptionSerializer
    ordering_fields = ['id']
    ordering = ['id']

    def create(self, request, *args, **kwargs):
        rfq_number = request.data['rfq_number']
        dictsqueries = request.data['dictsqueries']
        print(type(dictsqueries))
        product_biddings = request.data.get('product_biddings', None)
        updated_by = request.data.get('updated_by', None)
        try:
            for i in range(0,len(dictsqueries)):
                for keys in dictsqueries[i]:
                    RfqTermsDescription.objects.create(rfq_number=rfq_number,
                                                       terms=keys,
                                                       description=dictsqueries[i][keys],
                                                       product_biddings=BuyerProductBidding.objects.get(
                                                           product_bidding_id=product_biddings),
                                                       updated_by=SelfRegistration.objects.get(id=updated_by),
                                                       created_by=updated_by)


            return Response({'status': 201, 'message': 'Terms and Descriptions are created'}, status=201)
        except Exception as e:
            return Response({'status': 500, 'message': str(e)}, status=500)




class SelectVendorsForBiddingProductView(viewsets.ModelViewSet):
    queryset = SelectVendorsForBiddingProduct.objects.all()
    serializer_class = SelectVendorsForBiddingProductSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        userid = request.data.get('userid', None)
        rfq_number = request.data['rfq_number']
        vendor_code = request.data['vendor_code']
        vendorcodearray = []

        try:
            selectvendorobj = SelectVendorsForBiddingProduct.objects.filter(rfq_number=rfq_number).values()
            for i in range(0, len(selectvendorobj)):
                vcode = selectvendorobj[i].get('vendor_code')
                vendorcodearray.append(vcode)

            for i in range(0, len(vendor_code)):
                if vendor_code[i] not in vendorcodearray:
                    print(vendor_code[i])
                    SelectVendorsForBiddingProduct.objects.create(rfq_number=rfq_number,
                                                                  created_by=userid,
                                                                  updated_by=SelfRegistration.objects.get(id=userid),
                                                                  vendor_code=vendor_code[i]
                                                                  )
            return Response({'status':201,'message':'Select Vendor For Product Bidding is Created'},status=201)




        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def rfq_bid_list_summary_advance_search(request):
    data=request.data
    user_rfq_number=data['user_rfq_number']
    product_rfq_title=data['product_rfq_title']
    product_publish_date=data['product_publish_date']
    product_department=data['product_department']
    product_rfq_category=data['product_rfq_category']
    product_rfq_currency=data['product_rfq_currency']
    product_deadline_date=data['product_deadline_date']
    product_delivery_date=data['product_delivery_date']
    try:
        rfqbiddingproduct = BuyerProductBidding.objects.filter(updated_by=data['userid'],
                                                               user_rfq_number__icontains=user_rfq_number,
                                                               product_rfq_title__icontains=product_rfq_title,
                                                               product_publish_date__icontains=product_publish_date,
                                                               product_department__icontains=product_department,
                                                               product_rfq_category__icontains=product_rfq_category,
                                                               product_rfq_currency__icontains=product_rfq_currency,
                                                               product_deadline_date__icontains=product_deadline_date,
                                                               product_delivery_date__icontains=product_delivery_date).values('user_rfq_number','product_rfq_title','product_publish_date','product_department','product_rfq_category','product_rfq_currency','product_deadline_date','product_delivery_date','updated_by_id')

        return Response({'status': 200, 'message': 'Search Success','data':rfqbiddingproduct}, status=200)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def rfq_type_based_list(request):
    data=request.data
    userid=data['userid']
    product_rfq_type=data['product_rfq_type']
    try:
        rfqtypeobj=BuyerProductBidding.objects.filter(updated_by=userid).values().order_by('product_bidding_id')
        if len(rfqtypeobj)>0:
            if product_rfq_type == 'Product':
                rfqtypeproductobj= BuyerProductBidding.objects.filter(updated_by=userid, product_rfq_type=product_rfq_type).values().order_by('product_bidding_id')
                return Response({'status': 200, 'message': 'Rfq Type Product', 'data':rfqtypeproductobj}, status=200)
            elif product_rfq_type=='Service':
                rfqtypeserviceobj = BuyerProductBidding.objects.filter(updated_by=userid, product_rfq_type=product_rfq_type).values().order_by('product_bidding_id')
                return Response({'status': 200, 'message': 'Rfq Type Service', 'data': rfqtypeserviceobj}, status=200)

            else:
                return Response({'status': 204, 'error':'Not present or rfq_type is wrong','data':[]}, status=204)
        else:
            return Response({'status': 202, 'error': 'Data Not Present For this user id'}, status=202)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


class BiddingTermMasterSettingsView(viewsets.ModelViewSet):
    queryset = BiddingTermMasterSettings.objects.all()
    serializer_class = BiddingTermMasterSettingsSerializer
    permission_classes = [permissions.AllowAny]
    ordering_fields = ['id']
    ordering = ['id']


    def create(self, request, *args, **kwargs):
        term_masters=request.data.get('term_masters',None)
        userid=request.data.get('userid',None)
        try:
            for i in term_masters:
                print(i)
                termobjbid=BiddingTermMasterSettings.objects.create(term_masters=i,
                                                                    created_by=userid,
                                                                    updated_by=SelfRegistration.objects.get(id=userid))
            return Response({'status':201,'message':'Term Masters Bidding Created'},status=201)
        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)


    def get_queryset(self):
        biddingtermsmastersettings = BiddingTermMasterSettings.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if biddingtermsmastersettings:
            return biddingtermsmastersettings
        raise ValidationError({'message': 'Bidding  Term Master details of particular user id is not exist', 'status': 204})


#
# @api_view(['post'])
# @permission_classes((AllowAny,))
# def get_buyer_product_bidding_details(request):
#     data=request.data
#     value=data['value']
#     userid=data['userid']
#     rfqnumber=data['rfqnumber']
#     try:
#         if value=="Bidding_Buyer_Product":
#             bidproduct=BuyerProductBidding.objects.filter(updated_by=userid,user_rfq_number=rfqnumber).values().order_by('product_bidding_id')
#             if len(bidproduct)>0:
#                 return Response({'status':200,'message':"Buyer Product Bidding List Success",'data':bidproduct},status=200)
#             else:
#                 return Response({'status': 204, 'message': "Details are not present for this particular user and rfq"}, status=204)
#         if value=="Bidding_Buyer_Product_Details":
#             bidproductdetails=BiddingBuyerProductDetails.objects.filter(updated_by=userid,buyer_rfq_number=rfqnumber).values().order_by('id')
#             if len(bidproductdetails)>0:
#                 return Response({'status': 200, 'message': "Product Details of Buyer Bidding List Success", 'data': bidproductdetails},
#                                 status=200)
#             else:
#                 return Response({'status': 204, 'message': "Product Details are not presenefor this particular user and rfq",}, status=204)
#         if value=="Terms_Description_Rfq_Buyer":
#             bidterms=RfqTermsDescription.objects.filter(updated_by=userid,rfq_number=rfqnumber).values().order_by('id')
#             if len(bidterms)>0:
#                 return Response({'status': 200, 'message': "Terms and Description Producty Bidding",'data': bidterms},status=200)
#             else:
#                 return Response({'status': 204,'message': "terms and description not present"},status=204)
#
#     except Exception as e:
#         return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def get_buyer_product_bid_by_user_rfq(request):
    data=request.data
    rfqnumber=data['rfqnumber']
    try:
        bidproduct = BuyerProductBidding.objects.filter(user_rfq_number=rfqnumber).values().order_by(
            'product_bidding_id')
        if len(bidproduct) > 0:
            return Response({'status': 200, 'message': "Buyer Product Bidding List Success", 'data': bidproduct},
                            status=200)
        else:
            return Response({'status': 204, 'message': "Details are not present for this particular user and rfq"},
                            status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def get_buyer_product_details_by_user_rfq(request):
    data=request.data
    rfqnumber=data['rfqnumber']
    try:
        bidproductdetails = BiddingBuyerProductDetails.objects.filter(buyer_rfq_number=rfqnumber).values().order_by('id')
        if len(bidproductdetails) > 0:
            return Response({'status': 200, 'message': "Buyer Product Details List Success", 'data': bidproductdetails},
                            status=200)
        else:
            return Response({'status': 204, 'message': "Product Details are not present for this particular user and rfq"},
                            status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
@permission_classes((AllowAny,))
def get_buyer_bid_terms_by_user_rfq(request):
    data=request.data
    rfqnumber=data['rfqnumber']
    try:
        bidtermsdescription = RfqTermsDescription.objects.filter(rfq_number=rfqnumber).values().order_by('id')
        if len(bidtermsdescription) > 0:
            return Response({'status': 200, 'message': "Buyer terms and description", 'data': bidtermsdescription},
                            status=200)
        else:
            return Response({'status': 204, 'message': "Terms and Descripiton are not present for this particular user and rfq"},
                            status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def open_bid_list_buyer_pulish_list(request):
    data=request.data
    userid=data['userid']
    openbidarray=[]
    try:
        basicobj=BasicCompanyDetails.objects.get(updated_by=userid)
        print(basicobj)
        selectvendorsobj=SelectVendorsForBiddingProduct.objects.filter(vendor_code=basicobj.company_code,vendor_status='Pending').values()
        print(len(selectvendorsobj))
        if len(selectvendorsobj)>0:
            for i in range(0,len(selectvendorsobj)):
                print(selectvendorsobj[i].get('rfq_number'))
                biddingval=BuyerProductBidding.objects.get(user_rfq_number=selectvendorsobj[i].get('rfq_number'))
                basicobjval=BasicCompanyDetails.objects.get(updated_by_id=biddingval.updated_by_id)
                print(basicobjval)
                if biddingval.product_deadline_date < date.today():
                    pass
                else:
                    openbidarray.append({'vendor_code':basicobjval.company_code,
                                         'company_name':basicobjval.company_name,
                                         'product_rfq_type':biddingval.product_rfq_type,
                                         'product_rfq_title':biddingval.product_rfq_title,
                                         'product_rfq_status':biddingval.product_rfq_status,
                                         'product_publish_date':biddingval.product_publish_date,
                                         'product_deadline_date':biddingval.product_deadline_date,
                                         'product_delivery_date':biddingval.product_delivery_date,
                                         'product_rfq_currency':biddingval.product_rfq_currency,
                                         'product_rfq_category':biddingval.product_rfq_category,
                                         'product_department':biddingval.product_department
                                         })

            return Response({'status': 200, 'message': "Open Leads", 'data': openbidarray},status=200)
        else:
            return Response({'status': 202, 'message': 'Vendors are not selected for any bidding'}, status=202)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


class VendorProductBiddingView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = VendorProductBidding.objects.all()
    serializer_class = VendorProductBiddingSerializer
    ordering_fields = ['vendor_product_bidding_id']
    ordering = ['vendor_product_bidding_id']


class VendorBiddingBuyerProductDetailsView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = VendorBiddingBuyerProductDetails.objects.all()
    serializer_class = VendorBiddingBuyerProductDetailsSerializer
    ordering_fields = ['id']
    ordering = ['id']

    def create(self, request, *args, **kwargs):
        vendorproductdetails = request.data['vendorproductdetails']
        vendor_rfq_number = request.data.get('vendor_rfq_number', None)
        userid = request.data.get('userid', None)
        try:
            for i in range(0, len(vendorproductdetails)):
                VendorBiddingBuyerProductDetails.objects.create(vendor_rfq_number=vendor_rfq_number,
                                                          vendor_item_code=vendorproductdetails[i].get('vendor_item_code'),
                                                          vendor_item_name=vendorproductdetails[i].get('vendor_item_name'),
                                                          vendor_item_description=vendorproductdetails[i].get(
                                                              'vendor_item_description'),
                                                          vendor_uom=vendorproductdetails[i].get('vendor_uom'),
                                                          vendor_category=vendorproductdetails[i].get('vendor_category'),
                                                          vendor_quantity=vendorproductdetails[i].get('vendor_quantity'),
                                                          vendor_document=vendorproductdetails[i].get('vendor_document'),
                                                          updated_by=SelfRegistration.objects.get(id=userid),
                                                          created_by=userid)
            return Response({'status':201,'message':'Vendor Bidding Buyer Produt Details are Created'},status=201)
        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)

    def get_queryset(self):
        vendorproductdetailsobj = VendorBiddingBuyerProductDetails.objects.filter(
            updated_by=self.request.GET.get('updated_by'))
        if vendorproductdetailsobj:
            return vendorproductdetailsobj
        raise ValidationError(
            {'message': 'Vendor Bidding Product details of particular user id is not exist', 'status': 204})




class VendorRfqTermsDescriptionView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = VendorRfqTermsDescription.objects.all()
    serializer_class = VendorRfqTermsDescriptionSerializer
    ordering_fields = ['id']
    ordering = ['id']

    def create(self, request, *args, **kwargs):
        vendor_rfq_number = request.data['vendor_rfq_number']
        dictsqueries = request.data['dictsqueries']
        print(type(dictsqueries))
        vendor_product_biddings = request.data.get('vendor_product_biddings', None)
        updated_by = request.data.get('updated_by', None)
        try:
            for i in range(0, len(dictsqueries)):
                for keys in dictsqueries[i]:
                    VendorRfqTermsDescription.objects.create(vendor_rfq_number=vendor_rfq_number,
                                                       vendor_terms=keys,
                                                       vendor_description=dictsqueries[i][keys],
                                                       vendor_product_biddings=VendorProductBidding.objects.get(
                                                           vendor_product_bidding_id=vendor_product_biddings),
                                                       updated_by=SelfRegistration.objects.get(id=updated_by),
                                                       created_by=updated_by)

            return Response({'status': 201, 'message': 'Vendor Terms and Descriptions are created'}, status=201)
        except Exception as e:
            return Response({'status': 500, 'message': str(e)}, status=500)
