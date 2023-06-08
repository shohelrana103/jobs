from django.contrib import admin
from .models.authentication import Authentication
from .models.user_otp import UserOtp

# Register your models here.


admin.site.register(Authentication)
# admin.site.register(UserOtp)
