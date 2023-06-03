from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from ..models.company import Company, CompanySerializer, CompanyDetailsSerializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class CompanyView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]

    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, company_id):
        try:
            company = Company.objects.get(pk=company_id)
        except:
            content = {
                'status': 0,
                'message': 'Company Not Found',
            }
            return JsonResponse(content, status=status.HTTP_200_OK)
        serialized_company = CompanyDetailsSerializer(company)
        content = {
            'status': 1,
            'message': 'Success',
            'data': serialized_company.data
        }
        return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_all_company(request):
    content = {
        'status': 0
    }
    companies = Company.objects.all()
    serialized_jobs = CompanySerializer(companies, many=True)
    content['status'] = 1
    content['message'] = 'Success'
    content['companies'] = serialized_jobs.data
    return JsonResponse(content, status=status.HTTP_200_OK)
