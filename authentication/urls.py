from django.urls import path
from .views.authentication_view import *
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
]
