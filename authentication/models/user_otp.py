from django.db import models
from rest_framework import serializers
from ..models.authentication import Authentication


# authentication Model
class UserOtp(models.Model):
    id = models.BigAutoField(primary_key=True)
    auth_user = models.ForeignKey(Authentication, on_delete=models.CASCADE)
    otp = models.IntegerField()
    otp_send_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

