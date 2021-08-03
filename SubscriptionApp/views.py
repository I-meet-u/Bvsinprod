from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from Vendorsinprojectversion2.settings import RAZORPAY_PUBLIC_KEY, RAZORPAY_SECRET_KEY
from .models import *
from .serializers import *
import razorpay

class PlanModelViewset(viewsets.ModelViewSet):
    queryset = PlanModel.objects.all()
    serializer_class = PlanModelSerializer

    def get_queryset(self):
        fetchplanbyid = PlanModel.objects.filter(plan_id=self.request.GET.get('plan_id'))
        if fetchplanbyid:
            return fetchplanbyid
        raise ValidationError(
            {'message': 'Data not exist for this plan id', 'status': 204})


@api_view(['get'])
def fetch_all_plan(request):
    try:
        fetchallplan = PlanModel.objects.filter().values()
        if len(fetchallplan)>0:
            return Response({'status': 200, 'message': 'All Plan List','data': fetchallplan},
                    status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'Not Present'},status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubscriptionModelViewset(viewsets.ModelViewSet):
    queryset = SubscriptionModel.objects.all()
    serializer_class = SubscriptionModelSerializer


    def get_queryset(self):
        fetchsubscriptionbbyid = SubscriptionModel.objects.filter(subscription_id=self.request.GET.get('subscription_id'))
        if fetchsubscriptionbbyid:
            return fetchsubscriptionbbyid
        raise ValidationError(
            {'message': 'Data not exist for this subscription id', 'status': 204})

@api_view(['get'])
def fetch_all_subscriptions(request):
    try:
        fetachallsubscriptionsobj=SubscriptionModel.objects.filter().values()
        if len(fetachallsubscriptionsobj)>0:
            return Response({'status': 200, 'message': 'All Subscription List', 'data': fetachallsubscriptionsobj},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': 204, 'message': 'Not Present'}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#
# class RazorpayModelViewset(viewsets.ModelViewSet):
#     queryset = RazorpayModel.objects.all()
#     serializer_class = RazorpayModelSerializer