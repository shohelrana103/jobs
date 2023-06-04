from django.db import models


class Degree(models.Model):
    id = models.BigAutoField(primary_key=True)
    degree_name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Degrees'

    def __str__(self):
        return self.degree_name
