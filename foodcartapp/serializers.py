import requests
from rest_framework.serializers import ModelSerializer

from places.geo_helper import fetch_coordinates
from places.models import Place

from .models import Order, OrderItem, Product


class OrderItemSerializer(ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'image',
                  'special_status', 'description']

class OrderSerializer(ModelSerializer):
    products = OrderItemSerializer(many=True,
                                   allow_empty=False,
                                   write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'products', 'firstname',
                  'lastname', 'phonenumber', 'address']

    def create(self, validated_data):
        products = validated_data.pop('products')
        new_order = Order.objects.create(**validated_data)

        for product in products:
            if not product.get('price'):
                product['price'] = product['quantity']  \
                                   * product['product'].price
            OrderItem.objects.create(order=new_order, **product)

        address = validated_data.get('address')
        try:
            lon, lat = fetch_coordinates(address)
        except requests.HTTPError:
            lon, lat = None, None
        Place.objects.get_or_create(address=address,
                                    lat=lat,
                                    lon=lon)
        return new_order

    def update(self, instance, validated_data):
        address = validated_data.get('address')
        for field in validated_data:
            instance.field = validated_data.get(field)
        if address not in Place.objects.values_list('address', flat=True):
            try:
                lon, lat = fetch_coordinates(address)
            except requests.HTTPError:
                lon, lat = None, None
            Place.objects.get_or_create(
                address=address,
                lat=lat,
                lon=lon
            )
        instance.save()
        return instance
