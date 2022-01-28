from django.urls import path, include
from rest_framework import routers

from . import  views

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
router.register('item-group-master',views.ItemGroupMasterView)
router.register('transit-insurance-master',views.TransitInsuranceMasterView)
router.register('payment-master',views.PaymentMasterView)
router.register('validity-master',views.ValidityMasterView)
router.register('rfq-category-master',views.RfqCategoryMasterView)
router.register('price-basis-master',views.PriceBasisMasterView)
router.register('inspection-master',views.InspectionMasterView)
router.register('liquidated-damage-master',views.LiquidatedDamageMasterView)
router.register('tax-duties-master',views.TaxesAndDutiesMasterView)
router.register('test-qap-master',views.TestAndQapMasterView)
router.register('performance-guarantee-master',views.PerformanceGuaranteesMasterView)
router.register('division-master',views.DivisionMasterView)

# router.register('SubCategoryMasterPaginationView',views.SubCategoryMasterPaginationView)
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
    # path('uom-master-history/',views.uom_master_history),
    path('uom-master-user-id/',views. uom_master_user_id),

    path('disable-department-master/', views.disable_department_master),
    path('enable-department-master/', views.enable_department_master),
    path('delete-department-master/', views.delete_department_master),
    # path('history-department-master/', views.department_master_history),
    path('department-master-get-by-userid/', views.department_master_user_id),
    path('getopenbidsmasters/',views.getopenbidsmasters),

    #
    # path('industry-to-serve-master-history/', views.industry_to_serve_master_history),
    # path('nature-of-business-master-history/',views.nature_of_business_master_history),
    # path('supply-capabilites-master-history/', views.supply_capabilites_master_history),
    # path('maincore-master-history/',views.maincore_master_history),
    # path('category-master-history/',views.category_master_history),
    # path('sub-category-master-history/',views.sub_category_master_history),


    path('disable-maincore-master/',views.disable_maincore_master),
    path('enable-maincore-master/',views.enable_maincore_master),
    path('delete-maincore-master/',views.delete_maincore_master),

    path('disable-category-master/', views.disable_category_master),
    path('enable-category-master/', views.enable_category_master),
    path('delete-category-master/', views.delete_category_master),

    path('disable-sub-category-master/', views.disable_sub_category_master),
    path('enable-sub-category-master/', views.enable_sub_category_master),
    path('delete-sub-category-master/', views.delete_sub_category_master),
    path('import-bulk-industry-serve/', views.IndustryServeUploadView.as_view()),

    # disable,enable,delete,history of item group master
    path('disable-item-group-master/', views.disable_item_group_master),
    path('enable-item-group-master/', views.enable_item_group_master),
    path('delete-item-group-master/', views.delete_item_group_master),
    # path('history-item-group-master/', views.item_group_master_history),

    # disable,enable,delete,history of item group master
    path('disable-hsn-master/', views.disable_hsn_master),
    path('enable-hsn-master/', views.enable_hsn_master),
    path('delete-hsn-master/', views.delete_hsn_master),
    # path('history-hsn-master/', views.hsn_master_history),

    path('disable-sac-master/', views.disable_sac_master),
    path('enable-sac-master/', views.enable_sac_master),
    path('delete-sac-master/', views.delete_sac_master),
    # path('history-sac-master/', views.sac_master_history),

    path('disable-frieght-master/', views.disable_frieght_charges_master),
    path('enable-frieght-master/', views.enable_frieght_charges_master),
    path('delete-frieght-master/', views.delete_freight_master),
    # path('history-frieght-master/', views.frieght_master_history),
    path('frieght-master-get-by-userid/',views.frieght_masters_user_id),



    path('disable-pf-charge-master/', views.disable_pf_charge_master),
    path('enable-pf_charge-master/', views.enable_pf_charge_master),
    path('delete-pf_charge-master/', views.delete_pf_charge_master),
    # path('history-pf_charge-master/', views.pf_charges_master_history),
    path('pf_charge-master-get-by-userid/', views.pf_charges_master_get_by_userid),

    path('hsn-master-get-by-userid/', views.hsn_masters_user_id),
    path('sac-master-get-by-userid/', views.sac_masters_user_id),

    path('disable-guarantee-master/', views.disable_guarantee_master),
    path('enable-guarantee-master/', views.enable_guarantee_master),
    path('delete-guarantee-master/', views.delete_guarantee_master),
    # path('history-guarantee-master/', views.guarantee_master_history),
    path('guarantee-master-get-by-userid/', views.guarantee_masters_user_id),


    path('disable-designation-master/', views.disable_designation_master),
    path('enable-designation-master/', views.enable_designation_master),
    path('delete-designation-master/', views.delete_designation_master),
    # path('history-designation-master/', views.designation_master_history),
    path('designation-master-get-by-userid/', views.designation_masters_user_id),

    path('disable-transit-insurance-master/', views.disable_transit_insurance_master),
    path('enable-transit-insurance-master/', views.enable_transit_insurance_master),
    path('delete-transit-insurance-master/', views.delete_transit_insurance_master),
    # path('history-transit-insurance-master/', views.transit_insurance_master_history),
    path('transit-insurance-master-get-by-userid/', views.transit_insurance_master_user_id),

    path('disable-payment-master/', views.disable_payment_master),
    path('enable-payment-master/', views.enable_payment_master),
    path('delete-payment-master/', views.delete_payment_master),
    # path('history-payment-master/', views.payment_master_history),
    path('payment-master-get-by-userid/', views.payment_master_user_id),

    path('disable-validity-master/', views.disable_validity_master),
    path('enable-validity-master/', views.enable_validity_master),
    path('delete-validity-master/', views.delete_validity_master),
    # path('history-validity-master/', views.validity_master_history),
    path('validity-master-get-by-userid/', views.validity_master_user_id),

    path('disable-delivery-master/', views.disable_delivery_master),
    path('enable-delivery-master/', views.enable_delivery_master),
    path('delete-delivery-master/', views.delete_delivery_master),
    # path('history-delivery-master/', views.delivery_master_history),
    path('delivery-master-get-by-userid/', views.delivery_master_user_id),

    path('disable-country-master/', views.disable_country_master),
    path('enable-country-master/', views.enable_country_master),
    path('delete-country-master/', views.delete_country_master),
    # path('history-country-master/', views.country_master_history),
    path('country-master-get-by-userid/', views.country_master_user_id),

    path('disable-tax-master/', views.disable_tax_master),
    path('enable-tax-master/', views.enable_tax_master),
    path('delete-tax-master/', views.delete_tax_master),
    # path('history-tax-master/', views.tax_master_history),
    path('tax-master-get-by-userid/', views.tax_master_user_id),

    path('disable-currency-master/', views.disable_currency_master),
    path('enable-currency-master/', views.enable_currency_master),
    path('delete-currency-master/', views.delete_currency_master),
    # path('history-currency-master/', views.currency_master_history),
    path('currency-master-get-by-userid/', views.currency_master_user_id),

    path('hsn-master-get-by-userid/',views.hsn_masters_user_id),
    path('sac-master-get-by-userid/', views.sac_masters_user_id),
    path('getfrightdeialswithvendorsindata/',views.getfrightdeialswithvendorsindata),
    path('getfrightbasedonid/',views.getfrightbasedonid),
    path('updatefright/',views.updatefright),
    path('getdesinationdeailsid/',views.getdesinationdeailsid),
    path('updatedesignation/',views.updatedesignation),
    path('getselectedcatmasters/',views.getselectedcatmasters),
    path('get-trending-categories/',views.get_trending_categories),
    path('get-admin-trending-sub-categories/',views.get_admin_trending_sub_categories),
    path('get-admin-selected-sub-categories/', views.get_admin_selected_sub_categories),
    path('sub_categories_data_by_cat_id/',views.sub_categories_data_by_cat_id),
    path('get_sub_categories_by_cat_maincat/', views.get_sub_categories_by_cat_maincat),

]

