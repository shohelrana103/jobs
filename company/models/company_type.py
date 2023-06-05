from django.db import models


class CompanyType(models.Model):
    id = models.BigAutoField(primary_key=True)
    company_type_name = models.CharField(max_length=100)

    def __str__(self):
        return self.company_type_name
