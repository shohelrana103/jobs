from django.db import models
from rest_framework import serializers


class WorkPlace(models.Model):
    id = models.BigAutoField(primary_key=True)
    work_place = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Work Places'

    def __str__(self):
        return self.work_place


class WorkPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPlace
        exclude = ('created_at', 'updated_at')
