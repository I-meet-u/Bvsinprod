from django.urls import path,include
from rest_framework import  routers
from . import  views

router=routers.DefaultRouter()

router.register('buyer-product-bidding',views.BuyerProductBiddingView)
router.register('buyer-bidding-product-details',views.BiddingBuyerProductDetailsView)
router.register('rfq-code-settings',views.RfqCodeSettingsView)
router.register('rfq-terms-description',views.RfqTermsDescriptionView)
router.register('select-vendors-for-bidding-product',views.SelectVendorsForBiddingProductView)
router.register('bidding-term-master-settings',views.BiddingTermMasterSettingsView)
router.register('vendor-product-bidding',views.VendorProductBiddingView)
router.register('vendor-bidding-product-details',views.VendorBiddingBuyerProductDetailsView)
router.register('vendor-rfq-terms-description',views.VendorRfqTermsDescriptionView)
router.register('source-list-create-items',views.SourceList_CreateItemViewSet)
router.register('source-publish',views.SourcePublishViewSet)

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
    path('open-bid-list-buyer-publish-list/',views.open_bid_list_buyer_publish_list),
    path('source-list-leads/',views.source_list_leads),
    path('update-source-vendor-codes/',views.update_source_vendor_codes),
    path('source-leads-advance-search/',views.advance_search_source_leads),
    path('update-buyer-bid-pending-to-publish/',views.update_buyer_bid_status_pending_to_publish),
    path('source-status-update-to-publish/',views.source_status_update_to_publish),
    path('source-status-update-to-decline/',views.source_status_update_to_decline),
    path('get-source-items-by-source-user-id/',views.get_source_items_list_by_source_user_id),
    path('get-buyer-bidding-by-bidding-id-rfq/',views.get_buyer_bidding_by_bidding_id_and_rfq),
    path('update-buyer-bidding-deadline-date/',views.update_buyer_bidding_deadline_date),
    path('status-vendor-accept/',views.status_vendor_accept),
    path('status-vendor-reject/',views.status_vendor_reject),
    path('vendor-bidding-all-details/',views.vendor_bidding_all_details),
    path('get-vendor-published-leads/',views.get_vendor_published_leads),
    path('open-leads-product-advance-search/',views.open_leads_product_advance_search),
    path('get-source-based-on-item-type-user-id/',views.get_source_based_on_item_type_user_id),
    path('source-list-advance-search/',views.source_list_advance_search),
    path('bidding-data-response-count/',views.bidding_data_responses_count),
    path('status-vendor-accept/',views.status_vendor_accept),
    path('status-vendor-reject/', views.status_vendor_reject),
    path('selected-vendors-product-list/',views.selected_vendors_product_list),
    path('accepted-response-list/',views.accepted_response_list),
    path('pending-response-list/',views.pending_response_list),
    path('rejected-response-list/', views.rejected_response_list),
    path('get-ccode_by_userid/',views.get_ccode_by_userid),
    path('price-analysis-product/',views.price_analysis_product)

]