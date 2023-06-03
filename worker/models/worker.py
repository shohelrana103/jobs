from django.db import models
from common.models.country import Country
from common.models.city import City
from common.models.state import State
from rest_framework import serializers


class Worker(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    location_id = models.CharField(max_length=255, null=True, blank=True)
    address_line1 = models.TextField()
    address_line2 = models.TextField(null=True, blank=True)
    postal_code = models.CharField(max_length=30, null=True, blank=True)
    education_level = models.CharField(max_length=255, null=True, blank=True)
    employment_history = models.TextField(null=True, blank=True)
    skill_set = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=50)
    reference_id = models.CharField(max_length=255)
    field_of_work = models.CharField(max_length=255)
    photo = models.FileField(upload_to='worker/images', null=True, blank=True)
    attachment = models.FileField(upload_to='worker/files', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ('id', 'first_name', 'middle_name', 'last_name')


class WorkerDetailsSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.country_name', read_only=True)
    state_name = serializers.CharField(source='state.state_name', read_only=True)
    city_name = serializers.CharField(source='city.city_name', read_only=True)

    class Meta:
        model = Worker
        exclude = ('created_at', 'updated_at')
