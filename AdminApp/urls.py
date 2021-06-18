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
    path('admin-approval/',views.admin_approval)
    ]