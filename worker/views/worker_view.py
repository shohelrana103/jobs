from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from ..models.worker import Worker, WorkerSerializer, WorkerDetailsSerializer



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
