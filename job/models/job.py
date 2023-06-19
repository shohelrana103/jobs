from django.db import models
from company.models.company import Company
from ..models.job_category import JobCategory
from rest_framework import serializers
from common.models.area import Area
from ..models.employement_status import EmploymentStatus
from ..models.resume_receiving_option import ResumeReceivingOption
from common.models.degree import Degree
from common.models.gender import Gender
from worker.models.skill import Skill
from ..models.job_type import JobType
from ..models.job_level import JobLevel
from ..models.word_place import WorkPlace
from ..models.benefits import JobBenefit
from common.models.country import Country
from common.models.state import State
from common.models.city import City
from company.models.industry import Industry
from ..models.job_placement import JobPlacement


class Job(models.Model):
    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    job_category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    no_of_vacancies = models.IntegerField()
    job_level = models.ForeignKey(JobLevel, on_delete=models.CASCADE)
    employment_status = models.ForeignKey(EmploymentStatus, on_delete=models.CASCADE)
    salary_range = models.CharField(max_length=255)
    work_place = models.ForeignKey(WorkPlace, on_delete=models.CASCADE)
    degree_requirements = models.ForeignKey(Degree, on_delete=models.CASCADE, null=True, blank=True)
    benefits = models.ManyToManyField(JobBenefit)
    age_require_minimum = models.IntegerField(null=True, blank=True)
    age_require_maximum = models.IntegerField(null=True, blank=True)
    experience_requirements = models.TextField(null=True, blank=True)
    skills_requirements = models.ManyToManyField(Skill)
    gender_requirements = models.ManyToManyField(Gender)
    application_deadline = models.DateTimeField()
    cv_receiving_option = models.ManyToManyField(ResumeReceivingOption)
    job_responsibilities = models.TextField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    job_area = models.ForeignKey(Area, null=True, blank=True, on_delete=models.SET_NULL)
    salary_type = models.CharField(max_length=255, null=True, blank=True)
    trade_course_requirements = models.CharField(max_length=255, null=True, blank=True)
    certificate_course_requirements = models.CharField(max_length=255, null=True, blank=True)
    special_restrictions = models.TextField(null=True, blank=True)
    job_for_trade = models.CharField(max_length=255, null=True, blank=True)
    job_placement = models.ForeignKey(JobPlacement, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.job_title


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.company_name', read_only=True)

    class Meta:
        model = Job
        fields = ('id', 'job_title', 'company_name', 'no_of_vacancies')


class JobDetailsSerializer(serializers.ModelSerializer):
    company_id = serializers.IntegerField(source='company.id', read_only=True)
    company_name = serializers.CharField(source='company.company_name', read_only=True)

    class Meta:
        model = Job
        exclude = ('created_at', 'updated_at')
