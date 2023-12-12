from django import template
from geopy.distance import distance

from foodcartapp.models import Order, Restaurant

register = template.Library()

@register.simple_tag
def calculate_distance(order: Order, restaurant: Restaurant):
    order_coordinates = (order.lat, order.lon)
    restaurant_coordinates = (restaurant.lat, restaurant.lon)
    distance_km = round(distance(order_coordinates, restaurant_coordinates
                                 ).kilometers, 3)
    return distance_km
