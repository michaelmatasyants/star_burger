from json import loads

from django.http import JsonResponse
from django.templatetags.static import static
from phonenumber_field.phonenumber import PhoneNumber

from .models import Order, OrderItem, Product


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def register_order(request):
    try:
        order = loads(request.body.decode())
        ordered_items = order.get('products')
    except ValueError:
        return JsonResponse({'Error': 'ValueError'})
    print(order)
    new_order = Order.objects.create(
        first_name=order.get('firstname'),
        last_name=order.get('lastname'),
        contact_phone=PhoneNumber.from_string(
            phone_number=order.get('phonenumber'),
            region='RU'
        ).as_e164,
        address=order.get('address')
    )
    print(order, ordered_items, new_order, sep='\n')
    for item in ordered_items:
        ordered_product = Product.objects.get(id=item.get('product'))
        OrderItem.objects.create(
            order=new_order,
            product=ordered_product,
            quantity=item.get('quantity')
        )
    return JsonResponse({'status': 'created'})
