from django.contrib import admin
from .models.job import Job
from .models.job_category import JobCategory

# Register your models here.


admin.site.register(Job)
admin.site.register(JobCategory)
