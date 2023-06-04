from django.db import models
from rest_framework import serializers
from common.models.degree import Degree


class EducationHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    institute = models.CharField(max_length=255)
    passing_year = models.DateField(null=True, blank=True)
    is_currently_reading = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Education Histories'

    def __str__(self):
        return self.degree_name


class EducationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationHistory
        fields = ('id', 'degree_name', 'institute', 'passing_year', 'is_currently_reading')