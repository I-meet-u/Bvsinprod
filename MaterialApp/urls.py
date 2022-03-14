from django.urls import path, include
from rest_framework import routers
from . import views

router=routers.DefaultRouter()

router.register('vendor-product-basic-details', views.VendorProduct_BasicDetailsView)
router.register('vendor-product-general-details',views.VendorProduct_GeneralDetailsView)
router.register('vendor-product-technical', views.VendorProduct_TechnicalSpecificationsView)
router.register('vendor-product-features', views.VendorProduct_ProductFeaturesView)
router.register('vendor-product-document', views.VendorProduct_DocumentsView)
router.register('vendor-product-requirements',views.VendorProduct_RequirementsViewSet)
router.register('buyer-product-details', views.BuyerProductDetailsView)
router.register('buyer-service-details', views.BuyerServiceDetailsView)
router.register('buyer-machinary-details', views.BuyerMachinaryDetailsView)
router.register('item-code-settings', views.ItemCodeSettingsView)
router.register('landing-page-bidding-publish',views.LandingPageBidding_PublishViewSet)
router.register('LandingPageBiddingRFQAwardsSerializerViewSet',views.LandingPageBiddingRFQAwardsSerializerViewSet)
router.register('LandingPageBiddingRFQ_SelectVendorSerializerview',views.LandingPageBiddingRFQ_SelectVendorSerializerview)
router.register('landing-page-po',views.LandingPageListingLeadsPurchaseOrderViewSet)
router.register('buyer-product-requirements',views.BuyerProduct_RequirementsViewSet)
urlpatterns = [
    path('vendor-product-router-urls/',include(router.urls)),
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
    path('get-all-types-of-products-by-ccode/',views.get_all_types_of_products_by_ccode),
    path('vendor-product-based-on-maincore-name/',views.vendor_product_based_on_maincore_name),
    path('vendor-product-based-on-category-name/',views.vendor_product_based_on_category_name),
    path('update-buyer-products/',views.update_buyer_products),
    path('get-product-all-details-based-on-id-and-userid/',views.get_product_all_details_based_on_id_and_userid),
    path('buyer-product-search/',views.buyer_product_search),
    path('advance-search-vendor-product/',views.advance_search_vendor_product),
    path('get_product_all_details_based_on_id_multiple_and_userid/',views.get_product_all_details_based_on_id_multiple_and_userid),
    path('fetch-vendor-product-basic-details-by-category/', views.fetch_vendor_product_basic_details_by_category),
    path('get-previous-value-of-buyer-details/',views.get_previous_value_of_buyer_details),
    path('fetch-vendor-product-general-details/', views.fetch_vendor_product_general_details),
    path('fetch-vendor-product-technical-details/', views.fetch_vendor_product_technical_details),
    path('fetch-vendor-product-product_features-details/', views.fetch_vendor_product_productfeatures_details),
    path('fetch-vendor-product-document-details/', views.fetch_vendor_product_document_details),
    path('get-vendor-details-by-sub-category/',views.get_vendor_details_by_sub_category),
    path('fetch-vendor-product-basic-details-by-subcategory/',views.fetch_vendor_product_basic_details_by_subcategory),
    path('fetch-vendor-product-basic-details-by-userid-all/', views.fetch_vendor_product_basic_details_by_userid_all),
    path('landing-page-bidding-create/', views.landing_page_bidding_create),
    path('get-landing-page-bidding-by-userid-buyer-list/', views.get_landing_page_bidding_by_userid_buyer_list),
    path('get-landing-page-bidding-by-userid-vendors-list/', views.get_landing_page_bidding_by_userid_vendors_list),
    path('fetch-vendor-product-basic-details-by-pk/', views.fetch_vendor_product_basic_details_by_pk),
    path('edit-technical-specifications/', views.edit_technical_specifications),
    path('landing-page-listing-leads-pending-list/', views.landing_page_listing_leads_pending_list),
    path('update-landing-page-status-to-decline/', views.update_landing_page_status_to_decline),
    path('get-landing-page-bidding-by-pk/',views.get_landing_page_bidding_by_pk),
    path('fetch-vendor-product-details-by-userid-and-pk/', views.fetch_vendor_product_details_by_userid_and_pk),
    path('landing-page-listing-leads-closed-list/', views.landing_page_listing_leads_closed_list),
    path('fetch-general-details-by-foreign-key/', views.fetch_general_details_by_foreign_key),
    path('fetch-technical-specifications-by-foreign-key/', views.fetch_techincal_specification_by_foreign_key),
    path('fetch-product-features-by-foreign-key/', views.fetch_product_features_by_foreign_key),
    path('fetch-product-documents-by-foreign-key/', views.fetch_product_documents_foreign_key),
    path('get-landing-page-bidding-list-response/', views.get_landing_page_bidding_list_response),
    path('fetch-vendor-product-details-by-pk/', views.fetch_vendor_product_details_by_pk),
    path('get_landing_page_bidding_by_pid/',views.get_landing_page_bidding_by_pid),
    path('getbuyerpostedresponse/',views.getbuyerpostedresponse),
    path('get-buyer-posted-response-by-pk/',views.get_buyer_posted_response_by_pk),
    path('get-buyer-award-details-by-userid/',views.get_buyer_award_details_by_userid),
    path('pending-list-listing-leads/',views.pending_list_listing_leads),
    path('update-status-from-pending-to-reject/', views.update_status_from_pending_to_reject),
    path('update-status-from-pending-to-published/',views.update_status_from_pending_to_published),
    path('getawardlistoflistingleadsnew/',views.getawardlistoflistingleadsnew),
    path('landing-page-listing-leads-rejected-list/',views.landing_page_listing_leads_rejected_list),
    path('landing-page-published-list-by-user-id/',views.landing_page_published_list_by_user_id),
    path('landing-page-listing-leads-expired-list/',views.landing_page_listing_leads_expired_list),
    path('landing-page-published-list/',views.landing_page_published_list),
    path('updatelandingpagevendor_publish/',views.updatelandingpagevendor_publish_update),
    path('get-award-list-by-pk-value/',views.get_award_list_by_pk_value),
    path('listing-leads-po-status-update/',views.listing_leads_po_status_update),
    path('main_cat_subcat_data/',views.main_cat_subcat_data),
    path('store_vendor_publish/',views.store_vendor_publish),
    path('vendor_product_details_based_on_itemtype/',views.vendor_product_details_based_on_itemtype),
    path('fetch-vendor-product-basic-details-by-ccode/',views.fetch_vendor_product_basic_details_by_ccode),
    path('get-vendor-product-details-based-on-ccode-distinct/',views.get_vendor_product_details_based_on_ccode_distinct),
    path('get_vendor_product_details_difference_industry_category/',views.get_vendor_product_details_difference_industry_category),
    path('get_vendor_product_details_based_on_maincore/',views.get_vendor_product_details_based_on_maincore),
    path('get_vendor_product_details_based_on_category/',views.get_vendor_product_details_based_on_category),
    path('get_vendor_product_details_based_on_subcategory/',views.get_vendor_product_details_based_on_subcategory),
    path('get_vendor_product_details_based_on_main_id_cat_id_subcat_name/',
         views.get_vendor_product_details_based_on_main_id_cat_id_subcat_name),
    path('get_vendor_product_details_by_pk/', views.get_vendor_product_details_by_pk),
    path('get_admin_added_vendor_product_details/',views.get_admin_added_vendor_product_details),
    path('update_vendor_product_basic_details/<int:vendor_product_id>',views.update_vendor_product_basic_details),
    path('get_companies_based_on_landing_page_pk/',views.get_companies_based_on_landing_page_pk),
    path('vendor_source_responses_listing_leads/',views.vendor_source_responses_listing_leads),
    path('update_productgeneraldetails/',views.update_productgeneraldetails),
    path('update_vendor_product_documents_details/', views.update_vendor_product_documents_details),
    path('get_vendor_product_requirements_based_on_vendor_pk/',views.get_vendor_product_requirements_based_on_vendor_pk),
    path('posted_rfq_award_list/',views.posted_rfq_award_list),
    path('get_landing_page_po_details_based_on_vendor_user_id/',views.get_landing_page_po_details_based_on_vendor_user_id),
        # path('update_vendor_product_specifications_details', views.update_vendor_product_specifications_details)
    path('get_landing_page_po_details_based_on_vendor_user_id_hsb/',views.get_landing_page_po_details_based_on_vendor_user_id_hsb),
    path('delete_vendor_product_requirement/',views.delete_vendor_product_requirement),
    path('update_buyer_requirement_pk_in_post_rfq/',views.update_buyer_requirement_pk_in_post_rfq),
    path('update_landing_pk_in_buyer_requirement/',views.update_landing_pk_in_buyer_requirement),
    path('update_listing_leads_pk_in_buyer_requirement/',views.update_listing_leads_pk_in_buyer_requirement)
        # fghjj
]