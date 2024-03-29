from django.urls import path
from .views.authentication_view import *
from .views.company_authentication import *
urlpatterns = [
    path('send/otp/', worker_send_otp),
    path('verify/otp/', worker_verify_otp),
    path('set/worker/basic/', worker_set_basic_information),
    path('set/worker/address/', worker_set_address),
    path('set/worker/education/', worker_set_education),
    path('set/worker/skill/', worker_set_skill),
    path('send/otp/email/', worker_send_otp_email),
    path('verify/otp/email/', worker_verify_otp_email),
    path('signup/', worker_signup),
    path('company/signup/', company_signup),
    path('company/login/', company_login),
    path('company/change/password/', company_change_password),
    path('company/verify/signup/otp/', company_verify_signup_otp),
    path('company/send/reset/password/otp/', company_send_reset_password_otp),
    path('company/verify/reset/password/otp/', company_verify_reset_password_otp),
    path('company/reset/password/', company_reset_password),
]
