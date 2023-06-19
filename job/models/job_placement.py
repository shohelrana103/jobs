from django.db import models
from rest_framework import serializers


class JobPlacement(models.Model):
    id = models.BigAutoField(primary_key=True)
    type_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Job Placements'

    def __str__(self):
        return self.type_name


class JobLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPlacement
        exclude = ('created_at', 'updated_at')
