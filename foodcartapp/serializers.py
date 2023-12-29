from rest_framework.serializers import ListField, ModelSerializer

from places.models import Place

from .models import Order, OrderItem


class OrderItemSerializer(ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']


class OrderSerializer(ModelSerializer):
    products = ListField(many=True,
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

        Place.objects.get_or_create(address=validated_data.address)
        return new_order

    def update(self, instance, validated_data):
        for field in validated_data:
            instance.field = validated_data.get(field)
        if validated_data.address not in Place.objects.values_list('address',
                                                                   flat=True):
            Place.objects.get_or_create(address=validated_data.address)
        instance.save()
        return instance
