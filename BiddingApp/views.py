import io
from datetime import date, datetime
from itertools import chain, groupby
from pprint import pprint

import requests
from django.http import HttpRequest
from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from MaterialApp.models import BuyerProductDetails, BuyerServiceDetails, BuyerMachinaryDetails
from RegistrationApp.models import BasicCompanyDetails, BillingAddress, ShippingAddress
from .serializers import *

from .models import *

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


# Create your views here.
class BuyerProductBiddingView(viewsets.ModelViewSet):
    queryset = BuyerProductBidding.objects.all()
    serializer_class = BuyerProductBiddingSerializer
    # permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        created_by = request.data.get('created_by', None)
        updated_by = request.data.get('updated_by', None)
        product_rfq_type = request.data.get('product_rfq_type', None)
        product_publish_date = request.data.get('product_publish_date', None)
        product_deadline_date = request.data.get('product_deadline_date', None)
        product_delivery_date = request.data.get('product_delivery_date', None)
        product_department = request.data.get('product_department', None)
        product_rfq_currency = request.data.get('product_rfq_currency', None)
        product_rfq_category = request.data.get('product_rfq_category', None)
        product_bill_address = request.data.get('product_bill_address', None)
        product_ship_address = request.data.get('product_ship_address', None)
        product_rfq_title = request.data.get('product_rfq_title', None)
        from_registration=request.data.get('from_registration',None)
        rfqcodesettingsobj = RfqCodeSettings.objects.filter(updated_by=updated_by).order_by('-id').values()
        print(rfqcodesettingsobj)
        print(len(rfqcodesettingsobj))

        if len(rfqcodesettingsobj) > 0:

            buyerbid = BuyerProductBidding.objects.filter(updated_by=updated_by).values()
            if len(buyerbid) == 0:
                request.data['user_prefix'] = rfqcodesettingsobj[0].get('prefix')
                request.data['user_rfq_number'] = rfqcodesettingsobj[0].get('prefix') + str(
                    int(rfqcodesettingsobj[0].get('numeric')))
                request.data['user_bidding_numeric'] = int(rfqcodesettingsobj[0].get('numeric')) + 1
            else:
                buyerbid = BuyerProductBidding.objects.filter(updated_by=updated_by).order_by(
                    '-product_bidding_id').values()
                print(buyerbid)
                request.data['user_prefix'] = buyerbid[0].get('user_prefix')
                bidding_numeric = int(buyerbid[0].get('user_bidding_numeric')) + 1
                user_rfq_number = buyerbid[0].get('user_prefix') + str(int(buyerbid[0].get('user_bidding_numeric')))
                request.data['user_rfq_number'] = user_rfq_number
                request.data['user_bidding_numeric'] = bidding_numeric

            return super().create(request, *args, **kwargs)
        else:
            return Response({'status': 204, 'message': 'Rfq Code Settings Not Present,Please Create Rfq in Settings'},
                            status=204)

    def get_queryset(self):
        buyerproductbiddingobj = BuyerProductBidding.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if buyerproductbiddingobj:
            return buyerproductbiddingobj
        raise ValidationError(
            {'message': 'Buyer Product Bidding details of particular user id is not exist', 'status': 204})


class BiddingBuyerProductDetailsView(viewsets.ModelViewSet):
    queryset = BiddingBuyerProductDetails.objects.all()
    serializer_class = BiddingBuyerProductDetailsSerializer
    # permission_classes = [permissions.AllowAny]
    ordering_fields = ['id']
    ordering = ['id']

    def create(self, request, *args, **kwargs):
        productdetails = request.data['productdetails']
        buyer_rfq_number = request.data.get('buyer_rfq_number', None)
        from_registration=request.data.get('from_registration',None)
        auto_rfq_number=request.data.get('auto_rfq_number',None)
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
                                                          buyer_item_type=productdetails[i].get('buyer_item_type'),
                                                          updated_by=SelfRegistration.objects.get(id=userid),
                                                          auto_rfq_number=auto_rfq_number,
                                                          from_registration=from_registration,
                                                          created_by=userid)

            return Response({'status': 200, 'message': 'Product Details Are Added'}, status=200)
        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)

    def get_queryset(self):
        buyerproductdetailsobj = BiddingBuyerProductDetails.objects.filter(
            updated_by=self.request.GET.get('updated_by')).order_by('id')
        if buyerproductdetailsobj:
            return buyerproductdetailsobj
        raise ValidationError(
            {'message': 'Buyer Bidding Product details of particular user id is not exist', 'status': 204})


class RfqCodeSettingsView(viewsets.ModelViewSet):
    # permission_classes = [permissions.AllowAny]
    queryset = RfqCodeSettings.objects.all()
    serializer_class = RfqCodeSettingsSerializer
    ordering_fields = ['id']
    ordering = ['id']

    def create(self, request, *args, **kwargs):
        prefix = request.data.get('prefix', None)
        numeric = request.data.get('numeric', None)
        suffix = request.data.get('suffix', None)
        try:
            rfq_number = prefix + suffix + numeric
            request.data['rfq_number'] = rfq_number
            return super().create(request, *args, **kwargs)

        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)

    def get_queryset(self):
        rfqnumberobj = RfqCodeSettings.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if rfqnumberobj:
            return rfqnumberobj
        raise ValidationError({'message': 'Rfq Number details of particular user id is not exist', 'status': 204})

@api_view(['put'])
# @permission_classes((AllowAny,))
def updated_rfq_code_settings_and_rfq_number(request):
    data = request.data
    userid = data['userid']
    prefix = data['prefix']
    suffix = data['suffix']
    numeric = data['numeric']
    try:
        rfqcodesettingsobj = RfqCodeSettings.objects.filter(updated_by=userid).order_by('-id').values()
        if len(rfqcodesettingsobj) > 0:
            rfqcodeobj = RfqCodeSettings.objects.get(updated_by=userid, id=rfqcodesettingsobj[0].get('id'))
            if rfqcodeobj.prefix != prefix:
                rfqcodeobj.prefix = prefix
                rfqcodeobj.save()
            if rfqcodeobj.suffix != suffix:
                rfqcodeobj.suffix = suffix
                rfqcodeobj.save()

            if rfqcodeobj.numeric != numeric:
                rfqcodeobj.numeric = numeric
                rfqcodeobj.save()

                value = rfqcodeobj.prefix + rfqcodeobj.suffix + rfqcodeobj.numeric
                rfqcodeobj.rfq_number = value
                rfqcodeobj.save()

            rfqbid = BuyerProductBidding.objects.filter(updated_by_id=userid).order_by('-product_bidding_id').values()
            if len(rfqbid) > 0:
                rfqval = BuyerProductBidding.objects.get(product_bidding_id=rfqbid[0].get('product_bidding_id'),
                                                         updated_by_id=rfqbid[0].get('updated_by_id'))
                print(rfqval.product_bidding_id)
                if rfqval.user_rfq_number != rfqcodeobj.rfq_number:
                    rfqval.user_rfq_number = rfqcodeobj.rfq_number
                    rfqval.save()
                if rfqval.user_bidding_numeric != rfqcodeobj.numeric:
                    rfqval.user_bidding_numeric = int(rfqcodeobj.numeric) + 1
                    rfqval.save()

                if rfqval.user_prefix != rfqcodeobj.prefix:
                    rfqval.user_prefix = rfqcodeobj.prefix
                    rfqval.save()

                return Response({'status': 202, 'message': 'Buyer Product Bidding and Rfq Code Settings Upadted'},
                                status=202)

            else:
                return Response({'status': 200, 'message': 'Buyer Product Bidding Not Present'}, status=200)

        else:
            return Response({'status': 204, 'message': 'Rfq Code Settigs data for this user id is not present'},
                            status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


class RfqTermsDescriptionView(viewsets.ModelViewSet):
    # permission_classes = [permissions.AllowAny]
    queryset = RfqTermsDescription.objects.all()
    serializer_class = RfqTermsDescriptionSerializer
    ordering_fields = ['id']
    ordering = ['id']

    def create(self, request, *args, **kwargs):
        rfq_number = request.data['rfq_number']
        dictsqueries = request.data['dictsqueries']
        print(type(dictsqueries))
        product_biddings = request.data.get('product_biddings', None)
        from_registration=request.data.get('from_registration',None)
        auto_rfq_number=request.data.get('auto_rfq_number',None)
        rfq_type=request.data.get('rfq_type',None)
        updated_by = request.data.get('updated_by', None)
        try:
            for i in range(0, len(dictsqueries)):
                for keys in dictsqueries[i]:
                    RfqTermsDescription.objects.create(rfq_number=rfq_number,
                                                       terms=keys,
                                                       description=dictsqueries[i][keys],
                                                       product_biddings=BuyerProductBidding.objects.get(
                                                           product_bidding_id=product_biddings),
                                                       updated_by=SelfRegistration.objects.get(id=updated_by),
                                                       rfq_type=rfq_type,
                                                       auto_rfq_number=auto_rfq_number,
                                                       from_registration=from_registration,
                                                       created_by=updated_by)

            return Response({'status': 201, 'message': 'Terms and Descriptions are created'}, status=201)
        except Exception as e:
            return Response({'status': 500, 'message': str(e)}, status=500)


class SelectVendorsForBiddingProductView(viewsets.ModelViewSet):
    queryset = SelectVendorsForBiddingProduct.objects.all()
    serializer_class = SelectVendorsForBiddingProductSerializer
    # permission_classes = [permissions.AllowAny]
    parser = [MultiPartParser]

    def create(self, request, *args, **kwargs):
        userid = request.data.get('userid', None)
        rfq_number = request.data.get('rfq_number',None)
        auto_rfq_number=request.data.get('auto_rfq_number',None)
        vendor_code = request.data.get('vendor_code',None)
        rfq_type=request.data.get('rfq_type',None)
        # from_registration=request.data.get('from_registration',None)
        vendorcodearray = []

        try:
            print("rfq--",rfq_number)
            selectvendorobj = SelectVendorsForBiddingProduct.objects.filter(rfq_number=rfq_number).values()
            if len(selectvendorobj)==0:
            # print('ok')
            # for i in range(0, len(selectvendorobj)):
            #     vcode = selectvendorobj[i].get('vendor_code')
            #     vendorcodearray.append(vcode)
                totalquantity=0
                bidcreater=BasicCompanyDetails.objects.filter(updated_by=userid).values()
                baddress = BillingAddress.objects.filter(updated_by=userid).values().order_by('id')
                saddress = ShippingAddress.objects.filter(updated_by=userid).values().order_by('id')

                for i in range(0, len(vendor_code)):
                        print(vendor_code[i])
                        Basicobj=BasicCompanyDetails.objects.filter(company_code=vendor_code[i]).values()
                        if Basicobj:
                            print(Basicobj[0].get('updated_by_id'))
                            Regobj=SelfRegistration.objects.get(id=Basicobj[0].get('updated_by_id'))
                            email=Regobj.username

                            configuration = sib_api_v3_sdk.Configuration()
                            configuration.api_key[
                                'api-key'] = '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'
                            headers = {
                                'accept': 'application/json',
                                'content-type': 'application/json',
                            }
                            bidproductdetails=BiddingBuyerProductDetails.objects.filter(buyer_rfq_number=rfq_number).values()
                            print("{{{{{{",len(bidproductdetails))
                            if len(bidproductdetails)>0:
                                for j in range(0,len(bidproductdetails)):
                                    totalquantity=totalquantity + int(bidproductdetails[j].get('buyer_quantity'))

                            print("total count",totalquantity)

                            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
                            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=[{"email": email, "name": Regobj.contact_person}],
                                                                           template_id=21, params={"billing": str(baddress[0].get('bill_address')),
                                                                                                   "shipping": str(saddress[0].get('ship_address')),
                                                                                                   "rfqno":rfq_number ,
                                                                                                   "totalqnty":str(totalquantity),
                                                                                                   "totalproduct":str(len(bidproductdetails)),
                                                                                                   "cname":bidcreater[0].get('company_name'),
                                                                                                   "mail": Regobj.username,
                                                                                                   "phone": Regobj.phone_number,
                                                                                                   "contact_name":Regobj.contact_person
                                                                                                   },
                                                                           headers=headers,
                                                                           subject='Bidding Invitation'
                                                                           )  # SendSmtpEmail | Values to send a transactional email
                            # Send a transactional email
                            api_response = api_instance.send_transac_email(send_smtp_email)
                            print(api_response)





                        SelectVendorsForBiddingProduct.objects.create(rfq_number=rfq_number,
                                                                      created_by=userid,
                                                                      updated_by=SelfRegistration.objects.get(id=userid),
                                                                      vendor_code=vendor_code[i],
                                                                      rfq_type=rfq_type,
                                                                      # auto_rfq_number=auto_rfq_number,
                                                                      # from_registration=from_registration,
                                                                      )
                return Response({'status': 201, 'message': 'Select Vendor For Product Bidding is Created'}, status=201)

            else:
                return Response({'status': 204, 'message': 'Vendors already present'}, status=204)

        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
# @permission_classes((AllowAny,))
def rfq_bid_list_summary_advance_search(request):
    data = request.data
    user_rfq_number = data['user_rfq_number']
    product_rfq_title = data['product_rfq_title']
    product_publish_date = data['product_publish_date']
    product_department = data['product_department']
    product_rfq_category = data['product_rfq_category']
    product_rfq_currency = data['product_rfq_currency']
    product_deadline_date = data['product_deadline_date']
    product_delivery_date = data['product_delivery_date']
    try:
        rfqbiddingproduct = BuyerProductBidding.objects.filter(updated_by=data['userid'],
                                                               user_rfq_number__icontains=user_rfq_number,
                                                               product_rfq_title__icontains=product_rfq_title,
                                                               product_publish_date__icontains=product_publish_date,
                                                               product_department__icontains=product_department,
                                                               product_rfq_category__icontains=product_rfq_category,
                                                               product_rfq_currency__icontains=product_rfq_currency,
                                                               product_deadline_date__icontains=product_deadline_date,
                                                               product_delivery_date__icontains=product_delivery_date).values(
            'user_rfq_number', 'product_rfq_title', 'product_publish_date', 'product_department',
            'product_rfq_category', 'product_rfq_currency', 'product_deadline_date', 'product_delivery_date',
            'updated_by_id')

        return Response({'status': 200, 'message': 'Search Success', 'data': rfqbiddingproduct}, status=200)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
# @permission_classes((AllowAny,))
def rfq_type_based_list(request):
    data = request.data
    userid = data['userid']
    product_rfq_type = data['product_rfq_type']
    from_registration=data['from_registration']
    try:
        if from_registration=='False':
            rfqtypeobj = BuyerProductBidding.objects.filter(updated_by=userid).values().order_by('product_bidding_id')
            if len(rfqtypeobj) > 0:
                if product_rfq_type == 'Product':
                    rfqtypeproductobj = BuyerProductBidding.objects.filter(updated_by=userid,
                                                                           product_rfq_type=product_rfq_type,from_registration='False').values().order_by(
                        'product_bidding_id')
                    return Response({'status': 200, 'message': 'Rfq Type Product', 'data': rfqtypeproductobj}, status=200)
                elif product_rfq_type == 'Service':
                    rfqtypeserviceobj = BuyerProductBidding.objects.filter(updated_by=userid,
                                                                           product_rfq_type=product_rfq_type,from_registration='False').values().order_by(
                        'product_bidding_id')
                    return Response({'status': 200, 'message': 'Rfq Type Service', 'data': rfqtypeserviceobj}, status=200)
                elif product_rfq_type == 'Machinary & equipments':
                    rfqtypemachinaryobj = BuyerProductBidding.objects.filter(updated_by=userid,
                                                                           product_rfq_type=product_rfq_type,from_registration='False').values().order_by(
                        'product_bidding_id')
                    return Response({'status': 200, 'message': 'Rfq Type Machinary', 'data': rfqtypemachinaryobj}, status=200)

                else:
                    return Response({'status': 204, 'error': 'Not present or rfq_type is wrong', 'data': []}, status=204)
            else:
                return Response({'status': 202, 'error': 'Data Not Present For this user id'}, status=202)
        else:
            if from_registration == 'True':
                rfqtypeobj = BuyerProductBidding.objects.filter(updated_by=userid).values().order_by(
                    'product_bidding_id')
                if len(rfqtypeobj) > 0:
                    if product_rfq_type == 'Product':
                        rfqtypeproductobj = BuyerProductBidding.objects.filter(updated_by=userid,
                                                                               product_rfq_type=product_rfq_type,from_registration='True').values().order_by(
                            'product_bidding_id')
                        return Response({'status': 200, 'message': 'Rfq Type Product from registration', 'data': rfqtypeproductobj},
                                        status=200)
                    elif product_rfq_type == 'Service':
                        rfqtypeserviceobj = BuyerProductBidding.objects.filter(updated_by=userid,
                                                                               product_rfq_type=product_rfq_type,from_registration='True').values().order_by(
                            'product_bidding_id')
                        return Response({'status': 200, 'message': 'Rfq Type Service from registration', 'data': rfqtypeserviceobj},
                                        status=200)
                    elif product_rfq_type == 'Machinary & equipments':
                        rfqtypemachinaryobj = BuyerProductBidding.objects.filter(updated_by=userid,
                                                                                 product_rfq_type=product_rfq_type,from_registration='True').values().order_by(
                            'product_bidding_id')
                        return Response({'status': 200, 'message': 'Rfq Type Machinary from registration', 'data': rfqtypemachinaryobj},
                                        status=200)

                    else:
                        return Response({'status': 204, 'error': 'Not present or rfq_type is wrong', 'data': []},
                                        status=204)
                else:
                    return Response({'status': 202, 'error': 'Data Not Present For this user id'}, status=202)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


class BiddingTermMasterSettingsView(viewsets.ModelViewSet):
    queryset = BiddingTermMasterSettings.objects.all()
    serializer_class = BiddingTermMasterSettingsSerializer

    def get_queryset(self):
        biddingtermsmastersettings = BiddingTermMasterSettings.objects.filter(
            updated_by=self.request.GET.get('updated_by'))
        if biddingtermsmastersettings:
            return biddingtermsmastersettings
        raise ValidationError(
            {'message': 'Bidding  Term Master details of particular user id is not exist', 'status': 204})

@api_view(['post'])
def add_terms_to_bidding_terms_settings(request):
    data=request.data
    termnames=data['termnames']
    userid=data['userid']
    try:
        for i in range(0,len(termnames)):
            termobj=BiddingTermMasterSettings.objects.create(terms_name=termnames[i],
                                                             created_by=userid,
                                                             updated_by=SelfRegistration.objects.get(id=userid)

                                                             )
        return Response({'status':201,'message':'Bidding Terms Created'},status=201)
    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)




@api_view(['post'])
# @permission_classes((AllowAny,))
def get_buyer_product_bid_by_user_rfq(request):
    data = request.data
    rfqnumber = data['rfqnumber']
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
# @permission_classes((AllowAny,))
def get_buyer_product_details_by_user_rfq(request):
    data = request.data
    rfqnumber = data['rfqnumber']
    docarray=[]
    dict1={}
    try:
        bidproductdetails = BiddingBuyerProductDetails.objects.filter(buyer_rfq_number=rfqnumber).values().order_by(
            'id')
        if len(bidproductdetails) > 0:
            for i in range(0,len(bidproductdetails)):
                buyerproductobj=BuyerProductDetails.objects.filter(buyer_item_code=bidproductdetails[i].get('buyer_item_code')).values()
                if not buyerproductobj[0].get('buyer_document'):
                    bidproductdetails[i].__setitem__('document', "")
                else:
                    bidproductdetails[i].__setitem__('document',
                                                     "https://v2apis.vendorsin.com/media/" + buyerproductobj[0].get(
                                                         'buyer_document'))


                if not buyerproductobj[0].get('buyer_document_1'):
                    bidproductdetails[i].__setitem__('document_1',"")
                else:
                    bidproductdetails[i].__setitem__('document_1',
                                                     "https://v2apis.vendorsin.com/media/" + buyerproductobj[0].get(
                                                         'buyer_document_1'))

                if not buyerproductobj[0].get('buyer_document_2'):
                    bidproductdetails[i].__setitem__('document_2',"")

                else:
                    bidproductdetails[i].__setitem__('document_2',
                                                     "https://v2apis.vendorsin.com/media/" + buyerproductobj[0].get(
                                                         'buyer_document_2'))

            return Response({'status': 200, 'message': "Buyer Product Details List Success", 'data': bidproductdetails},
                            status=200)
        else:
            return Response(
                {'status': 204, 'message': "Product Details are not present for this particular user and rfq"},
                status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
# @permission_classes((AllowAny,))
def get_buyer_bid_terms_by_user_rfq(request):
    data = request.data
    rfqnumber = data['rfqnumber']
    try:
        bidtermsdescription = RfqTermsDescription.objects.filter(rfq_number=rfqnumber).values().order_by('id')
        if len(bidtermsdescription) > 0:
            return Response({'status': 200, 'message': "Buyer terms and description", 'data': bidtermsdescription},
                            status=200)
        else:
            return Response(
                {'status': 204, 'message': "Terms and Descripiton are not present for this particular user and rfq"},
                status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
# @permission_classes((AllowAny,))
def open_bid_list_buyer_publish_list(request):
    data = request.data
    userid = data['userid']
    from_registration=data['from_registration']
    openbidarray = []
    try:
        if from_registration=='False':
            basicobj = BasicCompanyDetails.objects.filter(updated_by=userid).values()
            # print(basicobj)
            selectvendorsobj = SelectVendorsForBiddingProduct.objects.filter(vendor_code=basicobj[0].get('company_code'),
                                                                             vendor_status='Pending',from_registration='False').values()
            print(len(selectvendorsobj),'length')
            if len(selectvendorsobj) > 0:
                for i in range(0, len(selectvendorsobj)):
                    print(selectvendorsobj[i].get('rfq_number'),'selected vendors rfq')
                    biddingval = BuyerProductBidding.objects.get(user_rfq_number=selectvendorsobj[i].get('rfq_number'),from_registration=from_registration)
                    basicobjval = BasicCompanyDetails.objects.filter(updated_by_id=biddingval.updated_by_id).values()
                    openbidarray.append({'vendor_code': basicobjval[0].get('company_code'),
                                         'user_rfq_number': biddingval.user_rfq_number,
                                         'company_name': basicobjval[0].get('company_name'),
                                         'product_rfq_type': biddingval.product_rfq_type,
                                         'product_rfq_title': biddingval.product_rfq_title,
                                         'product_rfq_status': biddingval.product_rfq_status,
                                         'product_publish_date': biddingval.product_publish_date,
                                         'product_deadline_date': biddingval.product_deadline_date,
                                         'product_delivery_date': biddingval.product_delivery_date,
                                         'product_rfq_currency': biddingval.product_rfq_currency,
                                         'product_rfq_category': biddingval.product_rfq_category,
                                         'product_department': biddingval.product_department,
                                             })

                return Response({'status': 200, 'message': "Open Leads", 'data': openbidarray}, status=200)
            else:
                return Response({'status': 202, 'message': 'Vendors are not selected for any bidding','data':openbidarray}, status=202)
        elif from_registration=='True':
            basicobj = BasicCompanyDetails.objects.filter(updated_by=userid).values()
                # print(basicobj)
            selectvendorsobj = SelectVendorsForBiddingProduct.objects.filter(vendor_code=basicobj[0].get('company_code'),
                                                                             vendor_status='Pending',from_registration=from_registration).values()

            print(len(selectvendorsobj),'length')
            if len(selectvendorsobj) > 0:
                for i in range(0, len(selectvendorsobj)):
                    print(selectvendorsobj[i].get('auto_rfq_number'))
                    biddingval = BuyerProductBidding.objects.get(product_rfq_number=selectvendorsobj[i].get('auto_rfq_number'),from_registration='True')
                    basicobjval = BasicCompanyDetails.objects.filter(updated_by_id=biddingval.updated_by_id).values()
                    print(basicobjval)
                    openbidarray.append({'vendor_code': basicobjval[0].get('company_code'),
                                         'auto_rfq_number': biddingval.product_rfq_number,
                                         'user_rfq_number':"",
                                         'company_name': basicobjval[0].get('company_name'),
                                         'product_rfq_type': biddingval.product_rfq_type,
                                         'product_rfq_title': biddingval.product_rfq_title,
                                         'product_rfq_status': biddingval.product_rfq_status,
                                         'product_publish_date': biddingval.product_publish_date,
                                         'product_deadline_date': biddingval.product_deadline_date,
                                         'product_delivery_date': biddingval.product_delivery_date,
                                         'product_rfq_currency': biddingval.product_rfq_currency,
                                         'product_rfq_category': biddingval.product_rfq_category,
                                         'product_department': biddingval.product_department,
                                             })

                return Response({'status': 200, 'message': "Open Leads Values", 'data': openbidarray}, status=200)
            else:
                return Response({'status': 202, 'message': 'Vendors are not selected for any bidding','data':openbidarray}, status=202)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


class VendorProductBiddingView(viewsets.ModelViewSet):
    # permission_classes = [permissions.AllowAny]
    queryset = VendorProductBidding.objects.all()
    serializer_class = VendorProductBiddingSerializer

# Common open RFQ bid vendor Response model
class VendorProductBiddingOpenCommonBidView(viewsets.ModelViewSet):
    queryset = VendorProductBiddingOpenCommonBid.objects.all()
    serializer_class = VendorProductBiddingOpenCommonBidSerializer

class VendorBiddingBuyerProductDetailsView(viewsets.ModelViewSet):
    # permission_classes = [permissions.AllowAny]
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
                                                                vendor_item_code=vendorproductdetails[i].get(
                                                                    'vendor_item_code'),
                                                                vendor_item_name=vendorproductdetails[i].get(
                                                                    'vendor_item_name'),
                                                                vendor_item_description=vendorproductdetails[i].get(
                                                                    'vendor_item_description'),
                                                                vendor_uom=vendorproductdetails[i].get('vendor_uom'),
                                                                vendor_category=vendorproductdetails[i].get(
                                                                    'vendor_category'),
                                                                vendor_quantity=vendorproductdetails[i].get(
                                                                    'vendor_quantity'),
                                                                buyer_quantity=vendorproductdetails[i].get(
                                                                    'buyer_quantity'),
                                                                vendor_rate=vendorproductdetails[i].get('vendor_rate'),
                                                                vendor_tax=vendorproductdetails[i].get('vendor_tax'),
                                                                vendor_discount=vendorproductdetails[i].get(
                                                                    'vendor_discount'),
                                                                vendor_final_amount=vendorproductdetails[i].get(
                                                                    'vendor_final_amount'),
                                                                vendor_total_amount=vendorproductdetails[i].get(
                                                                    'vendor_total_amount'),
                                                                vendor_document=vendorproductdetails[i].get(
                                                                    'vendor_document'),
                                                                vendor_item_type=vendorproductdetails[i].get('vendor_item_type'),
                                                                vendor_code=vendorproductdetails[i].get('vendor_code'),
                                                                # auto_rfq_number=vendorobj.vendor_product_rfq_number,
                                                                # from_registration=from_registration,
                                                                updated_by=SelfRegistration.objects.get(id=userid),
                                                                created_by=userid)
            return Response({'status': 201, 'message': 'Vendor Bidding Buyer Product Details are Created'}, status=201)
        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)

    def get_queryset(self):
        vendorproductdetailsobj = VendorBiddingBuyerProductDetails.objects.filter(
            updated_by=self.request.GET.get('updated_by')).order_by('id')
        if vendorproductdetailsobj:
            return vendorproductdetailsobj
        raise ValidationError(
            {'message': 'Vendor Bidding Product details of particular user id is not exist', 'status': 204})


# common open RFQ Bid vendor product model
class VendorBiddingBuyerProductDetailsOpenCommonBidView(viewsets.ModelViewSet):
    queryset = VendorBiddingBuyerProductDetailsOpenCommonBid.objects.all()
    serializer_class = VendorProductBiddingOpenCommonBidproductdetailsSerializer
    ordering_fields = ['id']
    ordering = ['id']

    def create(self, request, *args, **kwargs):
        vendorproductdetails = request.data['vendorproductdetails']
        vendor_rfq_number = request.data.get('vendor_rfq_number', None)
        userid = request.data.get('userid', None)
        try:
            for i in range(0, len(vendorproductdetails)):
                VendorBiddingBuyerProductDetailsOpenCommonBid.objects.create(vendor_rfq_number=vendor_rfq_number,
                                                                vendor_item_code=vendorproductdetails[i].get(
                                                                    'vendor_item_code'),
                                                                vendor_item_name=vendorproductdetails[i].get(
                                                                    'vendor_item_name'),
                                                                vendor_item_description=vendorproductdetails[i].get(
                                                                    'vendor_item_description'),
                                                                vendor_uom=vendorproductdetails[i].get('vendor_uom'),
                                                                vendor_category=vendorproductdetails[i].get(
                                                                    'vendor_category'),
                                                                vendor_quantity=vendorproductdetails[i].get(
                                                                    'vendor_quantity'),
                                                                buyer_quantity=vendorproductdetails[i].get(
                                                                    'buyer_quantity'),
                                                                vendor_rate=vendorproductdetails[i].get('vendor_rate'),
                                                                vendor_tax=vendorproductdetails[i].get('vendor_tax'),
                                                                vendor_discount=vendorproductdetails[i].get(
                                                                    'vendor_discount'),
                                                                vendor_final_amount=vendorproductdetails[i].get(
                                                                    'vendor_final_amount'),
                                                                vendor_total_amount=vendorproductdetails[i].get(
                                                                    'vendor_total_amount'),
                                                                vendor_document=vendorproductdetails[i].get(
                                                                    'vendor_document'),
                                                                vendor_item_type=vendorproductdetails[i].get('vendor_item_type'),
                                                                vendor_code=vendorproductdetails[i].get('vendor_code'),
                                                                # auto_rfq_number=vendorobj.vendor_product_rfq_number,
                                                                # from_registration=from_registration,
                                                                updated_by=SelfRegistration.objects.get(id=userid),
                                                                created_by=userid)
            return Response({'status': 201, 'message': 'Vendor Bidding Buyer Product Details are Created'}, status=201)
        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)

    def get_queryset(self):
        vendorproductdetailsobj = VendorBiddingBuyerProductDetailsOpenCommonBid.objects.filter(
            updated_by=self.request.GET.get('updated_by')).order_by('id')
        if vendorproductdetailsobj:
            return vendorproductdetailsobj
        raise ValidationError(
            {'message': 'Vendor Bidding Product details of particular user id is not exist', 'status': 204})

