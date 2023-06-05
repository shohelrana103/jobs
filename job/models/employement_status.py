from django.db import models
from rest_framework import serializers


class EmploymentStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    status_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Employment Status'

    def __str__(self):
        return self.status_name


class EmploymentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentStatus
        exclude = ('created_at', 'updated_at')
