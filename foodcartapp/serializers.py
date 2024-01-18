import requests
from rest_framework.serializers import ListField, ModelSerializer

from places.geo_helper import fetch_coordinates
from places.models import Place

from .models import Order, OrderItem, Product


class OrderItemSerializer(ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'image',
                  'special_status', 'description']


class OrderSerializer(ModelSerializer):
    products = ProductSerializer(many=True,
                                 allow_empty=False,
                                 write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'firstname', 'lastname', 'phonenumber',
                  'address', 'products']

    def create(self, validated_data):
        products = validated_data.pop('products')
        new_order = Order.objects.create(**validated_data)

        for product in products:
            if not product.get('price'):
                product['price'] = product['quantity']  \
                                   * product['product'].price
            OrderItem.objects.create(order=new_order, **product)

        try:
            lon, lat = fetch_coordinates(validated_data.address)
        except requests.HTTPError:
            lon, lat = 0, 0
        Place.objects.get_or_create(address=validated_data.address,
                                    lat=lat,
                                    lon=lon)
        return new_order

    def update(self, instance, validated_data):
        for field in validated_data:
            instance.field = validated_data.get(field)
        if validated_data.address not in Place.objects.values_list('address',
                                                                   flat=True):
            try:
                lon, lat = fetch_coordinates(validated_data.address)
            except requests.HTTPError:
                lon, lat = 0, 0
            Place.objects.get_or_create(address=validated_data.address,
                                        lat=lat,
                                        lon=lon)
        instance.save()
        return instance