# common open RFQ Bid vendor terms and desc
class VendorRfqTermsDescriptionOpenCommonBidView(viewsets.ModelViewSet):
    queryset = VendorRfqTermsDescriptionOpenCommonBid.objects.all()
    serializer_class = VendorProductBiddingOpenCommonBidtermsSerializer


    def create(self, request, *args, **kwargs):
        vendor_rfq_number = request.data['vendor_rfq_number']
        dictsqueries = request.data['dictsqueries']
        vendor_product_biddings = request.data.get('vendor_product_biddings', None)
        updated_by = request.data.get('updated_by', None)
        rfq_type=request.data.get('rfq_type', None)
        try:
            for i in range(0, len(dictsqueries)):

                for keys in dictsqueries[i]:
                    VendorRfqTermsDescriptionOpenCommonBid.objects.create(vendor_rfq_number=vendor_rfq_number,
                                                             vendor_terms=keys,
                                                             vendor_description=dictsqueries[i][keys][0],
                                                             vendor_response=dictsqueries[i][keys][1],
                                                             vendor_product_rfq_bid_by_pk_id=VendorProductBiddingOpenCommonBid.objects.get(vendor_product_bidding_id=vendor_product_biddings),
                                                             updated_by=SelfRegistration.objects.get(id=updated_by),
                                                             rfq_type=rfq_type,
                                                             created_by=updated_by)

            return Response({'status': 201, 'message': 'Vendor Terms and Descriptions are created'}, status=201)
        except Exception as e:
            return Response({'status': 500, 'message': str(e)}, status=500)


class VendorBiddingBuyerServiceDetailsView(viewsets.ModelViewSet):
    # permission_classes = [permissions.AllowAny]
    queryset = VendorBiddingBuyerServiceDetails.objects.all()
    serializer_class = VendorBiddingBuyerServiceDetailsSerializer

    def create(self, request, *args, **kwargs):
        vendorservicedetails = request.data['vendorservicedetails']
        vendor_service_rfq_number = request.data.get('vendor_service_rfq_number', None)
        userid = request.data.get('userid', None)
        try:
            for i in range(0, len(vendorservicedetails)):
                VendorBiddingBuyerServiceDetails.objects.create(vendor_service_rfq_number=vendor_service_rfq_number,
                                                                vendor_service_item_code=vendorservicedetails[i].get(
                                                                    'vendor_service_item_code'),
                                                                vendor_service_item_name=vendorservicedetails[i].get(
                                                                    'vendor_service_item_name'),
                                                                vendor_service_item_description=vendorservicedetails[i].get(
                                                                    'vendor_service_item_description'),
                                                                vendor_service_uom=vendorservicedetails[i].get('vendor_service_uom'),
                                                                vendor_service_category=vendorservicedetails[i].get(
                                                                    'vendor_service_category'),
                                                                buyer_service_quantity=vendorservicedetails[i].get(
                                                                    'buyer_service_quantity'),
                                                                vendor_service_quantity=vendorservicedetails[i].get(
                                                                    'vendor_service_quantity'),
                                                                vendor_service_rate=vendorservicedetails[i].get('vendor_service_rate'),
                                                                vendor_service_tax=vendorservicedetails[i].get('vendor_service_tax'),
                                                                vendor_service_discount=vendorservicedetails[i].get(
                                                                    'vendor_service_discount'),
                                                                vendor_service_final_amount=vendorservicedetails[i].get(
                                                                    'vendor_service_final_amount'),
                                                                vendor_service_total_amount=vendorservicedetails[i].get(
                                                                    'vendor_service_total_amount'),
                                                                vendor_service_document=vendorservicedetails[i].get(
                                                                    'vendor_service_document'),
                                                                vendor_service_item_type=vendorservicedetails[i].get('vendor_service_item_type'),
                                                                vendor_code=vendorservicedetails[i].get('vendor_code'),
                                                                updated_by=SelfRegistration.objects.get(id=userid),
                                                                created_by=userid)
            return Response({'status': 201, 'message': 'Vendor Bidding Buyer Service Details are Created'}, status=201)
        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)

    def get_queryset(self):
        vendorservicedetailsobj = VendorBiddingBuyerServiceDetails.objects.filter(
            updated_by=self.request.GET.get('updated_by')).order_by('id')
        if vendorservicedetailsobj:
            return vendorservicedetailsobj
        raise ValidationError(
            {'message': 'Vendor Bidding Service details of particular user id is not exist', 'status': 204})


class VendorBiddingBuyerMachinaryDetailsView(viewsets.ModelViewSet):
    # permission_classes = [permissions.AllowAny]
    queryset = VendorBiddingBuyerMachinaryDetails.objects.all()
    serializer_class = VendorBiddingBuyerMachinaryDetailsSerializer
    ordering_fields = ['id']
    ordering = ['id']

    def create(self, request, *args, **kwargs):
        vendormachinarydetails = request.data['vendormachinarydetails']
        vendor_machinary_rfq_number = request.data.get('vendor_machinary_rfq_number', None)
        userid = request.data.get('userid', None)
        try:
            for i in range(0, len(vendormachinarydetails)):
                VendorBiddingBuyerMachinaryDetails.objects.create(vendor_machinary_rfq_number=vendor_machinary_rfq_number,
                                                                vendor_machinary_item_code=vendormachinarydetails[i].get(
                                                                    'vendor_machinary_item_code'),
                                                                vendor_machinary_item_name=vendormachinarydetails[i].get(
                                                                    'vendor_machinary_item_name'),
                                                                vendor_machinary_item_description=vendormachinarydetails[i].get(
                                                                    'vendor_machinary_item_description'),
                                                                vendor_machinary_uom=vendormachinarydetails[i].get('vendor_machinary_uom'),
                                                                vendor_machinary_category=vendormachinarydetails[i].get(
                                                                    'vendor_machinary_category'),
                                                                buyer_machinary_quantity=vendormachinarydetails[i].get(
                                                                    'buyer_machinary_quantity'),
                                                                vendor_machinary_quantity=vendormachinarydetails[i].get(
                                                                    'vendor_machinary_quantity'),
                                                                vendor_machinary_rate=vendormachinarydetails[i].get('vendor_machinary_rate'),
                                                                vendor_machinary_tax=vendormachinarydetails[i].get('vendor_machinary_tax'),
                                                                vendor_machinary_discount=vendormachinarydetails[i].get(
                                                                    'vendor_machinary_discount'),
                                                                vendor_machinary_final_amount=vendormachinarydetails[i].get(
                                                                    'vendor_machinary_final_amount'),
                                                                vendor_machinary_total_amount=vendormachinarydetails[i].get(
                                                                    'vendor_machinary_total_amount'),
                                                                vendor_machinary_document=vendormachinarydetails[i].get(
                                                                    'vendor_machinary_document'),
                                                                vendor_machinary_item_type=vendormachinarydetails[i].get('vendor_machinary_item_type'),
                                                                vendor_code=vendormachinarydetails[i].get('vendor_code'),
                                                                updated_by=SelfRegistration.objects.get(id=userid),
                                                                created_by=userid)
            return Response({'status': 201, 'message': 'Vendor Bidding Buyer Machinary Details are Created'}, status=201)
        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)

    def get_queryset(self):
        vendormachinarydetailsobj = VendorBiddingBuyerMachinaryDetails.objects.filter(
            updated_by=self.request.GET.get('updated_by')).order_by('id')
        if vendormachinarydetailsobj:
            return vendormachinarydetailsobj
        raise ValidationError(
            {'message': 'Vendor Bidding Machinary details of particular user id is not exist', 'status': 204})

class VendorRfqTermsDescriptionView(viewsets.ModelViewSet):
    # permission_classes = [permissions.AllowAny]
    queryset = VendorRfqTermsDescription.objects.all()
    serializer_class = VendorRfqTermsDescriptionSerializer


    def create(self, request, *args, **kwargs):
        vendor_rfq_number = request.data['vendor_rfq_number']
        dictsqueries = request.data['dictsqueries']
        vendor_product_biddings = request.data.get('vendor_product_biddings', None)
        updated_by = request.data.get('updated_by', None)
        rfq_type=request.data.get('rfq_type', None)
        try:
            for i in range(0, len(dictsqueries)):

                for keys in dictsqueries[i]:
                    VendorRfqTermsDescription.objects.create(vendor_rfq_number=vendor_rfq_number,
                                                             vendor_terms=keys,
                                                             vendor_description=dictsqueries[i][keys][0],
                                                             vendor_response=dictsqueries[i][keys][1],
                                                             vendor_product_biddings=VendorProductBidding.objects.get(
                                                                 vendor_product_bidding_id=vendor_product_biddings),
                                                             updated_by=SelfRegistration.objects.get(id=updated_by),
                                                             rfq_type=rfq_type,
                                                             created_by=updated_by)

            return Response({'status': 201, 'message': 'Vendor Terms and Descriptions are created'}, status=201)
        except Exception as e:
            return Response({'status': 500, 'message': str(e)}, status=500)


@api_view(['put'])
def update_buyer_bid_status_pending_to_publish(request):
    data = request.data
    user_rfq_number = data['user_rfq_number']
    userid = data['userid']
    try:

        vendorobj = BuyerProductBidding.objects.get(user_rfq_number=user_rfq_number, updated_by=userid)
        if vendorobj:
            if vendorobj.product_rfq_status == 'Pending':
                vendorobj.product_rfq_status = 'Published'
                vendorobj.save()
                return Response({'status': 200, 'message': 'Pending Status Changed to Published',
                                 'data': vendorobj.product_rfq_status}, status=200)
            else:
                return Response({'status': 202, 'error': 'Already Status Changed to  Published'}, status=202)
        else:
            return Response({'status': 204, 'message': 'No data present for this Rfq'}, status=204)

    except Exception as e:
        return Response({'status': 200, 'error': str(e)}, status=500)


@api_view(['post'])
def get_buyer_bidding_by_bidding_id_and_rfq(request):
    data = request.data
    product_bidding_id = data['product_bidding_id']
    user_rfq_number = data['user_rfq_number']
    try:
        buyerbidobj = BuyerProductBidding.objects.filter(product_bidding_id=product_bidding_id,
                                                         user_rfq_number=user_rfq_number).values()
        if len(buyerbidobj) > 0:
            return Response({'status': 200, 'message': 'Buyer Bidding List Success', 'data': buyerbidobj},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'No data present for this Rfq'},
                            status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 200, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['put'])
def update_buyer_bidding_deadline_date(request):
    data = request.data
    product_bidding_id = data['product_bidding_id']
    user_rfq_number = data['user_rfq_number']
    product_deadline_date = data['product_deadline_date']
    qtycount=0
    try:
        buyerbidupdateobj = BuyerProductBidding.objects.filter(product_bidding_id=product_bidding_id,
                                                               user_rfq_number=user_rfq_number).values()

        if len(buyerbidupdateobj) > 0:
            basicobj = BasicCompanyDetails.objects.filter(updated_by=buyerbidupdateobj[0].get('updated_by_id')).values()
            buyerobj = BuyerProductBidding.objects.get(product_bidding_id=product_bidding_id,
                                                       user_rfq_number=user_rfq_number)

            buyerproductobj=BiddingBuyerProductDetails.objects.filter(buyer_rfq_number=user_rfq_number).values()
            for i in range(len(buyerproductobj)):
                qtycount=qtycount+int(buyerproductobj[i].get('buyer_quantity'))
            if buyerobj.product_deadline_date != product_deadline_date:
                buyerobj.product_deadline_date = product_deadline_date
                buyerobj.save()
                resarray=["Accept","Pending"]
                selectedobj=SelectVendorsForBiddingProduct.objects.filter(rfq_number=user_rfq_number,vendor_status__in=resarray).values()

                configuration = sib_api_v3_sdk.Configuration()
                configuration.api_key[
                    'api-key'] = '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'
                headers = {
                    'accept': 'application/json',
                    'content-type': 'application/json',
                }
                for i in range(0,len(selectedobj)):
                    basicobj=BasicCompanyDetails.objects.filter(company_code=selectedobj[i].get('vendor_code')).values()
                    regobj=SelfRegistration.objects.filter(id=basicobj[0].get('updated_by_id')).values()

                    datevalue=datetime.strptime(product_deadline_date, '%Y-%m-%d').strftime('%d/%m/%y')
                    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
                    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=[{"email": regobj[0].get('username'), "name": "harish"}],
                                                                   template_id=25, params={
                            "billing":str(buyerobj.product_bill_address) ,
                            "shipping":str(buyerobj.product_ship_address) ,
                            "exdate":datevalue,
                            "rfqno": user_rfq_number,
                            "totalqnty": str(qtycount),
                            "totalproduct": str(len(buyerproductobj)),
                            "cname": basicobj[0].get('company_name')},
                                                                   headers=headers,
                                                                   subject='Bidding Invitation'
                                                                   )  # SendSmtpEmail | Values to send a transactional email
                    # Send a transactional email
                    api_response = api_instance.send_transac_email(send_smtp_email)
                    print(api_response)


                return Response({'status': 200, 'message': 'Deadline Date is updated'}, status=200)
            else:
                return Response({'status': 202, 'message': 'Deadline Date is Already Updated'}, status=202)

        else:
            return Response({'status': 204, 'message': 'No data'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['post'])
def vendor_bidding_all_details(request):
    data = request.data
    updated_by = data['updated_by']
    try:
        vendorproductbiddingobj = VendorProductBidding.objects.filter(updated_by=updated_by).values()
        vendorproductdetails = VendorBiddingBuyerProductDetails.objects.filter(updated_by=updated_by).values()
        vendortermsobj = VendorRfqTermsDescription.objects.filter(updated_by=updated_by).values()
        vendorobj = list(chain(vendorproductbiddingobj, vendorproductdetails, vendortermsobj))
        return Response({'status': 200, 'message': 'Vendor Bidding List', 'data': vendorobj}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['post'])
def get_vendor_published_leads(request):
    data = request.data
    userid = data['userid']
    vendorpublishleads = []
    selectsarray = []
    try:
        basic = BasicCompanyDetails.objects.filter(updated_by_id=userid).values()
        print(basic[0].get('company_code'))
        selects = SelectVendorsForBiddingProduct.objects.filter(vendor_code=basic[0].get('company_code'),vendor_status='Accept').values().order_by('id')
        print(len(selects))
        if len(selects) > 0:
            for i in range(0, len(selects)):
                selectsarray.append(selects[i].get('rfq_number'))

            bidobj = BuyerProductBidding.objects.filter(user_rfq_number__in=selectsarray).values().order_by(
                'user_rfq_number')
            print(len(bidobj))
            for i in range(0, len(selects)):
                basicobj = BasicCompanyDetails.objects.filter(updated_by_id=bidobj[i].get('updated_by_id')).values()
                vendorpublishleads.append({'user_rfq_number': bidobj[i].get('user_rfq_number'),
                                           'vendor_code': basicobj[0].get('company_code'),
                                           'vendor_status': selects[i].get('vendor_status'),
                                           'updatedby': selects[i].get('updated_by_id'),
                                           'product_bidding_id': bidobj[i].get('product_bidding_id'),
                                           'product_rfq_status': bidobj[i].get('product_rfq_status'),
                                           'product_rfq_type': bidobj[i].get('product_rfq_type'),
                                           'product_publish_date': bidobj[i].get('product_publish_date'),
                                           'product_department': bidobj[i].get('product_department'),
                                           'product_deadline_date': bidobj[i].get('product_deadline_date'),
                                           'product_bill_address': bidobj[i].get('product_bill_address'),
                                           'product_ship_address': bidobj[i].get('product_ship_address'),
                                           'product_rfq_title': bidobj[i].get('product_rfq_title'),
                                           'company_name': basicobj[0].get('company_name')

                                           })

            return Response({'status': 200, 'message': 'Getting data', 'data': vendorpublishleads}, status=200)
        else:
            return Response({'status': 202, 'message': 'No Data Found','data':[]}, status=202)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
def open_leads_product_advance_search(request):
    data=request.data
    user_rfq_number=data['user_rfq_number']
    company_name=data['company_name']
    product_rfq_type=data['product_rfq_type']
    product_rfq_title=data['product_rfq_title']
    product_rfq_status=data['product_rfq_status']
    product_publish_date=data['product_publish_date']
    product_deadline_date=data['product_deadline_date']
    product_delivery_date=data['product_delivery_date']
    product_rfq_currency=data['product_rfq_currency']
    product_rfq_category=data['product_rfq_category']
    product_department=data['product_department']
    valuearray = data['valuearray']
    openleadssearch=[]

    try:
        for i in range(0,len(valuearray)):
            if user_rfq_number.lower() in valuearray[i].get('user_rfq_number').lower() and \
                    company_name.lower() in valuearray[i].get('company_name').lower() and \
                    product_rfq_type.lower() in valuearray[i].get('product_rfq_type').lower() and \
                    product_rfq_title.lower() in valuearray[i].get('product_rfq_title').lower() and \
                    product_rfq_status.lower() in valuearray[i].get('product_rfq_status').lower() and \
                    product_publish_date in valuearray[i].get('product_publish_date') and \
                    product_deadline_date in valuearray[i].get('product_deadline_date') and \
                    product_delivery_date in valuearray[i].get('product_delivery_date') and \
                    product_rfq_currency.lower()  in valuearray[i].get('product_rfq_currency').lower() and \
                    product_rfq_category.lower() in valuearray[i].get('product_rfq_category').lower()  and \
                    product_department.lower() in valuearray[i].get('product_department').lower():
                openleadssearch.append(valuearray[i])
            else:
                print('Not Present')
        return Response({'status': 200, 'message': 'Open Leads Search Success', 'data': openleadssearch}, status=200)



    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



# ----------------------------------------------------------------SOURCE---------------------------------------------------------------------

class SourceList_CreateItemViewSet(viewsets.ModelViewSet):
    # permission_classes=[permissions.AllowAny]
    queryset = SourceList_CreateItems.objects.all()
    serializer_class = SourceList_CreateItemsSerializer
    parser = [MultiPartParser]


    def get_queryset(self):
        sourcelistcreateitemsobj = SourceList_CreateItems.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if sourcelistcreateitemsobj:
            return sourcelistcreateitemsobj
        raise ValidationError({'message': 'Source List Create Items of particular user id is not exist', 'status': 204})


@api_view(['post'])
def getsourcebasedpk(request):
    data=request.data
    pkid=data['pkid']
    try:
        sourcelistcreateitemsobj = SourceList_CreateItems.objects.filter(id=pkid).values()
        if sourcelistcreateitemsobj:
            Billingaddrsobj=BillingAddress.objects.filter(updated_by=sourcelistcreateitemsobj[0].get('updated_by_id')).values().order_by('id')
            shippingaddrsobj=ShippingAddress.objects.filter(updated_by=sourcelistcreateitemsobj[0].get('updated_by_id')).values().order_by('id')
            comp=BasicCompanyDetails.objects.filter(updated_by=sourcelistcreateitemsobj[0].get('updated_by_id')).values()
            resdict={}
            resdict.setdefault('cname',str(comp[0].get('company_name')))
            resdict.setdefault('shippaddress',shippingaddrsobj[0].get('ship_address'))
            resdict.setdefault('Billingaddress', Billingaddrsobj[0].get('bill_address'))
            sourcelistcreateitemsobj[0].setdefault('address',resdict)
            return Response({'status': 200, 'message': 'Source Leads','data':sourcelistcreateitemsobj}, status=200)
    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)

@api_view(['post'])
def source_list_leads(request):
    data = request.data
    userid = data['userid']
    sourceleadsarray = []
    pk=[]
    listarray=[]
    try:
        sourcepublish = SourcePublish.objects.filter(updated_by_id=userid).values().order_by('id')
        for i in range(0,len(sourcepublish)):
            sourceleadsarray.append(sourcepublish[i].get('source_id'))
        basicobj = BasicCompanyDetails.objects.filter(updated_by_id=userid).values()
        if len(basicobj)>0:
            sourcobj = SourceList_CreateItems.objects.filter(source_vendors__contains=[basicobj[0].get('company_code')]).values()
            if len(sourcobj)>0:
                for i in range(0,len(sourcobj)):
                    print(sourcobj[i].get('source_vendors'),'ccode')
                    if sourcobj[i].get('id') not in sourceleadsarray:
                        basicval = BasicCompanyDetails.objects.filter(updated_by_id=sourcobj[i].get('updated_by_id')).values()
                        if basicval:
                            regobj= SelfRegistration.objects.filter(id=basicval[0].get('updated_by_id')).values()
                            if regobj:
                                billingobj = BillingAddress.objects.filter(company_code_id=basicval[0].get('company_code'),
                                                                       updated_by_id=basicval[0].get('updated_by_id')).values()
                                if billingobj:
                                    listarray.append({'id': sourcobj[i].get('id'),
                                                      'company_code': basicval[0].get('company_code'),
                                                      'company_name': basicval[0].get('company_name'),
                                                      'source_code': sourcobj[i].get('source_code'),
                                                      'source': sourcobj[i].get('source'),
                                                      'item_type': sourcobj[i].get('item_type'),
                                                      'quantity': sourcobj[i].get('quantity'),
                                                      'source_required_city': sourcobj[i].get('source_required_city'),
                                                      'product_category': sourcobj[i].get('product_category'),
                                                      'client_city': billingobj[0].get('bill_city'),
                                                      'updated_by': sourcobj[i].get('updated_by_id'),
                                                      'item_name': sourcobj[i].get('item_name'),
                                                      'maincore':sourcobj[i].get('maincore'),
                                                      'category':sourcobj[i].get('category'),
                                                      'uom':sourcobj[i].get('uom'),
                                                      'publish_date':sourcobj[i].get('publish_date'),
                                                      'deadline_date':sourcobj[i].get('deadline_date'),
                                                      'item_description':sourcobj[i].get('item_description'),
                                                      'profile_image':regobj[0].get('profile_cover_photo'),
                                                      'bill_address':billingobj[0].get('bill_address')

                                                      })
                                else:
                                    listarray.append({'id': sourcobj[i].get('id'),
                                                      'company_code': basicval[0].get('company_code'),
                                                      'company_name': basicval[0].get('company_name'),
                                                      'source_code': sourcobj[i].get('source_code'),
                                                      'source': sourcobj[i].get('source'),
                                                      'item_type': sourcobj[i].get('item_type'),
                                                      'quantity': sourcobj[i].get('quantity'),
                                                      'source_required_city': sourcobj[i].get('source_required_city'),
                                                      'product_category': sourcobj[i].get('product_category'),
                                                      'client_city': "",
                                                      'updated_by': sourcobj[i].get('updated_by_id'),
                                                      'item_name': sourcobj[i].get('item_name'),
                                                      'maincore': sourcobj[i].get('maincore'),
                                                      'category': sourcobj[i].get('category'),
                                                      'uom': sourcobj[i].get('uom'),
                                                      'publish_date': sourcobj[i].get('publish_date'),
                                                      'deadline_date': sourcobj[i].get('deadline_date'),
                                                      'item_description': sourcobj[i].get('item_description'),
                                                      'profile_image': regobj[0].get('profile_cover_photo'),
                                                      'bill_address': ""

                                                      })
                    else:
                        print('already present in publish')
                return Response({'status': 200, 'message': 'Source Leads', 'data': listarray}, status=200)
            else:
                return Response({'status':202,'message':'Source Leads Not Present'},status=204)

        else:
            return Response({'status': 204, 'message': 'Basic details are not present','data':[]}, status=204)

    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)


@api_view(['put'])
def update_source_vendor_codes(request):
    data = request.data
    userid = data['userid']
    sourceid = data['sourceid']
    vcodes = data['vcodes']
    try:
        sourcobj = SourceList_CreateItems.objects.filter(updated_by=userid, id=sourceid).values()
        if len(sourcobj) > 0:
            sourceval = SourceList_CreateItems.objects.get(id=sourceid, updated_by=userid)
            if sourceval.source_vendors == "" or sourceval.source_vendors != sourceid:
                sourceval.source_vendors = vcodes
                sourceval.save()
                return Response({'status': 200, 'message': 'Updated Source Data'}, status=200)
        else:
            return Response({'status': 204, 'message': 'Data Not Present '}, status=204)

    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)


@api_view(['post'])
def advance_search_source_leads(request):
    # source leads advance search
    data = request.data
    company_code = data['company_code']
    company_name = data['company_name']
    source = data['source']
    item_type = data['item_type']
    quantity = data['quantity']
    source_required_city = data['source_required_city']
    product_category = data['product_category']
    client_city = data['client_city']
    source_code = data['source_code']
    valuearray = data['valuearray']
    sourceleadsadvancesearcharray = []
    try:
        for i in range(0, len(valuearray)):
            if company_code in valuearray[i].get('company_code') and company_name.lower() in valuearray[i].get(
                    'company_name').lower() and source.lower() in valuearray[i].get(
                'source').lower() and item_type.lower() in valuearray[i].get('item_type').lower() \
                    and quantity.lower() in valuearray[i].get('quantity').lower() and source_required_city.lower() in \
                    valuearray[i].get(
                        'source_required_city').lower() and product_category.lower() in valuearray[i].get(
                'product_category').lower() \
                    and client_city.lower() in valuearray[i].get('client_city') and source_code.lower() in valuearray[
                i].get('source_code').lower():
                sourceleadsadvancesearcharray.append(valuearray[i])
            else:
                print('Not Present')
        return Response(
            {'status': 200, 'message': 'Source Leads Advance Search Success', 'data': sourceleadsadvancesearcharray},
            status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


class SourcePublishViewSet(viewsets.ModelViewSet):
    queryset = SourcePublish.objects.all()
    serializer_class = SourcePublishSerializer
    ordering_fields = ['id']
    ordering = ['id']


@api_view(['put'])
def source_status_update_to_decline(request):
    data = request.data
    source_id = data['source_id']
    try:
        sourceitems = SourceList_CreateItems.objects.filter(id=source_id).values()
        if len(sourceitems) > 0:
            sourceobj = SourceList_CreateItems.objects.get(id=source_id)
            if sourceobj.status == 'Pending':
                sourceobj.status = 'Decline'
                sourceobj.save()
                return Response({'status': 200, 'message': 'Status Changed to Decline'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 202, 'message': 'Already Declined or pending details are not present'},
                                status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['post'])
# @permission_classes((AllowAny,))
def get_buyer_product_based_on_userid_pk(request):
    data = request.data
    buyerproductid = data['buyerproductid']
    userid = data['userid']
    try:
        buyerproductobj = BuyerProductDetails.objects.filter(buyer_product_id__in=buyerproductid,
                                                             updated_by=userid).values()
        buyerserviceobj = BuyerServiceDetails.objects.filter(buyer_service_id__in=buyerproductid,
                                                             updated_by_id=userid).values()
        buyermachinaryobj = BuyerMachinaryDetails.objects.filter(buyer_machinary_id__in=buyerproductid,
                                                             updated_by_id=userid).values()
        if len(buyerproductobj) > 0:
            return Response({'status': 200, 'message': 'Buyer Product List', 'data': buyerproductobj}, status=200)
        elif len(buyerserviceobj)>0:
                return Response({'status': 200, 'message': 'Buyer Service List', 'data': buyerserviceobj}, status=200)
        elif len(buyermachinaryobj)>0:
            return Response({'status': 200, 'message': 'Buyer Machinary List', 'data': buyermachinaryobj}, status=200)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=204)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def get_source_based_on_item_type_user_id(request):
    data=request.data
    userid=data['userid']
    itemtype=data['itemtype']
    try:
        if itemtype=='Product':
            sourceobj=SourceList_CreateItems.objects.filter(updated_by_id=userid,item_type='Product').values()
            if len(sourceobj)>0:
                for i in range(0,len(sourceobj)):
                    basicobj=BasicCompanyDetails.objects.filter(updated_by_id=sourceobj[i].get('updated_by_id')).values()
                    if basicobj:
                        sourceobj[i].__setitem__('company_code',basicobj[0].get('company_code'))
                        sourceobj[i].__setitem__('company_name', basicobj[0].get('company_name'))
                    else:
                        sourceobj[i].__setitem__('company_code', "")
                        sourceobj[i].__setitem__('company_name', "")
                return Response({'status':200,'message':'Product Source List','data':sourceobj},status=status.HTTP_200_OK)
            else:
                return Response({'status': 204, 'message': 'Product Source Code Not Present'},status=status.HTTP_204_NO_CONTENT)
        elif itemtype=='Service':
            sourceobj=SourceList_CreateItems.objects.filter(updated_by_id=userid,item_type='Service').values()
            if len(sourceobj)>0:
                for i in range(0, len(sourceobj)):
                    basicobj = BasicCompanyDetails.objects.filter(
                        updated_by_id=sourceobj[i].get('updated_by_id')).values()
                    if basicobj:
                        sourceobj[i].__setitem__('company_code', basicobj[0].get('company_code'))
                        sourceobj[i].__setitem__('company_name', basicobj[0].get('company_name'))
                    else:
                        sourceobj[i].__setitem__('company_code', "")
                        sourceobj[i].__setitem__('company_name', "")
                return Response({'status':200,'message':'Service Source List','data':sourceobj},status=status.HTTP_200_OK)
            else:
                return Response({'status': 204, 'message': 'Service Source Code Not Present'},status=status.HTTP_204_NO_CONTENT)
        elif itemtype=='Equipment':
            sourceobj=SourceList_CreateItems.objects.filter(updated_by_id=userid,item_type='Equipment').values()
            if len(sourceobj)>0:
                for i in range(0, len(sourceobj)):
                    basicobj = BasicCompanyDetails.objects.filter(
                        updated_by_id=sourceobj[i].get('updated_by_id')).values()
                    if basicobj:
                        sourceobj[i].__setitem__('company_code', basicobj[0].get('company_code'))
                        sourceobj[i].__setitem__('company_name', basicobj[0].get('company_name'))
                    else:
                        sourceobj[i].__setitem__('company_code', "")
                        sourceobj[i].__setitem__('company_name', "")
                return Response({'status':200,'message':'Equipment Source List','data':sourceobj},status=status.HTTP_200_OK)
            else:
                return Response({'status': 204, 'message': 'Equipment Source Code Not Present'},status=status.HTTP_204_NO_CONTENT)
        elif itemtype=='Machinery':
            sourceobj=SourceList_CreateItems.objects.filter(updated_by_id=userid,item_type='Machinery').values()
            if len(sourceobj)>0:
                for i in range(0, len(sourceobj)):
                    basicobj = BasicCompanyDetails.objects.filter(
                        updated_by_id=sourceobj[i].get('updated_by_id')).values()
                    if basicobj:
                        sourceobj[i].__setitem__('company_code', basicobj[0].get('company_code'))
                        sourceobj[i].__setitem__('company_name', basicobj[0].get('company_name'))
                    else:
                        sourceobj[i].__setitem__('company_code', "")
                        sourceobj[i].__setitem__('company_name', "")
                return Response({'status':200,'message':'Machinery Source List','data':sourceobj},status=status.HTTP_200_OK)
            else:
                return Response({'status': 204, 'message': 'Machinery Source Code Not Present'},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'status':204,'message':'Mis Spelled itemtype name,Please check itemtype'},status=status.HTTP_204_NO_CONTENT)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
