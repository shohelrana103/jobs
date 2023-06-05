from django.db import models


class Gender(models.Model):
    id = models.BigAutoField(primary_key=True)
    gender_name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Genders'

    def __str__(self):
        return self.gender_name
