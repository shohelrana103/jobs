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
from ..models.employment_history import EmploymentHistory
from ..models.job_favorite import WorkerFavoriteJob


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
    shortlisted_job_ids = list(
        WorkerShortListedJob.objects.filter(worker_id=worker, is_active=True).values_list('job_id', flat=True))
    favorite_job_ids = list(
        WorkerFavoriteJob.objects.filter(worker_id=worker, is_active=True).values_list('job_id', flat=True))
    applied_jobs = list(JobApplication.objects.filter(worker_id=worker).values_list('job_id', flat=True))
    jobs = Job.objects.filter(pk__in=applied_jobs)
    send_data = []
    for job in jobs:
        serialized_job = JobSerializer(job, context={'request': request}).data
        serialized_job.update({"is_applied": True})
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
    content['data'] = send_data
    return JsonResponse(content, status=status.HTTP_200_OK)


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


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def worker_make_job_favorite(request):
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
        try:
            worker_job = WorkerFavoriteJob.objects.get(job_id=job, worker_id=worker)
            if worker_job.is_active:
                worker_job.is_active = False
                worker_job.save()
                content['status'] = 1
                content['message'] = 'Favorite Remove'
                return JsonResponse(content, status=status.HTTP_200_OK)
            else:
                worker_job.is_active = True
                worker_job.save()
                content['status'] = 1
                content['message'] = 'Favorite Successful'
                return JsonResponse(content, status=status.HTTP_200_OK)
        except:
            worker_job = WorkerFavoriteJob.objects.create(job_id=job, worker_id=worker)
            content['status'] = 1
            content['message'] = 'Favorite Successful'
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
    serialized_applied_job = JobSerializer(jobs, many=True, context={'request': request})
    content['status'] = 1
    content['message'] = 'Success'
    content['data'] = serialized_applied_job.data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_worker_favorite_job(request, worker_id):
    content = {
        'status': 0
    }

    try:
        worker = Worker.objects.get(pk=worker_id)
    except:
        content['message'] = 'Worker Not Found'
        return JsonResponse(content, status=status.HTTP_200_OK)

    shortlisted_job_ids = list(WorkerShortListedJob.objects.filter(worker_id=worker, is_active=True).values_list('job_id', flat=True))
    applied_job_ids = list(JobApplication.objects.filter(worker_id=worker).values_list('job_id', flat=True))
    favorite_job_ids = list(WorkerFavoriteJob.objects.filter(worker_id=worker, is_active=True).values_list('job_id', flat=True))
    jobs = Job.objects.filter(pk__in=favorite_job_ids)
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
    content['data'] = send_data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def set_worker_experiences(request):
    content = {
        'status': 0
    }
    if 'worker_id' in request.data and 'experience_list' in request.data:
        worker_id = request.data['worker_id']
        try:
            worker = Worker.objects.get(pk=worker_id)
        except:
            content['message'] = 'Worker Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        experience_list = request.data['experience_list']
        experiences_to_add = []
        for experience in experience_list:
            created_experience = EmploymentHistory.objects.create(
                company_name=experience['company_name'],
                designation=experience['designation'],
                start_at=experience['start_at'],
                end_date=experience['end_at'],
                responsibilities=experience['responsibilities'],
                is_currently_working=bool(experience['is_currently_working'])
            )
            experiences_to_add.append(created_experience)
        worker.employment_history.add(*experiences_to_add)
        content['status'] = 1
        content['message'] = 'Experience Set Successful'
        return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        content['message'] = 'Parameter Missing!'
        return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def upload_worker_resume(request):
    content = {
        'status': 0
    }
    if 'worker_id' in request.data and 'attachment' in request.data:
        worker_id = request.data['worker_id']
        try:
            worker = Worker.objects.get(pk=worker_id)
        except:
            content['message'] = 'Worker Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        attachment = request.FILES.get('attachment', False)
        if attachment is not False:
            worker.attachment = attachment
            worker.save()
        else:
            content['message'] = 'Require File'
            return JsonResponse(content, status=status.HTTP_200_OK)
        content['status'] = 1
        content['message'] = 'Attachment Added Successful'
        return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        content['message'] = 'Parameter Missing!'
        return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def upload_worker_video_resume(request):
    content = {
        'status': 0
    }
    if 'worker_id' in request.data and 'video_resume' in request.data:
        worker_id = request.data['worker_id']
        try:
            worker = Worker.objects.get(pk=worker_id)
        except:
            content['message'] = 'Worker Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        video_resume = request.FILES.get('video_resume', False)
        if video_resume is not False:
            worker.video_resume = video_resume
            worker.save()
        else:
            content['message'] = 'Require File'
            return JsonResponse(content, status=status.HTTP_200_OK)
        content['status'] = 1
        content['message'] = 'Video Added Successful'
        return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        content['message'] = 'Parameter Missing!'
        return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def upload_worker_profile_picture(request):
    content = {
        'status': 0
    }
    if 'worker_id' in request.data and 'profile_picture' in request.data:
        worker_id = request.data['worker_id']
        try:
            worker = Worker.objects.get(pk=worker_id)
        except:
            content['message'] = 'Worker Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        profile_picture = request.FILES.get('profile_picture', False)
        if profile_picture is not False:
            worker.photo = profile_picture
            worker.save()
        else:
            content['message'] = 'Require File'
            return JsonResponse(content, status=status.HTTP_200_OK)
        content['status'] = 1
        content['message'] = 'Successful'
        return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        content['message'] = 'Parameter Missing!'
        return JsonResponse(content, status=status.HTTP_200_OK)