# @permission_classes((AllowAny,))
def source_list_advance_search(request):
    data = request.data
    itemcode = data['itemcode']
    itemname = data['itemname']
    itemdescription = data['itemdescription']
    uom = data['uom']
    presentcost = data['presentcost']
    targetcost = data['targetcost']
    annualconsumption = data['annualconsumption']
    department = data['department']
    priority=data['priority']
    userid=data['userid']
    try:
        sourceobj = SourceList_CreateItems.objects.filter(updated_by_id=userid,
                                                          item_code__icontains=itemcode,
                                                          item_name__icontains=itemname,
                                                          item_description__icontains=itemdescription,
                                                          uom__icontains=uom,
                                                          present_cost__icontains=presentcost,
                                                          target_cost__icontains=targetcost,
                                                          annual_consumption__icontains=annualconsumption,
                                                          department__icontains=department,
                                                          priority__icontains=priority

                                                          ).values()
        return Response({'status': 200, 'message': 'Source List Search Success', 'data': sourceobj}, status=200)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['post'])
# @permission_classes((AllowAny,))
def bidding_data_responses_count(request):
    data = request.data
    totalresponse = []
    accepted = 0
    rejected = 0
    pending = 0
    totalsent = 0
    rfxarray = []
    userid=data['userid']
    from_registration=data['from_registration']
    try:
        if from_registration=='False':
            uservendorrfxdetails = SelectVendorsForBiddingProduct.objects.filter(updated_by_id=userid,from_registration=from_registration).values()
            for i in range(0, len(uservendorrfxdetails)):
                if uservendorrfxdetails[i].get('rfq_number') not in rfxarray:
                    rfxarray.append(uservendorrfxdetails[i].get('rfq_number'))
            for i in range(0, len(rfxarray)):
                biddingbasicdatadetails = BuyerProductBidding.objects.filter(user_rfq_number=rfxarray[i],from_registration=from_registration).values()
                basicobj=BasicCompanyDetails.objects.filter(updated_by_id=userid).values()

                rfxdetails = SelectVendorsForBiddingProduct.objects.filter(rfq_number=rfxarray[i],from_registration=from_registration).values().order_by(
                    'rfq_number')
                for j in range(0, len(rfxdetails)):
                    totalsent = totalsent + 1
                    if (rfxdetails[j].get('vendor_status') == "Accept"):
                        accepted = accepted + 1
                    if (rfxdetails[j].get('vendor_status') == "Reject"):
                        rejected = rejected + 1
                    if (rfxdetails[j].get('vendor_status') == "Pending"):
                        pending = pending + 1

                if len(biddingbasicdatadetails)!=0:

                    totalresponse.append({'rfq_number': rfxarray[i],
                                      'rfq_title': biddingbasicdatadetails[0].get('product_rfq_title'),
                                      'rfq_type':biddingbasicdatadetails[0].get('product_rfq_type'),
                                      'total_sent': totalsent,
                                      'total_response': accepted + rejected,
                                      'pending': pending,
                                      'total_rejected': rejected,
                                      'total_accepted': accepted,
                                      'publish_date': biddingbasicdatadetails[0].get('product_publish_date'),
                                      'deadline_date': biddingbasicdatadetails[0].get('product_deadline_date'),
                                      'department_master': biddingbasicdatadetails[0].get('product_department'),
                                      'company_code':basicobj[0].get('company_code'),
                                      'company_name':basicobj[0].get('company_name'),
                                      'rfq_status':biddingbasicdatadetails[0].get('product_rfq_status')

                                      })

                pending = 0
                totalsent = 0
                accepted = 0
                rejected = 0
            return Response({'status': 200, 'message': 'Response List', 'data': totalresponse}, status=200)
        else:
            if from_registration == 'True':
                uservendorrfxdetails = SelectVendorsForBiddingProduct.objects.filter(updated_by_id=userid,
                                                                                     from_registration=from_registration).values()
                for i in range(0, len(uservendorrfxdetails)):
                    if uservendorrfxdetails[i].get('auto_rfq_number') not in rfxarray:
                        rfxarray.append(uservendorrfxdetails[i].get('auto_rfq_number'))
                for i in range(0, len(rfxarray)):
                    biddingbasicdatadetails = BuyerProductBidding.objects.get(product_rfq_number=rfxarray[i],
                                                                              from_registration=from_registration)
                    basicobj = BasicCompanyDetails.objects.filter(updated_by_id=userid).values()

                    rfxdetails = SelectVendorsForBiddingProduct.objects.filter(auto_rfq_number=rfxarray[i],
                                                                               from_registration=from_registration).values().order_by(
                        'rfq_number')
                    for j in range(0, len(rfxdetails)):
                        totalsent = totalsent + 1
                        if (rfxdetails[j].get('vendor_status') == "Accept"):
                            accepted = accepted + 1
                        if (rfxdetails[j].get('vendor_status') == "Reject"):
                            rejected = rejected + 1
                        if (rfxdetails[j].get('vendor_status') == "Pending"):
                            pending = pending + 1
                    totalresponse.append({'rfq_number': rfxarray[i],
                                          'rfq_title': biddingbasicdatadetails.product_rfq_title,
                                          'rfq_type': biddingbasicdatadetails.product_rfq_type,
                                          'total_sent': totalsent,
                                          'total_response': accepted + rejected,
                                          'pending': pending,
                                          'total_rejected': rejected,
                                          'total_accepted': accepted,
                                          'publish_date': biddingbasicdatadetails.product_publish_date,
                                          'deadline_date': biddingbasicdatadetails.product_deadline_date,
                                          'department_master': biddingbasicdatadetails.product_department,
                                          'company_code': basicobj[0].get('company_code'),
                                          'company_name': basicobj[0].get('company_name')

                                          })
                    print(biddingbasicdatadetails.product_rfq_title)
                    pending = 0
                    totalsent = 0
                    accepted = 0
                    rejected = 0
                return Response({'status': 200, 'message': 'Response List from registration', 'data': totalresponse}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['put'])
# @permission_classes((AllowAny,))
def status_vendor_accept(request):
    data = request.data
    rfq_number = data['rfq_number']
    userid = data['userid']
    try:
        basicobj = BasicCompanyDetails.objects.filter(updated_by_id=userid).values()
        vends = SelectVendorsForBiddingProduct.objects.filter(rfq_number__icontains=rfq_number,vendor_code=basicobj[0].get('company_code')).values().order_by('rfq_number')
        if len(vends)>0:
            for i in range(0, len(vends)):
                vendobj = SelectVendorsForBiddingProduct.objects.get(id=vends[i].get('id'))
                print(vendobj)
                if vendobj.vendor_status == 'Pending':
                    vendobj.vendor_status = 'Accept'
                    vendobj.save()
                    return Response(
                        {'status': 200, 'message': 'Status Accepted', 'data': vendobj.vendor_status},
                        status=200)
                else:
                    return Response({'status': 202, 'error': 'Already Accepted'}, status=202)
        return Response({'status':204,'message':'Not Present','data':vends},status=204)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['put'])
# @permission_classes((AllowAny,))
def status_vendor_reject(request):
    data = request.data
    rfq_number = data['rfq_number']
    userid = data['userid']
    try:
        basicobj=BasicCompanyDetails.objects.filter(updated_by_id=userid).values()
        vends = SelectVendorsForBiddingProduct.objects.filter(rfq_number__icontains=rfq_number,vendor_code=basicobj[0].get('company_code')).values().order_by('rfq_number')
        print(vends)
        if len(vends)>0:
            for i in range(0, len(vends)):
                vendobjvalues = SelectVendorsForBiddingProduct.objects.get(id=vends[i].get('id'))
                print(vendobjvalues)
                if vendobjvalues.vendor_status == 'Pending':
                    vendobjvalues.vendor_status = 'Reject'
                    vendobjvalues.save()
                    return Response(
                        {'status': 200, 'message': 'Status Rejected', 'data': vendobjvalues.vendor_status},
                        status=200)
                else:
                    return Response({'status': 202, 'error': 'Already Rejected'}, status=202)
        return Response({'status': 204, 'message': 'Not Present'}, status=204)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def selected_vendors_product_list(request):
    data = request.data
    userid = data['userid']
    rfqnumber = data['rfqnumber']
    selectarray = []
    try:
        selectobj = SelectVendorsForBiddingProduct.objects.filter(updated_by_id=userid, rfq_number=rfqnumber).values().order_by(
            'vendor_code')
        print(len(selectobj))
        if len(selectobj)>0:
            # print('yes')
            for i in range(0, len(selectobj)):
                # print(len(selectobj),selectobj[i].get('vendor_code'))

                basicobj = BasicCompanyDetails.objects.filter(company_code=selectobj[i].get('vendor_code')).values()
                if len(basicobj)>0:
                    billobj=BillingAddress.objects.filter(updated_by_id=basicobj[0].get('updated_by_id')).values()
                    # print(basicobj[0].get('updated_by_id'))
                    regobj = SelfRegistration.objects.filter(id=basicobj[0].get('updated_by_id')).values()
                    selectarray.append({'rfq_number': selectobj[i].get('rfq_number'),
                                        'vendorcode': basicobj[0].get('company_code'),
                                        'company_name': basicobj[0].get('company_name'),
                                        'userid': selectobj[i].get('updated_by_id'),
                                        'vendor_status': selectobj[i].get('vendor_status'),
                                        'company_type': basicobj[0].get('company_type'),
                                        'nature_of_business': regobj[0].get('nature_of_business'),
                                        'bill_state': billobj[0].get('bill_state'),
                                        'email': regobj[0].get('username'),
                                        'phoneno': regobj[0].get('phone_number')
                                        })
                else:
                    pass

            return Response({'status': 200, 'message': 'Selected Vendors Of Products List', 'data': selectarray},
                            status=200)
        else:
            return Response({'status': 204, 'message': 'No content'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def accepted_response_list(request):
    data = request.data
    rfq_number = data['rfq_number']
    updated_by = data['updated_by']
    responses = data['responses']
    rfqtype=data['rfqtype']
    responselistarray = []

    try:
        if responses == 'Accept' and rfqtype=='Product':
            vendobj = SelectVendorsForBiddingProduct.objects.filter(rfq_number=rfq_number, updated_by_id=updated_by,
                                                               vendor_status=responses,rfq_type=rfqtype).values()
            if len(vendobj) > 0:
                for i in range(0, len(vendobj)):
                    ratesum = 0
                    orderqtsum = 0
                    discountsum = 0
                    ccode = vendobj[i].get('vendor_code')
                    basicobj = BasicCompanyDetails.objects.filter(company_code=ccode).values()
                    cname = basicobj[0].get('company_name')
                    productdetailsvalue = VendorBiddingBuyerProductDetails.objects.filter(vendor_rfq_number=rfq_number,
                                                                                      vendor_code=ccode).values()
                    if len(productdetailsvalue) == 0:
                        raise ValueError({'message': 'vendor not present in vendor product details', 'status': 204})
                    else:

                        for i in range(0, len(productdetailsvalue)):
                            orderqtsum = orderqtsum + int(productdetailsvalue[i].get('buyer_quantity'))
                            ratesum = ratesum + int(productdetailsvalue[i].get('vendor_rate'))
                            discountsum = discountsum + int(productdetailsvalue[i].get('vendor_discount'))
                        responselistarray.append({'rfq_number': rfq_number,
                                                  'order_quantity': orderqtsum,
                                                  'total_discount': discountsum,
                                                  'total_rate': ratesum,
                                                  'final_amount': productdetailsvalue[i].get('vendor_final_amount'),
                                                  'total_amount': productdetailsvalue[i].get('vendor_total_amount'),
                                                  'company_code': ccode,
                                                  'company_name': cname
                                                  })
                return Response({'status': 200, 'message': 'Response List Product', 'data': responselistarray},
                                status=200)
            else:
                return Response({'status': 204, 'message': 'No Product  details found'}, status=204)

        elif responses=='Accept' and rfqtype=='Service':
            vendobj = SelectVendorsForBiddingProduct.objects.filter(rfq_number=rfq_number, updated_by_id=updated_by,
                                                                    vendor_status=responses, rfq_type=rfqtype).values()
            if len(vendobj) > 0:
                for i in range(0, len(vendobj)):
                    ratesum = 0
                    orderqtsum = 0
                    discountsum = 0
                    ccode = vendobj[i].get('vendor_code')
                    basicobj = BasicCompanyDetails.objects.filter(company_code=ccode).values()
                    cname = basicobj[0].get('company_name')
                    productdetailsvalue = VendorBiddingBuyerProductDetails.objects.filter(vendor_rfq_number=rfq_number,
                                                                                          vendor_code=ccode).values()
                    if len(productdetailsvalue) == 0:
                        raise ValueError({'message': 'vendor not present in vendor product details', 'status': 204})
                    else:

                        for i in range(0, len(productdetailsvalue)):
                            orderqtsum = orderqtsum + int(productdetailsvalue[i].get('buyer_quantity'))
                            ratesum = ratesum + int(productdetailsvalue[i].get('vendor_rate'))
                            discountsum = discountsum + int(productdetailsvalue[i].get('vendor_discount'))
                        responselistarray.append({'rfq_number': rfq_number,
                                                  'order_quantity': orderqtsum,
                                                  'total_discount': discountsum,
                                                  'total_rate': ratesum,
                                                  'final_amount': productdetailsvalue[i].get('vendor_final_amount'),
                                                  'total_amount': productdetailsvalue[i].get('vendor_total_amount'),
                                                  'company_code': ccode,
                                                  'company_name': cname
                                                  })
                return Response({'status': 200, 'message': 'Response List Service', 'data': responselistarray},
                                status=200)
            else:
                return Response({'status': 204, 'message': 'No Service details found'}, status=204)


        elif responses == 'Accept' and rfqtype == 'Machinary & equipments':
            vendobj = SelectVendorsForBiddingProduct.objects.filter(rfq_number=rfq_number, updated_by_id=updated_by,
                                                                    vendor_status=responses, rfq_type=rfqtype).values()
            if len(vendobj) > 0:
                for i in range(0, len(vendobj)):
                    ratesum = 0
                    orderqtsum = 0
                    discountsum = 0
                    ccode = vendobj[i].get('vendor_code')
                    basicobj = BasicCompanyDetails.objects.filter(company_code=ccode).values()
                    cname = basicobj[0].get('company_name')
                    productdetailsvalue = VendorBiddingBuyerProductDetails.objects.filter(vendor_rfq_number=rfq_number,
                                                                                          vendor_code=ccode).values()
                    if len(productdetailsvalue) == 0:
                        raise ValueError({'message': 'vendor not present in vendor product details', 'status': 204})
                    else:

                        for i in range(0, len(productdetailsvalue)):
                            orderqtsum = orderqtsum + int(productdetailsvalue[i].get('buyer_quantity'))
                            ratesum = ratesum + int(productdetailsvalue[i].get('vendor_rate'))
                            discountsum = discountsum + int(productdetailsvalue[i].get('vendor_discount'))
                        responselistarray.append({'rfq_number': rfq_number,
                                                  'order_quantity': orderqtsum,
                                                  'total_discount': discountsum,
                                                  'total_rate': ratesum,
                                                  'final_amount': productdetailsvalue[i].get('vendor_final_amount'),
                                                  'total_amount': productdetailsvalue[i].get('vendor_total_amount'),
                                                  'company_code': ccode,
                                                  'company_name': cname
                                                  })
                return Response({'status': 200, 'message': 'Response List Service', 'data': responselistarray},
                                status=200)
            else:
                return Response({'status': 204, 'message': 'No Service details found'}, status=204)


        else:
            return Response({'status': 202, 'message': 'No data present for this response or mis-spelled'}, status=202)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
def pending_response_list(request):
    data = request.data
    pendingarray = []
    rfq_number = data['rfq_number']
    responses = data['responses']
    updated_by = data['updated_by']

    try:
        if responses == 'Pending':
            vendobj = SelectVendorsForBiddingProduct.objects.filter(rfq_number=rfq_number, updated_by_id=updated_by,
                                                               vendor_status=responses).values()
            if len(vendobj)>0:
                for i in range(0, len(vendobj)):
                    ccode = vendobj[i].get('vendor_code')
                    print(ccode)
                    rfq_number = vendobj[i].get('rfq_number')
                    print(rfq_number)
                    basicobj = BasicCompanyDetails.objects.filter(company_code=ccode).values('company_name')
                    print(basicobj)
                    for i in range(0, len(basicobj)):
                        pendingarray.append({'company_code': ccode,
                                             'company_name': basicobj[i].get('company_name'),
                                             'rfq_number': rfq_number
                                             })
                return Response({'status': 200, 'message': 'Pending List', 'data': pendingarray}, status=200)
            else:
                return Response({'status': 204, 'message': 'vendors not present'}, status=204)
        else:
            return Response({'status':204,'message':"Check response spelling is mis-spelled or entered response is not correct"},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def rejected_response_list(request):
    data=request.data
    rfq_number = data['rfq_number']
    responses = data['responses']
    updated_by = data['updated_by']
    rejectedarray = []

    try:
        if responses == 'Reject':
            vendobj = SelectVendorsForBiddingProduct.objects.filter(rfq_number=rfq_number, updated_by_id=updated_by,
                                                                    vendor_status=responses).values()
            if len(vendobj)>0:
                for i in range(0, len(vendobj)):
                    ccode = vendobj[i].get('vendor_code')
                    print(ccode)
                    rfq_number = vendobj[i].get('rfq_number')
                    print(rfq_number)
                    basicobj = BasicCompanyDetails.objects.filter(company_code=ccode).values('company_name')
                    print(basicobj)
                    for i in range(0, len(basicobj)):
                        rejectedarray.append({'company_code': ccode,
                                             'company_name': basicobj[i].get('company_name'),
                                             'rfq_number': rfq_number
                                             })
                return Response({'status': 200, 'message': 'Rejected List', 'data': rejectedarray}, status=200)
            else:
                return Response({'status': 204, 'message': 'vendors not present'}, status=204)
        else:
            return Response({'status': 204, 'message': "Check response spelling is mis-spelled or entered response is not correct"},status=204)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def get_ccode_by_userid(request):
    data = request.data
    basicarray = []
    try:
        basicobj = BasicCompanyDetails.objects.filter(updated_by_id=data['userid']).values()
        if len(basicobj) > 0:
            regobj = SelfRegistration.objects.get(id=data['userid'])
            basicarray.append({'company_code': basicobj[0].get('company_code'),
                               'user_type': regobj.user_type,
                               'cname':basicobj[0].get('company_name')
                               })

            return Response({'status': 200, 'message': 'Company Code', 'data': basicarray}, status=200)
        else:
            return Response({'status': 204, 'message': 'company code not present'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['post'])
@permission_classes((AllowAny,))
def get_ccode_by_userid_without_tk(request):
    data = request.data
    basicarray = []
    key=data['key']
    try:
        if key=='vsinadmindb':
            basicobj = BasicCompanyDetails.objects.filter(updated_by_id=data['userid']).values('company_code')
            if len(basicobj) > 0:
                regobj = SelfRegistration.objects.get(id=data['userid'])
                basicarray.append({'company_code': basicobj[0].get('company_code'),
                                   'user_type': regobj.user_type,
                                   'userid':regobj.id
                                   })

                return Response({'status': 200, 'message': 'Company Code', 'data': basicarray}, status=200)
            else:
                return Response({'status': 204, 'message': 'company code not present'}, status=204)
        else:
            return Response({'status': 400, 'message':'bad request'}, status=400)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)






@api_view(['post'])
@permission_classes((AllowAny,))
def price_analysis_product(request):
    data = request.data
    resarray = []
    rfq_number = data['rfq_number']
    vendor_code = data['vendor_code']

    try:
        biddingbuyerproductdetailsobj = BiddingBuyerProductDetails.objects.filter(buyer_rfq_number=rfq_number).values()
        if len(biddingbuyerproductdetailsobj)>0:
            for i in range(0, len(biddingbuyerproductdetailsobj)):
                resarray.append({'product_code': biddingbuyerproductdetailsobj[i].get('buyer_item_code'),
                                 'product_name': biddingbuyerproductdetailsobj[i].get('buyer_item_name'),
                                 'Material_Description': biddingbuyerproductdetailsobj[i].get('buyer_item_description'),
                                 'UOM': biddingbuyerproductdetailsobj[i].get('buyer_uom'),
                                 'Quantity': biddingbuyerproductdetailsobj[i].get('buyer_quantity'),
                                 'item_type':biddingbuyerproductdetailsobj[i].get('item_type')
                                 })

                vpdetails = VendorBiddingBuyerProductDetails.objects.filter(vendor_rfq_number=rfq_number, vendor_code__in=vendor_code,
                                                                            vendor_item_code=biddingbuyerproductdetailsobj[
                                                                                i].get('buyer_item_code')).values().order_by('vendor_code')

                for j in range(0, len(vpdetails)):

                    resarray[i].setdefault('ccode' + str(j), vpdetails[j].get('vendor_code'))
                    resarray[i].setdefault('rate' + str(j), vpdetails[j].get('vendor_rate'))
                    resarray[i].setdefault('tax' + str(j), vpdetails[j].get('vendor_tax'))
                    resarray[i].setdefault('discount' + str(j), vpdetails[j].get('vendor_discount'))
                    resarray[i].setdefault('totalcost' + str(j), vpdetails[j].get('vendor_final_amount'))
                    resarray[i].setdefault('total_all_cost' + str(j), vpdetails[j].get('vendor_total_amount'))
                print("---------------------------------")
                # for j in range(0,len())

            return Response({'status': 200, 'message': 'Product Price Analysis', 'data': resarray}, status=200)
        else:
            return Response({'status': 204, 'message': 'Buyer Product Details Not Present'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def price_analysis_service(request):
    data = request.data
    resarray = []
    rfq_number = data['rfq_number']
    vendor_code = data['vendor_code']
    rfq_type=data['rfq_type']

    try:
        if rfq_type=='Service':
            biddingbuyerproductdetailsobj = BiddingBuyerProductDetails.objects.filter(buyer_rfq_number=rfq_number,buyer_item_type='Service').values()
            if len(biddingbuyerproductdetailsobj)>0:
                # print(biddingbuyerproductdetailsobj)
                for i in range(0, len(biddingbuyerproductdetailsobj)):
                    resarray.append({'product_code': biddingbuyerproductdetailsobj[i].get('buyer_item_code'),
                                     'product_name': biddingbuyerproductdetailsobj[i].get('buyer_item_name'),
                                     'Material_Description': biddingbuyerproductdetailsobj[i].get('buyer_item_description'),
                                     'UOM': biddingbuyerproductdetailsobj[i].get('buyer_uom'),
                                     'Quantity': biddingbuyerproductdetailsobj[i].get('buyer_quantity')})

                    vpdetails = VendorBiddingBuyerProductDetails.objects.filter(vendor_rfq_number=rfq_number, vendor_code__in=vendor_code,
                                                                                vendor_item_code=biddingbuyerproductdetailsobj[
                                                                                    i].get('buyer_item_code'),vendor_item_type='Service').values().order_by('vendor_code')

                    for j in range(0, len(vpdetails)):

                        resarray[i].setdefault('ccode' + str(j), vpdetails[j].get('vendor_code'))
                        resarray[i].setdefault('rate' + str(j), vpdetails[j].get('vendor_rate'))
                        resarray[i].setdefault('tax' + str(j), vpdetails[j].get('vendor_tax'))
                        resarray[i].setdefault('discount' + str(j), vpdetails[j].get('vendor_discount'))
                        resarray[i].setdefault('totalcost' + str(j), vpdetails[j].get('vendor_final_amount'))
                        resarray[i].setdefault('total_all_cost' + str(j), vpdetails[j].get('vendor_total_amount'))
                    print("---------------------------------")
                    # for j in range(0,len())

                return Response({'status': 200, 'message': 'Product Price Analysis', 'data': resarray}, status=200)
            else:
                return Response({'status': 204, 'message': 'Buyer Product Details Not Present'}, status=204)
        else:
            return Response({'status': 202, 'message': 'product rfq_type is mis-spelled or not present'}, status=202)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


# -----------------------------------PRICE ANALYSIS MACHINARY-----------------------------------------------
@api_view(['post'])
def price_analysis_machinary(request):
    data = request.data
    resarray = []
    rfq_number = data['rfq_number']
    vendor_code = data['vendor_code']
    rfq_type = data['rfq_type']

    try:
        if rfq_type == 'Machinary & equipments':
            biddingbuyerproductdetailsobj = BiddingBuyerProductDetails.objects.filter(buyer_rfq_number=rfq_number,
                                                                                      buyer_item_type='Machinary & equipments').values()
            if len(biddingbuyerproductdetailsobj) > 0:
                # print(biddingbuyerproductdetailsobj)
                for i in range(0, len(biddingbuyerproductdetailsobj)):
                    resarray.append({'product_code': biddingbuyerproductdetailsobj[i].get('buyer_item_code'),
                                     'product_name': biddingbuyerproductdetailsobj[i].get('buyer_item_name'),
                                     'Material_Description': biddingbuyerproductdetailsobj[i].get(
                                         'buyer_item_description'),
                                     'UOM': biddingbuyerproductdetailsobj[i].get('buyer_uom'),
                                     'Quantity': biddingbuyerproductdetailsobj[i].get('buyer_quantity')})

                    vpdetails = VendorBiddingBuyerProductDetails.objects.filter(vendor_rfq_number=rfq_number,
                                                                                vendor_code__in=vendor_code,
                                                                                vendor_item_code=
                                                                                biddingbuyerproductdetailsobj[
                                                                                    i].get('buyer_item_code'),
                                                                                vendor_item_type='Machinary & equipments').values().order_by(
                        'vendor_code')

                    for j in range(0, len(vpdetails)):
                        resarray[i].setdefault('ccode' + str(j), vpdetails[j].get('vendor_code'))
                        resarray[i].setdefault('rate' + str(j), vpdetails[j].get('vendor_rate'))
                        resarray[i].setdefault('tax' + str(j), vpdetails[j].get('vendor_tax'))
                        resarray[i].setdefault('discount' + str(j), vpdetails[j].get('vendor_discount'))
                        resarray[i].setdefault('totalcost' + str(j), vpdetails[j].get('vendor_final_amount'))
                        resarray[i].setdefault('total_all_cost' + str(j), vpdetails[j].get('vendor_total_amount'))
                    print("---------------------------------")
                    # for j in range(0,len())

                return Response({'status': 200, 'message': 'Product Price Analysis', 'data': resarray}, status=200)
            else:
                return Response({'status': 204, 'message': 'Buyer Product Details Not Present'}, status=204)
        else:
            return Response({'status': 202, 'message': 'product rfq_type is mis-spelled or not present'}, status=202)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def buyer_bidlist_based_on_rfqnumber(request):
    data = request.data
    try:
        bidrfqobj = BuyerProductBidding.objects.filter(user_rfq_number=data['rfq_number']).values().order_by('product_bidding_id')
        if len(bidrfqobj)>0:
            return Response({'status': 200, 'message': 'Buyer Bidding List', 'data': bidrfqobj}, status=200)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def vendor_query_description(request):
    data = request.data
    rfq_number = data['rfq_number']
    resarray = []
    try:
        vendorbidobj = VendorRfqTermsDescription.objects.filter(vendor_rfq_number=rfq_number).values()
        if len(vendorbidobj)>0:
            for i in range(0, len(vendorbidobj)):
                basicobj = BasicCompanyDetails.objects.filter(updated_by_id=vendorbidobj[i].get('updated_by_id')).values()
                resarray.append({'cname':basicobj[0].get('company_name'),
                                 'vendor_terms':vendorbidobj[i].get('vendor_terms'),
                                 'vendor_description':vendorbidobj[i].get('vendor_description'),
                                 'vendor_response':vendorbidobj[i].get('vendor_response')
                                 })
            return Response({'status': 200, 'message': 'Success', 'data': resarray}, status=200)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=204)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
def company_names_get_by_ccode(request):
    data = request.data
    ccodearray = data['ccodearray']
    cnamearray = []
    try:
        basicdata = BasicCompanyDetails.objects.filter(company_code__in=ccodearray).order_by('company_code').values()
        if len(basicdata)>0:
            for i in range(0, len(basicdata)):
                print(basicdata[i].get('company_code'))
                cnamearray.append({'compcode': basicdata[i].get('company_code'),
                                   'compname': basicdata[i].get('company_name')})

            return Response({'status': 200, 'message': 'Success', 'data': cnamearray}, status=200)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=204)

    except Exception as e:
        return Response({'sttaus': 500, 'error': str(e)}, status=500)





@api_view(['post'])
def award_total_count_product(request):
    data = request.data
    rfq_number = data['rfq_number']
    productvendordetails = data['productvendordetails']
    totalproductarray = []
    userid = data['userid']
    try:
        if productvendordetails:
            for i in range(0, len(productvendordetails)):
                totalamountsum = 0
                ratesum = 0
                orderqtsum = 0
                discountsum = 0
                pcode = productvendordetails[i].get('productcode')
                ccode = productvendordetails[i].get('vendorcode')
                for product in pcode:
                    for codes in ccode:
                        print('ok----')
                        bidobj = VendorProductBidding.objects.get(vendor_product_rfq_number=rfq_number, vendor_code=codes)
                        print(bidobj.vendor_product_rfq_number)
                        basicobj = BasicCompanyDetails.objects.get(company_code=codes)
                        cname = basicobj.company_name
                        rfq_number = bidobj.vendor_product_rfq_number
                        # frieght = bidobj.freight_transportation
                        # pandf = bidobj.packaging_forwarding
                        publishdate = bidobj.vendor_product_publish_date
                        deadlinedate = bidobj.vendor_product_deadline_date
                        rfqtitle = bidobj.vendor_product_rfq_title
                        rfqstatus = bidobj.vendor_product_rfq_status
                    productdetails = VendorBiddingBuyerProductDetails.objects.get(vendor_rfq_number=rfq_number,
                                                                                  vendor_code=codes,
                                                                                  vendor_item_code=product)
                    if not productdetails:
                        return Response({'status': 204, 'message': 'No product details of vendor'}, status=204)

                    discountsum = discountsum + int(productdetails.vendor_discount)
                    totalamountsum = totalamountsum + float(productdetails.vendor_total_amount)
                    orderqtsum = orderqtsum + int(productdetails.buyer_quantity)
                    ratesum = ratesum + int(productdetails.vendor_rate)
                    pname = productdetails.vendor_item_name
                    pdesc = productdetails.vendor_item_description
                    # bidquantitysum=bidquantitysum+int(productdetails.bidquantity)
                print('-----------ok---------------')
                totalproductarray.append({'rfq_number': rfq_number,
                                          'order_quantity': orderqtsum,
                                          'total_rate': ratesum,
                                          'total_discount': discountsum,
                                          'total_amount': totalamountsum,
                                          'vendorcode': codes,
                                          'company_name': cname,
                                          # 'frieght_cost': frieght,
                                          # 'packaging_and_forwarding': pandf,
                                          'publish_date': publishdate,
                                          'deadline_date': deadlinedate,
                                          'rfq_title': rfqtitle,

                                          })



            # else:
                # print(len(awardobj))
                # return Response({'status':204,'message':'already present'},status=204)

            return Response({'status': 200, 'message': 'List Success', 'data': totalproductarray}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def award_get_list_of_vendor(request):
    data = request.data
    # vendorcode = data['vendorcode']
    userid=data['userid']
    awardarray = []
    try:
        # strvendor = str(vendorcode)
        # print(strvendor)
        awardobj = Awards.objects.filter(updated_by=userid).values()
        print(awardobj)
        if len(awardobj) > 0:
            for i in range(0,len(awardobj)):
                awardeecode = awardobj[i].get('company_code')
                basicobj = BasicCompanyDetails.objects.filter(company_code=awardeecode).values()
                # print(basicobj, 'userbasic')
                awardarray.append({
                    'rfq_number':awardobj[i].get('rfq_number'),
                   'rfq_title': awardobj[i].get('rfq_title'),
                    'company_code': basicobj[0].get('company_code'),
                    'company_name':basicobj[0].get('company_name'),
                   'awarded_date': awardobj[i].get('awarded_date'),
                   'publish_date': awardobj[i].get('publish_date'),
                   'deadline_date': awardobj[i].get('deadline_date'),
                   'awardstatus': awardobj[i].get('awardstatus'),
                   # 'frieght_cost': awardobj[i].get('frieght_cost'),
                   # 'p_f_charge': awardobj[i].get('p_f_charge'),
                   'order_quantity': awardobj[i].get('order_quantity'),
                   'totalamount': awardobj[i].get('totalamount'),
                   'product_code': awardobj[i].get('product_code')
                })
            # return Response({'status': 200, 'message': 'ok', 'data': awardarray}, status=200)
        else:
            return Response({'status': 202, 'message': 'No data'}, status=202)
        return Response({'status': 200, 'message': 'ok', 'data': awardarray}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


class BiddingBuyerServiceDetailsView(viewsets.ModelViewSet):
    queryset = BiddingBuyerServiceDetails.objects.all()
    serializer_class = BiddingBuyerServiceDetailsSerializer
    # permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        servicedetails = request.data['servicedetails']
        service_buyer_rfq_number = request.data.get('service_buyer_rfq_number', None)
        userid = request.data.get('userid', None)
        from_registration = request.data.get('from_registration', None)
        try:
            bidobj=BuyerProductBidding.objects.get(user_rfq_number=service_buyer_rfq_number)
            for i in range(0, len(servicedetails)):
                BiddingBuyerServiceDetails.objects.create(service_buyer_rfq_number=service_buyer_rfq_number,
                                                          service_buyer_item_code=servicedetails[i].get(
                                                              'buyer_service_item_code'),
                                                          service_buyer_item_name=servicedetails[i].get(
                                                              'buyer_service_item_name'),
                                                          service_buyer_item_description=servicedetails[i].get(
                                                              'buyer_service_item_description'),
                                                          service_buyer_uom=servicedetails[i].get('buyer_service_uom'),
                                                          service_buyer_category=servicedetails[i].get(
                                                              'buyer_service_category'),
                                                          service_buyer_quantity=servicedetails[i].get(
                                                              'service_quantity'),
                                                          service_buyer_document=servicedetails[i].get(
                                                              'buyer_service_document'),
                                                          service_item_type=servicedetails[i].get('buyer_service_item_type'),
                                                          updated_by=SelfRegistration.objects.get(id=userid),
                                                          auto_rfq_number=bidobj.product_rfq_number,
                                                          from_registration=from_registration,
                                                          created_by=userid)

            return Response({'status': 201, 'message': 'Service Details Are Created'}, status=201)
        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)

    def get_queryset(self):
        buyerservicedetailsobj = BiddingBuyerServiceDetails.objects.filter(
            updated_by=self.request.GET.get('updated_by')).order_by('id')
        if buyerservicedetailsobj:
            return buyerservicedetailsobj
        raise ValidationError(
            {'message': 'Buyer Bidding Service details of particular user id is not exist', 'status': 204})



class BiddingBuyerMachinaryDetailsView(viewsets.ModelViewSet):
    queryset = BiddingBuyerMachinaryDetails.objects.all()
    serializer_class = BiddingBuyerMachinaryDetailsSerializer
    # permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        machinarydetails = request.data['machinarydetails']
        machinary_buyer_rfq_number = request.data.get('machinary_buyer_rfq_number', None)
        from_registration = request.data.get('from_registration', None)
        userid = request.data.get('userid', None)
        try:
            bidobj = BuyerProductBidding.objects.filter(user_rfq_number=machinary_buyer_rfq_number).values()
            for i in range(0, len(machinarydetails)):
                BiddingBuyerMachinaryDetails.objects.create(machinary_buyer_rfq_number=machinary_buyer_rfq_number,
                                                          machinary_buyer_item_code=machinarydetails[i].get('buyer_machinary_item_code'),
                                                          machinary_buyer_item_name=machinarydetails[i].get('buyer_machinary_item_name'),
                                                          machinary_buyer_item_description=machinarydetails[i].get(
                                                              'buyer_machinary_item_description'),
                                                          machinary_buyer_uom=machinarydetails[i].get('buyer_machinary_uom'),
                                                          machinary_buyer_category=machinarydetails[i].get('buyer_machinary_category'),
                                                          machinary_buyer_quantity=machinarydetails[i].get('machinary_quantity'),
                                                          machinary_buyer_document=machinarydetails[i].get('buyer_machinary_document'),
                                                          machinary_item_type=machinarydetails[i].get('buyer_machinary_item_type'),
                                                          updated_by=SelfRegistration.objects.get(id=userid),
                                                            auto_rfq_number=bidobj[0].get('product_rfq_number'),
                                                            from_registration=from_registration,
                                                          created_by=userid)

            return Response({'status': 201, 'message': 'Machinary Details Are Created'}, status=201)
        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)

    def get_queryset(self):
        buyermachinarydetailsobj = BiddingBuyerMachinaryDetails.objects.filter(
            updated_by=self.request.GET.get('updated_by')).order_by('id')
        if buyermachinarydetailsobj:
            return buyermachinarydetailsobj
        raise ValidationError(
            {'message': 'Buyer Bidding Machinary details of particular user id is not exist', 'status': 204})


@api_view(['post'])
def fetch_buyer_service_details_by_userid_rfq(request):
    data=request.data
    rfqnumber=data['rfq_number']
    try:
        buyerservice=BiddingBuyerServiceDetails.objects.filter(service_buyer_rfq_number=rfqnumber).values().order_by('id')
        if len(buyerservice)>0:
            return Response({'status':200,'message':'Buyer Service Bidding Details','data':buyerservice},status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'Buyer Service Bidding Details Not Present'},
                    status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def fetch_buyer_machinary_details_by_userid_rfq(request):
    data=request.data
    rfqnumber=data['rfq_number']
    try:
        buyermachinary=BiddingBuyerMachinaryDetails.objects.filter(machinary_buyer_rfq_number=rfqnumber).values().order_by('id')
        if len(buyermachinary)>0:
            return Response({'status':200,'message':'Buyer Machinary Bidding Details','data':buyermachinary},status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'Buyer Machinary Bidding Details Not Present'},
                    status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


class AwardViewSet(viewsets.ModelViewSet):
    queryset = Awards.objects.all()
    serializer_class = AwardsSerializer
    # permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        awardobj = Awards.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by('id')
        if awardobj:
            return awardobj
        raise ValidationError(
            {'message': 'Award Product  details of particular user id is not exist', 'status': 204})

class ServiceAwardViewSet(viewsets.ModelViewSet):
    queryset = ServiceAwards.objects.all()
    serializer_class = ServiceAwardsSerializer
    # permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        awardobj = ServiceAwards.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by('id')
        if awardobj:
            return awardobj
        raise ValidationError(
            {'message': 'Award Service  details of particular user id is not exist', 'status': 204})

class MachinaryAwardViewSet(viewsets.ModelViewSet):
    queryset = Awards.objects.all()
    serializer_class = MachinaryAwardsSerializer
    # permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        awardobj = MachinaryAwards.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by('id')
        if awardobj:
            return awardobj
        raise ValidationError(
            {'message': 'Award Machinary  details of particular user id is not exist', 'status': 204})

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    parser = [MultiPartParser]

    def create(self, request, *args, **kwargs):
        rfq_number = request.data.get('rfq_number', None)
        vendorcode = request.data.get('vendorcode', None)
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key[
            'api-key'] = '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'
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
        }
        if request.data['rfq_type'] == 'Product':
            awardobj = Awards.objects.filter(rfq_number=rfq_number, company_code=vendorcode).values()
            ccode = awardobj[0].get('company_code')
            quantity = awardobj[0].get('buyer_bid_quantity')
            itemstotal = awardobj[0].get('product_code')
            print(len(itemstotal), 'length')
            basicobj = BasicCompanyDetails.objects.get(company_code=ccode)
            regobj = SelfRegistration.objects.get(id=basicobj.updated_by_id)
            print(regobj.username, 'ok')
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": regobj.username, "name": regobj.contact_person}],
                template_id=23, params={
                    "rfqnumber": rfq_number,
                    "podate": request.data['PO_date'],
                    "ponumber": request.data['PO_num'],
                    "poexpiry": request.data['PO_expirydate'],
                    "quantity": str(quantity),
                    'items': str(len(itemstotal)),
                    "companyname": basicobj.company_name
                },
                headers=headers,
                subject='PO Confirm'
            )  # SendSmtpEmail | Values to send a transactional email
            # Send a transactional email
            api_response = api_instance.send_transac_email(send_smtp_email)
            print(api_response)

        elif request.data['rfq_type'] == 'Service':
            awardobj = Awards.objects.filter(rfq_number=rfq_number, company_code=vendorcode).values()
            ccode = awardobj[0].get('company_code')
            quantity = awardobj[0].get('buyer_bid_quantity')
            itemstotal = awardobj[0].get('product_code')
            print(len(itemstotal), 'length')
            basicobj = BasicCompanyDetails.objects.get(company_code=ccode)
            regobj = SelfRegistration.objects.get(id=basicobj.updated_by_id)
            print(regobj.username, 'ok')
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": regobj.username, "name": regobj.contact_person}],
                template_id=23, params={
                    "rfqnumber": rfq_number,
                    "podate": request.data['PO_date'],
                    "ponumber": request.data['PO_num'],
                    "poexpiry": request.data['PO_expirydate'],
                    "quantity": str(quantity),
                    'items': str(len(itemstotal)),
                    "companyname": basicobj.company_name
                },
                headers=headers,
                subject='PO Confirm'
            )  # SendSmtpEmail | Values to send a transactional email
            # Send a transactional email
            api_response = api_instance.send_transac_email(send_smtp_email)
            print(api_response)
        elif request.data['rfq_type'] == 'Machinary & equipments':
            awardobj = Awards.objects.filter(rfq_number=rfq_number, company_code=vendorcode).values()
            ccode = awardobj[0].get('company_code')
            quantity = awardobj[0].get('buyer_bid_quantity')
            itemstotal = awardobj[0].get('product_code')
            print(len(itemstotal), 'length')
            basicobj = BasicCompanyDetails.objects.get(company_code=ccode)
            regobj = SelfRegistration.objects.get(id=basicobj.updated_by_id)
            print(regobj.username, 'ok')
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": regobj.username, "name": regobj.contact_person}],
                template_id=23, params={
                    "rfqnumber": rfq_number,
                    "podate": request.data['PO_date'],
                    "ponumber": request.data['PO_num'],
                    "poexpiry": request.data['PO_expirydate'],
                    "quantity": str(quantity),
                    'items': str(len(itemstotal)),
                    "companyname": basicobj.company_name
                },
                headers=headers,
                subject='PO Confirm'
            )  # SendSmtpEmail | Values to send a transactional email
            # Send a transactional email
            api_response = api_instance.send_transac_email(send_smtp_email)
            print(api_response)
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        poobj = PurchaseOrder.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by('id')
        if poobj:
            return poobj
        raise ValidationError(
            {'message': 'Purchase Order details of particular user id is not exist', 'status': 204})


