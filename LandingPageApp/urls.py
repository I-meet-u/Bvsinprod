from django.conf.urls.static import static
from django.urls import path,include
from . import views
from django.conf import settings

urlpatterns = [
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

]
