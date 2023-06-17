from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from ..models.job_category import JobCategory, JobCategorySerializer
from ..models.job import Job, JobSerializer, JobDetailsSerializer
from company.models.industry import Industry


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_job_category(request):
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
# @permission_classes((IsAuthenticated,))
def get_job_by_category(request, category_id):
    content = {
        'status': 0
    }
    try:
        job_category = JobCategory.objects.get(pk=category_id)
    except:
        content['message'] = 'Job Category Not Found'
        return JsonResponse(content, status=status.HTTP_200_OK)
    jobs = Job.objects.filter(job_category=job_category)
    print(jobs)
    serialized_jobs = JobSerializer(jobs, many=True)
    content['status'] = 1
    content['message'] = 'Success'
    content['jobs'] = serialized_jobs.data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_job_detail(request, job_id):
    content = {
        'status': 0
    }
    try:
        job = Job.objects.get(pk=job_id)
    except:
        content['message'] = 'Job Not Found'
        return JsonResponse(content, status=status.HTTP_200_OK)
    serialized_job = JobDetailsSerializer(job)
    content['status'] = 1
    content['message'] = 'Success'
    content['job_details'] = serialized_job.data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_job_by_industry(request, industry_id):
    content = {
        'status': 0
    }
    try:
        industry = Industry.objects.get(pk=industry_id)
    except:
        content['message'] = 'Industry Not Found'
        return JsonResponse(content, status=status.HTTP_200_OK)
    jobs = Job.objects.filter(industry=industry)
    serialized_jobs = JobSerializer(jobs, many=True)
    content['status'] = 1
    content['message'] = 'Success'
    content['jobs'] = serialized_jobs.data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_all_job(request):
    content = {
        'status': 0
    }
    jobs = Job.objects.all()
    serialized_jobs = JobSerializer(jobs, many=True)
    content['status'] = 1
    content['message'] = 'Success'
    content['jobs'] = serialized_jobs.data
    return JsonResponse(content, status=status.HTTP_200_OK)