@api_view(['post'])
def award_product_create(request):
    data=request.data
    rfq_number = data['rfq_number']
    productvendordetails = data['productvendordetails']
    totalproductarray = []
    userid = data['userid']
    rfq_type=data['rfq_type']
    try:
        award_obj=Awards.objects.filter(rfq_number=rfq_number).values()
        if len(award_obj)==0:
            if productvendordetails:
                for i in range(0, len(productvendordetails)):
                    totalamountsum = 0
                    ratesum = 0
                    orderqtsum = 0
                    discountsum = 0
                    vendorbidquantitysum=0
                    parrray=[]
                    pdescarray=[]
                    pcode = productvendordetails[i].get('productcode')
                    print(type(pcode))

                    ccode = productvendordetails[i].get('vendorcode')
                    for product in pcode:
                        pass
                        for codes in ccode:
                            print('ok----')
                            bidobj = VendorProductBidding.objects.get(vendor_user_rfq_number=rfq_number,vendor_code=codes)
                            print(bidobj, 'fsds')
                            basicobj = BasicCompanyDetails.objects.get(company_code=codes)
                            cname = basicobj.company_name
                            updatedby=basicobj.updated_by_id
                            rfq_number = bidobj.vendor_user_rfq_number
                            print(rfq_number,'rfqqqqqqqq')
                            publishdate = bidobj.vendor_product_publish_date
                            deadlinedate = bidobj.vendor_product_deadline_date
                            rfqtitle = bidobj.vendor_product_rfq_title
                            rfqstatus = bidobj.vendor_product_rfq_status
                        print(codes,'d')
                        productdetails=VendorBiddingBuyerProductDetails.objects.get(vendor_rfq_number=rfq_number,vendor_item_code=product,vendor_code=codes)
                        print(productdetails,'----------')
                        
                        if not productdetails:
                            return Response({'status': 204, 'message': 'No product details of vendor'}, status=204)

                        discountsum = discountsum + int(productdetails.vendor_discount)
                        totalamountsum = totalamountsum + float(productdetails.vendor_total_amount)
                        orderqtsum = orderqtsum + int(productdetails.buyer_quantity)
                        ratesum = ratesum + int(productdetails.vendor_rate)
                        vendorbidquantitysum=vendorbidquantitysum+int(productdetails.vendor_quantity)
                        parrray.append(productdetails.vendor_item_name)
                        pdescarray.append(productdetails.vendor_item_description)

                    print('-----------ok---------------')
                    awardobj = Awards.objects.filter(rfq_number=rfq_number,company_code=codes,product_code=pcode).values()
                    if len(awardobj) > 0 and awardobj:
                        print(len(awardobj))
                        return Response({'status': 204, 'message': 'already present'}, status=204)
                    else:
                        awardobj1=Awards.objects.create(rfq_number=rfq_number,
                                                        company_code=codes,
                                                        company_name=cname,
                                                        buyer_bid_quantity=orderqtsum,
                                                        vendor_bid_quantity=vendorbidquantitysum,
                                                       totalamount=totalamountsum,
                                                       rfq_title=rfqtitle,
                                                       rfq_status=rfqstatus,
                                                       product_code=pcode,
                                                       product_name=parrray,
                                                       product_description=pdescarray,
                                                       publish_date=publishdate,
                                                       updated_by=SelfRegistration.objects.get(id=userid),
                                                        rfq_type=rfq_type,
                                                       deadline_date=deadlinedate)
                        configuration = sib_api_v3_sdk.Configuration()
                        configuration.api_key[
                            'api-key'] = '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'
                        headers = {
                            'accept': 'application/json',
                            'content-type': 'application/json',
                        }
                        regobj=SelfRegistration.objects.get(id=updatedby)
                        print(regobj.username ,'ok')

                        print("{{{{{{",vendorbidquantitysum)

                        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
                        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=[{"email": regobj.username, "name":regobj.contact_person}],
                                                                       template_id=22, params={
                                "rfqnumber": rfq_number,
                                "awardeddate": awardobj1.awarded_date,
                                "rfqtitle": rfqtitle,
                                "quantity": str(vendorbidquantitysum),
                                "items":len(parrray),
                                "CompanyName": cname
                            },
                                # "cname": bidcreater[0].get('company_name')},
                                                                       headers=headers,
                                                                       subject='Bidding Invitation'
                                                                       )  # SendSmtpEmail | Values to send a transactional email
                        # Send a transactional email
                        api_response = api_instance.send_transac_email(send_smtp_email)
                        print(api_response)

        elif len(award_obj)!=0:
            print("already present")
            for i in range(0,len(award_obj)):
                award_obj_delete=Awards.objects.get(id=award_obj[i].get('id'))
                award_obj_delete.delete()

            if productvendordetails:
                for i in range(0, len(productvendordetails)):
                    totalamountsum = 0
                    ratesum = 0
                    orderqtsum = 0
                    discountsum = 0
                    vendorbidquantitysum = 0
                    parrray = []
                    pdescarray = []
                    pcode = productvendordetails[i].get('productcode')
                    print(type(pcode))

                    ccode = productvendordetails[i].get('vendorcode')
                    for product in pcode:
                        print(product)
                        for codes in ccode:
                            print(codes)
                            print('ok----')
                            bidobj = VendorProductBidding.objects.get(vendor_user_rfq_number=rfq_number,
                                                                      vendor_code=codes)
                            print(bidobj, 'fsds')
                            basicobj = BasicCompanyDetails.objects.get(company_code=codes)
                            cname = basicobj.company_name
                            updatedby = basicobj.updated_by_id
                            rfq_number = bidobj.vendor_user_rfq_number
                            # frieght = bidobj.freight_transportation
                            # pandf = bidobj.packaging_forwarding
                            publishdate = bidobj.vendor_product_publish_date
                            deadlinedate = bidobj.vendor_product_deadline_date
                            rfqtitle = bidobj.vendor_product_rfq_title
                            rfqstatus = bidobj.vendor_product_rfq_status
                        print(codes, 'd')
                        productdetails = VendorBiddingBuyerProductDetails.objects.get(vendor_rfq_number=rfq_number,
                                                                                      vendor_code=codes,
                                                                                      vendor_item_code=product)
                        print(productdetails)

                        if not productdetails:
                            return Response({'status': 204, 'message': 'No product details of vendor'}, status=204)

                        discountsum = discountsum + int(productdetails.vendor_discount)
                        totalamountsum = totalamountsum + float(productdetails.vendor_total_amount)
                        orderqtsum = orderqtsum + int(productdetails.buyer_quantity)
                        ratesum = ratesum + int(productdetails.vendor_rate)
                        pname = productdetails.vendor_item_name
                        pdesc = productdetails.vendor_item_description
                        vendorbidquantitysum = vendorbidquantitysum + int(productdetails.vendor_quantity)
                        parrray.append(productdetails.vendor_item_name)
                        pdescarray.append(productdetails.vendor_item_description)
                    print('-----------ok---------------')
                    awardobj = Awards.objects.filter(rfq_number=rfq_number, company_code__in=codes,
                                                     product_code=pcode).values()

                    if len(awardobj) > 0 and awardobj:
                        print(len(awardobj))
                        return Response({'status': 204, 'message': 'already present'}, status=204)
                    else:

                        awardobj1 = Awards.objects.create(rfq_number=rfq_number,
                                                          company_code=codes,
                                                          company_name=cname,
                                                          buyer_bid_quantity=orderqtsum,
                                                          vendor_bid_quantity=vendorbidquantitysum,
                                                          totalamount=totalamountsum,
                                                          rfq_title=rfqtitle,
                                                          rfq_status=rfqstatus,
                                                          product_code=pcode,
                                                          product_name=parrray,
                                                          product_description=pdescarray,
                                                          publish_date=publishdate,
                                                          rfq_type=rfq_type,
                                                          updated_by=SelfRegistration.objects.get(id=userid),
                                                          deadline_date=deadlinedate)
                        configuration = sib_api_v3_sdk.Configuration()
                        configuration.api_key[
                            'api-key'] = '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'
                        headers = {
                            'accept': 'application/json',
                            'content-type': 'application/json',
                        }
                        regobj = SelfRegistration.objects.get(id=updatedby)
                        print(regobj.username, 'ok')

                        print("{{{{{{", vendorbidquantitysum)

                        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
                        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                            to=[{"email": regobj.username, "name": "harish"}],
                            template_id=22, params={
                                 "rfqnumber": rfq_number,
                                "awardeddate": awardobj1.awarded_date,
                                "rfqtitle": rfqtitle,
                                "quantity": str(vendorbidquantitysum),
                                "items":len(parrray),
                                "CompanyName": cname
                            },
                            # "cname": bidcreater[0].get('company_name')},
                            headers=headers,
                            subject='RFQ Award'
                            )  # SendSmtpEmail | Values to send a transactional email
                        # Send a transactional email
                        api_response = api_instance.send_transac_email(send_smtp_email)
                        print(api_response)





        return Response({'status': 200, 'message': 'Award Created'}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['post'])
