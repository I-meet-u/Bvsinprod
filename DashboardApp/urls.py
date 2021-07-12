
from django.urls import path,include
from rest_framework import routers
from . import views

router=routers.DefaultRouter()

router.register('invite-vendor', views.InviteVendorView)
router.register('business-request', views.BusinessRequestView)
router.register('internal-vendor', views.InternalVendorView)
router.register('internal-buyer', views.InternalBuyerView)

urlpatterns = [
    path('dashboard-router-urls/',include(router.urls)),
    path('get-all-details-for-business-request/',views.get_all_details_for_business_request),
    path('external-vendor/',views.external_vendor),
    path('advancesearch-business-request/',views.advancesearch_business_request),
    path('advance-search-external-vendor/',views.advance_search_external_vendor),
    path('advance-search-invite-vendor/', views.advance_search_invite_vendor),
    ]