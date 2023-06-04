from django.db import models
from ..models.country import Country
from ..models.state import State


class City(models.Model):
    id = models.BigAutoField(primary_key=True)
    city_name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.city_name
