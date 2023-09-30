from django.db import models
from company.models.company import Company


class CompanyDeviceToken(models.Model):
    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    device_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
