from django.urls import path,include
from rest_framework import routers
from . import views

router=routers.DefaultRouter()

router.register('admin-invite', views.AdminInviteView)
router.register('create-user', views.CreateUserView)
router.register('admin-register',views.AdminRegisterView)
router.register('permissions',views.PermissionsView)


urlpatterns = [
    path('admin-router-urls/',include(router.urls)),
    path('admin-login/',views.admin_login),
    path('create-user-status-update/',views.create_user_status_update),
    path('admin-email-otp-verify/',views.admin_email_otp_verify),
    path('registration-list/', views.registration_list),
    path('admin-approval-from-pending/',views.admin_approval_from_pending),
    path('admin-verify-from-approve/', views.admin_verify_from_approve),
    path('admin-approved-from-verify/', views.admin_approved_from_verify),
    path('admin-pending-list/',views.admin_pending_list),
    path('admin-verified-list/', views.admin_verified_list),
    path('admin-approved-list/',views.admin_approved_list),

]