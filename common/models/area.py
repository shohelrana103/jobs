from django.db import models


class Area(models.Model):
    id = models.BigAutoField(primary_key=True)
    area_name = models.CharField(max_length=100)

    def __str__(self):
        return self.area_name
