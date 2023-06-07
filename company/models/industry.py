from django.db import models


class Industry(models.Model):
    id = models.BigAutoField(primary_key=True)
    industry_name = models.CharField(max_length=100)

    def __str__(self):
        return self.industry_name
