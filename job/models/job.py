from django.db import models
from company.models.company import Company
from ..models.job_category import JobCategory
from rest_framework import serializers
from common.models.area import Area
from ..models.employement_status import EmploymentStatus
from ..models.resume_receiving_option import ResumeReceivingOption, ResumeReceivingOptionStatusSerializer
from common.models.degree import Degree
from common.models.gender import Gender, GenderSerializer
from worker.models.skill import Skill, SkillSerializer
from ..models.job_type import JobType
from ..models.job_level import JobLevel
from ..models.word_place import WorkPlace
from ..models.benefits import JobBenefit, JobBenefitSerializer
from common.models.country import Country
from common.models.state import State
from common.models.city import City
from company.models.industry import Industry
from ..models.job_placement import JobPlacement

JOB_STATUS = (
    ('1', 'Draft'),
    ('2', 'Active'),
    ('3', 'Deactivate'),
    ('4', 'Deleted'),
)


class Job(models.Model):
    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, null=True,blank=True)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    job_category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    job_description = models.TextField(null=True, blank=True)
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
    job_status = models.CharField(max_length=100, choices=JOB_STATUS, default=2)

    def __str__(self):
        return self.job_title


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.company_name', read_only=True)
    job_type = serializers.CharField(source='job_type.type_name', read_only=True)
    job_category = serializers.CharField(source='job_category.category_name', read_only=True)
    country = serializers.CharField(source='country.country_name', read_only=True)
    state = serializers.CharField(source='state.state_name', read_only=True)
    city = serializers.CharField(source='city.city_name', read_only=True)
    job_area = serializers.CharField(source='job_area.area_name', read_only=True)
    company_logo = serializers.SerializerMethodField()
    company_website = serializers.CharField(source='company.company_website', read_only=True)
    about_company = serializers.CharField(source='company.about_company', read_only=True)
    company_email = serializers.CharField(source='company.company_email', read_only=True)
    company_phone = serializers.CharField(source='company.company_contact_number', read_only=True)

    class Meta:
        model = Job
        fields = ('id', 'job_title', 'company_name', 'no_of_vacancies', 'job_type', 'job_category', 'country', 'state', 'city', 'job_area',
                  'application_deadline', 'salary_range', 'company_logo', 'company_website', 'about_company',
                  'salary_type', 'job_description', 'company_email', 'company_phone')

    def get_company_logo(self, obj):
        if obj.company.company_logo:
            request = self.context.get('request')
            return str(request.build_absolute_uri(obj.company.company_logo.url))
        else:
            return None


class JobDetailsSerializer(serializers.ModelSerializer):
    industry = serializers.CharField(source='industry.industry_name', read_only=True)
    company_id = serializers.IntegerField(source='company.id', read_only=True)
    company = serializers.CharField(source='company.company_name', read_only=True)
    job_category = serializers.CharField(source='job_category.category_name', read_only=True)
    job_category_id = serializers.IntegerField(source='job_category.id', read_only=True)
    job_type = serializers.CharField(source='job_type.type_name', read_only=True)
    job_type_id = serializers.IntegerField(source='job_type.id', read_only=True)
    job_level = serializers.CharField(source='job_level.option_name', read_only=True)
    job_level_id = serializers.IntegerField(source='job_level.id', read_only=True)
    employment_status = serializers.CharField(source='employment_status.status_name', read_only=True)
    employment_status_id = serializers.IntegerField(source='employment_status.id', read_only=True)
    country = serializers.CharField(source='country.country_name', read_only=True)
    country_id = serializers.IntegerField(source='country.id', read_only=True)
    state = serializers.CharField(source='state.state_name', read_only=True)
    state_id = serializers.IntegerField(source='state.id', read_only=True)
    city = serializers.CharField(source='city.city_name', read_only=True)
    city_id = serializers.IntegerField(source='city.id', read_only=True)
    job_area = serializers.CharField(source='job_area.area_name', read_only=True)
    job_area_id = serializers.IntegerField(source='job_area.id', read_only=True)
    work_place = serializers.CharField(source='work_place.work_place', read_only=True)
    work_place_id = serializers.IntegerField(source='work_place.id', read_only=True)
    benefits = JobBenefitSerializer(many=True)
    skills_requirements = SkillSerializer(many=True)
    gender_requirements = GenderSerializer(many=True)
    degree_requirements = serializers.CharField(source='degree_requirements.degree_name', read_only=True)
    cv_receiving_option = ResumeReceivingOptionStatusSerializer(many=True)
    company_logo = serializers.SerializerMethodField()
    company_website = serializers.CharField(source='company.company_website', read_only=True)
    about_company = serializers.CharField(source='company.about_company', read_only=True)
    company_email = serializers.CharField(source='company.company_email', read_only=True)
    company_phone = serializers.CharField(source='company.company_contact_number', read_only=True)
    company_size = serializers.IntegerField(source='company.company_size', read_only=True)


    class Meta:
        model = Job
        exclude = ('created_at', 'updated_at')

    def get_company_logo(self, obj):
        if obj.company.company_logo:
            request = self.context.get('request')
            return str(request.build_absolute_uri(obj.company.company_logo.url))
        else:
            return None
