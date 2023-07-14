from django.contrib import admin
from .models.worker import Worker
from .models.skill import Skill
from .models.job_application import JobApplication
from .models.education import EducationHistory
from .models.employment_history import EmploymentHistory
from .models.worker_shortlisted_job import WorkerShortListedJob
from .models.job_favorite import WorkerFavoriteJob


# Register your models here.
class WorkerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'email', 'phone_number',
                    'country', 'gender']
    filter_horizontal = ('educations', 'employment_history', 'skill_set')


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['job_id', 'worker_id', 'is_short_listed']


admin.site.register(Worker, WorkerAdmin)
admin.site.register(Skill)
admin.site.register(JobApplication, JobApplicationAdmin)
admin.site.register(EducationHistory)
admin.site.register(EmploymentHistory)
admin.site.register(WorkerShortListedJob)
admin.site.register(WorkerFavoriteJob)
