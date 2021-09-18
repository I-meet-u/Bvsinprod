
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
    path('advance-search-invite-vendor/', views.advance_search_invite_vendor),
    path('advance-search-external-vendor/', views.advance_search_external_vendor),
    path('getinternalvendor/',views.getinternalvendor),
    path('buzrequestcreate/',views.buzrequestcreate),
    path('sendergetbuzrequestdata/',views.sendergetbuzrequestdata),
    path('searchinternalvendor/',views.searchinternalvendor),
    path('buzrequest/',views.buzrequest),
    path('business-request-accept-reject-advance-search/',views.business_request_accept_reject_advance_search),
    path('search-business-request-advance-search/',views.search_business_request_advance_search),
    path('update-business-status/',views.update_business_status),
    path('get-internal-buyer/',views.get_internal_buyer),
    path('buyer-list/',views.buyer_list),
    path('add-users-internal-buyer-and-internal-vendor/',views.add_users_internal_buyer_and_internal_vendor),
    path('update-invite-vendor-registration-status/', views.update_invite_vendor_registration_status),
    path('all-vendors-list/', views.all_vendors_list),
    path('business-request-accept-list/', views.business_request_accept_list),
    path('business-request-accept-list-userid/', views.business_request_accept_list_user_id),
    path('business-request-reject-list/', views.business_request_reject_list),
    path('buyer-dashboard-charts-counts/', views.buyer_dashboard_charts_counts),
    path('vendor-dashboard-count/', views.vendor_dashboard_count),
    path('advance-search-item-list/', views.advance_search_item_list)

    ]