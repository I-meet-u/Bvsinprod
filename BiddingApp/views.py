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

    # def create(self, request, *args, **kwargs):
    #     userid = request.data.get('userid',None)
    #     product_rfq_type=request.data.get('product_rfq_type',None)
    #     product_publish_date=request.data.get('product_publish_date',None)
    #     product_deadline_date=request.data.get('product_deadline_date',None)
    #     product_delivery_date=request.data.get('product_delivery_date',None)
    #     product_department=request.data.get('product_department',None)
    #     product_rfq_currency = request.data.get('product_rfq_currency', None)
    #     product_rfq_category = request.data.get('product_rfq_category', None)
    #     product_bill_address=request.data.get('product_bill_address',None)
    #     product_ship_address=request.data.get('product_ship_address',None)
    #     product_rfq_title=request.data.get('product_rfq_title',None)
    #
    #     buyerbiddingobj = BuyerProductBidding.objects.filter(updated_by=userid).order_by('-bidding_numeric').values()
    #     if buyerbiddingobj:
    #         numeric=buyerbiddingobj[0].get('buyer_numeric')+1
    #         buyer_rfq_number=str(buyerbiddingobj[0].get('buyer_numeric'))
    #         request.data['buyer_rfq_number'] = buyer_rfq_number
    #         request.data['numeric'] = numeric
    #
    #     else:
    #         numeric =40002
    #         buyer_rfq_number =40001
    #         request.data['buyer_rfq_number'] = buyer_rfq_number
    #         request.data['numeric'] = numeric
    #         return super().create(request, *args, **kwargs)

class BiddingBuyerProductDetailsView(viewsets.ModelViewSet):
    queryset = BiddingBuyerProductDetails.objects.all()
    serializer_class = BiddingBuyerProductDetailsSerializer
    permission_classes = [permissions.AllowAny]
    ordering_fields = ['id']
    ordering = ['id']


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