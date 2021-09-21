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
    path('add-data-based-on-user-type-to-create-user/', views.add_data_based_on_user_type_to_create_user)




]