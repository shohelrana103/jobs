from django.db import models
from rest_framework import serializers


class ZipAddress(models.Model):
    id = models.BigAutoField(primary_key=True)
    zip_code = models.CharField(max_length=50)
    country_code = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city_en = models.CharField(max_length=50, null=True, blank=True)
    state_en = models.CharField(max_length=50, null=True, blank=True)
    state_code = models.CharField(max_length=50, null=True, blank=True)
    province = models.CharField(max_length=50, null=True, blank=True)
    province_code = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Zip Address'

    def __str__(self):
        return self.zip_code


class ZipAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZipAddress
        fields = '__all__'
