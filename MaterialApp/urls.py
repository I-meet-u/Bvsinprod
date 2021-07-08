from django.urls import path, include
from rest_framework import routers
from . import views

router=routers.DefaultRouter()

router.register('vendor-product-basic-details', views.VendorProduct_BasicDetailsView)
router.register('vendor-product-general-details',views.VendorProduct_GeneralDetailsView)
router.register('vendor-product-technical', views.VendorProduct_TechnicalSpecificationsView)
router.register('vendor-product-features', views.VendorProduct_ProductFeaturesView)
router.register('vendor-product-document', views.VendorProduct_DocumentsView)
router.register('buyer-product-details', views.BuyerProductDetailsView)
router.register('item-code-settings', views.ItemCodeSettingsView)
urlpatterns = [
    path('vendor-product-router-urls/',include(router.urls)),
    path('buyer-product-create/',views.buyer_product_create),
    path('get-itemtype-based-on-userid/',views.get_itemtype_based_on_userid),
    path('item-code-settings-list/',views.item_code_settings_list),
    path('disable-buyer-product/',views.disable_buyer_product),
    path('enable-buyer-product/',views.enable_buyer_product),
    path('delete-buyer-product/',views.delete_buyer_product),
    ]