def award_service_create(request):
    data=request.data
    rfq_number = data['rfq_number']
    servicevendordetails = data['servicevendordetails']
    totalproductarray = []
    userid = data['userid']
    try:
        award_obj=ServiceAwards.objects.filter(service_rfq_number=rfq_number).values()
        if len(award_obj)==0:
            if servicevendordetails:
                for i in range(0, len(servicevendordetails)):
                    totalamountsum = 0
                    ratesum = 0
                    orderqtsum = 0
                    discountsum = 0
                    vendorbidquantitysum=0
                    snamearray=[]
                    sdescarray=[]
                    scode = servicevendordetails[i].get('servicecode')
                    print(type(scode))

                    ccode = servicevendordetails[i].get('vendorcode')
                    for service in scode:
                        print(service)
                        for codes in ccode:
                            print(codes)
                            print('ok----')
                            bidobj = VendorProductBidding.objects.get(vendor_user_rfq_number=rfq_number,vendor_product_rfq_type='Service',vendor_code=codes)
                            print(bidobj, 'fsds')
                            basicobj = BasicCompanyDetails.objects.get(company_code=codes)
                            cname = basicobj.company_name
                            updatedby=basicobj.updated_by_id
                            rfq_number = bidobj.vendor_user_rfq_number
                            publishdate = bidobj.vendor_product_publish_date
                            deadlinedate = bidobj.vendor_product_deadline_date
                            rfqtitle = bidobj.vendor_product_rfq_title
                            rfqstatus = bidobj.vendor_product_rfq_status
                        print(codes,'d')
                        servicedetails = VendorBiddingBuyerServiceDetails.objects.get(vendor_service_rfq_number=rfq_number,
                                                                                      vendor_code=codes,
                                                                                      vendor_service_item_code=service)
                        print(servicedetails)


                        if not servicedetails:
                            return Response({'status': 204, 'message': 'No service details of vendor'}, status=204)

                        discountsum = discountsum + int(servicedetails.vendor_service_discount)
                        totalamountsum = totalamountsum + float(servicedetails.vendor_service_total_amount)
                        orderqtsum = orderqtsum + int(servicedetails.buyer_service_quantity)
                        ratesum = ratesum + int(servicedetails.vendor_service_rate)
                        vendorbidquantitysum=vendorbidquantitysum+int(servicedetails.vendor_service_quantity)
                        snamearray.append(servicedetails.vendor_service_item_name)
                        sdescarray.append(servicedetails.vendor_service_item_description)
                    print('-----------ok---------------')
                    serviceawardobj = ServiceAwards.objects.filter(service_rfq_number=rfq_number,service_company_code=codes,service_code=scode).values()
                    if len(serviceawardobj) > 0 and serviceawardobj:
                        print(len(serviceawardobj))
                        return Response({'status': 204, 'message': 'already present'}, status=204)
                    else:
                        serviceawardobj=ServiceAwards.objects.create(service_rfq_number=rfq_number,
                                                                    service_company_code=codes,
                                                                    service_company_name=cname,
                                                                    service_buyer_bid_quantity=orderqtsum,
                                                                    service_vendor_bid_quantity=vendorbidquantitysum,
                                                                      service_totalamount=totalamountsum,
                                                                      service_rfq_title=rfqtitle,
                                                                      service_rfq_status=rfqstatus,
                                                                      service_code=scode,
                                                                      service_name=snamearray,
                                                                      service_description=sdescarray,
                                                                      service_publish_date=publishdate,
                                                                       rfq_type='Service',

                                                                      updated_by=SelfRegistration.objects.get(id=userid),
                                                                      service_deadline_date=deadlinedate)
                        configuration = sib_api_v3_sdk.Configuration()
                        configuration.api_key[
                            'api-key'] = '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'
                        headers = {
                            'accept': 'application/json',
                            'content-type': 'application/json',
                        }
                        regobj = SelfRegistration.objects.get(id=updatedby)
                        print(regobj.username, 'ok')

                        print("{{{{{{", orderqtsum)

                        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
                        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                            to=[{"email": regobj.username, "name": "harish"}],
                            template_id=22, params={
                                "rfqnumber": rfq_number,
                                "awardeddate": serviceawardobj.service_awarded_date,
                                "rfqtitle": rfqtitle,
                                "quantity": str(orderqtsum),
                                "items": len(snamearray),
                                "CompanyName": cname
                            },
                            # "cname": bidcreater[0].get('company_name')},
                            headers=headers,
                            subject='RFQ Award'
                        )  # SendSmtpEmail | Values to send a transactional email
                        # Send a transactional email
                        api_response = api_instance.send_transac_email(send_smtp_email)
                        print(api_response)
        elif len(award_obj)!=0:
            print("already present")
            for i in range(0,len(award_obj)):
                award_obj_delete=ServiceAwards.objects.get(id=award_obj[i].get('id'))
                award_obj_delete.delete()

            if servicevendordetails:
                for i in range(0, len(servicevendordetails)):
                    totalamountsum = 0
                    ratesum = 0
                    orderqtsum = 0
                    discountsum = 0
                    vendorbidquantitysum = 0
                    snamearray = []
                    sdescarray = []
                    scode = servicevendordetails[i].get('servicecode')
                    print(type(scode))

                    ccode = servicevendordetails[i].get('vendorcode')
                    for service in scode:
                        print(service)
                        for codes in ccode:
                            print(codes)
                            print('ok----')
                            bidobj = VendorProductBidding.objects.get(vendor_user_rfq_number=rfq_number,
                                                                      vendor_product_rfq_type='Service',
                                                                      vendor_code=codes)
                            print(bidobj, 'fsds')
                            basicobj = BasicCompanyDetails.objects.get(company_code=codes)
                            cname = basicobj.company_name
                            updatedby=basicobj.updated_by_id
                            rfq_number = bidobj.vendor_user_rfq_number
                            publishdate = bidobj.vendor_product_publish_date
                            deadlinedate = bidobj.vendor_product_deadline_date
                            rfqtitle = bidobj.vendor_product_rfq_title
                            rfqstatus = bidobj.vendor_product_rfq_status
                        print(codes, 'd')
                        servicedetails = VendorBiddingBuyerServiceDetails.objects.get(
                            vendor_service_rfq_number=rfq_number,
                            vendor_code=codes,
                            vendor_service_item_code=service)
                        print(servicedetails)

                        if not servicedetails:
                            return Response({'status': 204, 'message': 'No service details of vendor'}, status=204)

                        discountsum = discountsum + int(servicedetails.vendor_service_discount)
                        totalamountsum = totalamountsum + float(servicedetails.vendor_service_total_amount)
                        orderqtsum = orderqtsum + int(servicedetails.buyer_service_quantity)
                        ratesum = ratesum + int(servicedetails.vendor_service_rate)
                        snamearray.append(servicedetails.vendor_service_item_name)
                        sdescarray.append(servicedetails.vendor_service_item_description)
                        vendorbidquantitysum = vendorbidquantitysum + int(servicedetails.vendor_service_quantity)
                    print('-----------ok---------------')
                    serviceawardobj = ServiceAwards.objects.filter(service_rfq_number=rfq_number,
                                                                   service_company_code=codes,
                                                                   service_code=scode).values()
                    if len(serviceawardobj) > 0 and serviceawardobj:
                        print(len(serviceawardobj))
                        return Response({'status': 204, 'message': 'already present'}, status=204)
                    else:
                        serviceawardobj = ServiceAwards.objects.create(service_rfq_number=rfq_number,
                                                                       service_company_code=codes,
                                                                       service_company_name=cname,
                                                                       service_buyer_bid_quantity=orderqtsum,
                                                                       service_vendor_bid_quantity=vendorbidquantitysum,
                                                                       service_totalamount=totalamountsum,
                                                                       service_rfq_title=rfqtitle,
                                                                       service_rfq_status=rfqstatus,
                                                                       service_code=scode,
                                                                       service_name=snamearray,
                                                                       service_description=sdescarray,
                                                                       service_publish_date=publishdate,
                                                                       updated_by=SelfRegistration.objects.get(
                                                                           id=userid),
                                                                       rfq_type='Service',
                                                                       service_deadline_date=deadlinedate)
                        configuration = sib_api_v3_sdk.Configuration()
                        configuration.api_key[
                            'api-key'] = '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'
                        headers = {
                            'accept': 'application/json',
                            'content-type': 'application/json',
                        }
                        regobj = SelfRegistration.objects.get(id=updatedby)
                        print(regobj.username, 'ok')

                        print("{{{{{{", orderqtsum)

                        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
                        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                            to=[{"email": regobj.username, "name": "harish"}],
                            template_id=22, params={
                                "rfqnumber": rfq_number,
                                "awardeddate": serviceawardobj.service_awarded_date,
                                "rfqtitle": rfqtitle,
                                "quantity": str(orderqtsum),
                                "items": len(snamearray),
                                "CompanyName": cname
                            },
                            # "cname": bidcreater[0].get('company_name')},
                            headers=headers,
                            subject='RFQ Award'
                        )  # SendSmtpEmail | Values to send a transactional email
                        # Send a transactional email
                        api_response = api_instance.send_transac_email(send_smtp_email)
                        print(api_response)
        return Response({'status': 200, 'message': 'Award Service Created'}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def award_machinary_create(request):
    data=request.data
    rfq_number = data['rfq_number']
    machinaryvendordetails = data['machinaryvendordetails']
    totalproductarray = []
    userid = data['userid']
    try:
        award_obj=MachinaryAwards.objects.filter(machinary_rfq_number=rfq_number).values()
        if len(award_obj)==0:
            if machinaryvendordetails:
                for i in range(0, len(machinaryvendordetails)):
                    totalamountsum = 0
                    ratesum = 0
                    orderqtsum = 0
                    discountsum = 0
                    vendorbidquantitysum=0
                    mnamearray=[]
                    mdescarray=[]
                    mcode = machinaryvendordetails[i].get('machinarycode')
                    print(type(mcode))

                    ccode = machinaryvendordetails[i].get('vendorcode')
                    for machinary in mcode:
                        print(machinary)
                        for codes in ccode:
                            print(codes)
                            print('ok----')
                            bidobj = VendorProductBidding.objects.get(vendor_user_rfq_number=rfq_number,vendor_product_rfq_type='Machinary & equipments',vendor_code=codes)
                            print(bidobj, 'fsds')
                            basicobj = BasicCompanyDetails.objects.get(company_code=codes)
                            cname = basicobj.company_name
                            updatedby=basicobj.updated_by_id
                            rfq_number = bidobj.vendor_user_rfq_number
                            publishdate = bidobj.vendor_product_publish_date
                            deadlinedate = bidobj.vendor_product_deadline_date
                            rfqtitle = bidobj.vendor_product_rfq_title
                            rfqstatus = bidobj.vendor_product_rfq_status
                        print(codes,'d')
                        machinarydetails = VendorBiddingBuyerMachinaryDetails.objects.get(vendor_machinary_rfq_number=rfq_number,
                                                                                      vendor_code=codes,
                                                                                      vendor_machinary_item_code=machinary)
                        print(machinarydetails)


                        if not machinarydetails:
                            return Response({'status': 204, 'message': 'No service details of vendor'}, status=204)

                        discountsum = discountsum + int(machinarydetails.vendor_machinary_discount)
                        totalamountsum = totalamountsum + float(machinarydetails.vendor_machinary_total_amount)
                        orderqtsum = orderqtsum + int(machinarydetails.buyer_machinary_quantity)
                        ratesum = ratesum + int(machinarydetails.vendor_machinary_rate)
                        mnamearray.append(machinarydetails.vendor_machinary_item_name)
                        mdescarray.append(machinarydetails.vendor_machinary_item_description)
                        vendorbidquantitysum=vendorbidquantitysum+int(machinarydetails.buyer_machinary_quantity)
                    print('-----------ok---------------')
                    machinaryobj = MachinaryAwards.objects.filter(machinary_rfq_number=rfq_number,machinary_company_code=codes,machinary_code=mcode).values()
                    if len(machinaryobj) > 0 and machinaryobj:
                        print(len(machinaryobj))
                        return Response({'status': 204, 'message': 'already present'}, status=204)
                    else:
                        machinaryawardobj=MachinaryAwards.objects.create(machinary_rfq_number=rfq_number,
                                                                        machinary_company_code=codes,
                                                                        machinary_company_name=cname,
                                                                        machinary_buyer_bid_quantity=orderqtsum,
                                                                        machinary_vendor_bid_quantity=vendorbidquantitysum,
                                                                      machinary_totalamount=totalamountsum,
                                                                      machinary_rfq_title=rfqtitle,
                                                                      machinary_rfq_status=rfqstatus,
                                                                      machinary_code=mcode,
                                                                      machinary_name=mnamearray,
                                                                      machinary_description=mdescarray,
                                                                      machinary_publish_date=publishdate,
                                                                         rfq_type='Machinary & equipments',
                                                                      updated_by=SelfRegistration.objects.get(id=userid),
                                                                      machinary_deadline_date=deadlinedate)
                        configuration = sib_api_v3_sdk.Configuration()
                        configuration.api_key[
                            'api-key'] = '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'
                        headers = {
                            'accept': 'application/json',
                            'content-type': 'application/json',
                        }
                        regobj = SelfRegistration.objects.get(id=updatedby)
                        print(regobj.username, 'ok')

                        print("{{{{{{", orderqtsum)

                        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
                        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                            to=[{"email": regobj.username, "name": "harish"}],
                            template_id=22, params={
                                "rfqnumber": rfq_number,
                                "awardeddate": machinaryawardobj.machinary_awarded_date,
                                "rfqtitle": rfqtitle,
                                "quantity": str(orderqtsum),
                                "items": len(mnamearray),
                                "CompanyName": cname
                            },
                            # "cname": bidcreater[0].get('company_name')},
                            headers=headers,
                            subject='RFQ Award'
                        )  # SendSmtpEmail | Values to send a transactional email
                        # Send a transactional email
                        api_response = api_instance.send_transac_email(send_smtp_email)
                        print(api_response)
        elif len(award_obj)!=0:
            print("already present")
            for i in range(0,len(award_obj)):
                award_obj_delete=MachinaryAwards.objects.get(id=award_obj[i].get('id'))
                award_obj_delete.delete()

            if machinaryvendordetails:
                for i in range(0, len(machinaryvendordetails)):
                    totalamountsum = 0
                    ratesum = 0
                    orderqtsum = 0
                    discountsum = 0
                    vendorbidquantitysum = 0
                    mnamearray = []
                    mdescarray = []
                    mcode = machinaryvendordetails[i].get('machinarycode')
                    print(type(mcode))

                    ccode = machinaryvendordetails[i].get('vendorcode')
                    for machinary in mcode:
                        print(machinary)
                        for codes in ccode:
                            print(codes)
                            print('ok----')
                            bidobj = VendorProductBidding.objects.get(vendor_user_rfq_number=rfq_number,
                                                                      vendor_product_rfq_type='Machinary & equipments',
                                                                      vendor_code=codes)
                            print(bidobj, 'fsds')
                            basicobj = BasicCompanyDetails.objects.get(company_code=codes)
                            cname = basicobj.company_name
                            updatedby=basicobj.updated_by_id
                            rfq_number = bidobj.vendor_user_rfq_number
                            publishdate = bidobj.vendor_product_publish_date
                            deadlinedate = bidobj.vendor_product_deadline_date
                            rfqtitle = bidobj.vendor_product_rfq_title
                            rfqstatus = bidobj.vendor_product_rfq_status
                        print(codes, 'd')
                        machinarydetails = VendorBiddingBuyerMachinaryDetails.objects.get(
                            vendor_machinary_rfq_number=rfq_number,
                            vendor_code=codes,
                            vendor_machinary_item_code=machinary)
                        print(machinarydetails)

                        if not machinarydetails:
                            return Response({'status': 204, 'message': 'No service details of vendor'}, status=204)

                        discountsum = discountsum + int(machinarydetails.vendor_machinary_discount)
                        totalamountsum = totalamountsum + float(machinarydetails.vendor_machinary_total_amount)
                        orderqtsum = orderqtsum + int(machinarydetails.buyer_machinary_quantity)
                        ratesum = ratesum + int(machinarydetails.vendor_machinary_rate)
                        mnamearray.append(machinarydetails.vendor_machinary_item_name)
                        mdescarray = machinarydetails.vendor_machinary_item_description
                        vendorbidquantitysum = vendorbidquantitysum + int(machinarydetails.buyer_machinary_quantity)

                    print('-----------ok---------------')
                    machinaryobj = MachinaryAwards.objects.filter(machinary_rfq_number=rfq_number,
                                                                     machinary_company_code=codes,
                                                                     machinary_code=mcode).values()
                    if len(machinaryobj) > 0 and machinaryobj:
                        print(len(machinaryobj))
                        return Response({'status': 204, 'message': 'already present'}, status=204)
                    else:
                        machinaryawardobj = MachinaryAwards.objects.create(machinary_rfq_number=rfq_number,
                                                                           machinary_company_code=codes,
                                                                           machinary_company_name=cname,
                                                                           machinary_buyer_bid_quantity=orderqtsum,
                                                                           machinary_vendor_bid_quantity=vendorbidquantitysum,
                                                                           machinary_totalamount=totalamountsum,
                                                                           machinary_rfq_title=rfqtitle,
                                                                           machinary_rfq_status=rfqstatus,
                                                                           machinary_code=mcode,
                                                                           machinary_name=mnamearray,
                                                                           machinary_description=mdescarray,
                                                                           machinary_publish_date=publishdate,
                                                                           updated_by=SelfRegistration.objects.get(
                                                                               id=userid),
                                                                           rfq_type='Machinary & equipments',
                                                                           machinary_deadline_date=deadlinedate)
                        configuration = sib_api_v3_sdk.Configuration()
                        configuration.api_key[
                            'api-key'] = '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'
                        headers = {
                            'accept': 'application/json',
                            'content-type': 'application/json',
                        }
                        regobj = SelfRegistration.objects.get(id=updatedby)
                        print(regobj.username, 'ok')

                        print("{{{{{{", vendorbidquantitysum)

                        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
                        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                            to=[{"email": regobj.username, "name": "harish"}],
                            template_id=22, params={
                                 "rfqnumber": rfq_number,
                                "awardeddate": machinaryawardobj.machinary_awarded_date,
                                "rfqtitle": rfqtitle,
                                "quantity": str(orderqtsum),
                                "items": len(mnamearray),
                                "CompanyName": cname
                            },
                            # "cname": bidcreater[0].get('company_name')},
                            headers=headers,
                            subject='RFQ Award'
                        )  # SendSmtpEmail | Values to send a transactional email
                        # Send a transactional email
                        api_response = api_instance.send_transac_email(send_smtp_email)
                        print(api_response)
        return Response({'status': 200, 'message': 'Award Machinary Created'}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['put'])
def po_status_update_product(request):
    data = request.data
    awardpk = data['awardpk']
    rfq_number = data['rfq_number']
    try:
        awardobj = Awards.objects.filter(id=awardpk, rfq_number=rfq_number).values()
        if len(awardobj) > 0:
            awards = Awards.objects.get(id=awardpk)
            if awards.postatus == 'Pending':
                awards.postatus = 'PO_Sent'
                awards.save()
                return Response({'status': 200, 'message': 'Product PO sent successfully', 'data': awards.postatus}, status=200)
            else:
                if awards.postatus=='PO_Sent':
                    return Response({'status': 202, 'message': 'PO Already Sent'}, status=202)
                else:
                    return Response({'status': 202, 'message': 'PO sent failed or po not sent'}, status=202)

        else:
            return Response({'status': 204, 'message': 'No data found'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['post'])
def fetch_vendor_bid_details(request):
    data=request.data
    rfqtype=data['rfqtype']
    rfqnumber=data['rfqnumber']
    vendorcode=data['vendorcode']
    vendorarray=[]
    try:
        basicobj=BasicCompanyDetails.objects.filter(company_code=vendorcode).values()
        if rfqtype=='Product':
            vendorobj=VendorProductBidding.objects.filter(vendor_user_rfq_number=rfqnumber,vendor_product_rfq_type='Product',vendor_code=vendorcode).values().order_by('vendor_product_bidding_id')
            if len(vendorobj)>0:
                for i in range(0,len(vendorobj)):
                    vendorproductobj=VendorBiddingBuyerProductDetails.objects.filter(vendor_rfq_number=rfqnumber,vendor_item_type='Product',vendor_code=vendorcode).values().order_by('id')
                    for j in range(0,len(vendorproductobj)):
                        print('s print')
                    vendorterms=VendorRfqTermsDescription.objects.filter(vendor_rfq_number=rfqnumber,rfq_type='Product',updated_by_id=basicobj[0].get('updated_by_id')).values().order_by('id')
                    for k in range(0,len(vendorterms)):
                        print('correct')
                    vendorobj[i].__setitem__('product',vendorproductobj)
                    vendorobj[i].__setitem__('vendor_rfq_terms',vendorterms)

                return Response({'status': 200, 'message': 'Vendor Product Bidding List','data':vendorobj}, status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)
        elif rfqtype=='Service':
            vendorobj = VendorProductBidding.objects.filter(vendor_user_rfq_number=rfqnumber,
                                                            vendor_product_rfq_type='Service',
                                                            vendor_code=vendorcode).values().order_by(
                'vendor_product_bidding_id')
            if len(vendorobj) > 0:
                for i in range(0, len(vendorobj)):
                    vendorproductobj = VendorBiddingBuyerProductDetails.objects.filter(vendor_rfq_number=rfqnumber,
                                                                                       vendor_item_type='Service',
                                                                                       vendor_code=vendorcode).values().order_by(
                        'id')
                    for j in range(0, len(vendorproductobj)):
                        print('s print')
                    vendorterms = VendorRfqTermsDescription.objects.filter(vendor_rfq_number=rfqnumber,
                                                                           rfq_type='Service',
                                                                           updated_by_id=basicobj[0].get('updated_by_id')).values().order_by(
                        'id')
                    for k in range(0, len(vendorterms)):
                        print('correct')
                    vendorobj[i].__setitem__('product', vendorproductobj)
                    vendorobj[i].__setitem__('vendor_rfq_terms', vendorterms)

                return Response({'status': 200, 'message': 'Vendor Product Bidding List', 'data': vendorobj},
                                status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)
        elif rfqtype=='Machinary & equipments':
            vendorobj = VendorProductBidding.objects.filter(vendor_user_rfq_number=rfqnumber,
                                                            vendor_product_rfq_type='Machinary & equipments',
                                                            vendor_code=vendorcode).values().order_by(
                'vendor_product_bidding_id')
            if len(vendorobj) > 0:
                for i in range(0, len(vendorobj)):
                    vendorproductobj = VendorBiddingBuyerProductDetails.objects.filter(vendor_rfq_number=rfqnumber,
                                                                                       vendor_item_type='Machinary & equipments',
                                                                                       vendor_code=vendorcode).values().order_by(
                        'id')
                    for j in range(0, len(vendorproductobj)):
                        print('s print')
                    vendorterms = VendorRfqTermsDescription.objects.filter(vendor_rfq_number=rfqnumber,
                                                                           rfq_type='Machinary & equipments',
                                                                           updated_by_id=basicobj[0].get('updated_by_id')).values().order_by(
                        'id')
                    for k in range(0, len(vendorterms)):
                        print('correct')
                    vendorobj[i].__setitem__('product', vendorproductobj)
                    vendorobj[i].__setitem__('vendor_rfq_terms', vendorterms)

                return Response({'status': 200, 'message': 'Vendor Product Bidding List', 'data': vendorobj},
                                status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)
        else:
            return Response({'status': 202, 'message': 'rfq type is mispelled or not present'}, status=202)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)





@api_view(['post'])
def price_analysis_vendor_terms_list(request):
    data = request.data
    rfq_number = data['rfq_number']
    vendor_code = data['vendor_code']
    selectsarray=[]
    priceanalysisarray=[]
    vendorterms=[]
    dival={}

    try:
        selectobj=SelectVendorsForBiddingProduct.objects.filter(rfq_number=rfq_number,vendor_code__in=vendor_code).values()
        for i in range(0,len(selectobj)):
            selectsarray.append(selectobj[i].get('rfq_number'))
        print(selectsarray)
        # buyerobj = RfqTermsDescription.objects.filter(rfq_number__in=selectsarray).values().order_by('terms')
        vendorobj=VendorRfqTermsDescription.objects.filter(vendor_rfq_number__in=selectsarray).values().order_by('vendor_terms')
        print(len(vendorobj))
        for i in range(0,len(vendorobj)):
            print('-------------------------------------------------------------------')
            priceanalysisarray.append(vendorobj[i].get('updated_by_id'))
        print(priceanalysisarray)
        return Response({'status': 200, 'message': 'Success','vendorterms': vendorterms}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def get_previous_value_of_rfq_details(request):
    data = request.data
    userid = data['userid']
    try:
        rfqcodesettings = RfqCodeSettings.objects.filter(updated_by_id=userid).last()
        if rfqcodesettings:
            buyerproductobj = BuyerProductBidding.objects.filter(updated_by_id=userid).last()
            if buyerproductobj:
                buyer_product = {
                    'rfq_number': str(rfqcodesettings.prefix) + str(
                        rfqcodesettings.suffix) + buyerproductobj.user_bidding_numeric,
                    'user_id': buyerproductobj.updated_by_id
                }
                return Response({'status': 200, 'message': 'Buyer Bidding Product List', 'data': buyer_product},
                                status=200)
            else:
                rfq_number_settings = {
                    'rfq_number': rfqcodesettings.prefix + rfqcodesettings.suffix + rfqcodesettings.numeric,
                    'user_id': rfqcodesettings.updated_by_id
                }
                return Response({'status': 200, 'message': 'Code Settings', 'data': rfq_number_settings}, status=200)
        else:
            rfq_number_settings = {
                'rfq_number': rfqcodesettings.prefix + rfqcodesettings.suffix + rfqcodesettings.numeric,
                'user_id': rfqcodesettings.updated_by_id
            }
            return Response({'status': 200, 'message': 'Code Settings', 'data': rfq_number_settings}, status=200)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def fetch_vendor_bid_details_userid(request):
    data=request.data
    rfqtype=data['rfqtype']
    rfqnumber=data['rfqnumber']
    vendorcode=data['vendorcode']
    userid=data['userid']
    vendorarray=[]
    try:
        basicobj=BasicCompanyDetails.objects.filter(company_code=vendorcode).values()
        if rfqtype=='Product':
            vendorobj=VendorProductBidding.objects.filter(vendor_user_rfq_number=rfqnumber,vendor_product_rfq_type='Product',vendor_code=vendorcode,updated_by_id=userid).values().order_by('vendor_product_bidding_id')
            if len(vendorobj)>0:
                for i in range(0,len(vendorobj)):
                    vendorproductobj=VendorBiddingBuyerProductDetails.objects.filter(vendor_rfq_number=rfqnumber,vendor_item_type='Product',vendor_code=vendorcode,updated_by_id=userid).values().order_by('id')
                    for j in range(0,len(vendorproductobj)):
                        print('s print')
                    vendorterms=VendorRfqTermsDescription.objects.filter(vendor_rfq_number=rfqnumber,rfq_type='Product',updated_by_id=basicobj[0].get('updated_by_id')).values().order_by('id')
                    for k in range(0,len(vendorterms)):
                        print('correct')
                    vendorobj[i].__setitem__('product',vendorproductobj)
                    vendorobj[i].__setitem__('vendor_rfq_terms',vendorterms)

                return Response({'status': 200, 'message': 'Vendor Product Bidding List','data':vendorobj}, status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)
        elif rfqtype=='Service':
            vendorobj = VendorProductBidding.objects.filter(vendor_user_rfq_number=rfqnumber,
                                                            vendor_product_rfq_type='Service',
                                                            vendor_code=vendorcode).values().order_by(
                'vendor_product_bidding_id')
            if len(vendorobj) > 0:
                for i in range(0, len(vendorobj)):
                    vendorproductobj = VendorBiddingBuyerProductDetails.objects.filter(vendor_rfq_number=rfqnumber,
                                                                                       vendor_item_type='Service',
                                                                                       vendor_code=vendorcode).values().order_by(
                        'id')
                    for j in range(0, len(vendorproductobj)):
                        print('s print')
                    vendorterms = VendorRfqTermsDescription.objects.filter(vendor_rfq_number=rfqnumber,
                                                                           rfq_type='Service',
                                                                           updated_by_id=basicobj[0].get('updated_by_id')).values().order_by(
                        'id')
                    for k in range(0, len(vendorterms)):
                        print('correct')
                    vendorobj[i].__setitem__('product', vendorproductobj)
                    vendorobj[i].__setitem__('vendor_rfq_terms', vendorterms)

                return Response({'status': 200, 'message': 'Vendor Product Bidding List', 'data': vendorobj},
                                status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)
        elif rfqtype=='Machinary & equipments':
            vendorobj = VendorProductBidding.objects.filter(vendor_user_rfq_number=rfqnumber,
                                                            vendor_product_rfq_type='Machinary & equipments',
                                                            vendor_code=vendorcode).values().order_by(
                'vendor_product_bidding_id')
            if len(vendorobj) > 0:
                for i in range(0, len(vendorobj)):
                    vendorproductobj = VendorBiddingBuyerProductDetails.objects.filter(vendor_rfq_number=rfqnumber,
                                                                                       vendor_item_type='Machinary & equipments',
                                                                                       vendor_code=vendorcode).values().order_by(
                        'id')
                    for j in range(0, len(vendorproductobj)):
                        print('s print')
                    vendorterms = VendorRfqTermsDescription.objects.filter(vendor_rfq_number=rfqnumber,
                                                                           rfq_type='Machinary & equipments',
                                                                           updated_by_id=basicobj[0].get('updated_by_id')).values().order_by(
                        'id')
                    for k in range(0, len(vendorterms)):
                        print('correct')
                    vendorobj[i].__setitem__('product', vendorproductobj)
                    vendorobj[i].__setitem__('vendor_rfq_terms', vendorterms)

                return Response({'status': 200, 'message': 'Vendor Product Bidding List', 'data': vendorobj},
                                status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['PUT'])
def edit_vendor_bidding_product(request):
    data = request.data
    userid = data['userid']
    frontarray = data['frontarray']
    rfq_type=data['rfq_type']
    # frontarray=[{'id':262,'tax':10,'hsn':'10001','rate':5,"discount":10,'totalamount':"3292.8"},
    #             {'id':263,'tax':5,'hsn':'10002','rate':15,"discount":12,'totalamount':"4488.75"},
    #             {'id':264,'tax':6,'hsn':'10003','rate':12,"discount":12,'totalamount':"872.256"}]
    try:
        if rfq_type=='Product':
            vendorproductobj=VendorBiddingBuyerProductDetails.objects.filter(updated_by_id=userid,vendor_item_type=rfq_type).values()
            if len(vendorproductobj)>0:
                for i in range(0, len(frontarray)):
                    print('ok')
                    vendobj = VendorBiddingBuyerProductDetails.objects.get(id=frontarray[i].get('id'),vendor_item_type=rfq_type)
                    if vendobj != "":
                        print('yes')
                        if vendobj.vendor_quantity!=frontarray[i].get('vendor_quantity') and vendobj.vendor_quantity!="":
                            vendobj.vendor_quantity=frontarray[i].get('vendor_quantity')
                            vendobj.save()
                        if vendobj.vendor_tax != frontarray[i].get('vendor_tax') and vendobj.vendor_tax != "":
                            vendobj.vendor_tax = frontarray[i].get('vendor_tax')
                            vendobj.save()
                        if vendobj.vendor_rate != frontarray[i].get('vendor_rate') and vendobj.vendor_rate != "":
                            vendobj.vendor_rate = frontarray[i].get('vendor_rate')
                            vendobj.save()
                        if vendobj.vendor_discount != frontarray[i].get('vendor_discount') and vendobj.vendor_discount != "":
                            vendobj.vendor_discount = frontarray[i].get('vendor_discount')
                            vendobj.save()
                        if vendobj.vendor_total_amount != frontarray[i].get('vendor_total_amount') and vendobj.vendor_total_amount != "":
                            vendobj.vendor_total_amount = frontarray[i].get('vendor_total_amount')
                            vendobj.save()
                        if vendobj.vendor_final_amount != frontarray[i].get('vendor_final_amount') and vendobj.vendor_final_amount != "":
                            vendobj.vendor_final_amount = frontarray[i].get('vendor_final_amount')
                            vendobj.save()
                return Response({'status': 200, 'message': 'Vendor Product Edited Successfully'}, status=200)
            else:
                return Response({'status': 204, 'message': 'vendor products are not present with this user id'}, status=204)
        else:
            return Response({'status': 202, 'message': 'rfq type is mis-spelled ot not exist'}, status=202)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['PUT'])
def edit_vendor_bidding_service(request):
    data = request.data
    userid = data['userid']
    serviceeditarray = data['serviceeditarray']
    rfq_type=data['rfq_type']
    # frontarray=[{'id':262,'tax':10,'hsn':'10001','rate':5,"discount":10,'totalamount':"3292.8"},
    #             {'id':263,'tax':5,'hsn':'10002','rate':15,"discount":12,'totalamount':"4488.75"},
    #             {'id':264,'tax':6,'hsn':'10003','rate':12,"discount":12,'totalamount':"872.256"}]
    try:
        if rfq_type=='Service':
            vendorserviceobj=VendorBiddingBuyerServiceDetails.objects.filter(updated_by_id=userid,vendor_service_item_type=rfq_type).values()
            if len(vendorserviceobj)>0:
                for i in range(0, len(serviceeditarray)):
                    print('ok')
                    serviceobj = VendorBiddingBuyerServiceDetails.objects.get(id=serviceeditarray[i].get('id'),vendor_service_item_type=rfq_type)
                    if serviceobj != "":
                        print('yes')
                        if serviceobj.vendor_service_quantity != serviceeditarray[i].get('vendor_service_quantity') and serviceobj.vendor_service_quantity != "":
                            serviceobj.vendor_service_quantity = serviceeditarray[i].get('vendor_service_quantity')
                            serviceobj.save()

                        if serviceobj.vendor_service_tax != serviceeditarray[i].get('vendor_service_tax') and serviceobj.vendor_service_tax != "":
                            serviceobj.vendor_service_tax = serviceeditarray[i].get('vendor_service_tax')
                            serviceobj.save()
                        if serviceobj.vendor_service_rate != serviceeditarray[i].get('vendor_service_rate') and serviceobj.vendor_service_rate != "":
                            serviceobj.vendor_service_rate = serviceeditarray[i].get('vendor_service_rate')
                            serviceobj.save()
                        if serviceobj.vendor_service_discount != serviceeditarray[i].get('vendor_service_discount') and serviceobj.vendor_service_discount != "":
                            serviceobj.vendor_service_discount = serviceeditarray[i].get('vendor_service_discount')
                            serviceobj.save()
                        if serviceobj.vendor_service_total_amount != serviceeditarray[i].get('vendor_service_total_amount') and serviceobj.vendor_service_total_amount != "":
                            serviceobj.vendor_service_total_amount = serviceeditarray[i].get('vendor_service_total_amount')
                            serviceobj.save()
                        if serviceobj.vendor_service_final_amount != serviceeditarray[i].get('vendor_service_final_amount') and serviceobj.vendor_service_final_amount != "":
                            serviceobj.vendor_service_final_amount = serviceeditarray[i].get('vendor_service_final_amount')
                            serviceobj.save()
                return Response({'status': 200, 'message': 'Vendor Service Edited Successfully'}, status=200)
            else:
                return Response({'status': 204, 'message': 'vendor services are not present with this user id'}, status=204)
        else:
            return Response({'status': 202, 'message': 'rfq type is mis-spelled ot not exist'}, status=202)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['PUT'])
