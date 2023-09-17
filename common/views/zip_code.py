import requests
from ..models.country import Country
from ..models.city import City
from ..models.state import State
from django.conf import settings


def get_address_details(zip_code):
    headers = {
        "apikey": settings.ZIP_CODE_APIKEY}

    params = (
        ("codes", zip_code),
        ("country", "us"),
    )
    try:
        response = requests.get('https://app.zipcodebase.com/api/v1/search', headers=headers, params=params);
        # response = requests.get('https://app.zipcodebase.com/api/v1/search?apikey=365c3820-5565-11ee-87ee-7fca7f07c81d&codes=11021', headers=headers)
        result = response.json()['results']
        response_obj = result[str(zip_code)]
        get_country, is_c = Country.objects.get_or_create(country_name='USA')
        get_city, is_city = City.objects.get_or_create(city_name=response_obj[0]['city'], country=get_country)
        get_state, is_state = State.objects.get_or_create(state_name=response_obj[0]['state'], country=get_country)
    except:
        get_country=None
        get_city=None
        get_state=None
    return get_country,get_city,get_state

