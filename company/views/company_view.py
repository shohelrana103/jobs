from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from ..models.company import Company, CompanySerializer
from django.http import JsonResponse

class CompanyView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        companies = Company.objects.all()
        serialized_company = CompanySerializer(companies, many=True)
        content ={
            'status': 1,
            'message': 'Success',
            'data': serialized_company.data
        }
        return JsonResponse(content)
