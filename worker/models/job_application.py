from django.db import models
from job.models.job import Job
from ..models.worker import Worker


class JobApplication(models.Model):
    id = models.BigAutoField(primary_key=True)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    worker_id = models.ForeignKey(Worker, on_delete=models.CASCADE)
    is_short_listed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'My Applied Jobs'

    def __str__(self):
        return self.job_id.job_title
