from django.db import models
from common.models.country import Country
from common.models.city import City
from common.models.state import State
from common.models.area import Area
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
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True)
    zip_code = models.CharField(max_length=30, null=True, blank=True)
    contact_person_name = models.CharField(max_length=255)
    contact_person_position = models.CharField(max_length=255)
    contact_person_mobile = models.CharField(max_length=255)
    contact_person_email = models.CharField(max_length=255)
    company_logo = models.FileField(upload_to='worker/images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.company_name


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'company_name')


class CompanyDetailsSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.country_name', read_only=True)
    state_name = serializers.CharField(source='state.state_name', read_only=True)
    city_name = serializers.CharField(source='city.city_name', read_only=True)
    company_logo = serializers.SerializerMethodField()

    class Meta:
        model = Company
        exclude = ('created_at', 'updated_at', 'updated_by')

    def get_company_logo(self, company):
        if company.company_logo:
            request = self.context.get('request')
            return str(request.build_absolute_uri(company.company_logo.url))
        else:
            return None
