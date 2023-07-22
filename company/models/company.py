from django.db import models
from common.models.country import Country
from common.models.city import City
from common.models.state import State
from common.models.area import Area
from rest_framework import serializers
from ..models.industry import Industry


class Company(models.Model):
    id = models.BigAutoField(primary_key=True)
    company_name = models.CharField(max_length=255)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, null=True, blank=True)
    company_contact_number = models.CharField(max_length=50, null=True, blank=True)
    company_email = models.CharField(max_length=50, null=True, blank=True)
    company_address_line_1 = models.TextField(null=True, blank=True)
    company_address_line_2 = models.TextField(null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True)
    zip_code = models.CharField(max_length=30, null=True, blank=True)
    contact_person_name = models.CharField(max_length=255, null=True, blank=True)
    contact_person_position = models.CharField(max_length=255, null=True, blank=True)
    contact_person_mobile = models.CharField(max_length=255, null=True, blank=True)
    contact_person_email = models.CharField(max_length=255, null=True, blank=True)
    company_logo = models.FileField(upload_to='worker/images', null=True, blank=True)
    company_website = models.CharField(max_length=100, null=True, blank=True)
    company_size = models.IntegerField(null=True, blank=True)
    about_company = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.company_name


class CompanySerializer(serializers.ModelSerializer):
    industry = serializers.CharField(source='industry.industry_name', read_only=True)
    industry_id = serializers.IntegerField(source='industry.id', read_only=True)
    country = serializers.CharField(source='country.country_name', read_only=True)
    country_id = serializers.IntegerField(source='country.id', read_only=True)
    state = serializers.CharField(source='state.state_name', read_only=True)
    state_id = serializers.IntegerField(source='state.id', read_only=True)
    city = serializers.CharField(source='city.city_name', read_only=True)
    city_id = serializers.IntegerField(source='city.id', read_only=True)
    area = serializers.CharField(source='area.area_name', read_only=True)
    area_id = serializers.IntegerField(source='area.id', read_only=True)
    company_logo = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ('id', 'industry', 'company_name', 'company_logo', 'company_contact_number', 'country',
                  'state', 'city', 'area', 'company_website', 'company_size', 'country_id', 'state_id',
                  'city_id', 'area_id', 'industry_id')

    def get_company_logo(self, company):
        if company.company_logo:
            request = self.context.get('request')
            return str(request.build_absolute_uri(company.company_logo.url))
        else:
            return None


class CompanyDetailsSerializer(serializers.ModelSerializer):
    industry = serializers.CharField(source='industry.industry_name', read_only=True)
    industry_id = serializers.IntegerField(source='industry.id', read_only=True)
    country = serializers.CharField(source='country.country_name', read_only=True)
    country_id = serializers.IntegerField(source='country.id', read_only=True)
    state = serializers.CharField(source='state.state_name', read_only=True)
    state_id = serializers.IntegerField(source='state.id', read_only=True)
    city = serializers.CharField(source='city.city_name', read_only=True)
    city_id = serializers.IntegerField(source='city.id', read_only=True)
    area = serializers.CharField(source='area.area_name', read_only=True)
    area_id = serializers.IntegerField(source='area.id', read_only=True)
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
