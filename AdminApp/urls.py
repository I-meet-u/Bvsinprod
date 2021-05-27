from django.urls import path,include
from rest_framework import routers
from . import views

router=routers.DefaultRouter()

router.register('invite-admin', views.AdminInviteView)
router.register('create-user', views.CreateUserView)
router.register('admin-register',views.AdminRegisterView)
router.register('permissions',views.PermissionsView)

urlpatterns = [
    path('admin-router-urls',include(router.urls)),
    path('admin-login/',views.admin_login)
    ]