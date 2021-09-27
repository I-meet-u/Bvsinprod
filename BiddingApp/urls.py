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

router.register('buyer-bidding-service-details',views.BiddingBuyerServiceDetailsView)
router.register('buyer-bidding-machinary-details',views.BiddingBuyerMachinaryDetailsView)

router.register('vendor-bidding-service-details',views.VendorBiddingBuyerServiceDetailsView)
router.register('vendor-bidding-machinary-details',views.VendorBiddingBuyerMachinaryDetailsView)
router.register('product-award',views.AwardViewSet)
router.register('service-award',views.ServiceAwardViewSet)
router.register('machinary-award',views.MachinaryAwardViewSet)
router.register('purchase-order',views.PurchaseOrderViewSet)
router.register('source-list-create-items',views.SourceList_CreateItemViewSet)
router.register('source-publish',views.SourcePublishViewSet)
router.register('source-awards',views.SourceAwardsViewSet)

urlpatterns = [
    path('bidding-router-urls/',include(router.urls)),
    path('getsorcelistresponse/', views.getsorcelistresponse),
    path('get-buyer-product-details/',views.get_buyer_product_based_on_userid_pk),
    path('updated-rfq-code-settings-and-rfq-number/',views.updated_rfq_code_settings_and_rfq_number),
    path('rfq-bid-list-summary-advance-search/',views.rfq_bid_list_summary_advance_search),
    path('rfq-type-based-list/',views.rfq_type_based_list),
    path('get-buyer-product-bid-by-user-rfq/',views.get_buyer_product_bid_by_user_rfq),
    path('get-buyer-product-details-by-user-rfq/',views.get_buyer_product_details_by_user_rfq),
    path('get-buyer-bid-terms-by-user-rfq/',views.get_buyer_bid_terms_by_user_rfq),
    path('open-bid-list-buyer-publish-list/',views.open_bid_list_buyer_publish_list),
    path('source-list-leads/',views.source_list_leads),
    path('update-source-vendor-codes/',views.update_source_vendor_codes),
    path('source-leads-advance-search/',views.advance_search_source_leads),
    path('update-buyer-bid-pending-to-publish/',views.update_buyer_bid_status_pending_to_publish),
    path('source-status-update-to-decline/',views.source_status_update_to_decline),
    path('get-source-items-by-source-user-id/',views.get_source_items_list_by_source_user_id),
    path('get-buyer-bidding-by-bidding-id-rfq/',views.get_buyer_bidding_by_bidding_id_and_rfq),
    path('update-buyer-bidding-deadline-date/',views.update_buyer_bidding_deadline_date),
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
    path('price-analysis-product/',views.price_analysis_product),
    path('vendor-query-description/',views.vendor_query_description),
    path('company_names_get_by_ccode/',views.company_names_get_by_ccode),
    path('buyer-bidlist-based-on-rfqnumber/',views.buyer_bidlist_based_on_rfqnumber),
    path('award-total-count-product/',views.award_total_count_product),
    path('award-product-create/',views.award_product_create),
    path('award-get-list-of-vendor/',views.award_get_list_of_vendor),
    path('fetch-buyer-service-details-by-userid-rfq/',views.fetch_buyer_service_details_by_userid_rfq),
    path('fetch-buyer-machinary-details-by-userid-rfq/',views.fetch_buyer_machinary_details_by_userid_rfq),
    path('award-service-create/',views.award_service_create),
    path('award-machinary-create/',views.award_machinary_create),
    path('po-status-update-product/',views.po_status_update_product),
    path('price-analysis-service/',views.price_analysis_service),
    path('price-analysis-machinary/', views.price_analysis_machinary),
    path('fetch-vendor-bid-details/',views.fetch_vendor_bid_details),
    path('price-analysis-vendor-terms-list/',views.price_analysis_vendor_terms_list),
    path('get-previous-value-of-rfq_details/',views.get_previous_value_of_rfq_details),
    path('fetch-vendor-bid-details-userid/',views.fetch_vendor_bid_details_userid),
    path('edit-vendor-bidding-product/',views.edit_vendor_bidding_product),
    path('edit-vendor-bidding-service/',views.edit_vendor_bidding_service),
    path('edit-vendor-bidding-machinary/',views.edit_vendor_bidding_machinary),
    path('buyer-bid-status-changed-to-publish/',views.buyer_bid_status_changed_to_publish),
    path('get-buyer-bid-list-by-userid/',views.get_buyer_bid_list_by_userid),
    path('get-all-types-of-awards/',views.get_all_types_of_awards),
    path('get-all-awards-based-on-userid-and-rfqtype/',views.get_all_awards_based_on_userid_and_rfqtype),
    path('add-terms-to-bidding-terms-settings/',views.add_terms_to_bidding_terms_settings),
    path('purchase-order-vendors-list/', views.purchase_order_vendors_list),
    path('awards-vendor-list/', views.awards_vendor_list),
    path('createbuyerbidding/', views.createbuyerbidding),
    path('termsanddescriptionpriceanalysis/',views.termsanddescriptionpriceanalysis),
    path('getsourcebasedpk/', views.getsourcebasedpk),
    path('deadline-expired-list/', views.deadline_expired_list),
    path('extended-deadline-date-list-create/', views.extended_deadline_date_list_create),
    path('extended-deadline-list-show/', views.extended_deadline_list_show),
    path('advance-search-bidding-list/', views.advance_search_bidding_list),
    path('advance-search-open-leads-list/', views.advance_search_open_leads_list),
    path('advance-search-published-leads-list/', views.advance_search_published_leads_list),
    path('advance-search-expired-list/', views.advance_search_expired_list),
    path('advance-search-po-list/', views.advance_search_po_list),
    path('advance-search-award-list/', views.advance_search_award_list),
    path('source-awards/', views.source_awards),
    path('update-status-to-po-sent/', views.update_status_to_po_sent),
    path('source-po-list-based-on-userid/', views.source_po_list_based_on_userid),
    path('vendor-side-award-search/', views.vendor_side_award_search),
    path('vendor-side-po-search/', views.vendor_side_po_search),
    path('source-award-search/', views.source_award_search),
    path('priceanalysistermsnew/',views.priceanalysistermslist),
    path('deadline-date-list/',views.deadline_date_list),
    path('purchase_order_email/',views.purchase_order_email)


]