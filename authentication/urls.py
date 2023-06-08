from django.urls import path
from .views.authentication_view import *
urlpatterns = [
    path('send/otp/', worker_send_otp),
    path('verify/otp/', worker_verify_otp)
]
