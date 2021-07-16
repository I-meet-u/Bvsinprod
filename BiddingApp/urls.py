from django.urls import path,include
from rest_framework import  routers
from . import  views

router=routers.DefaultRouter()

router.register('buyer-product-bidding',views.BuyerProductBiddingView)
router.register('buyer-product-details',views.BiddingBuyerProductDetailsView)
router.register('rfq-code-settings',views.RfqCodeSettingsView)
router.register('rfq-terms-description',views.RfqTermsDescriptionView)
router.register('select-vendors-for-bidding-product',views.SelectVendorsForBiddingProductView)
router.register('bidding-term-master-settings',views.BiddingTermMasterSettingsView)
router.register('vendor-product-bidding',views.VendorProductBiddingView)
router.register('vendor-product-details',views.VendorBiddingBuyerProductDetailsView)
router.register('vendor-rfq-terms-description',views.VendorRfqTermsDescriptionView)

urlpatterns = [
    path('bidding-router-urls/',include(router.urls)),
    path('get-buyer-product-details/',views.get_buyer_product_based_on_userid_pk),
    path('updated-rfq-code-settings-and-rfq-number/',views.updated_rfq_code_settings_and_rfq_number),
    path('rfq-bid-list-summary-advance-search/',views.rfq_bid_list_summary_advance_search),
    path('rfq-type-based-list/',views.rfq_type_based_list),
    # path('get-buyer-product-bidding-details/',views.get_buyer_product_bidding_details)
    path('get-buyer-product-bid-by-user-rfq/',views.get_buyer_product_bid_by_user_rfq),
    path('get-buyer-product-details-by-user-rfq/',views.get_buyer_product_details_by_user_rfq),
    path('get-buyer-bid-terms-by-user-rfq/',views.get_buyer_bid_terms_by_user_rfq),
    path('open-bid-list-buyer-publish-list/',views.open_bid_list_buyer_pulish_list)

]