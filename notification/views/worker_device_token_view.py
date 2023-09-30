from rest_framework.views import APIView
from rest_framework import status
from ..models.worker_device_token import WorkerDeviceToken
from worker.models.worker import Worker
from django.http import JsonResponse


class WorkerDeviceTokenView(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, worker_id=None, format=None):
        content = {"status": 0}
        if worker_id is None:
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            worker = Worker.objects.get(pk=worker_id)
        except:
            content['message'] = 'Worker Not Found'
            return JsonResponse(content, status=status.HTTP_404_NOT_FOUND)
        device_token_object = WorkerDeviceToken.objects.filter(worker=worker).first()
        if device_token_object:
            worker_device_token = device_token_object.device_token
            content['status'] = 1
        else:
            worker_device_token = None
            content['status'] = 1
        content['worker_id'] = worker.id
        content['worker_device_token'] = worker_device_token
        return JsonResponse(content, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        content = {"status": 0}
        if 'worker_id' in request.data and 'device_token' in request.data:
            worker_id = request.data['worker_id']
            device_token = request.data['device_token']
            try:
                worker = Worker.objects.get(pk=worker_id)
            except:
                content['message'] = 'Worker Not Found'
                return JsonResponse(content, status=status.HTTP_404_NOT_FOUND)
            WorkerDeviceToken.objects.get_or_create(worker=worker, device_token=device_token)
            content['message'] = 'Device Token Set Successful'
            content['status'] = 1
            return JsonResponse(content, status=status.HTTP_201_CREATED)
        else:
            content['message'] = 'Provide all requirements parameter'
            return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)
