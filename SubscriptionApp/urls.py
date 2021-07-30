from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router=DefaultRouter()
router.register('plan-model',views.PlanModelViewset)
router.register('subscription-model',views.SubscriptionModelViewset)

urlpatterns = [
    path('router-urls/',include(router.urls)),
    path('fetch-all-plan/',views.fetch_all_plan)
]
