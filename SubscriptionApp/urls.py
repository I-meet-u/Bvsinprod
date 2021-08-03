from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router=DefaultRouter()
router.register('plan-model',views.PlanModelViewset)
router.register('subscription-model',views.SubscriptionModelViewset),
# router.register('razorpay-model',views.RazorpayModelViewset)

urlpatterns = [
    path('razorpay-router-urls/',include(router.urls)),
    path('fetch-all-plans/',views.fetch_all_plan),
    path('fetch-all-subscriptions/',views.fetch_all_subscriptions)
]
