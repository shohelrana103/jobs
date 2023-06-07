from django.db import models
from rest_framework import serializers


class Industry(models.Model):
    id = models.BigAutoField(primary_key=True)
    industry_name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Industries'

    def __str__(self):
        return self.industry_name


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ('id', 'industry_name')
