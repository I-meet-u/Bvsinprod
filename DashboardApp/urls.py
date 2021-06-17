
from django.urls import path,include
from rest_framework import routers
from . import views

router=routers.DefaultRouter()

router.register('internal-vendor', views.InternalVendorView)

urlpatterns = [
    path('dashboard-router-urls/',include(router.urls))
    ]