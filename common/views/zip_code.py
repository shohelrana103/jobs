import requests
from ..models.country import Country
from ..models.city import City
from ..models.state import State
from django.conf import settings
from ..models.zip_address import ZipAddress


def get_address_details(zip_code):
    try:
        get_zip_address = ZipAddress.objects.get(zip_code=zip_code)
    except:
        try:
            headers = {
                "apikey": settings.ZIP_CODE_APIKEY}

            params = (
                ("codes", zip_code),
                ("country", "us"),
            )
            response = requests.get('https://app.zipcodebase.com/api/v1/search', headers=headers, params=params)
            result = response.json()['results']
            response_obj = result[str(zip_code)]
            # get_country, is_c = Country.objects.get_or_create(country_name='USA')
            # get_city, is_city = City.objects.get_or_create(city_name=response_obj[0]['city'], country=get_country)
            # get_state, is_state = State.objects.get_or_create(state_name=response_obj[0]['state'], country=get_country)
            get_zip_address = ZipAddress.objects.create(
                zip_code=zip_code,
                country_code=response_obj[0]['country_code'],
                latitude=response_obj[0]['latitude'],
                longitude=response_obj[0]['longitude'],
                city=response_obj[0]['city'],
                state=response_obj[0]['state'],
                city_en=response_obj[0]['city_en'],
                state_en=response_obj[0]['state_en'],
                state_code=response_obj[0]['state_code'],
                province=response_obj[0]['province'],
                province_code=response_obj[0]['province_code']
            )
        except Exception as e:
            get_zip_address = None
    return get_zip_address
