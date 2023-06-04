from django.db import models


class EducationHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    degree_name = models.CharField(max_length=255)
    institute = models.CharField(max_length=255)
    passing_year = models.DateField(null=True, blank=True)
    is_currently_reading = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.degree_name
