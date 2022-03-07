from django.conf.urls.static import static
from django.urls import path,include
from rest_framework import routers

from . import views
from django.conf import settings


router=routers.DefaultRouter()

router.register('company-review-rating', views.CompanyReviewViewSet)
# router.register('company-rating', views.CompanyRatingViewSet)

urlpatterns = [
    path('api/',include(router.urls)),
    path('maincore-all-list/',views.maincore_all_list),
    path('maincore-list/', views.maincore_list),
    path('category-list/', views.category_list),
    path('subcategory-list/', views.subcategory_list),
    path('subcategory-list-category-in-array/',views.subcategory_list_category_in_array),
    # path('categorysearch_byname',views.categorysearch_byname),
    path('company-name-search/',views.company_name_search),
    # path('getcompanycode_basedoncompanyname/',views.getcompanycode_basedoncompanyname),
    path('sub-category-search-by-name/', views.sub_category_search_by_name),
    path('company-details-by-category-id/', views.company_details_by_category_id),
    path('category-search-by-name/', views.category_search_by_name),
    path('company-details-by-subcategory-id/',views.company_details_by_subcategory_id),
    # path('getBasicDetails/',views.getBasicDetails),
    path('get-all-billing-cities/',views.get_all_billing_cities),
    path('get-all_company-details-company_code/',views.get_all_company_details_company_code),
    # path('getallcompanydetails_companycode/',views.getallcompanydetails_companycode)
    path('category-list-by-maincore/',views.category_list_by_maincore),
    path('basic-details-by-company_name/',views.basic_details_by_company_name),
    path('maincore-by-id/',views.maincore_by_id),
    path('get-all-company-products-services/',views.get_all_company_products_services),
    path('get-approved-companies-list/', views.get_approved_companies_list),
    path('get-all-vendor-product-details/', views.get_all_vendor_product_details),
    path('average-rating/',views.average_rating),
    path('search-texts/',views.search_texts),
    path('getproductbymaincore/',views.getproductbymaincore),
    path('company_details_by_maincore_id/',views.company_details_by_maincore_id),
    path('company_details_by_maincore_id_cat_id/',views.company_details_by_maincore_id_cat_id),

    # chat urls

    path('get-messages/<int:sender>/<int:receiver>', views.messages_lists, name='message-details'),  # get request
    path('receiver_sender_messages/<int:receiver>/<int:sender>',views.receiver_sender_messages), # get request
    path('create-messages/', views.messages_lists, name='message-create'),  # post request
    path('messages_user_list/',views.messages_user_list),
    path('messages_user_list_receiver/',views.messages_user_list_receiver),
    path('internal_external_trail_buyers_users_list/',views.internal_external_trail_buyers_users_list),
    path('post_listings/',views.post_listings),
    path('get_buyer_requirements_for_same_subcategories/',views.get_buyer_requirements_for_same_subcategories),
    path('source_listings/',views.source_listings),
    path('source_listings_based_on_category_for_get_vendors/',views.source_listings_based_on_category_for_get_vendors),
    path('source_listings_for_invite_vendors/',views.source_listings_for_invite_vendors),
    path('get_buyer_data_to_show_to_invite_vendors/',views.get_buyer_data_to_show_to_invite_vendors),
    path('buyer_bidding_rfq/', views.buyer_bidding_rfq),
    path('bidding_invite_vendor/',views.bidding_invite_vendor),
    path('bidding_get_vendor/',views.bidding_get_vendor)

]
