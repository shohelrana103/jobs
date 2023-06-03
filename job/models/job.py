from django.db import models
from company.models.company import Company
from ..models.job_category import JobCategory
from rest_framework import serializers


class Job(models.Model):
    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    job_for_trade = models.CharField(max_length=255, null=True, blank=True)
    no_of_vacancies = models.IntegerField()
    employment_status = models.CharField(max_length=255)
    salary = models.CharField(max_length=255)
    application_deadline = models.DateTimeField()
    cv_receiving_option = models.CharField(max_length=255, null=True, blank=True)
    job_responsibilities = models.TextField(null=True, blank=True)
    job_location = models.CharField(max_length=30, null=True, blank=True)
    salary_type = models.CharField(max_length=255, null=True, blank=True)
    trade_course_requirements = models.CharField(max_length=255, null=True, blank=True)
    certificate_course_requirements = models.CharField(max_length=255, null=True, blank=True)
    educational_requirements = models.CharField(max_length=255, null=True, blank=True)
    age_restriction = models.IntegerField()
    special_restrictions = models.TextField(null=True, blank=True)
    experience_requirements = models.TextField(null=True, blank=True)
    skills_requirements = models.TextField(null=True, blank=True)
    gender_requirements = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.job_title


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.company_name', read_only=True)

    class Meta:
        model = Job
        fields = ('id', 'job_title', 'company_name', 'job_location', 'no_of_vacancies')


class JobDetailsSerializer(serializers.ModelSerializer):
    company_id = serializers.IntegerField(source='company.id', read_only=True)
    company_name = serializers.CharField(source='company.company_name', read_only=True)

    class Meta:
        model = Job
        exclude = ('created_at', 'updated_at')
