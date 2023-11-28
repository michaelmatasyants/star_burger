from rest_framework.serializers import ListField, ModelSerializer

from .models import Order, OrderItem


class OrderItemSerializer(ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = ListField(child=OrderItemSerializer(), allow_empty=False)

    class Meta:
        model = Order
        fields = ['products', 'firstname', 'lastname',
                  'phonenumber', 'address']
