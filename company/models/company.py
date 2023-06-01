from django.db import models
from common.models.country import Country
from common.models.city import City
from common.models.state import State
from rest_framework import serializers


class Company(models.Model):
    id = models.BigAutoField(primary_key=True)
    company_name = models.CharField(max_length=255)
    company_contact_number = models.CharField(max_length=50)
    company_address_line_1 = models.TextField()
    company_address_line_2 = models.TextField(null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=30, null=True, blank=True)
    contact_person_name = models.CharField(max_length=255)
    contact_person_position = models.CharField(max_length=255)
    contact_person_mobile = models.CharField(max_length=255)
    contact_person_email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.company_name


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
