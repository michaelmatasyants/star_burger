import requests
from django.conf import settings
from rest_framework.validators import ValidationError


def fetch_coordinates(geocode: str):
    '''Parses coordinates by given address with use of geocode yandex api'''
    api_key = settings.GEO_API_KEY
    base_url = 'https://geocode-maps.yandex.ru/1.x/'
    payload = {
        'apikey': api_key,
        'geocode': geocode,
        'format': 'json',
    }
    geo_response = requests.get(url=base_url,
                                params=payload,
                                timeout=120)
    geo_response.raise_for_status()
    found_places = geo_response.json()['response']['GeoObjectCollection'][
                        'featureMember']
    if not found_places:
        raise ValidationError(detail='Некорректный адрес')

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split()
    return lon, lat
