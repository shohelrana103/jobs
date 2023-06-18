from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from ..models.company import Company, CompanySerializer, CompanyDetailsSerializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from ..models.industry import Industry
from common.models.country import Country
from common.models.state import State
from common.models.city import City
from common.models.area import Area


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
        serialized_company = CompanyDetailsSerializer(company, context={'request': request})
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


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def company_profile_update(request):
    content = {
        'status': 0
    }
    if all(k in request.data for k in ("user_id", "industry_id", "address",
                                       "country_id", "state_id", "city_id", "area_id", "zip_code",
                                       "contact_person_name", "contact_person_position", "contact_person_mobile",
                                       "contact_person_email")):
        user_id = request.data['user_id']
        country_id = request.data['country_id']
        state_id = request.data['state_id']
        city_id = request.data['city_id']
        area_id = request.data['area_id']
        industry_id = request.data['industry_id']
        address = request.data['address']
        zip_code = request.data['zip_code']
        contact_person_name = request.data['contact_person_name']
        contact_person_mobile = request.data['contact_person_mobile']
        contact_person_email = request.data['contact_person_email']
        contact_person_position = request.data['contact_person_position']
        try:
            company = Company.objects.get(pk=user_id)
        except:
            content['message'] = 'Company Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            country = Country.objects.get(pk=country_id)
        except:
            content['message'] = 'Country Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            industry = Industry.objects.get(pk=industry_id)
        except:
            content['message'] = 'Industry Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            state = State.objects.get(pk=state_id)
        except:
            content['message'] = 'State Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            city = City.objects.get(pk=city_id)
        except:
            content['message'] = 'City Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            area = Area.objects.get(pk=area_id)
        except:
            content['message'] = 'Area Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        company.industry = industry
        company.country = country
        company.state = state
        company.city = city
        company.area = area
        company.contact_person_name = contact_person_name
        company.company_address_line_1 = address
        company.zip_code = zip_code
        company.contact_person_position = contact_person_position
        company.contact_person_mobile = contact_person_mobile
        company.contact_person_email = contact_person_email
        company.save()
        content['message'] = "Update successful"
        return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        content['message'] = "Provide Require Parameters"
        return JsonResponse(content, status=status.HTTP_200_OK)
