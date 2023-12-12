from django.conf import settings
from rest_framework.serializers import ListField, ModelSerializer

from .geo_helper import fetch_coordinates
from .models import Order, OrderItem


class OrderItemSerializer(ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']


class OrderSerializer(ModelSerializer):
    products = ListField(child=OrderItemSerializer(),
                         allow_empty=False,
                         write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'firstname', 'lastname', 'phonenumber',
                  'address', 'products', 'lon', 'lat']

    def create(self, validated_data):
        validated_order = validated_data.copy()
        if 'products' in validated_order:
            del validated_order['products']
        validated_order['lon'], validated_order['lat'] = fetch_coordinates(
            geocode=validated_order['address']
        )
        new_order = Order.objects.create(**validated_order)

        for product in validated_data['products']:
            if not product.get('price'):
                product['price'] = product['quantity']  \
                                   * product['product'].price
            OrderItem.objects.create(order=new_order, **product)

        return new_order

    def update(self, instance, validated_data):
        for field in validated_data:
            instance.field = validated_data.get(field)
        instance.lon, instance.lat = fetch_coordinates(
            geocode=instance.get('address', instance.address)
        )
        instance.save()

        return instance
