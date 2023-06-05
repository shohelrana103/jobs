from django.db import models
from rest_framework import serializers


class JobType(models.Model):
    id = models.BigAutoField(primary_key=True)
    type_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Job Types'

    def __str__(self):
        return self.type_name


class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        exclude = ('created_at', 'updated_at')
