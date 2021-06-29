from django.urls import path, include
from rest_framework import routers

from . import  views
from .views import IndustryServeUploadView

router=routers.DefaultRouter()
#routers for Viewsets
router.register('industry-serve-master',views.IndustryToServeMasterView)
router.register('nature-of-business-master',views.NatureOfBusinessMasterView)
router.register('supply-capability-master',views.SupplyCapabilitiesMasterView)
router.register('maincore-master',views.MaincoreMasterView)
router.register('category-master',views.CategoryMasterView)
router.register('sub-category-master',views.SubCategoryMasterView)
router.register('pincode-master',views.PincodeMasterView)
router.register('uom-master',views.UOMMasterView)
router.register('department-master',views.DepartmentMasterView)
router.register('designation-master',views.DesignationMasterView)
router.register('tax-master',views.TaxMasterView)
router.register('hsn-master',views.HSNMasterSerializerView)
router.register('sac-master',views.SACMasterView)
router.register('currency-master',views.CurrencyMasterView)
router.register('pf-charge-master',views.PFChargesMasterView)
router.register('frieght-charge-master',views.FrieghtChargesMasterView)
router.register('warrantee-master',views.WarrantyMasterView)
router.register('guarantee-master',views.GuaranteeMasterView)
router.register('delivery-master',views.DeliveryMasterView)
router.register('country-master',views.CountryMasterView)
urlpatterns = [
    path('masters-router-urls/',include(router.urls)), #router urls are included

    # urls other than routers
    path('get-category-by-maincore/',views.get_category_by_maincore),
    path('get-sub-category-by-category/',views.get_subcategory_by_category),
    path('maincore-search/',views.maincore_search),
    path('category-search/',views.category_search),
    path('sub-category-search/',views.sub_category_search),

    path('disable-industry-serve-masters/', views.disable_industry_serve_masters),
    path('enable-industry-serve-masters/',views.enable_industry_serve_masters),
    path('delete-industry-serve-masters/',views.delete_industry_serve_masters),

    path('disable-nature-of-business-masters/', views.disable_nature_of_business_master),
    path('enable-nature-of-business-masters/',views.enable_nature_of_business_master),
    path('delete-nature-of-business-masters/',views.delete_nature_of_business_master),

    path('disable-supply-capabilities-master/',views.disable_supply_capabilities_master),
    path('enable-supply-capabilities-master/', views.enable_supply_capabilities_master),
    path('delete-supply-capabilities-master/', views.delete_supply_capabilities_master),

    path('disable-uom-master/',views.disable_uom_master),
    path('enable-uom-master/',views.enable_uom_master),
    path('all-masters/',views.all_masters),
    path('delete-uom-masters/',views.delete_uom_master),

    path('industry-to-serve-master-history/', views.industry_to_serve_master_history),
    path('nature-of-business-master-history/',views.nature_of_business_master_history),
    path('supply-capabilites-master-history/', views.supply_capabilites_master_history),
    path('maincore-master-history/',views.maincore_master_history),
    path('category-master-history/',views.category_master_history),
    path('sub-category-master-history/',views.sub_category_master_history),


    path('disable-maincore-master/',views.disable_maincore_master),
    path('enable-maincore-master/',views.enable_maincore_master),
    path('delete-maincore-master/',views.delete_maincore_master),

    path('disable-category-master/', views.disable_category_master),
    path('enable-category-master/', views.enable_category_master),
    path('delete-category-master/', views.delete_category_master),

    path('disable-sub-category-master/', views.disable_sub_category_master),
    path('enable-sub-category-master/', views.enable_sub_category_master),
    path('delete-sub-category-master/', views.delete_sub_category_master),
    # path('importindustry/', IndustryServeUploadView.as_view())






]