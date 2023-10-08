from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from ..models.job_category import JobCategory, JobCategorySerializer
from ..models.job import Job, JobSerializer, JobDetailsSerializer
from company.models.industry import Industry
from worker.models.worker import Worker
from worker.models.job_application import JobApplication
from worker.models.worker_shortlisted_job import WorkerShortListedJob
from worker.models.job_favorite import WorkerFavoriteJob
from company.models.company import Company
from common.models.country import Country
from datetime import datetime


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
    jobs = Job.objects.filter(job_category=job_category, application_deadline__gte=datetime.now(), job_status=2).order_by('-id')
    serialized_jobs = JobSerializer(jobs, many=True, context={'request': request})
    content['status'] = 1
    content['message'] = 'Success'
    content['jobs'] = serialized_jobs.data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_job_by_category_worker(request, category_id, worker_id):
    content = {
        'status': 0
    }
    try:
        job_category = JobCategory.objects.get(pk=category_id)
    except:
        content['message'] = 'Job Category Not Found'
        return JsonResponse(content, status=status.HTTP_200_OK)
    try:
        worker = Worker.objects.get(pk=worker_id)
    except:
        content['message'] = 'Worker not found'
        return JsonResponse(content, status=status.HTTP_200_OK)
    shortlisted_job_ids = list(WorkerShortListedJob.objects.filter(worker_id=worker, is_active=True).values_list('job_id', flat=True))
    applied_job_ids = list(JobApplication.objects.filter(worker_id=worker).values_list('job_id', flat=True))
    favorite_job_ids = list(WorkerFavoriteJob.objects.filter(worker_id=worker, is_active=True).values_list('job_id', flat=True))
    jobs = Job.objects.filter(job_category=job_category, application_deadline__gte=datetime.now(), job_status=2).order_by('-id')
    send_data = []
    for job in jobs:
        serialized_job = JobSerializer(job, context={'request': request}).data
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
    # serialized_jobs = JobSerializer(jobs, many=True, context={'request': request})
    content['status'] = 1
    content['message'] = 'Success'
    content['jobs'] = send_data
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
    serialized_job = JobDetailsSerializer(job, context={'request': request})
    content['status'] = 1
    content['message'] = 'Success'
    content['job_details'] = serialized_job.data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_job_detail_with_worker_id(request, job_id, worker_id):
    content = {
        'status': 0
    }
    try:
        job = Job.objects.get(pk=job_id)
    except:
        content['message'] = 'Job Not Found'
        return JsonResponse(content, status=status.HTTP_200_OK)
    try:
        worker = Worker.objects.get(pk=worker_id)
    except:
        content['message'] = 'Worker not found'
        return JsonResponse(content, status=status.HTTP_200_OK)

    serialized_job = JobDetailsSerializer(job, context={'request': request}).data

    try:
        get_applied = JobApplication.objects.get(worker_id=worker, job_id=job)
        serialized_job.update({"is_applied": True})
    except:
        serialized_job.update({"is_applied": False})

    try:
        get_shortlisted = WorkerShortListedJob.objects.get(worker_id=worker, job_id=job, is_active=True)
        serialized_job.update({"is_shortlisted": True})
    except:
        serialized_job.update({"is_shortlisted": False})

    try:
        get_favorite = WorkerFavoriteJob.objects.get(worker_id=worker, job_id=job, is_active=True)
        serialized_job.update({"is_favorite": True})
    except:
        serialized_job.update({"is_favorite": False})
    content['status'] = 1
    content['message'] = 'Success'
    content['job_details'] = serialized_job
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
    jobs = Job.objects.filter(industry=industry, application_deadline__gte=datetime.now(), job_status=2)
    serialized_jobs = JobSerializer(jobs, many=True, context={'request': request})
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
    jobs = Job.objects.filter(application_deadline__gte=datetime.now(), job_status=2).order_by('-id')
    serialized_jobs = JobSerializer(jobs, many=True, context={'request': request})
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
    shortlisted_job_ids = list(WorkerShortListedJob.objects.filter(worker_id=worker).values_list('job_id', flat=True))
    applied_job_ids = list(JobApplication.objects.filter(worker_id=worker).values_list('job_id', flat=True))
    favorite_job_ids = list(WorkerFavoriteJob.objects.filter(worker_id=worker).values_list('job_id', flat=True))
    jobs = Job.objects.filter(application_deadline__gte=datetime.now(), job_status=2).order_by('-id')
    send_data = []
    for job in jobs:
        serialized_job = JobSerializer(job, context={'request': request}).data
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


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def search_jobs(request):
    content = {
        'status': 0
    }
    jobs = Job.objects.filter(application_deadline__gte=datetime.now(), job_status=2).order_by('-id')
    query_params = request.query_params
    if "keyword" in query_params:
        keyword = query_params['keyword']
        jobs = jobs.filter(job_title__icontains=keyword)
    if "zip_code" in query_params:
        zip_code = query_params['zip_code']
        jobs = jobs.filter(zip_code=zip_code)
    if "category_id" in query_params:
        category_id = query_params['category_id']
        if category_id != 'all':
            jobs = jobs.filter(job_category__id=category_id)
    send_data = []
    if "worker_id" in query_params:
        worker_id = query_params['worker_id']
        try:
            worker = Worker.objects.get(pk=worker_id)
        except:
            content['message'] = 'Worker not found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        shortlisted_job_ids = list(WorkerShortListedJob.objects.filter(worker_id=worker).values_list('job_id', flat=True))
        applied_job_ids = list(JobApplication.objects.filter(worker_id=worker).values_list('job_id', flat=True))
        favorite_job_ids = list(WorkerFavoriteJob.objects.filter(worker_id=worker).values_list('job_id', flat=True))
        for job in jobs:
            serialized_job = JobSerializer(job, context={'request': request}).data
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
    else:
        send_data = JobSerializer(jobs, many=True, context={'request': request}).data
    content['status'] = 1
    content['message'] = 'Success'
    content['jobs'] = send_data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_job_statistic(request):
    content = {
        'status': 0
    }
    total_companies = Company.objects.all().count()
    total_worker = Worker.objects.all().count()
    total_countries = Country.objects.all().count()
    send_data = {
        'total_companies': total_companies,
        'total_worker': total_worker,
        'total_countries': total_countries
    }

    content['status'] = 1
    content['message'] = 'Success'
    content['statistic'] = send_data
    return JsonResponse(content, status=status.HTTP_200_OK)