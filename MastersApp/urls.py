from django.urls import path, include
from rest_framework import routers

from . import  views

router=routers.DefaultRouter()
router.register('industry-serve-master',views.IndustryToServeMasterView)
router.register('nature-of-business-master',views.NatureOfBusinessMasterView)
router.register('supply-capability-master',views.SupplyCapabilitiesMasterView)
router.register('maincore-master',views.MaincoreMasterView)
router.register('category-master',views.CategoryMasterView)
router.register('sub-category-master',views.SubCategoryMasterView)
router.register('country-master',views.CountryMasterView)
router.register('state-master',views.StateMasterView)
router.register('city-master',views.CityMasterView)
router.register('pincode-master',views.PincodeMasterView)

urlpatterns = [
    path('masters-router-urls/',include(router.urls)), #router urls are included
    path('get-category-by-maincore/',views.get_category_by_maincore),
    path('get-sub-category-by-category/',views.get_subcategory_by_category),
    path('maincore-search/',views.maincore_search),
    path('category-search/',views.category_search),
    path('sub-category-search/',views.sub_cateory_search)




]