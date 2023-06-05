from django.db import models
from rest_framework import serializers


class ResumeReceivingOption(models.Model):
    id = models.BigAutoField(primary_key=True)
    option_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Resume Receiving Options'

    def __str__(self):
        return self.option_name


class ResumeReceivingOptionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeReceivingOption
        exclude = ('created_at', 'updated_at')
