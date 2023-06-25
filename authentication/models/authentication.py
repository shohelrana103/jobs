from django.db import models
from rest_framework import serializers
from django.core.validators import MinLengthValidator


# authentication Model
class Authentication(models.Model):
    USER_TYPES = (
        ('1', 'Company'),
        ('2', 'Worker')
    )

    auth_id = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=100, blank=True, null=True, unique=True)
    username = models.CharField(max_length=100, blank=True, unique=True)
    password = models.CharField(max_length=100, validators=[MinLengthValidator(6)], null=True, blank=True)
    token = models.CharField(max_length=100)
    user_type = models.CharField(max_length=100, choices=USER_TYPES)
    user_phone = models.CharField(max_length=100, null=True, blank=True, unique=True)
    user_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.auth_id

    class Meta:
        ordering = ['-auth_id']


class AuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authentication
        fields = ('user_id', 'token', 'user_phone', 'email')
