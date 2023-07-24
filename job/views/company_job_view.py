from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from ..models.job_category import JobCategory, JobCategorySerializer
from ..models.job import Job, JobSerializer, JobDetailsSerializer
from company.models.company import Company
from ..models.job_type import JobType, JobTypeSerializer
from ..models.job_level import JobLevel, JobLevelSerializer
from ..models.employement_status import EmploymentStatus, EmploymentStatusSerializer
from ..models.word_place import WorkPlace, WorkPlaceSerializer
from ..models.benefits import JobBenefit, JobBenefitSerializer
from ..models.resume_receiving_option import ResumeReceivingOption, ResumeReceivingOptionStatusSerializer
from common.models.degree import Degree
from common.models.gender import Gender
from worker.models.skill import Skill
from common.models.country import Country
from common.models.state import State
from common.models.city import City
from common.models.area import Area
from worker.models.skill import Skill, SkillSerializer


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def create_job_basic(request):
    content = {
        'status': 0
    }
    job_categories = JobCategory.objects.all()
    serialized_categories = JobCategorySerializer(job_categories, many=True)
    content['status'] = 1
    content['message'] = 'Success'
    content['job_categories'] = serialized_categories.data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_job_type(request):
    content = {
        'status': 0
    }
    job_categories = JobType.objects.all()
    serialized_job_types = JobTypeSerializer(job_categories, many=True)
    content['status'] = 1
    content['message'] = 'Success'
    content['data'] = serialized_job_types.data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_job_levels(request):
    content = {
        'status': 0
    }
    job_levels = JobLevel.objects.all()
    serialized_job_levels = JobLevelSerializer(job_levels, many=True)
    content['status'] = 1
    content['message'] = 'Success'
    content['data'] = serialized_job_levels.data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_job_employment_status(request):
    content = {
        'status': 0
    }
    employment_status = EmploymentStatus.objects.all()
    serialized_employment_status = EmploymentStatusSerializer(employment_status, many=True)
    content['status'] = 1
    content['message'] = 'Success'
    content['data'] = serialized_employment_status.data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_job_work_places(request):
    content = {
        'status': 0
    }
    work_places = WorkPlace.objects.all()
    work_places_serialized = WorkPlaceSerializer(work_places, many=True)
    content['status'] = 1
    content['message'] = 'Success'
    content['data'] = work_places_serialized.data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_job_benefits(request):
    content = {
        'status': 0
    }
    job_benefits = JobBenefit.objects.all()
    job_benefits_serialized = JobBenefitSerializer(job_benefits, many=True)
    content['status'] = 1
    content['message'] = 'Success'
    content['data'] = job_benefits_serialized.data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_job_skills(request):
    content = {
        'status': 0
    }
    job_skills = Skill.objects.all()
    job_skills_serialized = SkillSerializer(job_skills, many=True)
    content['status'] = 1
    content['message'] = 'Success'
    content['data'] = job_skills_serialized.data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_job_cv_receiving_options(request):
    content = {
        'status': 0
    }
    cv_receiving_options = ResumeReceivingOption.objects.all()
    cv_receiving_options_serialized = ResumeReceivingOptionStatusSerializer(cv_receiving_options, many=True)
    content['status'] = 1
    content['message'] = 'Success'
    content['data'] = cv_receiving_options_serialized.data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def create_job_basic_information(request):
    content = {
        'status': 0
    }
    if all(k in request.data for k in ("user_id", "job_title", "job_type_id", "job_category_id",
                                       "job_level_id", "employment_status_id", "work_place_id",
                                       "salary_range", "no_of_vacancies", "job_responsibility",
                                       "application_deadline")):
        user_id = request.data['user_id']
        job_title = request.data['job_title']
        job_category_id = request.data['job_category_id']
        job_type_id = request.data['job_type_id']
        job_level_id = request.data['job_level_id']
        employment_status_id = request.data['employment_status_id']
        work_place_id = request.data['work_place_id']
        salary_range = request.data['salary_range']
        job_responsibility = request.data['job_responsibility']
        application_deadline = request.data['application_deadline']
        no_of_vacancies = request.data['no_of_vacancies']
        try:
            company = Company.objects.get(pk=user_id)
        except:
            content['message'] = "Company Not Found"
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            job_category = JobCategory.objects.get(pk=job_category_id)
        except:
            content['message'] = "Job Category Not Found"
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            job_level = JobLevel.objects.get(pk=job_level_id)
        except:
            content['message'] = "Job Level Not Found"
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            employment_status = EmploymentStatus.objects.get(pk=employment_status_id)
        except:
            content['message'] = "Employment Status Not Found"
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            work_place = WorkPlace.objects.get(pk=work_place_id)
        except:
            content['message'] = "Work Place Not Found"
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            job_type = JobType.objects.get(pk=job_type_id)
        except:
            content['message'] = "Job Type Not Found"
            return JsonResponse(content, status=status.HTTP_200_OK)
        created_job = Job.objects.create(
            company=company,
            industry=company.industry,
            job_type=job_type,
            job_category=job_category,
            job_title=job_title,
            job_level=job_level,
            employment_status=employment_status,
            salary_range=salary_range,
            work_place=work_place,
            no_of_vacancies=no_of_vacancies,
            application_deadline=application_deadline,
            job_responsibilities=job_responsibility
        )
        content['status'] = 1
        content['message'] = 'Success'
        content['job_id'] = created_job.id
        return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        content['message'] = 'Parameter Missing!'
        return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def edit_job_basic_information(request):
    content = {
        'status': 0
    }
    if all(k in request.data for k in ("job_id", "job_title", "job_type_id", "job_category_id",
                                       "job_level_id", "employment_status_id", "work_place_id",
                                       "salary_range", "no_of_vacancies", "job_responsibility",
                                       "application_deadline")):
        job_id = request.data['job_id']
        job_title = request.data['job_title']
        job_category_id = request.data['job_category_id']
        job_type_id = request.data['job_type_id']
        job_level_id = request.data['job_level_id']
        employment_status_id = request.data['employment_status_id']
        work_place_id = request.data['work_place_id']
        salary_range = request.data['salary_range']
        job_responsibility = request.data['job_responsibility']
        application_deadline = request.data['application_deadline']
        no_of_vacancies = request.data['no_of_vacancies']
        try:
            job = Company.objects.get(pk=job_id)
        except:
            content['message'] = "Company Not Found"
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            job_category = JobCategory.objects.get(pk=job_category_id)
        except:
            content['message'] = "Job Category Not Found"
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            job_level = JobLevel.objects.get(pk=job_level_id)
        except:
            content['message'] = "Job Level Not Found"
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            employment_status = EmploymentStatus.objects.get(pk=employment_status_id)
        except:
            content['message'] = "Employment Status Not Found"
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            work_place = WorkPlace.objects.get(pk=work_place_id)
        except:
            content['message'] = "Work Place Not Found"
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            job_type = JobType.objects.get(pk=job_type_id)
        except:
            content['message'] = "Job Type Not Found"
            return JsonResponse(content, status=status.HTTP_200_OK)
        job.job_type = job_type
        job.job_category = job_category
        job.job_title = job_title
        job.job_level = job_level
        job.employment_status = employment_status
        job.salary_range = salary_range
        job.work_place = work_place
        job.no_of_vacancies = no_of_vacancies
        job.application_deadline = application_deadline
        job.job_responsibilities = job_responsibility
        job.save()
        content['status'] = 1
        content['message'] = 'Update Success'
        return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        content['message'] = 'Parameter Missing!'
        return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def create_job_requirements(request):
    content = {
        'status': 0
    }
    if all(k in request.data for k in ("job_id", "minimum_age", "maximum_age", "degree_id",
                                       "skills_ids", "gender_ids", "cv_receiving_ids", "benefit_ids",
                                       "require_experience")):
        job_id = request.data['job_id']
        minimum_age = request.data['minimum_age']
        maximum_age = request.data['maximum_age']
        degree_id = request.data['degree_id']
        skills_ids = request.data['skills_ids']
        cv_receiving_ids = request.data['cv_receiving_ids']
        gender_ids = request.data['gender_ids']
        require_experience = request.data['require_experience']
        benefit_ids = request.data['benefit_ids']
        try:
            job = Job.objects.get(pk=job_id)
        except:
            content['message'] = "Job Not Found"
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            degree = Degree.objects.get(pk=degree_id)
        except:
            content['message'] = "Job Not Found"
            return JsonResponse(content, status=status.HTTP_200_OK)
        job.age_require_minimum = minimum_age
        job.age_require_maximum = maximum_age
        job.experience_requirements = require_experience
        job.degree_requirements = degree
        if "certificate_course_requirements" in request.data:
            certificate_course_requirements = request.data['certificate_course_requirements']
            job.certificate_course_requirements = certificate_course_requirements
        job.save()
        skills = Skill.objects.filter(pk__in=skills_ids)
        cv_receiving_options = ResumeReceivingOption.objects.filter(pk__in=cv_receiving_ids)
        genders = Gender.objects.filter(pk__in=gender_ids)
        benefits = JobBenefit.objects.filter(pk__in=benefit_ids)
        job.skills_requirements.add(*skills)
        job.cv_receiving_option.add(*cv_receiving_options)
        job.gender_requirements.add(*genders)
        job.benefits.add(*benefits)
        content['status'] = 1
        content['message'] = 'Update Successful'
        return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        content['message'] = 'Parameter Missing!'
        return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def create_job_address(request):
    content = {
        'status': 0
    }
    if all(k in request.data for k in ("job_id", "country_id", "state_id", "city_id",
                                       "area_id")):
        job_id = request.data['job_id']
        country_id = request.data['country_id']
        state_id = request.data['state_id']
        city_id = request.data['city_id']
        area_id = request.data['area_id']
        try:
            job = Job.objects.get(pk=job_id)
        except:
            content['message'] = "Job Not Found"
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            country = Country.objects.get(pk=country_id)
        except:
            content['message'] = "Country Not Found"
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            state = State.objects.get(pk=state_id)
        except:
            content['message'] = "State Not Found"
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            city = City.objects.get(pk=city_id)
        except:
            content['message'] = "City Not Found"
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            area = Area.objects.get(pk=area_id)
        except:
            content['message'] = "Area Not Found"
            return JsonResponse(content, status=status.HTTP_200_OK)
        job.country = country
        job.state = state
        job.city = city
        job.job_area = area
        job.save()
        content['status'] = 1
        content['message'] = 'Update Successful'
        return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        content['message'] = 'Parameter Missing!'
        return JsonResponse(content, status=status.HTTP_200_OK)
