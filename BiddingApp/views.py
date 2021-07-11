from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from MaterialApp.models import BuyerProductDetails
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
