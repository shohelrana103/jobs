from django.contrib import admin

# Register your models here.
from .models.company_device_token import CompanyDeviceToken
from .models.worker_device_token import WorkerDeviceToken

admin.site.register(CompanyDeviceToken)
admin.site.register(WorkerDeviceToken)