def edit_vendor_bidding_machinary(request):
    data = request.data
    userid = data['userid']
    machinaryeditarray = data['machinaryeditarray']
    rfq_type=data['rfq_type']
    # frontarray=[{'id':262,'tax':10,'hsn':'10001','rate':5,"discount":10,'totalamount':"3292.8"},
    #             {'id':263,'tax':5,'hsn':'10002','rate':15,"discount":12,'totalamount':"4488.75"},
    #             {'id':264,'tax':6,'hsn':'10003','rate':12,"discount":12,'totalamount':"872.256"}]
    try:
        if rfq_type=='Machinary & equipments':
            vendormachinaryobj=VendorBiddingBuyerMachinaryDetails.objects.filter(updated_by_id=userid,vendor_machinary_item_type=rfq_type).values()
            if len(vendormachinaryobj)>0:
                for i in range(0, len(machinaryeditarray)):
                    print('ok')
                    machinaryobj = VendorBiddingBuyerMachinaryDetails.objects.get(id=machinaryeditarray[i].get('id'),vendor_machinary_item_type=rfq_type)
                    if machinaryobj != "":
                        print('yes')
                        if machinaryobj.vendor_machinary_quantity != machinaryeditarray[i].get('vendor_machinary_quantity') and machinaryobj.vendor_machinary_quantity != "":
                            machinaryobj.vendor_machinary_quantity = machinaryeditarray[i].get('vendor_machinary_quantity')
                            machinaryobj.save()

                        if machinaryobj.vendor_machinary_tax != machinaryeditarray[i].get('vendor_machinary_tax') and machinaryobj.vendor_machinary_tax != "":
                            machinaryobj.vendor_machinary_tax = machinaryeditarray[i].get('vendor_machinary_tax')
                            machinaryobj.save()
                        if machinaryobj.vendor_machinary_rate != machinaryeditarray[i].get('vendor_machinary_rate') and machinaryobj.vendor_machinary_rate != "":
                            machinaryobj.vendor_machinary_rate = machinaryeditarray[i].get('vendor_machinary_rate')
                            machinaryobj.save()
                        if machinaryobj.vendor_machinary_discount != machinaryeditarray[i].get('vendor_machinary_discount') and machinaryobj.vendor_machinary_discount != "":
                            machinaryobj.vendor_machinary_discount = machinaryeditarray[i].get('vendor_machinary_discount')
                            machinaryobj.save()
                        if machinaryobj.vendor_machinary_total_amount != machinaryeditarray[i].get('vendor_machinary_total_amount') and machinaryobj.vendor_machinary_total_amount != "":
                            machinaryobj.vendor_machinary_total_amount = machinaryeditarray[i].get('vendor_machinary_total_amount')
                            machinaryobj.save()
                        if machinaryobj.vendor_machinary_final_amount != machinaryeditarray[i].get('vendor_machinary_final_amount') and machinaryobj.vendor_machinary_final_amount != "":
                            machinaryobj.vendor_machinary_final_amount = machinaryeditarray[i].get('vendor_machinary_final_amount')
                            machinaryobj.save()
                return Response({'status': 200, 'message': 'Vendor Machinary Edited Successfully'}, status=200)
            else:
                return Response({'status': 204, 'message': 'vendor machinary are not present with this user id'}, status=204)
        else:
            return Response({'status': 202, 'message': 'rfq type is mis-spelled ot not exist'}, status=202)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['put'])
def buyer_bid_status_changed_to_publish(request):
    data = request.data
    rfqnumber = data['rfqnumber']
    try:

        vendorobj = BuyerProductBidding.objects.get(user_rfq_number=rfqnumber)
        if vendorobj:
            if vendorobj.product_rfq_status == 'Pending':
                vendorobj.product_rfq_status = 'Published'
                vendorobj.save()
                return Response({'status': 200, 'message': 'Status Changed to Published', 'data': vendorobj.product_rfq_status},
                                status=200)
            else:
                return Response({'status': 202, 'error': 'Already Published'}, status=202)
        else:
            return Response({'status': 204, 'message': 'No details present for this rfq number'}, status=204)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def get_buyer_bid_list_by_userid(request):
    data=request.data
    userid=data['userid']
    from_registration=data['from_registration']
    try:
        if from_registration=='True':
            bidobj=BuyerProductBidding.objects.filter(updated_by_id=userid,from_registration=from_registration).values().order_by('product_bidding_id')
            if len(bidobj)>0:
                return Response(
                    {'status': 200, 'message': 'Buyer Bid List from Registration', 'data':bidobj},status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)
        else:
            if from_registration=='False':
                bidobjvalues = BuyerProductBidding.objects.filter(updated_by_id=userid,
                                                            from_registration=from_registration).values().order_by('product_bidding_id')
                if len(bidobjvalues) > 0:
                    return Response({'status': 200, 'message': 'Buyer Bid List', 'data': bidobjvalues}, status=200)
                else:
                    return Response({'status': 204, 'message': 'Not Present'}, status=204)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def get_all_types_of_awards(request):
    data=request.data
    userid=data['userid']
    try:
        awardsproductobj=Awards.objects.filter(updated_by_id=userid).values().order_by('id')
        awardsserviceobj=ServiceAwards.objects.filter(updated_by_id=userid).values().order_by('id')
        awardsmachinaryobj=MachinaryAwards.objects.filter(updated_by_id=userid).values().order_by('id')
        awardslist=list(chain(awardsproductobj,awardsserviceobj,awardsmachinaryobj))
        if len(awardsproductobj) or len(awardsserviceobj) or len(awardsmachinaryobj) > 0:
            return Response({'status': 200, 'message': 'All Awards List', 'data': awardslist}, status=200)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
# @permission_classes((AllowAny,))
def get_all_awards_based_on_userid_and_rfqtype(request):
    data=request.data
    userid=data['userid']
    rfqtype=data['rfqtype']
    try:
        if rfqtype=='Product':
            pawards=Awards.objects.filter(updated_by=userid,rfq_type=rfqtype).values().order_by('id')
            if len(pawards)>0:
                return Response({'status': 200, 'message': 'Award Product List','data':pawards}, status=200)
            else:
                return Response({'status': 202,'message': 'Not Present'}, status=202)


        elif rfqtype == 'Service':
            sawards = ServiceAwards.objects.filter(updated_by=userid,
                                                            rfq_type=rfqtype).values().order_by('id')
            if len(sawards)>0:
                return Response({'status': 200, 'message': 'Award Service List', 'data': sawards}, status=200)
            else:
                return Response({'status': 202, 'message': 'Not Present'}, status=202)
        elif rfqtype == 'Machinary & equipments':
            mawards = MachinaryAwards.objects.filter(updated_by=userid,
                                                                   rfq_type=rfqtype).values().order_by('id')
            if len(mawards)>0:
                return Response({'status': 200, 'message': 'Award Machinary List', 'data': mawards}, status=200)
            else:
                return Response({'status': 202, 'message': 'Not Present'}, status=202)

        else:
            return Response({'status': 204, 'error':'Not present or rfqtype is wrong','data':[]}, status=204)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def purchase_order_vendors_list(request):
    data = request.data
    userid = data['userid']
    purchaseorderarray = []
    try:
        basicobj=BasicCompanyDetails.objects.filter(updated_by_id=userid).values()
        # print(basicobj.company_code)
        poobj = PurchaseOrder.objects.filter(vendorcode=basicobj[0].get('company_code')).values()
        if len(poobj) > 0:
            for i in range(0, len(poobj)):
                print(poobj[i].get('rfq_number'))
                selectsobj = SelectVendorsForBiddingProduct.objects.filter(rfq_number=poobj[i].get('rfq_number')).values()
                print(len(selectsobj),'asfdfsdf')
                if len(selectsobj)>0:
                    selecteduserid = selectsobj[0].get('updated_by_id')
                    basicobj = BasicCompanyDetails.objects.filter(updated_by_id=selecteduserid).values()
                    purchaseorderarray.append({'rfq_number': poobj[i].get('rfq_number'),
                                               'rfq_title': poobj[i].get('rfq_title'),
                                               'PO_date': poobj[i].get('PO_date'),
                                               'PO_expirydate': poobj[i].get('PO_expirydate'),
                                               'subject': poobj[i].get('subject'),
                                               'attachment1': poobj[i].get('attachment1'),
                                               'attachment2': poobj[i].get('attachment2'),
                                               'attachment3': poobj[i].get('attachment3'),
                                               'PO_num': poobj[i].get('PO_num'),
                                               'delivery_date': poobj[i].get('delivery_date'),
                                               'remind_date': poobj[i].get('remind_date'),
                                               'delivery_days': poobj[i].get('delivery_days'),
                                               'company_code': basicobj[0].get('company_code'),
                                               'company_name': basicobj[0].get('company_name'),
                                               'rfq_type':poobj[i].get('rfq_type'),
                                               'userid': poobj[i].get('updated_by_id')


                                               })
                # else:
                #     return Response({'status': 202, 'message': 'No data'}, status=202)

            return Response({'status': 200, 'message': 'Purchase Order Vendor List', 'data': purchaseorderarray}, status=200)
        else:
            return Response({'status': 202, 'message': 'No data','data':[]}, status=202)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def awards_vendor_list(request):
    data = request.data
    userid=data['userid']
    awardarray = []
    try:
        basicobj=BasicCompanyDetails.objects.filter(updated_by_id=userid).values()
        awardobj = Awards.objects.filter(company_code=basicobj[0].get('company_code')).values()
        for i in range(0,len(awardobj)):
            print(awardobj[i].get('company_code'))
            selectsobj = SelectVendorsForBiddingProduct.objects.filter(vendor_code=awardobj[i].get('company_code')).values()
            if len(selectsobj)>0:
                print(len(selectsobj))
                selecteduserid = selectsobj[i].get('updated_by_id')
                basicobj = BasicCompanyDetails.objects.filter(updated_by_id=selecteduserid).values()
                awardarray.append({
                    'rfq_number':awardobj[i].get('rfq_number'),
                    'rfq_title': awardobj[i].get('rfq_title'),
                    'company_code': basicobj[0].get('company_code'),
                    'company_name':basicobj[0].get('company_name'),
                    'buyer_bid_quantity':awardobj[i].get('buyer_bid_quantity'),
                    'vendor_bid_quantity':awardobj[i].get('vendor_bid_quantity'),
                    'totalamount': awardobj[i].get('totalamount'),
                    'awarded_date': awardobj[i].get('awarded_date'),
                    'publish_date': awardobj[i].get('publish_date'),
                    'deadline_date': awardobj[i].get('deadline_date'),
                    'product_code': awardobj[i].get('product_code'),
                    'product_name':awardobj[i].get('product_name'),
                    'product_description': awardobj[i].get('product_description'),
                    'rfq_type':awardobj[i].get('rfq_type'),
                    'userid':awardobj[i].get('updated_by_id')
                })
        return Response({'status': 200, 'message': 'Awards Vendor List','data': awardarray}, status=200)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['post'])
