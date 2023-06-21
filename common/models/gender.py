from django.db import models
from rest_framework import serializers


class Gender(models.Model):
    id = models.BigAutoField(primary_key=True)
    gender_name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Genders'

    def __str__(self):
        return self.gender_name


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ('id', 'gender_name')
