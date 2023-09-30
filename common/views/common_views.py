from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from ..models.country import Country, CountrySerializer
from ..models.state import State, StateSerializer
from ..models.city import City, CitySerializer
from ..models.area import Area, AreaSerializer
from ..models.degree import Degree, DegreeSerializer
from .zip_code import get_address_details
from ..models.zip_address import ZipAddressSerializer


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_all_country(request):
    content = {
        'status': 0
    }
    counties = Country.objects.all()
    serialized_jobs = CountrySerializer(counties, many=True)
    content['status'] = 1
    content['message'] = 'Success'
    content['counties'] = serialized_jobs.data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_all_state(request, country_id):
    content = {
        'status': 0
    }
    try:
        country = Country.objects.get(pk=country_id)
    except:
        content['message'] = 'Country Not Found'
        return JsonResponse(content, status=status.HTTP_200_OK)
    states = State.objects.filter(country=country)
    serialized_jobs = StateSerializer(states, many=True)
    content['status'] = 1
    content['message'] = 'Success'
    content['states'] = serialized_jobs.data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_all_city(request, country_id):
    content = {
        'status': 0
    }
    try:
        country = Country.objects.get(pk=country_id)
    except:
        content['message'] = 'Country Not Found'
        return JsonResponse(content, status=status.HTTP_200_OK)
    cities = City.objects.filter(country=country)
    serialized_jobs = CitySerializer(cities, many=True)
    content['status'] = 1
    content['message'] = 'Success'
    content['cities'] = serialized_jobs.data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_all_area(request, country_id):
    content = {
        'status': 0
    }
    try:
        country = Country.objects.get(pk=country_id)
    except:
        content['message'] = 'Country Not Found'
        return JsonResponse(content, status=status.HTTP_200_OK)
    areas = Area.objects.filter(country=country)
    serialized_jobs = AreaSerializer(areas, many=True)
    content['status'] = 1
    content['message'] = 'Success'
    content['areas'] = serialized_jobs.data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_all_degrees(request):
    content = {
        'status': 0
    }
    degrees = Degree.objects.all()
    serialized_degree = DegreeSerializer(degrees, many=True)
    content['status'] = 1
    content['message'] = 'Success'
    content['areas'] = serialized_degree.data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_address_by_zip(request):
    content = {
        'status': 0
    }
    request_params = request.query_params
    if 'zip_code' in request_params and request_params['zip_code'] is not None:
        content['status'] = 1
        zip_address = get_address_details(request_params['zip_code'])
        content['zip_address'] = ZipAddressSerializer(zip_address).data
        return JsonResponse(content, status=status.HTTP_200_OK)

    else:
        content['message'] = 'Zip code is require'
        return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)