@permission_classes((AllowAny,))
def createbuyerbidding(request):
    data=request.data
    rfq=data['rfq']
    rfqtype=data['rfqtype']
    pdate=data['pdate']
    deadlinedate=data['deadlinedate']
    delidate=data['delidate']
    dept=data['dept']
    currency=data['currency']
    category=data['category']
    billto=data['billto']
    shipto=data['shipto']
    rfqtitle=data['rfqtitle']
    # productdetails=data['productdetails']
    termsdetails=data['termdetails']
    userid=data['userid']
    productdetails=data['pdetails']
    terms=data["terms"]
    contact_name=data['contact_name']
    phone_number=data['phone_number']
    email_id=data['email_id']

    try:
        rfqobjcode=RfqCodeSettings.objects.filter(updated_by=userid).values()
        if RfqCodeSettings:
            BuyerProductBiddingobj=BuyerProductBidding.objects.filter(updated_by=userid).values().order_by('-user_rfq_number')
            if BuyerProductBiddingobj:
                print("----+----",BuyerProductBiddingobj[0].get('user_rfq_number'))

                BuyerProductBiddingobj = BuyerProductBidding.objects.create(product_rfq_number=rfq, user_rfq_number=rfq,
                                                                            user_bidding_numeric=int(
                                                                                BuyerProductBiddingobj[0].get('user_bidding_numeric')) + 1,
                                                                            product_rfq_type=rfqtype,
                                                                            product_publish_date=pdate,
                                                                            product_deadline_date=deadlinedate,
                                                                            product_delivery_date=delidate,
                                                                            product_rfq_currency=currency,
                                                                            product_rfq_category=category,
                                                                            product_department=dept,
                                                                            product_bill_address=billto,
                                                                            product_ship_address=shipto,
                                                                            product_rfq_title=rfqtitle,
                                                                            created_by=userid,
                                                                            updated_by=SelfRegistration.objects.get(
                                                                                id=userid),
                                                                            contact_name=contact_name,
                                                                            phone_number=phone_number,
                                                                            email_id=email_id
                                                                            )

                for i in range(0, len(productdetails)):
                    print(productdetails[i].get('buyer_item_type'))
                    print(productdetails[i].get('buyer_quantity'))
                    BiddingBuyerProductDetails.objects.create(buyer_item_type=productdetails[i].get('buyer_item_type'),
                                                              buyer_item_code=productdetails[i].get('itemcode'),
                                                              buyer_item_name=productdetails[i].get('itemname'),
                                                              buyer_item_description=productdetails[i].get('itemdes'),
                                                              buyer_uom=productdetails[i].get('uom'),
                                                              buyer_category=productdetails[i].get('cate'),
                                                              buyer_quantity=productdetails[i].get('buyer_quantity'),
                                                              buyer_rfq_number=rfq,
                                                              updated_by=SelfRegistration.objects.get(id=userid),
                                                              created_by=userid)

                for i in range(0, len(terms)):
                    for keys in terms[i]:
                        RfqTermsDescription.objects.create(rfq_number=rfq,
                                                           terms=keys,
                                                           description=terms[i][keys],
                                                           created_by=userid,
                                                           updated_by=SelfRegistration.objects.get(id=userid),
                                                           product_biddings=BuyerProductBidding.objects.get(
                                                               product_bidding_id=BuyerProductBiddingobj.product_bidding_id),
                                                           rfq_type=rfqtype)

            else:
                print("-----",rfqobjcode)

                BuyerProductBiddingobj = BuyerProductBidding.objects.create(product_rfq_number=rfq, user_rfq_number=rfq,
                                                                          user_bidding_numeric=int(rfqobjcode[0].get('numeric'))+1,
                                                                          product_rfq_type=rfqtype,
                                                                          product_publish_date=pdate,
                                                                          product_deadline_date=deadlinedate,
                                                                          product_delivery_date=delidate,
                                                                          product_rfq_currency=currency,
                                                                          product_rfq_category=category,
                                                                          product_department=dept,
                                                                          product_bill_address=billto,
                                                                          product_ship_address=shipto,
                                                                          product_rfq_title=rfqtitle,
                                                                          created_by=userid,
                                                                          updated_by=SelfRegistration.objects.get(id=userid),
                                                                          contact_name=contact_name,
                                                                          phone_number=phone_number,
                                                                          email_id=email_id
                                                                      )

                for i in range(0, len(productdetails)):
                    print(productdetails[i].get('buyer_item_type'))
                    print(productdetails[i].get('buyer_quantity'))
                    BiddingBuyerProductDetails.objects.create(buyer_item_type=productdetails[i].get('buyer_item_type'),
                                                          buyer_item_code=productdetails[i].get('itemcode'),
                                                          buyer_item_name=productdetails[i].get('itemname'),
                                                          buyer_item_description=productdetails[i].get('itemdes'),
                                                          buyer_uom=productdetails[i].get('uom'),
                                                          buyer_category=productdetails[i].get('cate'),
                                                          buyer_quantity=productdetails[i].get('buyer_quantity'),
                                                          buyer_rfq_number=rfq,
                                                          updated_by=SelfRegistration.objects.get(id=userid),
                                                          created_by=userid)

                for i in range(0, len(terms)):
                    for keys in terms[i]:
                        RfqTermsDescription.objects.create(rfq_number=rfq,
                                                       terms=keys,
                                                       description=terms[i][keys],
                                                       created_by=userid,
                                                       updated_by=SelfRegistration.objects.get(id=userid),
                                                       product_biddings=BuyerProductBidding.objects.get(product_bidding_id=BuyerProductBiddingobj.product_bidding_id),
                                                       rfq_type=rfqtype)






            return Response({'status': 200, 'message': 'Buyer  Bidding created'}, status=200)


        else:
            return Response({'status': 200,'MSG':'RFQ code not present'}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def createbuyerbiddinggetvendors(request):
    data=request.data
    rfq=data['rfq']
    rfqtype=data['rfqtype']
    pdate=data['pdate']
    deadlinedate=data['deadlinedate']
    delidate=data['delidate']
    dept=data['dept']
    currency=data['currency']
    category=data['category']
    billto=data['billto']
    shipto=data['shipto']
    rfqtitle=data['rfqtitle']
    # productdetails=data['productdetails']
    termsdetails=data['termdetails']
    userid=data['userid']
    productdetails=data['pdetails']
    terms=data["terms"]
    contact_name=data['contact_name']
    phone_number=data['phone_number']
    email_id=data['email_id']

    try:
        rfqobjcode=RfqCodeSettings.objects.filter(updated_by=userid).values()
        if RfqCodeSettings:
            BuyerProductBiddingobj=BuyerProductBidding.objects.filter(updated_by=userid).values().order_by('-user_rfq_number')
            if BuyerProductBiddingobj:
                print("----+----",BuyerProductBiddingobj[0].get('user_rfq_number'))

                BuyerProductBiddingobj = BuyerProductBidding.objects.create(product_rfq_number=rfq, user_rfq_number=rfq,
                                                                            user_bidding_numeric=int(
                                                                                BuyerProductBiddingobj[0].get('user_bidding_numeric')) + 1,
                                                                            product_rfq_type=rfqtype,
                                                                            product_publish_date=pdate,
                                                                            product_deadline_date=deadlinedate,
                                                                            product_delivery_date=delidate,
                                                                            product_rfq_currency=currency,
                                                                            product_rfq_category=category,
                                                                            product_department=dept,
                                                                            product_bill_address=billto,
                                                                            product_ship_address=shipto,
                                                                            product_rfq_title=rfqtitle,
                                                                            created_by=userid,
                                                                            updated_by=SelfRegistration.objects.get(
                                                                                id=userid),
                                                                            contact_name=contact_name,
                                                                            phone_number=phone_number,
                                                                            email_id=email_id,
                                                                            get_vendors="True",
                                                                            maincore=data['maincore'],
                                                                            category=data['categorydb'],
                                                                            subcategory=data['subcategory']
                                                                            )

                for i in range(0, len(productdetails)):
                    print(productdetails[i].get('buyer_item_type'))
                    print(productdetails[i].get('buyer_quantity'))
                    BiddingBuyerProductDetails.objects.create(buyer_item_type=productdetails[i].get('buyer_item_type'),
                                                              buyer_item_code=productdetails[i].get('itemcode'),
                                                              buyer_item_name=productdetails[i].get('itemname'),
                                                              buyer_item_description=productdetails[i].get('itemdes'),
                                                              buyer_uom=productdetails[i].get('uom'),
                                                              buyer_category=productdetails[i].get('cate'),
                                                              buyer_quantity=productdetails[i].get('buyer_quantity'),
                                                              buyer_rfq_number=rfq,
                                                              updated_by=SelfRegistration.objects.get(id=userid),
                                                              created_by=userid)

                for i in range(0, len(terms)):
                    for keys in terms[i]:
                        RfqTermsDescription.objects.create(rfq_number=rfq,
                                                           terms=keys,
                                                           description=terms[i][keys],
                                                           created_by=userid,
                                                           updated_by=SelfRegistration.objects.get(id=userid),
                                                           product_biddings=BuyerProductBidding.objects.get(
                                                               product_bidding_id=BuyerProductBiddingobj.product_bidding_id),
                                                           rfq_type=rfqtype)

            else:
                print("-----",rfqobjcode)

                BuyerProductBiddingobj = BuyerProductBidding.objects.create(product_rfq_number=rfq, user_rfq_number=rfq,
                                                                          user_bidding_numeric=int(rfqobjcode[0].get('numeric'))+1,
                                                                          product_rfq_type=rfqtype,
                                                                          product_publish_date=pdate,
                                                                          product_deadline_date=deadlinedate,
                                                                          product_delivery_date=delidate,
                                                                          product_rfq_currency=currency,
                                                                          product_rfq_category=category,
                                                                          product_department=dept,
                                                                          product_bill_address=billto,
                                                                          product_ship_address=shipto,
                                                                          product_rfq_title=rfqtitle,
                                                                          created_by=userid,
                                                                          updated_by=SelfRegistration.objects.get(id=userid),
                                                                          contact_name=contact_name,
                                                                          phone_number=phone_number,
                                                                          email_id=email_id
                                                                      )

                for i in range(0, len(productdetails)):
                    print(productdetails[i].get('buyer_item_type'))
                    print(productdetails[i].get('buyer_quantity'))
                    BiddingBuyerProductDetails.objects.create(buyer_item_type=productdetails[i].get('buyer_item_type'),
                                                          buyer_item_code=productdetails[i].get('itemcode'),
                                                          buyer_item_name=productdetails[i].get('itemname'),
                                                          buyer_item_description=productdetails[i].get('itemdes'),
                                                          buyer_uom=productdetails[i].get('uom'),
                                                          buyer_category=productdetails[i].get('cate'),
                                                          buyer_quantity=productdetails[i].get('buyer_quantity'),
                                                          buyer_rfq_number=rfq,
                                                          updated_by=SelfRegistration.objects.get(id=userid),
                                                          created_by=userid)

                for i in range(0, len(terms)):
                    for keys in terms[i]:
                        RfqTermsDescription.objects.create(rfq_number=rfq,
                                                       terms=keys,
                                                       description=terms[i][keys],
                                                       created_by=userid,
                                                       updated_by=SelfRegistration.objects.get(id=userid),
                                                       product_biddings=BuyerProductBidding.objects.get(product_bidding_id=BuyerProductBiddingobj.product_bidding_id),
                                                       rfq_type=rfqtype)






            return Response({'status': 200, 'message': 'Buyer  Bidding created'}, status=200)


        else:
            return Response({'status': 200,'MSG':'RFQ code not present'}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
@permission_classes((AllowAny,))
def termsanddescriptionpriceanalysis(request):
    data=request.data
    userid=data['userid']
    rfq=data['rfq']
    vcode=data['vcode']
    useridarray=[]
    resarray=[]
    try:
        # vendtermsobj=VendorRfqTermsDescription.objects.filter(vendor_rfq_number=rfq,updated_by=userid).values()
        BasicCompanyDetailsobj=BasicCompanyDetails.objects.filter(company_code__in=vcode).values()
        for i in range(len(BasicCompanyDetailsobj)):
            useridarray.append(BasicCompanyDetailsobj[i].get('updated_by_id'))
        buyertermsobj=BuyerProductBidding.objects.filter(updated_by=userid).values()
        if buyertermsobj:
            BiddingBuyerProductDetailsobj=RfqTermsDescription.objects.filter(rfq_number=rfq,updated_by=userid).values()
            if BiddingBuyerProductDetailsobj:
                vendobj=VendorRfqTermsDescription.objects.filter(vendor_rfq_number=rfq,updated_by__in=useridarray).values()
                for i in range(len(vendobj)):
                    singlecomp = BasicCompanyDetails.objects.filter(
                        updated_by=vendobj[i].get('updated_by_id')).values()
                    resarray.append({'compname':singlecomp[0].get('company_name'),
                                     'Buyer_term':vendobj[i].get('vendor_terms'),
                                     'Buyer_description':vendobj[i].get('vendor_description'),
                                     'Vendor_description':vendobj[i].get('vendor_response')})

                print(resarray)

                return Response({'status': 200, 'message': 'ok','buyer_Terms':BiddingBuyerProductDetailsobj,'res':resarray}, status=200)

    except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
def getsourcebasedpk(request):
    data=request.data
    pkid=data['pkid']
    try:
        sourcelistcreateitemsobj = SourceList_CreateItems.objects.filter(id=pkid).values()
        if sourcelistcreateitemsobj:
            Billingaddrsobj=BillingAddress.objects.filter(updated_by=sourcelistcreateitemsobj[0].get('updated_by_id')).values().order_by('id')
            shippingaddrsobj=ShippingAddress.objects.filter(updated_by=sourcelistcreateitemsobj[0].get('updated_by_id')).values().order_by('id')
            comp=BasicCompanyDetails.objects.filter(updated_by=sourcelistcreateitemsobj[0].get('updated_by_id')).values()
            resdict={}
            resdict.setdefault('cname',str(comp[0].get('company_name')))
            resdict.setdefault('shippaddress',shippingaddrsobj[0].get('ship_address'))
            resdict.setdefault('Billingaddress', Billingaddrsobj[0].get('bill_address'))
            sourcelistcreateitemsobj[0].setdefault('address',resdict)
            return Response({'status': 200, 'message': 'Source Leads','data':sourcelistcreateitemsobj}, status=200)
    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)


@api_view(['post'])
def getsorcelistresponse(request):
    data=request.data
    try:
        userid=data['userid']
        resarry=[]
        srcobj=SourceList_CreateItems.objects.filter(updated_by=userid).values()
        print(srcobj)
        if len(srcobj)>0:
            for i in range(0,len(srcobj)):
                srcpublishobj=SourcePublish.objects.filter(source=srcobj[i].get('id')).values()
                # print(srcpublishobj)
                if len(srcpublishobj)>=5:
                    resarry.append({'type':srcobj[i].get('item_type'),
                                    'item_name':srcobj[i].get('item_name'),
                                    'description':srcobj[i].get('item_description'),
                                    'UOM':srcobj[i].get('uom'),
                                    'qty':srcobj[i].get('quantity'),
                                    'source_code':srcobj[i].get('source_code'),
                                    'publishcount':5})
                else:
                    resarry.append({'type': srcobj[i].get('item_type'),
                                    'item_name': srcobj[i].get('item_name'),
                                    'description': srcobj[i].get('item_description'),
                                    'UOM': srcobj[i].get('uom'),
                                    'qty': srcobj[i].get('quantity'),
                                    'source_code': srcobj[i].get('source_code'),
                                    'publishcount': len(srcpublishobj)})
            return Response({'status': 200,'message':'ok','data':resarry},status=200)
        else:
            return Response({'status': 204, 'message': 'Source List Not Present', 'data': []}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)





@api_view(['post'])
def deadline_expired_list(request):
    data = request.data
    userid = data['userid']
    selectsarray=[]
    expiredlistarray=[]
    try:
        basicobj = BasicCompanyDetails.objects.filter(updated_by_id=userid).values()
        selectobj = SelectVendorsForBiddingProduct.objects.filter(vendor_code=basicobj[0].get('company_code')).values().order_by('id')
        if len(selectobj)>0:
            for i in range(0,len(selectobj)):
                selectsarray.append(selectobj[i].get('rfq_number'))
            bidobj=BuyerProductBidding.objects.filter(user_rfq_number__in=selectsarray).values().order_by('product_bidding_id')
            if len(bidobj)>0:
                for i in range(0,len(bidobj)):
                    deadline = bidobj[i].get('product_deadline_date')
                    print(deadline,type(deadline))
                    publish = bidobj[i].get('product_publish_date')
                    publistdateobj = datetime.strptime(publish,'%d-%m-%Y')
                    convertedpublisdate=datetime.date(publistdateobj)
                    print(convertedpublisdate, type(convertedpublisdate))
                    todaydate = date.today()
                    if convertedpublisdate < todaydate > deadline:
                        bids = BuyerProductBidding.objects.get(user_rfq_number=bidobj[i].get('user_rfq_number'))
                        bids.product_rfq_status = 'Expired'
                        bids.save()
                        basicobjval = BasicCompanyDetails.objects.filter(updated_by_id=bidobj[i].get('updated_by_id')).values()
                        bidobjdata = BuyerProductBidding.objects.get(user_rfq_number=bids.user_rfq_number, product_rfq_status='Expired')
                        expiredlistarray.append({'rfq_number': bidobjdata.user_rfq_number,
                                                'vendorcode': basicobjval[0].get('company_code'),
                                                'company_name': basicobjval[0].get('company_name'),
                                                'rfq_title': bidobjdata.product_rfq_title,
                                                'updatedby_id': bidobjdata.updated_by_id,
                                                'publishdate': bidobjdata.product_publish_date,
                                                'deadlinedate': bidobjdata.product_deadline_date,
                                                'bidding_id': bidobjdata.product_bidding_id,
                                                'rfq_status': bidobjdata.product_rfq_status,
                                                'rfq_type': bidobjdata.product_rfq_type,
                                                'department_master': bidobjdata.product_department
                                                })
                return Response({'status': 200, 'message': 'Success', 'data': expiredlistarray}, status=200)
            else:
                return Response({'status': 202,'message': 'Bidding Details Not Present'}, status=202)


        else:
            return Response({'status':204,'message':'Vendors are not present'},status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def extended_deadline_date_list_create(request):
    data = request.data
    userid = data['userid']
    rfqnumber = data['rfqnumber']
    deadline_date = data['deadline_date']
    try:
        bidobj = BuyerProductBidding.objects.filter(user_rfq_number=rfqnumber).values()
        bidrfq = bidobj[0].get('user_rfq_number')
        selectobj = SelectVendorsForBiddingProduct.objects.filter(rfq_number=bidrfq,vendor_status='Accept').values()
        if len(selectobj)>0:
            for i in range(0, len(selectobj)):
                print(selectobj[i].get('vendor_code'))
                vendorcode = selectobj[i].get('vendor_code')
                basicobj = BasicCompanyDetails.objects.filter(company_code=vendorcode).values()
                print(basicobj[0].get('updated_by_id'))
                extended = ExtendedDateListBuyer.objects.create(user_rfq_number=bidrfq,
                                                              vendor_code=selectobj[i].get('vendor_code'),
                                                              product_bidding_id=bidobj[0].get('product_bidding_id'),
                                                              product_rfq_status=bidobj[0].get('product_rfq_status'),
                                                              rfq_type=bidobj[0].get('product_rfq_type'),
                                                              product_publish_date=bidobj[0].get('product_publish_date'),
                                                              product_department=bidobj[0].get('product_department'),
                                                              product_deadline_date=deadline_date,
                                                              product_rfq_title=bidobj[0].get('product_rfq_title'),
                                                              updated_by=SelfRegistration.objects.get(
                                                                  id=selectobj[i].get('updated_by_id')),
                                                              created_by=selectobj[i].get('updated_by_id'),
                                                              userid=userid,
                                                              company_name=basicobj[0].get('company_name'))
            return Response({'status': 201, 'message': 'Extended DeadLine Data Created Successfully'}, status=201)
        else:
            return Response({'status': 204, 'message': 'Vendors Not Present'}, status=204)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def extended_deadline_list_show(request):
    data = request.data
    # userid=data['userid']
    vendorcode = data['vendorcode']
    newarray = []
    try:
        extendedobj = ExtendedDateListBuyer.objects.filter(vendor_code=vendorcode).values()
        print(len(extendedobj))
        if len(extendedobj)>0:
            for i in range(0, len(extendedobj)):
                print('yes',extendedobj[i].get('user_rfq_number'))
                selectsobj = SelectVendorsForBiddingProduct.objects.filter(rfq_number=extendedobj[i].get('user_rfq_number')).values()
                print(len(selectsobj),'select')
                if len(selectsobj)>0:
                    userids = selectsobj[i].get('updated_by_id')
                    basicobj = BasicCompanyDetails.objects.filter(updated_by_id=userids).values()
                    newarray.append({'ccode': basicobj[0].get('company_code'),
                                     'cname': basicobj[0].get('company_name'),
                                     'rfq_number': extendedobj[i].get('user_rfq_number'),
                                     'rfq_title': extendedobj[i].get('product_rfq_title'),
                                     'rfq_type': extendedobj[i].get('rfq_type'),
                                     'status': extendedobj[i].get('product_rfq_status'),
                                     'published_date': extendedobj[i].get('product_publish_date'),
                                     'deadline_date': extendedobj[i].get('product_deadline_date'),
                                     'department': extendedobj[i].get('product_department')
                                     })
            return Response({'status': 200, 'message': 'ok', 'data': newarray}, status=200)
        else:
            return Response({'status': 204, 'message': 'Not found'}, status=204)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
# @permission_classes([AllowAny, ])
def advance_search_bidding_list(request):
    # external vendor advance search
    data = request.data
    user_rfq_number = data['user_rfq_number']
    product_rfq_title = data['product_rfq_title']
    product_publish_date = data['product_publish_date']
    product_department = data['product_department']
    product_rfq_currency = data['product_rfq_currency']
    product_rfq_category = data['product_rfq_category']
    product_deadline_date = data['product_deadline_date']
    product_delivery_date = data['product_delivery_date']
    valuearray = data['valuearray']
    bidlistarray = []
    try:
        for i in range(0, len(valuearray)):
            if user_rfq_number.lower() in valuearray[i].get('user_rfq_number').lower() and product_rfq_title.lower() in valuearray[i].get(
                    'product_rfq_title').lower() and product_rfq_title.lower() in valuearray[i].get('product_rfq_title').lower() and product_department.lower() in valuearray[i].get('product_department').lower() and \
                    product_rfq_currency.lower() in valuearray[i].get(
                'product_rfq_currency').lower() and product_rfq_category.lower() in valuearray[i].get('product_rfq_category').lower() and \
                    product_deadline_date.lower() in valuearray[i].get(
                'product_deadline_date').lower() and product_delivery_date.lower() in valuearray[i].get(
                'product_delivery_date').lower():
                bidlistarray.append(valuearray[i])
            else:
                print('Not Present')
        return Response({'status': 200, 'message': 'ok', 'data': bidlistarray}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
# @permission_classes([AllowAny, ])
def advance_search_open_leads_list(request):
    # external vendor advance search
    data = request.data
    vendor_code = data['vendor_code']
    user_rfq_number = data['user_rfq_number']
    company_name = data['company_name']
    product_rfq_title = data['product_rfq_title']
    product_publish_date = data['product_publish_date']
    product_deadline_date = data['product_deadline_date']
    product_delivery_date=data['product_delivery_date']
    product_rfq_currency=data['product_rfq_currency']
    product_rfq_category=data['product_rfq_category']
    product_department=data['product_department']
    valuearray = data['valuearray']
    openleadsarray = []
    try:
        for i in range(0, len(valuearray)):
            if vendor_code.lower() in valuearray[i].get('vendor_code').lower() and \
                    user_rfq_number.lower() in valuearray[i].get('user_rfq_number').lower() and \
                    company_name.lower() in valuearray[i].get('company_name').lower() and \
                    product_rfq_title.lower() in valuearray[i].get('product_rfq_title').lower() and \
                    product_publish_date.lower() in valuearray[i].get('product_publish_date').lower() and \
                    product_deadline_date.lower() in valuearray[i].get('product_deadline_date').lower() and \
                    product_delivery_date.lower() in valuearray[i].get('product_delivery_date').lower() and \
                    product_rfq_currency.lower() in valuearray[i].get('product_rfq_currency').lower() and \
                    product_rfq_category.lower() in valuearray[i].get('product_rfq_category').lower() and \
                    product_department.lower() in valuearray[i].get('product_department').lower():
                openleadsarray.append(valuearray[i])
            else:
                print('Not Present')
        return Response({'status': 200, 'message': 'ok', 'data': openleadsarray}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['post'])
# @permission_classes([AllowAny, ])
def advance_search_published_leads_list(request):
    # external vendor advance search
    data = request.data
    company_name = data['company_name']
    # product_bill_address = data['product_bill_address']
    product_deadline_date = data['product_deadline_date']
    product_department = data['product_department']
    product_publish_date = data['product_publish_date']
    # product_rfq_status = data['product_rfq_status']
    product_rfq_title = data['product_rfq_title']
    # product_rfq_type = data['product_rfq_type']
    # product_ship_address=data['product_ship_address']
    user_rfq_number=data['user_rfq_number']
    vendor_code=data['vendor_code']
    vendor_status=data['vendor_status']
    valuearray = data['valuearray']
    openleadsarray = []
    try:
        for i in range(0, len(valuearray)):
            if company_name.lower() in valuearray[i].get('company_name').lower() and \
                    product_deadline_date.lower() in valuearray[i].get('product_deadline_date').lower() and \
                    product_department.lower() in valuearray[i].get('product_department').lower() and \
                    product_publish_date.lower() in valuearray[i].get('product_publish_date').lower() and \
                    product_rfq_title.lower() in valuearray[i].get('product_rfq_title').lower() and \
                    user_rfq_number.lower() in valuearray[i].get('user_rfq_number').lower() and \
                    vendor_status.lower() in valuearray[i].get('vendor_status').lower() and \
                    product_department.lower() in valuearray[i].get('product_department').lower():
                openleadsarray.append(valuearray[i])
            else:
                print('Not Present')
        return Response({'status': 200, 'message': 'ok', 'data': openleadsarray}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
# @permission_classes([AllowAny, ])
def advance_search_expired_list(request):
    # external vendor advance search
    data = request.data
    company_name = data['company_name']
    deadlinedate = data['deadlinedate']
    department_master = data['department_master']
    publishdate = data['publishdate']
    rfq_number = data['rfq_number']
    # rfq_status = data['rfq_status']
    rfq_title = data['rfq_title']
    # rfq_type = data['rfq_type']
    valuearray = data['valuearray']
    openleadsarray = []
    try:
        for i in range(0, len(valuearray)):
            if company_name.lower() in valuearray[i].get('company_name').lower() and \
                    deadlinedate.lower() in valuearray[i].get('deadlinedate').lower() and \
                    department_master.lower() in valuearray[i].get('department_master').lower() and \
                    publishdate.lower() in valuearray[i].get('publishdate').lower() and \
                    rfq_number.lower() in valuearray[i].get('rfq_number').lower() and \
                    rfq_title.lower() in valuearray[i].get('rfq_title').lower():
                openleadsarray.append(valuearray[i])
            else:
                print('Not Present')
        return Response({'status': 200, 'message': 'ok', 'data': openleadsarray}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
# @permission_classes([AllowAny, ])
def advance_search_po_list(request):
    # external vendor advance search
    data = request.data
    PO_date = data['PO_date']
    PO_expirydate = data['PO_expirydate']
    PO_num = data['PO_num']
    company_name = data['company_name']
    delivery_date = data['delivery_date']
    # rfq_status = data['rfq_status']
    delivery_days = data['delivery_days']
    remind_date = data['remind_date']
    rfq_number=data['rfq_number']
    rfq_title=data['rfq_title']
    vendorcode=data['vendorcode']
    valuearray = data['valuearray']
    poarray = []
    try:
        for i in range(0, len(valuearray)):
            if PO_date.lower() in valuearray[i].get('PO_date').lower() and \
                    PO_expirydate.lower() in valuearray[i].get('PO_expirydate').lower() and \
                    PO_num.lower() in valuearray[i].get('PO_num').lower() and \
                    company_name.lower() in valuearray[i].get('company_name').lower() and \
                    delivery_date.lower() in valuearray[i].get('delivery_date').lower() and \
                    delivery_days.lower() in valuearray[i].get('delivery_days').lower() and \
                    remind_date.lower() in valuearray[i].get('remind_date').lower() and \
                    rfq_number.lower() in valuearray[i].get('rfq_number').lower() and \
                    rfq_title.lower() in valuearray[i].get('rfq_title').lower() and \
                    vendorcode.lower() in valuearray[i].get('vendorcode').lower():
                poarray.append(valuearray[i])
            else:
                print('Not Present')
        return Response({'status': 200, 'message': 'ok', 'data': poarray}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
# @permission_classes([AllowAny, ])
def advance_search_award_list(request):
    # external vendor advance search
    data = request.data
    rfq_number = data['rfq_number']
    company_code = data['company_code']
    company_name = data['company_name']
    totalamount = data['totalamount']
    rfq_title = data['rfq_title']
    # product_code = data['product_code']
    # product_name = data['product_name']
    # product_description=data['product_description']
    awarded_date=data['awarded_date']
    publish_date=data['publish_date']
    deadline_date=data['deadline_date']
    valuearray = data['valuearray']
    awardarray = []
    try:
        for i in range(0, len(valuearray)):
            print('yes')
            if rfq_number.lower() in valuearray[i].get('rfq_number').lower() and \
                    company_code.lower() in valuearray[i].get('company_code').lower() and \
                    company_name.lower() in valuearray[i].get('company_name').lower() and \
                    totalamount.lower() in valuearray[i].get('totalamount').lower() and \
                    rfq_title.lower() in valuearray[i].get('rfq_title').lower() and \
                    awarded_date.lower() in valuearray[i].get('awarded_date').lower() and \
                    publish_date.lower() in valuearray[i].get('publish_date').lower() and \
                    deadline_date.lower() in valuearray[i].get('deadline_date').lower():
                awardarray.append(valuearray[i])
            else:
                print('Not Present')
        return Response({'status': 200, 'message': 'ok', 'data': awardarray}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def source_awards(request):
    data=request.data
    source_code=data['source_code']
    source_type=data['source_type']
    source_item_type=data['source_item_type']
    source_item_name=data['source_item_name']
    source_item_description=data['source_item_description']
    source_uom=data['source_uom']
    source_delivery_charges=data['source_delivery_charges']
    source_frieght_charges=data['source_frieght_charges']
    source_pf_charges=data['source_pf_charges']
    source_product_category=data['source_product_category']
    source_priority=data['source_priority']
    source_department=data['source_department']
    userid = data['userid']
    sourcepk = data['sourcepk']
    item_details=data['item_details']

    try:
        print(len(item_details),'fsdfsdf')
        for i in range(0,len(item_details)):
            print(len(item_details), ' if length')
            sourceobj = SourceAwards.objects.filter(source_code=source_code,company_name=item_details[i].get('company_name'),source_publish_pk=item_details[i].get('source_publish_pk')).values()
            if len(sourceobj) == 0:
                basicobj=BasicCompanyDetails.objects.filter(company_name=item_details[i].get('company_name')).values()
                SourceAwards.objects.create(source_code=source_code,
                                      source_type=source_type,
                                      source_item_type=source_item_type,
                                      source_item_name=source_item_name,
                                      source_item_description=source_item_description,
                                      source_uom=source_uom,
                                      source_delivery_charges=source_delivery_charges,
                                      source_frieght_charges=source_frieght_charges,
                                      source_pf_charges=source_pf_charges,
                                      source_product_category=source_product_category,
                                      source_priority=source_priority,
                                      source_department=source_department,
                                      source_quantity=item_details[i].get('source_quantity'),
                                      source_unit_rate=item_details[i].get('source_unit_rate'),
                                      source_tax=item_details[i].get('source_tax'),
                                      source_discount=item_details[i].get('source_discount'),
                                      source_total_amount=item_details[i].get('source_total_amount'),
                                      company_name=item_details[i].get('company_name'),
                                      source_publish_pk=SourcePublish.objects.get(id=item_details[i].get('source_publish_pk')),
                                      company_code=basicobj[0].get('company_code'),
                                      created_by=userid,
                                      updated_by=SelfRegistration.objects.get(id=userid),
                                      source_create_pk=SourceList_CreateItems.objects.get(id=sourcepk))

            else:
                print('already_present')
                sourceobj = SourceAwards.objects.filter(source_code=source_code,company_name=item_details[i].get('company_name'),
                                                        source_publish_pk=item_details[i].get(
                                                            'source_publish_pk')).values()
                sourcedelete = SourceAwards.objects.get(id=sourceobj[0].get('id'))
                sourcedelete.delete()

                basicobj = BasicCompanyDetails.objects.filter(company_name=item_details[i].get('company_name')).values()
                SourceAwards.objects.create(source_code=source_code,
                                            source_type=source_type,
                                            source_item_type=source_item_type,
                                            source_item_name=source_item_name,
                                            source_item_description=source_item_description,
                                            source_uom=source_uom,
                                            source_delivery_charges=source_delivery_charges,
                                            source_frieght_charges=source_frieght_charges,
                                            source_pf_charges=source_pf_charges,
                                            source_product_category=source_product_category,
                                            source_priority=source_priority,
                                            source_department=source_department,
                                            source_quantity=item_details[i].get('source_quantity'),
                                            source_unit_rate=item_details[i].get('source_unit_rate'),
                                            source_tax=item_details[i].get('source_tax'),
                                            source_discount=item_details[i].get('source_discount'),
                                            source_total_amount=item_details[i].get('source_total_amount'),
                                            company_name=item_details[i].get('company_name'),
                                            source_publish_pk=SourcePublish.objects.get(
                                                id=item_details[i].get('source_publish_pk')),
                                            company_code=basicobj[0].get('company_code'),
                                            created_by=userid,
                                            updated_by=SelfRegistration.objects.get(id=userid),
                                            source_create_pk=SourceList_CreateItems.objects.get(id=sourcepk))
                # return Response({'status': 201, 'message': 'Source Award Created'}, status=201)
        return Response({'status': 201, 'message': 'Source Award Created'}, status=201)




    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


class SourceAwardsViewSet(viewsets.ModelViewSet):
    queryset = SourceAwards.objects.all()
    serializer_class = SourceAwardsSerializer


    def get_queryset(self):
        sourceawardsobj = SourceAwards.objects.filter(updated_by=self.request.GET.get('updated_by'))
        if sourceawardsobj:
            return sourceawardsobj
        raise ValidationError(
            {'message': 'Source Award of particular user id is not exist', 'status': 204})


@api_view(['put'])
def update_status_to_po_sent(request):
    data=request.data
    sourceaward=data['sourceaward']
    try:
        poobj=SourceAwards.objects.filter(id=sourceaward).values()
        if len(poobj)>0:
            poobjget=SourceAwards.objects.get(id=poobj[0].get('id'))
            if poobjget.source_po_status=='Pending':
                poobjget.source_po_status='PO_Sent'
                poobjget.save()
                return Response({'status': 200, 'message': 'Status Updated to PO_Sent'}, status=200)
            else:
                return Response({'status': 202, 'message': 'Already Updated'}, status=202)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=204)


    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def source_po_list_based_on_userid(request):
    data=request.data
    userid=data['userid']
    try:
        sourcepoobj=SourceAwards.objects.filter(updated_by_id=userid,source_po_status='PO_Sent').values()
        print(len(sourcepoobj))
        if len(sourcepoobj)>0:
            return Response({'status': 200, 'message': 'PO List','data':sourcepoobj}, status=200)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=202)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def priceanalysistermslist(request):
    data = request.data
    rfqno=data['rfqno']
    userid=data['userid']
    res=[]
    iter=0
    vcode=data['vcode']
    idaarray=[]
    try:

        basicobj=BasicCompanyDetails.objects.filter(company_code__in=vcode).values().order_by('company_name')
        print(basicobj)
        for i in range(0,len(basicobj)):
            idaarray.append(basicobj[i].get('updated_by_id'))
        print(idaarray)
        bidmaintable = BuyerProductBidding.objects.filter(product_rfq_number=rfqno).values()
        if bidmaintable:
            RfqTermsDescriptionobj=RfqTermsDescription.objects.filter(updated_by=userid,rfq_number=rfqno).values()
            selectedvendorobj=VendorRfqTermsDescription.objects.filter(vendor_rfq_number=rfqno,updated_by__in=idaarray).values().order_by('updated_by_id')
            print(len(selectedvendorobj))
            for i in range(len(RfqTermsDescriptionobj)):
                res.append({'BuyerTerm':RfqTermsDescriptionobj[i].get('terms'),
                            'BuyerDesc':RfqTermsDescriptionobj[i].get('description')})
                for j in range(0,len(selectedvendorobj)):
                    if RfqTermsDescriptionobj[i].get('terms')==selectedvendorobj[j].get('vendor_terms'):
                        print(RfqTermsDescriptionobj[i].get('terms'))
                        res[i].setdefault('compres'+str(iter),selectedvendorobj[j].get('vendor_response'))
                        iter=iter+1
                iter=0

            return Response({'status': 200, 'message': 'Term List', 'data': res}, status=200)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=202)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
def deadline_date_list(request):
    userid=request.data['userid']
    from_registration=request.data['from_registration']
    regarray=[]
    expiredarray=[]
    try:
        if from_registration == 'False':
            basicobj = BasicCompanyDetails.objects.filter(updated_by=userid).values()
            # print(basicobj)
            selectvendorsobj = SelectVendorsForBiddingProduct.objects.filter(vendor_code=basicobj[0].get('company_code'),
                                                                             vendor_status='Pending',
                                                                             from_registration='False').values()
            # print(len(selectvendorsobj),'length')
            if len(selectvendorsobj) > 0:
                for i in range(0, len(selectvendorsobj)):

                    # print(selectvendorsobj[i].get('rfq_number'),'selected vendors rfq')
                    biddingval = BuyerProductBidding.objects.get(user_rfq_number=selectvendorsobj[i].get('rfq_number'),
                                                                 from_registration=from_registration)
                    print(biddingval.product_deadline_date, '--------')
                    basicobjval = BasicCompanyDetails.objects.filter(updated_by_id=biddingval.updated_by_id).values()
                    todaydate = date.today()
                    if biddingval.product_deadline_date > todaydate:
                        pass
                    else:

                        expiredarray.append({'vendor_code': basicobjval[0].get('company_code'),
                                             'user_rfq_number': biddingval.user_rfq_number,
                                             'company_name': basicobjval[0].get('company_name'),
                                             'product_rfq_type': biddingval.product_rfq_type,
                                             'product_rfq_title': biddingval.product_rfq_title,
                                             'product_rfq_status': biddingval.product_rfq_status,
                                             'product_publish_date': biddingval.product_publish_date,
                                             'product_deadline_date': biddingval.product_deadline_date,
                                             'product_delivery_date': biddingval.product_delivery_date,
                                             'product_rfq_currency': biddingval.product_rfq_currency,
                                             'product_rfq_category': biddingval.product_rfq_category,
                                             'product_department': biddingval.product_department,
                                             })
                return Response({'status':200,'message':'ok','data':expiredarray},status=200)
            else:
                return Response({'status': 200, 'message': 'Data Not Present', 'data':expiredarray}, status=200)
    except Exception as e:
        return Response({'status':500,'error':str(e)},status=500)



@api_view(['post'])
def vendor_side_award_search(request):
    data=request.data
    rfq_number=data['rfq_number']
    company_name = data['company_name']
    company_code = data['company_code']
    rfq_title = data['rfq_title']
    # product_code = data['product_code']
    # rfq_status = data['rfq_status']
    # product_name = data['product_name']
    # product_description = data['product_description']
    awarded_date  = data['awarded_date']
    publish_date = data['publish_date']
    deadline_date  = data['deadline_date']
    total_amount=data['total_amount']
    valuearray = data['valuearray']
    vendorawardarray = []
    try:
        for i in range(0, len(valuearray)):
            if rfq_number.lower() in valuearray[i].get('rfq_number').lower() and \
                    company_name.lower() in valuearray[i].get('company_name').lower() and \
                    company_code.lower() in valuearray[i].get('company_code').lower() and \
                    rfq_title.lower() in valuearray[i].get('rfq_title').lower() and \
                    awarded_date.lower() in valuearray[i].get('awarded_date').lower() and \
                    publish_date.lower() in valuearray[i].get('publish_date').lower() and \
                    deadline_date.lower() in valuearray[i].get('deadline_date').lower() and \
                    total_amount.lower() in valuearray[i].get('total_amount').lower():
                vendorawardarray.append(valuearray[i])
            else:
                print('Not Present')
        return Response({'status': 200, 'message': 'ok', 'data': vendorawardarray}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
def vendor_side_po_search(request):
    data=request.data
    rfq_number = data['rfq_number']
    company_code = data['company_code']
    company_name = data['company_name']
    rfq_title = data['rfq_title']
    PO_num = data['PO_num']
    delivery_days = data['delivery_days']
    PO_date  = data['PO_date']
    PO_expirydate = data['PO_expirydate']
    delivery_date= data['delivery_date']
    remind_date=data['remind_date']
    valuearray = data['valuearray']
    poarray = []
    try:
        for i in range(0, len(valuearray)):
            if rfq_number.lower() in valuearray[i].get('rfq_number').lower() and \
                    company_code.lower() in valuearray[i].get('company_code').lower() and \
                    company_name.lower() in valuearray[i].get('company_name').lower() and \
                    rfq_title.lower() in valuearray[i].get('rfq_title').lower() and \
                    PO_num.lower() in valuearray[i].get('PO_num').lower() and \
                    delivery_days.lower() in valuearray[i].get('delivery_days').lower() and \
                    PO_date.lower() in valuearray[i].get('PO_date').lower() and \
                    PO_expirydate.lower() in valuearray[i].get('PO_expirydate').lower() and \
                    delivery_date.lower() in valuearray[i].get('delivery_date').lower() and \
                    remind_date.lower() in valuearray[i].get('remind_date').lower():
                poarray.append(valuearray[i])
            else:
                print('Not Present')
        return Response({'status': 200, 'message': 'ok', 'data': poarray}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def source_award_search(request):
    data=request.data
    company_code = data['company_code']
    company_name = data['company_name']
    source_code = data['source_code']
    source_type=data['source_type']
    source_item_type = data['source_item_type']
    source_item_name = data['source_item_name']
    source_quantity = data['source_quantity']
    source_delivery_charges = data['source_delivery_charges']
    source_frieght_charges = data['source_frieght_charges']
    source_pf_charges = data['source_pf_charges']
    source_department = data['source_department']
    source_product_category=data['source_product_category']
    source_total_amount=data['source_total_amount']
    valuearray = data['valuearray']
    sourceawardarray = []
    try:
        for i in range(0, len(valuearray)):
            if company_code.lower() in valuearray[i].get('company_code').lower() and \
                    company_name.lower() in valuearray[i].get('company_name').lower() and \
                    source_code.lower() in valuearray[i].get('source_code').lower() and \
                    source_type.lower() in valuearray[i].get('source_type').lower() and \
                    source_item_type.lower() in valuearray[i].get('source_item_type').lower() and \
                    source_item_name.lower() in valuearray[i].get('source_item_name').lower() and \
                    source_quantity.lower() in valuearray[i].get('source_quantity').lower() and \
                    source_delivery_charges.lower() in valuearray[i].get('source_delivery_charges').lower() and \
                    source_frieght_charges.lower() in valuearray[i].get('source_frieght_charges').lower() and \
                    source_pf_charges.lower() in valuearray[i].get('source_pf_charges').lower() and \
                    source_department.lower() in valuearray[i].get('source_department').lower() and \
                    source_product_category.lower() in valuearray[i].get('source_product_category').lower() and \
                    source_total_amount.lower() in valuearray[i].get('source_total_amount').lower():
                sourceawardarray.append(valuearray[i])
            else:
                print('Not Present')

        return Response({'status': 200, 'message': 'ok', 'data': sourceawardarray}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['post'])
def purchase_order_email(request):
    data=request.data
    pkid=data['pkid']
    rfq_type=data['rfq_type']
    dictval=[]
    try:
        poobj=PurchaseOrder.objects.filter(id=pkid).values()
        if len(poobj)>0:
            poobjget=PurchaseOrder.objects.get(id=poobj[0].get('id'))
            awardobj = Awards.objects.filter(rfq_number=poobjget.rfq_number, company_code=poobjget.vendorcode).values()
            if len(awardobj)>0:
                if poobjget.attachment1!="" or poobjget.attachment2!="" or poobjget.attachment3!="":
                    ccode = awardobj[0].get('company_code')
                    quantity = awardobj[0].get('buyer_bid_quantity')
                    itemstotal = awardobj[0].get('product_code')
                    basicobj = BasicCompanyDetails.objects.filter(company_code=ccode).values()
                    regobj = SelfRegistration.objects.get(id=basicobj[0].get('updated_by_id'))
                    if poobjget.attachment1:
                        urlvalue1 = "https://v2apis.vendorsin.com/" + poobjget.attachment1.url
                        dictval.append({"url":urlvalue1})

                    if poobjget.attachment2:
                        urlvalue2 = "https://v2apis.vendorsin.com/" + poobjget.attachment2.url
                        dictval.append({"url":urlvalue2})

                    if poobjget.attachment3:
                        urlvalue3 = "https://v2apis.vendorsin.com/" + poobjget.attachment3.url
                        dictval.append({"url": urlvalue3})
                    configuration = sib_api_v3_sdk.Configuration()
                    configuration.api_key[
                        'api-key'] = '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'
                    headers = {
                        'accept': 'application/json',
                        'content-type': 'application/json',
                    }
                    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
                    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                        to=[{"email": "vyshnavi.ms@vendorsin.com", "name": "vyshnavi"}],
                        template_id=23, params={
                            "rfqnumber": poobjget.rfq_number,
                            "podate": poobjget.PO_date,
                            "ponumber": poobjget.PO_num,
                            "poexpiry": poobjget.PO_expirydate,
                            "quantity": str(quantity),
                            'items': str(len(itemstotal)),
                            "companyname": basicobj[0].get('company_name')
                        },
                        headers=headers,
                        subject='PO Confirm',
                        attachment=dictval
                    )
                    api_response = api_instance.send_transac_email(send_smtp_email)
                    print(api_response)
                if poobjget.attachment1=="" and poobjget.attachment2=="" and poobjget.attachment3=="":
                    ccode = awardobj[0].get('company_code')
                    quantity = awardobj[0].get('buyer_bid_quantity')
                    itemstotal = awardobj[0].get('product_code')
                    basicobj = BasicCompanyDetails.objects.filter(company_code=ccode).values()
                    regobj = SelfRegistration.objects.get(id=basicobj[0].get('updated_by_id'))
                    configuration = sib_api_v3_sdk.Configuration()
                    configuration.api_key[
                        'api-key'] = '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'
                    headers = {
                        'accept': 'application/json',
                        'content-type': 'application/json',
                    }
                    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
                    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                        to=[{"email": "vyshnavi.ms@vendorsin.com", "name": "vyshnavi"}],
                        template_id=23, params={
                            "rfqnumber": poobjget.rfq_number,
                            "podate": poobjget.PO_date,
                            "ponumber": poobjget.PO_num,
                            "poexpiry": poobjget.PO_expirydate,
                            "quantity": str(quantity),
                            'items': str(len(itemstotal)),
                            "companyname": basicobj[0].get('company_name')
                        },
                        headers=headers,
                        subject='PO Confirm'
                    )
                    api_response = api_instance.send_transac_email(send_smtp_email)
                    print(api_response)
                return Response({'status': 200, 'message': 'ok', 'data': poobj}, status=200)
        return Response({'status': 204, 'message': 'Not Yet Awarded or award details are not present'}, status=200)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def source_list_leads_all(request):
    data = request.data
    sourceleadsarray = []
    userid = data['userid']
    listarray = []
    try:
        sourcepublish = SourcePublish.objects.filter(updated_by_id=userid).values().order_by('id')
        for i in range(0, len(sourcepublish)):
            sourceleadsarray.append(sourcepublish[i].get('source_id'))
        print(sourceleadsarray)
        for i in range(0,len(sourcepublish)):
            sourcobj = SourceList_CreateItems.objects.filter(id=sourceleadsarray[i], get_vendors='False').values()
            if sourcobj:
                basicval = BasicCompanyDetails.objects.filter(updated_by_id=sourcobj[0].get('updated_by_id')).values()
                billingobj = BillingAddress.objects.filter(company_code_id=basicval[0].get('company_code'),
                                                           updated_by_id=basicval[0].get('updated_by_id')).values()
                listarray.append({'id': sourcobj[0].get('id'),
                                  'company_code': basicval[0].get('company_code'),
                                  'company_name': basicval[0].get('company_name'),
                                  'source_code': sourcobj[0].get('source_code'),
                                  'source': sourcobj[0].get('source'),
                                  'item_type': sourcobj[0].get('item_type'),
                                  'quantity': sourcobj[0].get('quantity'),
                                  'source_required_city': sourcobj[0].get('source_required_city'),
                                  'product_category': sourcobj[0].get('product_category'),
                                  'client_city': billingobj[0].get('bill_city'),
                                  'updated_by': sourcobj[0].get('updated_by_id'),
                                  'item_name': sourcobj[0].get('item_name'),
                                  'source_publish_pk': sourcepublish[i].get('id')
                                  })

        return Response({'status': 200, 'message': 'Source Leads', 'data': listarray}, status=200)
    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)

@api_view(['post'])
def source_list_open_leads_all(request):
    data = request.data
    sourceleadsarray = []
    userid = data['userid']
    listarray = []
    try:
        sourcepublish = SourcePublish.objects.filter(updated_by_id=userid).values().order_by('id')
        for i in range(0, len(sourcepublish)):
            sourceleadsarray.append(sourcepublish[i].get('source_id'))
        print(sourceleadsarray)
        i = 0
        while i < len(sourcepublish):

            sourcobj = SourceList_CreateItems.objects.filter(id=sourceleadsarray[i],get_vendors='True').values()
            if sourcobj:
                basicval = BasicCompanyDetails.objects.filter(updated_by_id=sourcobj[0].get('updated_by_id')).values()
                billingobj = BillingAddress.objects.filter(company_code_id=basicval[0].get('company_code'),
                                                           updated_by_id=basicval[0].get('updated_by_id')).values()
                listarray.append({'id': sourcobj[0].get('id'),
                                  'company_code': basicval[0].get('company_code'),
                                  'company_name': basicval[0].get('company_name'),
                                  'source_code': sourcobj[0].get('source_code'),
                                  'source': sourcobj[0].get('source'),
                                  'item_type': sourcobj[0].get('item_type'),
                                  'quantity': sourcobj[0].get('quantity'),
                                  'source_required_city': sourcobj[0].get('source_required_city'),
                                  'product_category': sourcobj[0].get('product_category'),
                                  'client_city': billingobj[0].get('bill_city'),
                                  'updated_by': sourcobj[0].get('updated_by_id'),
                                  'item_name': sourcobj[0].get('item_name'),
                                  'vspid': sourcepublish[i].get('id')
                                  })
            i = i + 1

        return Response({'status': 200, 'message': 'Source Leads', 'data': listarray}, status=200)
    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)





@api_view(['post'])
def fetch_source_data_by_userid(request):
    data=request.data
    userid=data['userid']

    try:
        sourceobj=SourceList_CreateItems.objects.filter(updated_by_id=userid).values().order_by('id')
        if len(sourceobj)>0:
            return Response({'status':200,'message':'Source List','data':sourceobj},status=status.HTTP_200_OK)
        else:
            return  Response({'status':204,'message':'Source Data Not Present'},status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes((AllowAny,))
def buyer_award_bidding(request):
    data = request.data
    company_code= data['company_code']
    rfq_number = data['rfq_number']
    try:
            company_details=BasicCompanyDetails.objects.filter(company_code=company_code).values()
            if company_details:
                vendor_product_bidding =VendorProductBidding.objects.filter(vendor_user_rfq_number=rfq_number,updated_by=company_details[0].get('updated_by_id')).values()
                if vendor_product_bidding:
                    Vendor_Bidding_Buyer_Product_Details =VendorBiddingBuyerProductDetails.objects.filter(vendor_rfq_number=rfq_number,updated_by=company_details[0].get('updated_by_id')).values()
                    Vendor_Rfq_Terms_Description = VendorRfqTermsDescription.objects.filter(vendor_rfq_number=rfq_number,vendor_product_biddings =vendor_product_bidding[0].get('vendor_product_bidding_id')).values()
                return Response({'status': 200, 'message': 'ok','vendorbidbasic':vendor_product_bidding,'vendorbiddingbyerproductdetails':Vendor_Bidding_Buyer_Product_Details,'vendorrfqtermsdescription':Vendor_Rfq_Terms_Description}, status=200)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
@permission_classes((AllowAny,))
def get_all_source_leads(request):
    get_vendors=request.data['get_vendors']
    try:
        if get_vendors=='True':
            bidobj =SourceList_CreateItems.objects.filter(get_vendors=get_vendors).values().order_by('-id')
            if len(bidobj)>-0:
                for i in range(0,len(bidobj)):
                    basicobj=BasicCompanyDetails.objects.filter(updated_by_id=bidobj[i].get('updated_by_id')).values()
                    bidobj[i].__setitem__('company_name',basicobj[0].get('company_name'))
                return Response({'status': 200, 'message': 'ok', 'data': bidobj}, status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)
        else:
            return Response({'status': 202, 'message': 'Matching data does not exist'}, status=202)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)

@api_view(['post'])
@permission_classes((AllowAny,))
def get_all_source_leads_by_id(request):
    data = request.data
    id = data['source_pk']
    try:
        bidobj=SourceList_CreateItems.objects.filter(id=id).values()
        if len(bidobj)>0:
            basicobj=BasicCompanyDetails.objects.filter(updated_by_id=bidobj[0].get('updated_by_id')).values()
            if basicobj:
                billobj=BillingAddress.objects.filter(updated_by_id=basicobj[0].get('updated_by_id')).values()
                if billobj:
                    bidobj[0].__setitem__('company_code',basicobj[0].get('company_code'))
                    bidobj[0].__setitem__('company_name', basicobj[0].get('company_name'))
                    bidobj[0].__setitem__('bill_address',billobj[0].get('bill_address'))
                else:
                    bidobj[0].__setitem__('bill_address',"")


            else:
                bidobj[0].__setitem__('company_code', "")
                bidobj[0].__setitem__('company_name', "")

            return Response({'status': 200, 'message': 'ok', 'data': bidobj}, status=200)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
def terms_master_description_settings(request):
    data=request.data
    userid=data['userid']
    try:
        termmastersettingsobj=BiddingTermMasterSettings.objects.create(terms_name=data['terms_name'],
                                                                       terms_description=data['terms_description'],
                                                                       updated_by=SelfRegistration.objects.get(id=userid),
                                                                       created_by=userid
                                                                       )
        return Response({'status': 201, 'message': 'Terms Created'}, status=201)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
def terms_master_settings(request):
    data=request.data
    userid=data['userid']
    try:
        termmastersettingsobj=BiddingTermMasterSettings.objects.create(terms_name=data['terms_name'],
                                                                       terms_description=[],
                                                                       updated_by=SelfRegistration.objects.get(id=userid),
                                                                       created_by=userid
                                                                       )
        return Response({'status': 201, 'message': 'Terms Created'}, status=201)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)



# @api_view(['put'])
# def edit_terms_master_settings(request):
#     data=request.data
#     termid=data['termid']
#     try:
#         termobj=BiddingTermMasterSettings.objects.filter(id=id).values()
#         if len(termobj)>0:
#             termbidobj=BiddingTermMasterSettings.objects.get(id=id)
#             if termbidobj:
#                 termobj.term
#         return Response({'status': 201, 'message': 'Terms Created'}, status=201)
#     except Exception as e:
#         return Response({'status': 500, 'error': str(e)}, status=500)



@api_view(['post'])
@permission_classes((AllowAny,))
def get_all_bidding_leads(request):
    key=request.data['key']
    get_vendors=request.data['get_vendors']
    resarray=[]
    materialquantity=0
    try:
        if key == "vsinadmin":
            if get_vendors=='True':
                bidobj =BuyerProductBidding.objects.filter(get_vendors=get_vendors).values().order_by('-product_bidding_id')
                if len(bidobj)>0:
                    for i in range(0,len(bidobj)):
                        BiddingBuyerProductDetailsobj=BiddingBuyerProductDetails.objects.filter(buyer_rfq_number=bidobj[0].get('user_rfq_number')).values()
                        for j in range(0,len(BiddingBuyerProductDetailsobj)):
                            materialquantity=materialquantity+int(BiddingBuyerProductDetailsobj[j].get('buyer_quantity'))

                        resarray.append({'product_bidding_id':bidobj[0].get('product_bidding_id'),
                                          'product_rfq_number':bidobj[0].get('product_rfq_number'),
                                          'user_rfq_number':bidobj[0].get('user_rfq_number'),
                                          'product_rfq_type':bidobj[0].get('product_rfq_type'),
                                          'product_publish_date':bidobj[0].get('product_publish_date'),
                                          'product_deadline_date':bidobj[0].get('product_deadline_date'),
                                          'product_delivery_date':bidobj[0].get('product_delivery_date'),
                                          'product_bill_address':bidobj[0].get('product_bill_address'),
                                          'product_ship_address':bidobj[0].get('product_ship_address'),
                                          'product_rfq_title':bidobj[0].get('product_rfq_title'),
                                          'Maincore':bidobj[0].get('maincore'),
                                          'Category':bidobj[0].get('category'),
                                          'subcategory':bidobj[0].get('subcategory'),
                                          'productcount':len(BiddingBuyerProductDetailsobj),
                                          'quantitycount':materialquantity})
                        materialquantity=0
                    return Response({'status': 200, 'message': 'ok', 'data': resarray}, status=200)
                else:
                    return Response({'status': 204, 'message': 'Not Present'}, status=204)
            else:
                return Response({'status': 202, 'message': 'Matching data does not exist'}, status=202)
        else:
            return Response({'status': 401, 'message': 'UnAuthorized'}, status=401)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)




