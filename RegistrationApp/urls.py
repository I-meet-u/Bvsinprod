from django.urls import path, include
from rest_framework import routers



from . import  views
from .views import sendSMS, sendOtpmail

router=routers.DefaultRouter()

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
router.register('employee-basic-details',views.Employee_CompanyDetailsView)
router.register('employee-industry-info',views.EmployeeIndustrialInfoView)
router.register('contact-details',views.ContactDetailsViewset)
router.register('communication-details',views.CommunicationDetailsViewset)
router.register('post-enquiry',views.PostEnquiryViewSets)

urlpatterns = [
    path('router-register-urls/',include(router.urls)), #router urls are included

    #normal urls other than router
    path('logout/',views.Logout.as_view()), # logout
    path('get-token-key-by-userid/',views.get_token_key_by_userid),
    path('get-userid-by-token/',views.get_userid_by_token),
    path('change-email/',views.change_email),
    path('change-phonenumber/',views.change_phonenumber),
    path('change-password-with-phone-number/',views.change_password_with_phone_number),
    path('change-password-with-email/',views.change_password_with_email),
    path('otp-session-time-out-of-phone-and-email/',views.otp_session_time_out_of_phone_and_email),
    path('phone-otp-session-out/',views.phone_otp_session_out),
    path('email-otp-session-out/',views.email_otp_session_out),
    path('list-documents-user/',views.list_documents_user),
    path('all-basic-data/',views.all_basic_data),
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
    path('get-profile-photo/', views.get_profile_photo),
    path('getcompanycode/',views.getcompanycode),
    path('update-basic-details/',views.update_basic_details),
    path('admin-approval-mail-send/',views.admin_approval_mail_send),
    path('registration-list-by-user-id/', views.registration_list_by_user_id),
    path('employee-registration-list-by-user-id/',views.employee_registration_list_by_user_id),
    path('changeempinddetails/',views.changeempinddetails),
    path('changecompprofile/',views.changecompprofile),
    path('buyer-login/',views.buyer_login),
    path('sendbluemailforgot/',views.sendbluemailforgot),
    path('employeelogin/',views.employeelogin),
    path('delete-contact-details/',views.delete_contact_details),
    path('delete-communication-details/',views.delete_communication_details),
    path('delete-addresses/',views.delete_addressess),
    path('get-userid-by-ccode/',views.get_userid_by_ccode),
    path('get-contact-details/',views.get_contact_details),
    path('get-communication-details/',views.get_communication_details),
    path('get-billing-address-by-user-id/',views.get_billing_address_by_user_id),
    path('fetch-all-basic-company-details/',views.fetch_all_basic_company_details),
    path('delete-addresses/',views.delete_addressess),
    path('get-userid-by-ccode/',views.get_userid_by_ccode),
    path('get-contact-details/',views.get_contact_details),
    path('get-communication-details/',views.get_communication_details),
    path('get-billing-address-by-user-id/',views.get_billing_address_by_user_id),
    path('get-all-basic-details-without-token/', views.get_basic_details_without_token),
    path('get-all-basic-details-without-token-with-userid/', views.get_basic_details_without_token_and_with_userid),
    path('get-billing-address-without-token/', views.get_billing_address_without_token),
    path('get-shipping-address-without-token/', views.get_shipping_address_without_token),
    path('get-bank-details-without-token/', views.get_bank_details_without_token),
    path('get-industry-hierarchy-without-token/', views.get_industry_hierarchy_without_token),
    path('get-legal-details-without-token/', views.get_legal_details_without_token),
    path('get-employee-basic-details-without-token/', views.get_employee_basic_details_without_token),
    path('get-employee-industry-info-without-token/', views.get_employee_industry_info_without_token),
    path('get-industry-info-without-token/', views.get_industry_info_without_token),
    path('vendor-buyer-list/',views.vendor_buyer_list),
    path('admin_reject/',views.admin_reject),
    path('update_setup_status/',views.update_setup_status),
    path('update_setup_status_disable/',views.update_setup_status_disable),
    path('getregistrationbyccode/',views.getregistrationbyccode),
    path('postenquery/',views.postenquery),
    path('get_approved_companies_list/',views.get_approved_companies_list),  #get approved companies list

    # phone and email verificaiton
    path('phone-otp-verification/', views.phone_otp_verification),
    path('email-otp-verification/', views.email_otp_verification),
    path('otp-verification-status/', views.otp_verification_status)
]