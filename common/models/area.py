from django.db import models
from ..models.city import City
from ..models.state import State
from ..models.country import Country


class Area(models.Model):
    id = models.BigAutoField(primary_key=True)
    area_name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.area_name