@api_view(['post'])
@permission_classes((AllowAny,))
def get_all_bidding_by_id(request):
    data = request.data
    key=data['key']
    product_bidding_id = data['product_bidding_id']
    try:
        if key=="vsinadmin":
            bidobj =BuyerProductBidding.objects.filter(product_bidding_id=product_bidding_id).values()
            if len(bidobj)>0:
                return Response({'status': 200, 'message': 'ok', 'data': bidobj}, status=200)
            else:
                return Response({'status': 204, 'message': 'Not Present'}, status=204)
        else:
            return Response({'status': 401, 'message': 'UnAuthorized'}, status=401)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def bidding_list_leads(request):
    data = request.data
    vendorbiddingarray = []
    userid = data['userid']
    listarray = []
    try:
        vendorbidobj = VendorProductBidding.objects.filter(updated_by_id=userid).values().order_by('vendor_product_bidding_id')
        for i in range(0, len(vendorbidobj)):
            vendorbiddingarray.append(vendorbidobj[i].get('vendor_product_rfq_number'))
        print(vendorbiddingarray)
        for i in range(0,len(vendorbidobj)):
            bidobj = BuyerProductBidding.objects.filter(product_rfq_number=vendorbiddingarray[i], get_vendors='False').values()
            if bidobj:
                basicval = BasicCompanyDetails.objects.filter(updated_by_id=bidobj[0].get('updated_by_id')).values()
                billingobj = BillingAddress.objects.filter(company_code_id=basicval[0].get('company_code'),
                                                           updated_by_id=basicval[0].get('updated_by_id')).values()
                listarray.append({'product_bidding_id': bidobj[0].get('product_bidding_id'),
                                  'company_code': basicval[0].get('company_code'),
                                  'company_name': basicval[0].get('company_name'),
                                  'product_rfq_number': bidobj[0].get('product_rfq_number'),
                                  'user_rfq_number': bidobj[0].get('user_rfq_number'),
                                  'product_rfq_type': bidobj[0].get('product_rfq_type'),
                                  'product_rfq_status': bidobj[0].get('product_rfq_status'),
                                  'product_publish_date': bidobj[0].get('product_publish_date'),
                                  'product_deadline_date': bidobj[0].get('product_deadline_date'),
                                  'bill_city': billingobj[0].get('bill_city'),
                                  'updated_by': bidobj[0].get('updated_by_id'),
                                  'product_delivery_date': bidobj[0].get('product_delivery_date'),
                                  'product_rfq_currency':bidobj[0].get('product_rfq_currency'),
                                  'product_rfq_category':bidobj[0].get('product_rfq_category'),
                                  'product_department':bidobj[0].get('product_department'),
                                  'product_bill_address':bidobj[0].get('product_bill_address'),
                                  'product_ship_address':bidobj[0].get('product_ship_address'),
                                  'product_rfq_title':bidobj[0].get('product_rfq_title'),
                                  'contact_name':bidobj[0].get('contact_name'),
                                  'phone_number':bidobj[0].get('phone_number'),
                                  'email_id':bidobj[0].get('email_id'),
                                  'vendor_product_bidding_id': vendorbidobj[i].get('vendor_product_bidding_id')
                                  })

        return Response({'status': 200, 'message': 'Bidding Leads List', 'data': listarray}, status=200)
    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)



@api_view(['post'])
def bidding_open_leads_all_true(request):
    data = request.data
    bidarray = []
    userid = data['userid']
    listarray = []
    try:
        bidpublish = VendorProductBidding.objects.filter(updated_by_id=userid).values().order_by('vendor_product_bidding_id')
        for i in range(0, len(bidpublish)):
            bidarray.append(bidpublish[i].get('vendor_product_rfq_number'))
        print(bidarray)
        i = 0
        while i < len(bidpublish):

            bidobj = BuyerProductBidding.objects.filter(product_rfq_number=bidarray[i], get_vendors='True').values()
            if bidobj:
                basicval = BasicCompanyDetails.objects.filter(updated_by_id=bidobj[0].get('updated_by_id')).values()
                billingobj = BillingAddress.objects.filter(company_code_id=basicval[0].get('company_code'),
                                                           updated_by_id=basicval[0].get('updated_by_id')).values()
                listarray.append({'id': bidobj[0].get('product_bidding_id'),
                                  'company_code': basicval[0].get('company_code'),
                                  'company_name': basicval[0].get('company_name'),
                                  'product_rfq_number': bidobj[0].get('product_rfq_number'),
                                  'user_rfq_number': bidobj[0].get('user_rfq_number'),
                                  'product_rfq_type': bidobj[0].get('product_rfq_type'),                                  'product_rfq_status': bidobj[0].get('product_rfq_status'),
                                  'product_publish_date': bidobj[0].get('product_publish_date'),
                                  'product_deadline_date': bidobj[0].get('product_deadline_date'),
                                  'bill_city': billingobj[0].get('bill_city'),
                                  'updated_by': bidobj[0].get('updated_by_id'),
                                  'product_delivery_date': bidobj[0].get('product_delivery_date'),
                                  'product_rfq_currency':bidobj[0].get('product_rfq_currency'),
                                  'product_rfq_category':bidobj[0].get('product_rfq_category'),
                                  'product_department':bidobj[0].get('product_department'),
                                  'product_bill_address':bidobj[0].get('product_bill_address'),
                                  'product_ship_address':bidobj[0].get('product_ship_address'),
                                  'product_rfq_title':bidobj[0].get('product_rfq_title'),
                                  'contact_name':bidobj[0].get('contact_name'),
                                  'phone_number':bidobj[0].get('phone_number'),
                                  'email_id':bidobj[0].get('email_id'),
                                  'vendor_product_bidding_id': bidpublish[i].get('vendor_product_bidding_id')
                                  })
            i = i + 1

        return Response({'status': 200, 'message': 'Bidding Leads', 'data': listarray}, status=200)
    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)

@api_view(['post'])
@permission_classes((AllowAny,))
def getparticularcommonrfqdetailsinlandingpage(request):
    data=request.data
    listarray=[]
    try:
        if data['key']=="vsinadmin":
            BuyerProductBiddingobj=BuyerProductBidding.objects.filter(product_bidding_id=data['id']).values()
            if BuyerProductBiddingobj:
                rfqpublishedcompany = BasicCompanyDetails.objects.filter(updated_by=BuyerProductBiddingobj[0].get('updated_by_id')).values('company_name')
                BiddingBuyerProductDetailsobj=BiddingBuyerProductDetails.objects.filter(buyer_rfq_number=BuyerProductBiddingobj[0].get('product_rfq_number')).values()
                for i in range(0,len(BiddingBuyerProductDetailsobj)):
                    doc1=BuyerProductDetails.objects.filter(buyer_item_code=BiddingBuyerProductDetailsobj[0].get('buyer_item_code')).values('buyer_document')
                    if doc1:
                        if doc1[0].get('buyer_document'):
                            document1=doc1[0].get('buyer_document')
                        else:
                            document1=""
                        if doc1[0].get('buyer_document_1'):
                            document2=doc1[0].get('buyer_document_1')
                        else:
                            document2=""
                        if doc1[0].get('buyer_document_2'):
                            document3=doc1[0].get('buyer_document_2')
                        else:
                            document3=""
                RfqTermsDescriptionobj=RfqTermsDescription.objects.filter(rfq_number=BuyerProductBiddingobj[0].get('product_rfq_number')).values()
                return Response({'status': 200, 'message': 'Bidding Leads', 'Biddata': BuyerProductBiddingobj,'rfqproductdata':BiddingBuyerProductDetailsobj,'Bidterm':RfqTermsDescriptionobj,'compname':rfqpublishedcompany[0].get('company_name'),'document1':document1,'document2':document2,'document3':document3}, status=200)
            else:
                return Response({'status': 202, 'message': 'Bid not exist'}, status=202)
        else:
            return Response({'status': 400, 'message': 'bad request'}, status=400)
    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)

#Common RFQ Published List Api
@api_view(['post'])
def getpublishedcommonrfqbid(request):
    try:
        data=request.data
        resdata=[]
        i=0;
        VendorProductBiddingOpenCommonBidobj=VendorProductBiddingOpenCommonBid.objects.filter(updated_by=data['userid']).values()
        if VendorProductBiddingOpenCommonBidobj:
            print(VendorProductBiddingOpenCommonBidobj)
            while i<len(VendorProductBiddingOpenCommonBidobj):
                BuyerProductBiddingobj=BuyerProductBidding.objects.filter(product_rfq_number=VendorProductBiddingOpenCommonBidobj[i].get('vendor_product_rfq_number')).values()
                basiccompaniinfo=BasicCompanyDetails.objects.filter(updated_by=BuyerProductBiddingobj[0].get('updated_by_id')).values()
                resdata.append({'company_name':basiccompaniinfo[0].get('company_name'),
                                'vendor_code':basiccompaniinfo[0].get('company_code'),
                                'user_rfq_number':VendorProductBiddingOpenCommonBidobj[i].get('vendor_product_rfq_number'),
                                'product_rfq_title':VendorProductBiddingOpenCommonBidobj[i].get('vendor_product_rfq_title'),
                                'vendor_status':VendorProductBiddingOpenCommonBidobj[i].get('vendor_product_rfq_status'),
                                'product_publish_date':VendorProductBiddingOpenCommonBidobj[i].get('vendor_product_publish_date'),
                                'product_deadline_date':VendorProductBiddingOpenCommonBidobj[i].get('vendor_product_deadline_date'),
                                'product_rfq_type':VendorProductBiddingOpenCommonBidobj[i].get('vendor_product_rfq_type'),
                                'publishedID':VendorProductBiddingOpenCommonBidobj[i].get('vendor_product_bidding_id')})

                i=i+1
            return Response({'status': 200, 'message': 'Bidding Leads', 'data': resdata}, status=200)
        else:
            return Response({'status': 202, 'message': 'Not Exist'}, status=202)
    except Exception as e:
        return Response({'status': 500, 'message': str(e)}, status=500)



@api_view(['post'])
@permission_classes((AllowAny,))
def get_source_items_list_by_source_user_id(request):
    data = request.data
    sourceuserid = data['sourceuserid']
    try:
        sourceobj = SourcePublish.objects.filter(source_user_id=sourceuserid).values()
        if len(sourceobj) > 0:
            for i in range(0,len(sourceobj)):
                compobj=BasicCompanyDetails.objects.filter(updated_by=sourceobj[i].get('updated_by_id')).values()
                sourceobj[i].setdefault('compname',compobj[0].get('company_name'))
                sourcecreateobj=SourceList_CreateItems.objects.filter(id=sourceobj[i].get('source_id')).values()
                sourceobj[i].setdefault('source_required_city',sourcecreateobj[0].get('source_required_city'))

            return Response({'status': 200, 'message': 'Source Create Items List', 'data': sourceobj},
                            status=status.HTTP_200_OK)

        else:
            return Response({'status': 204, 'message': 'Not Found'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['post'])
def get_companies_based_on_source_pk(request):
    data=request.data
    buyer_source_pk=data['buyer_source_pk']
    companyarray=[]
    amountarray=[]
    count=0
    try:
        sourcepublishobj=SourcePublish.objects.filter(source_id=buyer_source_pk).values()
        if len(sourcepublishobj)>0:
            for i in range(0,len(sourcepublishobj)):
                amountarray.append(float(sourcepublishobj[i].get('source_total_amount')))
            amountarray.sort()

            for j in range(0, len(amountarray)):
                count = count + 1
                print(count)
                if count == 6:
                    print('5  oonly')
                    break
                publishsource = SourcePublish.objects.filter(source_id=buyer_source_pk).values()

                basicobj=BasicCompanyDetails.objects.filter(updated_by_id=publishsource[j].get('updated_by_id')).values()
                if len(basicobj)>0:
                    companyarray.append({
                        'company_code':basicobj[0].get('company_code'),
                        'company_name': basicobj[0].get('company_name'),
                        'user_id':basicobj[0].get('updated_by_id'),
                        'source_total_amount':amountarray[j]

                    })
                else:
                    pass
            return Response({'status':200,'message':'Vendor Publish Company List','data':companyarray},status=status.HTTP_200_OK)
        else:
            return Response({'status':204,'message':'Source Publish Details Not Present','data':companyarray},status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['post'])
def vendor_source_responses(request):
    data=request.data
    vendor_user_id=data['vendor_user_id']
    publish_pk=data['publish_pk']

    try:
        sourceobj=SourceList_CreateItems.objects.filter(id=publish_pk).values()
        if len(sourceobj)>0:
            sourcepublishobj=SourcePublish.objects.filter(updated_by_id=vendor_user_id,source_id=sourceobj[0].get('id')).values()
            return Response({'status':200,'message':'Vendor Response for Source','data':sourcepublishobj,'pf_charges':sourceobj[0].get('p_f_charges'),'frieght_charges':sourceobj[0].get('frieght_charges'),'delivery':sourceobj[0].get('delivery')},status=status.HTTP_200_OK)
        else:
            return Response({'status':204,'message':'Source Publish Details are not present'},status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['post'])
def get_source_awards_by_user_id(request):
    data=request.data
    userid=data['userid']
    try:
        sourceobj=SourceAwards.objects.filter(updated_by_id=userid).values().order_by('id')
        if len(sourceobj)>0:
            for i in range(0,len(sourceobj)):
                sourcecreateobj=SourceList_CreateItems.objects.filter(id=sourceobj[i].get('source_create_pk_id')).values()
                sourceobj[i].setdefault('deadline_date',sourcecreateobj[0].get('deadline_date'))
                sourceobj[i].setdefault('buyer_user_id',sourcecreateobj[0].get('updated_by_id')),
                sourceobj[i].setdefault('publish_date',sourcecreateobj[0].get('publish_date'))

            return Response({'status':200,'message':'Source Award List','data':sourceobj},status=status.HTTP_200_OK)
        else:
            return Response({'status':204,'message':'Source Award Not Present','data':sourceobj},status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['post'])
def get_source_pubish_leads_based_on_publish_pk(request):
    data = request.data
    source_publish_pk = data['source_publish_pk']
    try:
        sourceobj = SourcePublish.objects.filter(id=source_publish_pk).values().order_by('id')
        if len(sourceobj) > 0:
            for i in range(0, len(sourceobj)):
                sourcecreateobj = SourceList_CreateItems.objects.filter(id=sourceobj[i].get('source_id')).values()
                return Response(
                    {'status': 200, 'message': 'Source Publish List', 'source_create_buyer_data': sourcecreateobj,
                     'source_publish_vendor_data': sourceobj}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'Source Award Not Present', 'data': sourceobj},
                            status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SourcePurchaseOrderViewset(viewsets.ModelViewSet):
    queryset = SourcePurchaseOrder.objects.all()
    serializer_class = SourcePurchaseOrderSerializer

    def create(self, request, *args, **kwargs):
        source_publish_pk = request.data.get('source_publish_pk', None)
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key[
            'api-key'] = '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'
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
        }
        sourcepublishobj = SourcePublish.objects.filter(id=source_publish_pk).values()
        if sourcepublishobj:
            basicobj = BasicCompanyDetails.objects.get(updated_by_id=sourcepublishobj[0].get('updated_by_id'))
            regobj = SelfRegistration.objects.get(id=basicobj.updated_by_id)
            print(regobj.username, 'ok')
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": regobj.username, "name": regobj.contact_person}],
                template_id=33, params={
                    "itemname": request.data['item_name'],
                    "itemdescription": request.data['item_description'],
                    "podate": request.data['po_date'],
                    "ponum": request.data['po_number'],
                    # "poexpires": request.data['PO_expirydate'],
                    "quantity": sourcepublishobj[0].get('source_quantity'),
                    "companyname": basicobj.company_name
                },
                headers=headers,
                subject='PO Confirmation'
            )  # SendSmtpEmail | Values to send a transactional email
            # Send a transactional email
            api_response = api_instance.send_transac_email(send_smtp_email)
            print(api_response)
        else:
            print('Not Present')
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        sourceobj = SourcePurchaseOrder.objects.filter(updated_by=self.request.GET.get('updated_by')).order_by('id')
        if sourceobj:
            return sourceobj
        raise ValidationError(
            {'message': 'Source Purchase Order details of particular user id is not exist', 'status': 204})


@api_view(['put'])
def update_source_po_status(request):
    data = request.data
    awardpk = data['awardpk']
    try:
        awardobj = SourceAwards.objects.filter(id=awardpk).values()
        if len(awardobj) > 0:
            awards = SourceAwards.objects.get(id=awardpk)
            if awards.source_po_status == 'Pending':
                awards.source_po_status = 'PO_Sent'
                awards.save()
                return Response({'status': 200, 'message': 'Source PO sent successfully', 'data': awards.source_po_status},
                                status=200)
            else:
                if awards.source_po_status == 'PO_Sent':
                    return Response({'status': 202, 'message': 'Source PO Already Sent'}, status=202)
                else:
                    return Response({'status': 202, 'message': 'PO sent failed or po not sent'}, status=202)

        else:
            return Response({'status': 204, 'message': 'No data found'}, status=204)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def source_publish_data_store(request):
    try:
        data = request.data
        source_id = data['source_id']
        updated_by = data['updated_by']
        source_total_amount = data['source_total_amount']
        sourcearray=[]
        publish_array=[]
        sourcepublishobj = SourcePublish.objects.filter(
            source=source_id).values().order_by('source_total_amount')
        if len(sourcepublishobj) < 5:
            SourcePublish.objects.create(source_item_type=data['source_item_type'],
                                             source_type=data['source_type'],
                                             source_department=data['source_department'],
                                             source_code=data['source_code'],
                                             source_present_cost=data['source_present_cost'],
                                             source_target_cost=data['source_target_cost'],
                                             source_pf_charges=data['source_pf_charges'],
                                             source_frieght_charges=data['source_frieght_charges'],
                                             source_delivery_charges=data['source_delivery_charges'],
                                             source_item_code=data['source_item_code'],
                                             source_item_name=['source_item_name'],
                                             source_item_description=data['source_item_description'],
                                             source_uom=data['source_uom'],
                                             source_product_category=data['source_product_category'],
                                             source_priority=data['source_priority'],
                                             source_quantity=data['source_quantity'],
                                             source_tax=data['source_tax'],
                                             source_unit_rate=data['source_unit_rate'],
                                             source_discount=data['source_discount'],
                                             source_total_amount=data['source_total_amount'],
                                             source=SourceList_CreateItems.objects.get(
                                                 id=data['source_id']),
                                             source_user_id=data['source_user_id'],
                                             created_by=updated_by,
                                             updated_by=SelfRegistration.objects.get(id=updated_by),
                                             source_payment_terms=data['source_payment_terms'],
                                             source_warranty=data['source_warranty']
                                             )
        else:
            for i in range(0, len(sourcepublishobj)):
                if float(source_total_amount)==float(sourcepublishobj[i].get('source_total_amount')) and len(sourcepublishobj)==5:
                    return Response({'status':202,'message':'5 data exist already'},status=202)
                else:
                    sourcearray.append(float(sourcepublishobj[i].get('source_total_amount')))
                sourcearray.sort()
            val = max(sourcearray)
            if float(source_total_amount)< val:
                print(val,'lll')
                amount=int(val)

                sourcepublishobj1 = SourcePublish.objects.filter(
                    source_id=source_id,source_total_amount=amount).values().order_by('source_total_amount')
                print(len(sourcepublishobj1),'length')
                sourceobj = SourcePublish.objects.get(id=sourcepublishobj1[0].get('id'))
                print(sourceobj.source_total_amount, sourceobj.source_total_amount, sourceobj.id)
                sourceobj.delete()
                SourcePublish.objects.create(source_item_type=data['source_item_type'],
                                             source_type=data['source_type'],
                                             source_department=data['source_department'],
                                             source_code=data['source_code'],
                                             source_present_cost=data['source_present_cost'],
                                             source_target_cost=data['source_target_cost'],
                                             source_pf_charges=data['source_pf_charges'],
                                             source_frieght_charges=data['source_frieght_charges'],
                                             source_delivery_charges=data['source_delivery_charges'],
                                             source_item_code=data['source_item_code'],
                                             source_item_name=['source_item_name'],
                                             source_item_description=data['source_item_description'],
                                             source_uom=data['source_uom'],
                                             source_product_category=data['source_product_category'],
                                             source_priority=data['source_priority'],
                                             source_quantity=data['source_quantity'],
                                             source_tax=data['source_tax'],
                                             source_unit_rate=data['source_unit_rate'],
                                             source_discount=data['source_discount'],
                                             source_total_amount=data['source_total_amount'],
                                             source=SourceList_CreateItems.objects.get(
                                                 id=data['source_id']),
                                             source_user_id=data['source_user_id'],
                                             created_by=updated_by,
                                             updated_by=SelfRegistration.objects.get(id=updated_by),
                                             source_payment_terms=data['source_payment_terms'],
                                             source_warranty=data['source_warranty']
                                             )
        return Response({'status': 200, 'message': 'ok'}, status=200)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)