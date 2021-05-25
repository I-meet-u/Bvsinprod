from django.urls import path, include
from rest_framework import routers



from . import  views

router=routers.DefaultRouter()
router.register('user-register',views.SelfRegisterView)
router.register('user-register-sample',views.SelfRegistrationSampleView)
router.register('basic-company-details',views.BasicCompanyDetailsView)
router.register('billing-address',views.BillingAddressView),
router.register('shipping-address',views.ShippingAddressView),
router.register('industry-info',views.IndustrialInfoView),
router.register('industrial-hierarchy',views.IndustrialHierarchyView),
router.register('bank-details',views.BankDetailsView)
router.register('legal-documents',views.LegalDocumentsView)

urlpatterns = [
    path('router-register-urls/',include(router.urls)), #router urls are included
    path('logout/',views.Logout.as_view()), # logout
    path('phone-verification-otp/',views.phone_verification_otp),
    path('email-verification-otp/',views.email_verification_otp),
    path('get-token-key-by-userid/',views.get_token_key_by_userid),
    path('get-userid-by-token/',views.get_userid_by_token),
    path('email-verification-otp-to-change-email/',views.email_verification_otp_to_change_email),
    path('change-email/',views.change_email),
    path('phone-otp-verfication-to-change-phonenumber/',views.phone_otp_verfication_to_change_phonenumber),
    path('change-phonenumber/',views.change_phonenumber),
    path('change-password-with-phone-number/',views.change_password_with_phone_number),
    path('change-password-with-email/',views.change_password_with_email),
    # path('waiting-mail-for-admin-approval/',views.waiting_mail_for_admin_approval),
    path('otp-session-time-out-of-phone-and-email/',views.otp_session_time_out_of_phone_and_email),
    path('phone-otp-session-out/',views.phone_otp_session_out),
    path('email-otp-session-out/',views.email_otp_session_out),
    # path('send_mail/',views.send_mail),
    path('get-basic-info-by-gst/',views.get_basic_info_by_gst),
    path('get-bank-details-by-pk/',views.get_bank_details_by_pk)
    # path('send_mail_template/',views.send_mail_template)
    # path('subscribe_email/', MailSubscriptionAPIView.as_view(),name='subscribe-email')




]