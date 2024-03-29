from django.db import models
from common.models.country import Country
from common.models.city import City
from common.models.state import State
from rest_framework import serializers
from ..models.skill import Skill, SkillSerializer
from ..models.employment_history import EmploymentHistory, EmploymentHistorySerializer
from ..models.education import EducationHistory, EducationHistorySerializer
from common.models.area import Area
from common.models.gender import Gender
from common.models.zip_address import ZipAddress, ZipAddressSerializer

ACCOUNT_STATUS = (
    ('1', 'Active'),
    ('2', 'Deactivate'),
    ('3', 'Deleted')
)


class Worker(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True, unique=True)
    professional_description = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    # country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    # state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    # city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    # area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True)
    zip_address = models.ForeignKey(ZipAddress, on_delete=models.SET_NULL, null=True, blank=True)
    address_line1 = models.TextField(null=True, blank=True)
    address_line2 = models.TextField(null=True, blank=True)
    zip_code = models.CharField(max_length=30, null=True, blank=True)
    educations = models.ManyToManyField(EducationHistory)
    employment_history = models.ManyToManyField(EmploymentHistory, null=True, blank=True)
    skill_set = models.ManyToManyField(Skill)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, blank=True, null=True)
    passport_number = models.CharField(max_length=255, null=True, blank=True)
    driving_license_number = models.CharField(max_length=255, null=True, blank=True)
    reference_id = models.CharField(max_length=255, null=True, blank=True)
    field_of_work = models.CharField(max_length=255, null=True, blank=True)
    photo = models.FileField(upload_to='worker/images', null=True, blank=True)
    attachment = models.FileField(upload_to='worker/files', null=True, blank=True)
    video_resume = models.FileField(upload_to='worker/video', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    account_status = models.CharField(max_length=100, choices=ACCOUNT_STATUS, default=1)
    linkedin_profile = models.CharField(null=True, blank=True)


    # def __str__(self):
    #     return self.first_name


class WorkerSerializer(serializers.ModelSerializer):
    skill_set = SkillSerializer(read_only=True, many=True)
    zip_address = ZipAddressSerializer(read_only=True)

    class Meta:
        model = Worker
        fields = ('id', 'first_name', 'middle_name', 'last_name', 'skill_set', 'zip_code', 'zip_address')


class WorkerDetailsSerializer(serializers.ModelSerializer):
    # country_name = serializers.CharField(source='country.country_name', read_only=True)
    # state_name = serializers.CharField(source='state.state_name', read_only=True)
    # city_name = serializers.CharField(source='city.city_name', read_only=True)
    # area_name = serializers.CharField(source='area.area_name', read_only=True)
    zip_address = ZipAddressSerializer(read_only=True)
    educations = EducationHistorySerializer(read_only=True, many=True)
    employment_history = EmploymentHistorySerializer(read_only=True, many=True)
    skill_set = SkillSerializer(read_only=True, many=True)
    photo = serializers.SerializerMethodField()
    video_resume = serializers.SerializerMethodField()

    class Meta:
        model = Worker
        exclude = ('created_at', 'updated_at')

    def get_photo(self, worker):
        if worker.photo:
            request = self.context.get('request')
            return str(request.build_absolute_uri(worker.photo.url))
        else:
            return None

    def get_video_resume(self, worker):
        if worker.video_resume:
            request = self.context.get('request')
            return str(request.build_absolute_uri(worker.video_resume.url))
        else:
            return None
