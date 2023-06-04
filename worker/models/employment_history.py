from django.db import models


class EmploymentHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    start_at = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    responsibilities = models.TextField()
    is_currently_working = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name
