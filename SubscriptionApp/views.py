from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from Vendorsinprojectversion2.settings import RAZORPAY_PUBLIC_KEY, RAZORPAY_SECRET_KEY
from .models import *
from .serializers import *
# import  environ
import razorpay

# env=environ.Env()
# environ.Env.read_env()



class PlanModelViewset(viewsets.ModelViewSet):
    queryset = PlanModel.objects.all()
    serializer_class = PlanModelSerializer

    def create(self, request, *args, **kwargs):
        client = razorpay.Client(auth=(RAZORPAY_PUBLIC_KEY,RAZORPAY_SECRET_KEY))
        period=request.data.get('period')
        interval = request.data.get('interval')
        item=request.data.get('item')
        notes=request.data.get('notes_key_1',None)
        updated_by=request.data.get('updated_by',None)
        try:
            registerobj=SelfRegistration.objects.get(id=updated_by)

            planvalue=client.plan.create({'period':period,
                                          'interval':interval,
                                          'item':item,
                                          'notes':notes
                                          })
            planmodel=PlanModel.objects.create(plan_id=planvalue['id'],
                                               entity=planvalue['entity'],
                                               interval=planvalue['interval'],
                                               plan_created_at=planvalue['created_at'],
                                               period=planvalue['period'],
                                               notes=planvalue['notes'],
                                               item=planvalue['item'],
                                               item_id=planvalue['item']['id'],
                                               item_name=planvalue['item']['name'],
                                               item_description=planvalue['item']['description'],
                                               amount=planvalue['item']['amount'],
                                               currency=planvalue['item']['currency'],
                                               item_created_at=planvalue['item']['created_at'],
                                               item_updated_at=planvalue['item']['updated_at'],
                                               updated_by=SelfRegistration.objects.get(id=updated_by),
                                               email_id=registerobj.username,
                                               phone_number=registerobj.phone_number)
            serializer = PlanModelSerializer(planmodel)

            data={
                'Razorpay_Plan':planvalue,
                'Our_Server_Plan':serializer.data
            }
            print(data)
            return Response({'status': 201, 'message': 'Plan created', 'data':data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def get_queryset(self):
        fetchplanbyid = PlanModel.objects.filter(plan_id=self.request.GET.get('plan_id'))
        if fetchplanbyid:
            return fetchplanbyid
        raise ValidationError(
            {'message': 'Data not exist for this plan id', 'status': 204})


@api_view(['get'])
def fetch_all_plan(request):
    try:
        client = razorpay.Client(auth=(RAZORPAY_PUBLIC_KEY,RAZORPAY_SECRET_KEY))
        countplan=PlanModel.objects.count()
        fetchallplan = PlanModel.objects.filter().values()

        return Response({'status': 200, 'message': 'Plan created','count':countplan,'data': fetchallplan},
                    status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubscriptionModelViewset(viewsets.ModelViewSet):
    queryset = SubscriptionModel.objects.all()
    serializer_class = SubscriptionModelSerializer

    def create(self, request, *args, **kwargs):
        valq=[]
        plan_id=request.data.get('plan_id')
        total_count=request.data.get('total_count')
        start_at=request.data.get('start_at',None)
        expire_by=request.data.get('expire_by',None)
        # offer_id=request.data.get('offer_id',None)
        notes=request.data.get('notes',None)
        notify_info=request.data.get('notify_info',None)
        print(type(notify_info))
        customer_notify=request.data.get('customer_notify',None)
        try:
            for i in range(0,len(notify_info)):
                print(notify_info[i])
                print(notify_info[i]['notify_phone'])
                phone=notify_info[i]['notify_phone']
                email = notify_info[i]['notify_email']
                print(email)
            client = razorpay.Client(auth=(RAZORPAY_PUBLIC_KEY,RAZORPAY_SECRET_KEY))
            razorpaysubscription=client.subscription.create({'plan_id':plan_id,
                                                        'total_count':total_count,
                                                        'start_at':start_at,
                                                        'expire_by':expire_by,
                                                        # 'offer_id':offer_id,
                                                        'customer_notify':customer_notify,
                                                        'notes':notes,
                                                        'notify_info':notify_info
                                                        })


            # print(razorpaysubscription[])
            # our server subscription
            subscriptionobj=SubscriptionModel.objects.create(subscription_id=razorpaysubscription['id'],
                                                             entity=razorpaysubscription['entity'],
                                                             plan_id=razorpaysubscription['plan_id'],
                                                             status=razorpaysubscription['status'],
                                                             current_start=razorpaysubscription['current_start'],
                                                             current_end=razorpaysubscription['current_end'],
                                                             ended_at=razorpaysubscription['ended_at'],
                                                             quantity=razorpaysubscription['quantity'],
                                                             notes=razorpaysubscription['notes'],
                                                             charge_at=razorpaysubscription['charge_at'],
                                                             start_at=razorpaysubscription['start_at'],
                                                             end_at=razorpaysubscription['end_at'],
                                                             auth_attempts=razorpaysubscription['auth_attempts'],
                                                             total_count=razorpaysubscription['total_count'],
                                                             paid_count=razorpaysubscription['paid_count'],
                                                             customer_notify=razorpaysubscription['customer_notify'],
                                                             created_at=razorpaysubscription['created_at'],
                                                             expire_by=razorpaysubscription['expire_by'],
                                                             short_url=razorpaysubscription['short_url'],
                                                             has_scheduled_changes=razorpaysubscription['has_scheduled_changes'],
                                                             change_scheduled_at=razorpaysubscription['change_scheduled_at'],
                                                             # offer_id=razorpaysubscription['offer_id'],
                                                             remaining_count=razorpaysubscription['remaining_count'],
                                                             notify_email=email,
                                                             notify_phone=phone)
            serializer = SubscriptionModelSerializer(subscriptionobj)
            data={
                'subscriptionobj':serializer.data
            }
            return Response({'status':201,'message':'Subscription Created','data':data},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)