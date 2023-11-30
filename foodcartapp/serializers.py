from rest_framework.serializers import ListField, ModelSerializer

from .models import Order, OrderItem


class OrderItemSerializer(ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = ListField(child=OrderItemSerializer(),
                         allow_empty=False,
                         write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'firstname', 'lastname',
                  'phonenumber', 'address', 'products']

    def create(self, validated_data):
        validated_order = validated_data.copy()
        if 'products' in validated_order:
            del validated_order['products']

        new_order = Order.objects.create(**validated_order)
        for product in validated_data['products']:
            OrderItem.objects.create(order=new_order, **product)
        return new_order
