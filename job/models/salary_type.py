from django.db import models
from rest_framework import serializers


class SalaryType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Salary Types'

    def __str__(self):
        return self.name
class SalaryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryType
        exclude = ('created_at', 'updated_at')