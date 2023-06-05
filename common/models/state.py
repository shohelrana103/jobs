from django.db import models
from ..models.country import Country
from rest_framework import serializers


class State(models.Model):
    id = models.BigAutoField(primary_key=True)
    state_name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.state_name


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('id', 'state_name')
