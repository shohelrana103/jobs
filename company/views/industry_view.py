from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from ..models.industry import Industry, IndustrySerializer


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_all_industry(request):
    content = {
        'status': 0
    }
    industries = Industry.objects.all()
    serialized_jobs = IndustrySerializer(industries, many=True)
    content['status'] = 1
    content['message'] = 'Success'
    content['industries'] = serialized_jobs.data
    return JsonResponse(content, status=status.HTTP_200_OK)