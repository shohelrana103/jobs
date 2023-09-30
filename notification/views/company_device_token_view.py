from rest_framework.views import APIView
from rest_framework import status
from ..models.company_device_token import CompanyDeviceToken
from company.models.company import Company
from django.http import JsonResponse


class CompanyDeviceTokenView(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, company_id=None, format=None):
        content = {"status": 0}
        if company_id is None:
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            company = Company.objects.get(pk=company_id)
        except:
            content['message'] = 'Company Not Found'
            return JsonResponse(content, status=status.HTTP_404_NOT_FOUND)
        device_token_object = CompanyDeviceToken.objects.filter(company=company).first()
        if device_token_object:
            company_device_token = device_token_object.device_token
            content['status'] = 1
        else:
            company_device_token = None
            content['status'] = 1
        content['company_id'] = company.id
        content['company_device_token'] = company_device_token
        return JsonResponse(content, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        content = {"status": 0}
        if 'company_id' in request.data and 'device_token' in request.data:
            company_id = request.data['company_id']
            device_token = request.data['device_token']
            try:
                company = Company.objects.get(pk=company_id)
            except:
                content['message'] = 'Company Not Found'
                return JsonResponse(content, status=status.HTTP_404_NOT_FOUND)
            CompanyDeviceToken.objects.get_or_create(company=company, device_token=device_token)
            content['message'] = 'Device Token Set Successful'
            content['status'] = 1
            return JsonResponse(content, status=status.HTTP_201_CREATED)
        else:
            content['message'] = 'Provide all requirements parameter'
            return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)
