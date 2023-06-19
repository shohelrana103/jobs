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