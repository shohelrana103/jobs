from django.db import models
from rest_framework import serializers


class JobBenefit(models.Model):
    id = models.BigAutoField(primary_key=True)
    benefit_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Job Benefits'

    def __str__(self):
        return self.benefit_name


class JobBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobBenefit
        exclude = ('created_at', 'updated_at')
