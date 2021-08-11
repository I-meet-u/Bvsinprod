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
router.register('buyer-service-details', views.BuyerServiceDetailsView)
router.register('buyer-machinary-details', views.BuyerMachinaryDetailsView)
router.register('item-code-settings', views.ItemCodeSettingsView)
urlpatterns = [
    path('vendor-product-router-urls/',include(router.urls)),
    path('buyer-product-create/',views.buyer_product_create),
    path('buyer-service-create/', views.buyer_service_create),
    path('buyer-machinary-create/', views.buyer_machinary_create),
    path('get-itemtype-based-on-userid/',views.get_itemtype_based_on_userid),
    path('item-code-settings-list/',views.item_code_settings_list),
    path('disable-buyer-product/',views.disable_buyer_product),
    path('enable-buyer-product/',views.enable_buyer_product),
    path('delete-buyer-product/',views.delete_buyer_product),
    path('update-item-code-settings-and-item-code/',views.updated_item_code_settings_and_item_code),
    path('t-codes-datas/',views.t_codes_datas),
    path('get-item-code-details-by-userid-itemtype/',views.get_item_code_details_by_userid_itemtype),
    path('advance-search-buyer-product/',views.advance_search_buyer_product),
    path('get-all-types-of-products-by-user-id/',views.get_all_types_of_products_by_user_id),
    path('vendor-product-based-on-maincore-name/',views.vendor_product_based_on_maincore_name),
    path('vendor-product-based-on-category-name/',views.vendor_product_based_on_category_name),
    path('update-buyer-products/',views.update_buyer_products),
    path('get-product-all-details-based-on-id-and-userid/',views.get_product_all_details_based_on_id_and_userid),
    path('buyer-product-search/',views.buyer_product_search),
    path('advance-search-vendor-product/',views.advance_search_vendor_product),
    path('get_product_all_details_based_on_id_multiple_and_userid/',views.get_product_all_details_based_on_id_multiple_and_userid),
    path('fetch-vendor-product-basic-details-by-category/', views.fetch_vendor_product_basic_details_by_category),
    path('get-previous-value-of-buyer-details/',views.get_previous_value_of_buyer_details)
    ]