from django.contrib import admin
from .models.worker import Worker
from .models.skill import Skill
from .models.job_application import JobApplication


# Register your models here.
class WorkerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'email', 'phone_number',
                    'country', 'gender']


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['job_id', 'worker_id', 'is_short_listed']


admin.site.register(Worker, WorkerAdmin)
admin.site.register(Skill)
admin.site.register(JobApplication, JobApplicationAdmin)
