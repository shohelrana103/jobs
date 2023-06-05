from django.db import models
from rest_framework import serializers


class Degree(models.Model):
    id = models.BigAutoField(primary_key=True)
    degree_name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Degrees'

    def __str__(self):
        return self.degree_name


class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = ('id', 'degree_name')
