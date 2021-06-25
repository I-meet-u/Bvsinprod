from django.urls import path, include
from rest_framework import routers
from . import views

router=routers.DefaultRouter()

router.register('vendor-product-basic-details', views.VendorProduct_BasicDetailsView)
router.register('vendor-product-general-details',views.VendorProduct_GeneralDetailsView)
router.register('vendor-product-technical', views.VendorProduct_TechnicalSpecificationsView)
router.register('vendor-product-features', views.VendorProduct_ProductFeaturesView)
router.register('vendor-product-document', views.VendorProduct_DocumentsView)
urlpatterns = [
    path('vendor-product-router-urls/',include(router.urls)),
    path('vendor-product-all-details/',views.vendor_product_create)
    ]