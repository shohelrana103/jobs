from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from ..models.worker import Worker, WorkerSerializer, WorkerDetailsSerializer
from job.models.job import Job, JobSerializer
from ..models.job_application import JobApplication
from ..models.worker_shortlisted_job import WorkerShortListedJob


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_worker_details(request, worker_id):
    try:
        worker = Worker.objects.get(pk=worker_id)
    except:
        content = {
            'status': 0,
            'message': 'Worker Not Found',
        }
        return JsonResponse(content, status=status.HTTP_200_OK)
    serialized_company = WorkerDetailsSerializer(worker, context={'request': request})
    content = {
        'status': 1,
        'message': 'Success',
        'data': serialized_company.data
    }
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_all_worker(request):
    content = {
        'status': 0
    }
    workers = Worker.objects.all()
    serialized_jobs = WorkerSerializer(workers, many=True)
    content['status'] = 1
    content['message'] = 'Success'
    content['workers'] = serialized_jobs.data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def worker_apply_job(request):
    content = {
        'status': 0
    }
    if 'job_id' in request.data and 'worker_id' in request.data:
        job_id = request.data['job_id']
        worker_id = request.data['worker_id']
        try:
            job = Job.objects.get(pk=job_id)
        except:
            content['message'] = 'Job Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            worker = Worker.objects.get(pk=worker_id)
        except:
            content['message'] = 'Worker Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        worker_job, is_create = JobApplication.objects.get_or_create(job_id=job, worker_id=worker)
        content['status'] = 1
        content['message'] = 'Application successful'
        return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        content['message'] = 'Parameter Missing!'
        return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def worker_applied_job(request, worker_id):
    content = {
        'status': 0
    }

    try:
        worker = Worker.objects.get(pk=worker_id)
    except:
        content['message'] = 'Worker Not Found'
        return JsonResponse(content, status=status.HTTP_200_OK)
    applied_jobs = list(JobApplication.objects.filter(worker_id=worker).values_list('job_id', flat=True))
    jobs = Job.objects.filter(pk__in=applied_jobs)
    serialized_applied_job = JobSerializer(jobs, many=True)
    content['status'] = 1
    content['message'] = 'Success'
    content['data'] = serialized_applied_job.data
    return JsonResponse(content, status=status.HTTP_200_OK) \
 \
 \
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def worker_shortlist_job(request):
    content = {
        'status': 0
    }
    if 'job_id' in request.data and 'worker_id' in request.data:
        job_id = request.data['job_id']
        worker_id = request.data['worker_id']
        try:
            job = Job.objects.get(pk=job_id)
        except:
            content['message'] = 'Job Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            worker = Worker.objects.get(pk=worker_id)
        except:
            content['message'] = 'Worker Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        worker_job, is_create = WorkerShortListedJob.objects.get_or_create(job_id=job, worker_id=worker)
        content['status'] = 1
        content['message'] = 'Short Listed Successful'
        return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        content['message'] = 'Parameter Missing!'
        return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def worker_shortlisted_job(request, worker_id):
    content = {
        'status': 0
    }

    try:
        worker = Worker.objects.get(pk=worker_id)
    except:
        content['message'] = 'Worker Not Found'
        return JsonResponse(content, status=status.HTTP_200_OK)
    shortlisted_jobs = list(WorkerShortListedJob.objects.filter(worker_id=worker).values_list('job_id', flat=True))
    jobs = Job.objects.filter(pk__in=shortlisted_jobs)
    serialized_applied_job = JobSerializer(jobs, many=True)
    content['status'] = 1
    content['message'] = 'Success'
    content['data'] = serialized_applied_job.data
    return JsonResponse(content, status=status.HTTP_200_OK)
