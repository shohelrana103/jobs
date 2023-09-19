from django.db import models
from rest_framework import serializers
from common.models.degree import Degree


class EducationHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    institute = models.CharField(max_length=255)
    passing_year = models.DateField(null=True, blank=True)
    is_currently_reading = models.BooleanField(default=False)
    result = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Education Histories'

    def __str__(self):
        return self.degree.degree_name


class EducationHistorySerializer(serializers.ModelSerializer):
    degree_id = serializers.IntegerField(source='degree.id', read_only=True)
    degree_name = serializers.CharField(source='degree.degree_name', read_only=True)

    class Meta:
        model = EducationHistory
        fields = ('id', 'degree_id', 'degree_name', 'institute', 'passing_year', 'is_currently_reading', 'result')
