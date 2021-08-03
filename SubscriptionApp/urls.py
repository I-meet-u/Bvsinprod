from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router=DefaultRouter()
router.register('razorpay-model',views.RazorpayModelViewset)

urlpatterns = [
    path('razorpay-router-urls/',include(router.urls))
]
