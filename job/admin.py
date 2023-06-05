from django.contrib import admin
from .models.job import Job
from .models.job_category import JobCategory
from .models.job_type import JobType
from .models.employement_status import EmploymentStatus
from .models.resume_receiving_option import ResumeReceivingOption
from .models.job_level import JobLevel
from .models.word_place import WorkPlace
from .models.benefits import JobBenefit


# Register your models here.

class JobAdmin(admin.ModelAdmin):
    filter_horizontal = ('benefits', 'skills_requirements', 'gender_requirements', 'cv_receiving_option')


admin.site.register(Job, JobAdmin)
admin.site.register(JobCategory)
admin.site.register(JobType)
admin.site.register(EmploymentStatus)
admin.site.register(ResumeReceivingOption)
admin.site.register(JobLevel)
admin.site.register(WorkPlace)
admin.site.register(JobBenefit)
