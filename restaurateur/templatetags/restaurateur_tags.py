import requests
from django import template
from geopy.distance import distance

from foodcartapp.models import Order, Restaurant
from places.geo_helper import fetch_coordinates
from places.models import Place

register = template.Library()

@register.simple_tag
def calculate_distance(order: Order, restaurant: Restaurant):
    all_places = Place.objects.values_list('address', flat=True)

    if order.address not in all_places:
        try:
            lon, lat = fetch_coordinates(order.address)
        except requests.HTTPError:
            lon, lat = 0, 0
        order_place = Place.objects.create(address=order.address,
                                           lat=lat,
                                           lon=lon)
    else:
        order_place = Place.objects.create(address=order.address)
    order_coordinates = (order_place.lat, order_place.lon)

    if restaurant.address not in all_places:
        try:
            lon, lat = fetch_coordinates(restaurant.address)
        except requests.HTTPError:
            lon, lat = 0, 0
        restaurant_place = Place.objects.create(address=restaurant.address,
                                                lat=lat,
                                                lon=lon)
    else:
        restaurant_place = Place.objects.get(address=restaurant.address)
    restaurant_coordinates = (restaurant_place.lat, restaurant_place.lon)

    distance_km = round(distance(order_coordinates, restaurant_coordinates
                                 ).kilometers, 3)
    return distance_km
