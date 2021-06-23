from django.urls import path, include
from rest_framework import routers
from . import views

router=routers.DefaultRouter()

router.register('vendor-product-details', views.VendorProductsDetailView)
router.register('industrial-details-search-category',views.IndustrialDetails_SearchCategoryView)
# router.register('product-details', views.GeneralProductsDetailsView)
# router.register('pricing-offer', views.PricingOfferView)
# router.register('technical-details', views.TechnicalDetailsView)
# router.register('product-features', views.ProductFeaturesView)

urlpatterns = [
    path('vendor-product-router-urls/',include(router.urls)),
    ]