from django.db import models


class Country(models.Model):
    id = models.BigAutoField(primary_key=True)
    country_name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.country_name
