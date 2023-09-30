from django.db import models
from worker.models.worker import Worker


class WorkerDeviceToken(models.Model):
    id = models.BigAutoField(primary_key=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    device_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
