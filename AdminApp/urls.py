# from django.urls import path,include
# from rest_framework import routers
# from . import views
#
# router=routers.DefaultRouter()
#
# router.register('admin-invite', views.AdminInviteView)
# router.register('create-user', views.CreateUserView)
# router.register('admin-register',views.AdminRegisterView)
#
#
# urlpatterns = [
#     path('admin-router-urls/',include(router.urls)),
#     path('admin-login/',views.admin_login),
#     path('create-user-status-update/',views.create_user_status_update),
#     path('admin-email-otp-verify/',views.admin_email_otp_verify),
#     path('registration-list/', views.registration_list),
#     path('admin-approval-from-pending/',views.admin_approval_from_pending),
#     path('admin-verify-from-pending/', views.admin_verify_from_pending),
#     path('admin-approved-from-verify/', views.admin_approved_from_verify),
#     path('admin-update-from-pending-to-reject/', views.admin_update_from_pending_to_reject),
#     path('admin-pending-list/',views.admin_pending_list),
#     path('admin-verified-list/', views.admin_verified_list),
#     path('admin-approved-list/',views.admin_approved_list),
#     path('employee-all-list/',views.employee_all_list),
#
#     path('employee-pending-list/', views.employee_pending_list),
#     path('employee-approved-list/',views.employee_approved_list),
#     path('employee-verified-list/',views.employee_verified_list),
#     path('employee-status-update-from-pending-to-approve/', views.employee_status_update_from_pending_to_approved),
#     path('employee-status-update-from-pending-to-verify/', views.employee_status_update_from_pending_to_verified),
#     path('employee-status-update-from-approved-to-verified/',views.employee_status_update_from_approved_to_verified),
#     path('employee-status-update-from-pending-to-reject/',views.employee_status_update_from_pending_to_reject),
#     path('company-registration-list/',views.company_registration_list),
#     path('admin-reject-list/',views.admin_rejected_list),
#     path('employee-reject-list/',views.employee_rejected_list),
#     path('add-data-based-on-user-type-to-create-user/', views.add_data_based_on_user_type_to_create_user)
#
#
#
# ]

from django.urls import path,include
from rest_framework import routers
from . import views

router=routers.DefaultRouter()

router.register('admin-invite', views.AdminInviteView)
router.register('create-user', views.CreateUserView)
router.register('admin-register',views.AdminRegisterView)
router.register('create-buyer', views.CreateBuyerView)
router.register('open-leads-rfq', views.OpenLeadsRfqViewSet)
router.register('open-leads-items', views.OpenLeadsItemsViewSet)
router.register('open-leads-terms',views.OpenLeadsTermsDescriptionViewSet)
# router.register('open-leads-publish',views.OpenLeadsPublishViewSet)
router.register('buyer-product-details-admin',views.BuyerProductDetailsAdminViewSet)

router.register('open-leads-vendor-publish-rfq', views.OpenLeadsVendorPublishRfqViewSet)
router.register('open-leads-vendor-publish-items', views.OpenLeadsVendorPublishItemsViewSet)
router.register('open-leads-vendor-publish-terms',views.OpenLeadsVendorPublishTermsDescriptionViewSet)
router.register('open-leads-awards',views.OpenLeadsAwardsViewSet)

