from django.urls import path,include
from rest_framework import  routers
from . import  views

router=routers.DefaultRouter()

router.register('buyer-product-bidding',views.BuyerProductBiddingView)
router.register('buyer-product-details',views.BiddingBuyerProductDetailsView)
router.register('rfq-code-settings',views.RfqCodeSettingsView)
router.register('rfq-terms-description',views.RfqTermsDescriptionView)
# -------
urlpatterns = [
    path('bidding-router-urls/',include(router.urls)),
    path('get-buyer-product-details/',views.get_buyer_product_based_on_userid_pk),
    path('updated-rfq-code-settings-and-rfq-number/',views.updated_rfq_code_settings_and_rfq_number)

]