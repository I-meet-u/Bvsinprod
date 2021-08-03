from django.urls import path, include
from rest_framework import routers



from . import  views
from .views import sendSMS, sendOtpmail

router=routers.DefaultRouter()

# wwww
#routers are used with ViewSets in django rest framework to auto config the urls.
#when we are used serializers and viewsets we used router
router.register('user-register',views.SelfRegisterView)
router.register('user-register-sample',views.SelfRegistrationSampleView)
router.register('basic-company-details',views.BasicCompanyDetailsView)
router.register('billing-address',views.BillingAddressView),
router.register('shipping-address',views.ShippingAddressView),
router.register('industry-info',views.IndustrialInfoView),
router.register('industrial-hierarchy',views.IndustrialHierarchyView),
router.register('bank-details',views.BankDetailsView)
router.register('legal-documents',views.LegalDocumentsView)
router.register('basic-company-details-others',views.BasicCompanyDetailsOthersView)
# router.register('employee-registration',views.EmployeeRegistrationView)
router.register('employee-basic-details',views.Employee_CompanyDetailsView)
router.register('employee-industry-info',views.EmployeeIndustrialInfoView)
router.register('contact-details',views.ContactDetailsViewset)
router.register('communication-details',views.CommunicationDetailsViewset)
urlpatterns = [
    path('router-register-urls/',include(router.urls)), #router urls are included

    #normal urls other than router
    path('logout/',views.Logout.as_view()), # logout
    # path('phone-verification-otp/',views.phone_verification_otp),
    # path('email-verification-otp/',views.email_verification_otp),
    path('get-token-key-by-userid/',views.get_token_key_by_userid),
    path('get-userid-by-token/',views.get_userid_by_token),
    # path('email-verification-otp-to-change-email/',views.email_verification_otp_to_change_email),
    path('change-email/',views.change_email),
    # path('phone-otp-verfication-to-change-phonenumber/',views.phone_otp_verfication_to_change_phonenumber),
    path('change-phonenumber/',views.change_phonenumber),
    path('change-password-with-phone-number/',views.change_password_with_phone_number),
    path('change-password-with-email/',views.change_password_with_email),
    # path('waiting-mail-for-admin-approval/',views.waiting_mail_for_admin_approval),
    path('otp-session-time-out-of-phone-and-email/',views.otp_session_time_out_of_phone_and_email),
    path('phone-otp-session-out/',views.phone_otp_session_out),
    path('email-otp-session-out/',views.email_otp_session_out),
    # path('send_mail/',views.send_mail),
    path('list-documents-user/',views.list_documents_user),
    path('all-basic-data/',views.all_basic_data),
    # path('registration-list/',views.registration_list),
    path('sendbluemail/',views.sendbluemail),
    path('sendSMS/',sendSMS),
    path('sendOtpmail/',sendOtpmail),
    path('checkotp/',views.checkotp),
    path('checkemailotp/',views.checkemailotp),
    path('checkphoneotp/',views.checkphoneotp),
    path('changeemail/',views.changeemail),
    path('changephone/',views.changephone),
    path('uploaduserprofile/',views.uploaduserprofile),
    path('phone-otp-verify/',views.phone_otp_verify),
    path('email-otp-verify/',views.email_otp_verify),
    path('employee-login/',views.employee_login),
    path('get-profile-photo/', views.get_profile_photo),
    path('getcompanycode/',views.getcompanycode),
    path('update-basic-details/',views.update_basic_details),
    path('admin-approval-mail-send/',views.admin_approval_mail_send),
    path('registration-list-by-user-id/', views.registration_list_by_user_id),
    path('employee-registration-list-by-user-id/',views.employee_registration_list_by_user_id),

    path('changeempinddetails/',views.changeempinddetails),
    path('changecompprofile/',views.changecompprofile),
    path('buyer-login/',views.buyer_login)

    # path('send_mail_template/',views.send_mail_template)
    # path('subscribe_email/', MailSubscriptionAPIView.as_view(),name='subscribe-email')




]