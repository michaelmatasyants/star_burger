from django import template
from geopy.distance import distance

from foodcartapp.models import Order, Restaurant
from places.models import Place

register = template.Library()

@register.simple_tag
def calculate_distance(order: Order, restaurant: Restaurant):
    order_place, _ = Place.objects.get_or_create(address=order.address)
    order_coordinates = (order_place.lat, order_place.lon)
    restaurant_place, _ = Place.objects.get_or_create(
                                            address=restaurant.address)
    restaurant_coordinates = (restaurant_place.lat, restaurant_place.lon)
    distance_km = round(distance(order_coordinates, restaurant_coordinates
                                 ).kilometers, 3)
    return distance_km