# brand registration urls
router.register('brand-registration', views.BrandRegistrationView)
router.register('brand-company-details', views.BrandCompanyDetailsView)
router.register('basic-seller-distributor-details',views.BasicSellerOrDistributerDetailsView)
router.register('brand-company-communication-details',views.BrandCompanyCommunicationDetailsView)
router.register('seller-distributor-communication-details',views.SellerOrDistributerCommunicationDetailsView)
router.register('brand-legal-documents',views.BrandLegalDocumentsViewSet)
urlpatterns = [
    path('admin-router-urls/',include(router.urls)),
    path('admin-login/',views.admin_login),
    path('create-user-status-update/',views.create_user_status_update),
    path('admin-email-otp-verify/',views.admin_email_otp_verify),
    path('registration-list/', views.registration_list),
    path('admin-approval-from-pending/',views.admin_approval_from_pending),
    path('admin-verify-from-pending/', views.admin_verify_from_pending),
    path('admin-approved-from-verify/', views.admin_approved_from_verify),
    path('admin-update-from-pending-to-reject/', views.admin_update_from_pending_to_reject),
    path('admin-pending-list/',views.admin_pending_list),
    path('admin-verified-list/', views.admin_verified_list),
    path('admin-approved-list/',views.admin_approved_list),
    path('employee-all-list/',views.employee_all_list),

    path('employee-pending-list/', views.employee_pending_list),
    path('employee-approved-list/',views.employee_approved_list),
    path('employee-verified-list/',views.employee_verified_list),
    path('employee-status-update-from-pending-to-approve/', views.employee_status_update_from_pending_to_approved),
    path('employee-status-update-from-pending-to-verify/', views.employee_status_update_from_pending_to_verified),
    path('employee-status-update-from-verify-to-approve/',views.employee_status_update_from_verify_to_approved),
    path('employee-status-update-from-pending-to-reject/',views.employee_status_update_from_pending_to_reject),
    path('company-registration-list/',views.company_registration_list),
    path('admin-reject-list/',views.admin_rejected_list),
    path('employee-reject-list/',views.employee_rejected_list),
    path('add-data-based-on-user-type-to-create-user/', views.add_data_based_on_user_type_to_create_user),
    path('get-all-open-bids-vendors/',views.get_all_open_bids_vendors),
    path('get-all-buyers/',views.get_all_buyers),
    path('get-particular-buyer/',views.getbuyeraddedadminbyccode),
    path('fetch-all-buyer-product-details/',views.fetch_all_buyer_product_details),
    path('fetch-all-buyer-product-details-by-pk/', views.fetch_all_buyer_product_details_by_pk),
    path('fetch-open-leads-rfq/',views.fetch_open_leads_rfq),
    path('get-all-open-leads-by-pk/',views.get_all_open_leads_by_pk),
    path('get-open-bids-list/',views.get_open_bids_list),
    path('fetch-buyer-product-details-admin/',views.fetch_buyer_product_details_admin),
    path('fetch-vendor-open-leads/',views.fetch_vendor_open_leads),
    path('fetch-all-open-leads-rfq/',views.fetch_all_open_leads_rfq),
    path('fetch-vendor-open-leads-by-pk/',views.fetch_vendor_open_leads_by_pk),
    path('price-analysis-admin/',views.price_analysis_admin),
    path('get-buyer-name-by-ccode/',views.get_buyer_name_by_ccode),
    path('get_create_buyer_list/', views.get_create_buyer_list),
    path('get_create_buyer_list_companycode/',views.get_create_buyer_list_companycode),
    path('open_leads_vendor_publish_rfq/',views.open_leads_vendor_publish_rfq),
    path('open_leads_vendor_publishrfq_view/',views.open_leads_vendor_publishrfq_view),
    path('channel_leads_closed_leads_deadline_date/',views.channel_leads_closed_leads_deadline_date),
    path('create-admin-selected-categories/',views.create_admin_selected_categories),
    path('fetch-admin-selected-categories/', views.fetch_admin_selected_categories),
    path('create-admin-selected-trending-categories/',views.create_admin_selected_trending_categories),
    path('fetch-admin-trending-categories/', views.fetch_admin_trending_categories),
    path('create-admin-selected-sub-categories/',views.create_admin_selected_sub_categories),
    path('fetch-admin-selected-sub-categories/', views.fetch_admin_selected_sub_categories),
    path('create-admin-trending-sub-categories/',views.create_admin_trending_sub_categories),
    path('fetch-admin-trending-sub-categories/', views.fetch_admin_trending_sub_categories),

    #------------------------------delete-----------------------------------------------------
    path('delete-trending-category/',views.delete_trending_category),
    path('delete-admin-selected-category/',views.delete_admin_selected_category),
    path('delete-admin-selected-sub-category/',views.delete_admin_selected_sub_category),
    path('delete-trending-sub-category/',views.delete_trending_sub_category),


    #-------------------------------------edit------------------------------------------
    path('edit-admin-selected-categories/',views.edit_admin_selected_categories),
    path('edit-admin-trending-categories/',views.edit_admin_trending_categories),
    path('edit-admin-sub-categories/', views.edit_admin_sub_categories),
    path('edit-admin-trending-sub-categories/', views.edit_admin_trending_sub_categories),

    path('contact-us-send-mail/',views.contact_us_send_mail)


]