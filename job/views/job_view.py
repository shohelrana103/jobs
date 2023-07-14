from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from ..models.job_category import JobCategory, JobCategorySerializer
from ..models.job import Job, JobSerializer, JobDetailsSerializer
from company.models.industry import Industry
from worker.models.worker import Worker
from worker.models.job_application import JobApplication
from worker.models.worker_shortlisted_job import WorkerShortListedJob
from worker.models.job_favorite import WorkerFavoriteJob


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_job_category(request):
    content = {
        'status': 0
    }
    job_categories = JobCategory.objects.all()
    serialized_categories = JobCategorySerializer(job_categories, many=True,context={'request': request})
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


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_all_job_worker_id(request, worker_id):
    content = {
        'status': 0
    }
    try:
        worker = Worker.objects.get(pk=worker_id)
    except:
        content['message'] = 'Worker not found'
        return JsonResponse(content, status=status.HTTP_200_OK)
    shortlisted_job_ids = list(WorkerShortListedJob.objects.filter(worker_id=worker).values_list('worker_id', flat=True))
    applied_job_ids = list(JobApplication.objects.filter(worker_id=worker).values_list('worker_id', flat=True))
    favorite_job_ids = list(WorkerFavoriteJob.objects.filter(worker_id=worker).values_list('worker_id', flat=True))
    jobs = Job.objects.all()
    send_data = []
    for job in jobs:
        serialized_job = JobSerializer(job).data
        if job.id in applied_job_ids:
            serialized_job.update({"is_applied": True})
        else:
            serialized_job.update({"is_applied": False})
        if job.id in shortlisted_job_ids:
            serialized_job.update({"is_shortlisted": True})
        else:
            serialized_job.update({"is_shortlisted": False})
        if job.id in favorite_job_ids:
            serialized_job.update({"is_favorite": True})
        else:
            serialized_job.update({"is_favorite": False})
        send_data.append(serialized_job)
    content['status'] = 1
    content['message'] = 'Success'
    content['jobs'] = send_data
    return JsonResponse(content, status=status.HTTP_200_OK)
