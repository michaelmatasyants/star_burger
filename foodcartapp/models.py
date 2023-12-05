from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Sum
from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    name = models.CharField(
        'Название',
        max_length=50
    )
    address = models.CharField(
        'Адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = PhoneNumberField(
        'Контактный телефон',
        region='RU',
        blank=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Ресторан'
        verbose_name_plural = 'Рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'Название',
        max_length=50
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'Название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='Категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'Цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'Картинка'
    )
    special_status = models.BooleanField(
        'Спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'Описание',
        max_length=500,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name='Ресторан',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='Продукт',
    )
    availability = models.BooleanField(
        'В продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Пункт меню ресторана'
        verbose_name_plural = 'Пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f'{self.restaurant.name} - {self.product.name}'


class OrderQuerySet(models.QuerySet):
    def calculate_price(self):
        order = self.annotate(
            price=Sum(F("items__product__price") * F("items__quantity"))
        )
        return order


class Order(models.Model):
    firstname = models.CharField(verbose_name='Имя клиента',
                                 max_length=50)
    lastname = models.CharField(verbose_name='Фамилия клиента',
                                max_length=50)
    phonenumber = PhoneNumberField(verbose_name='Телефон',
                                    region='RU',
                                    db_index=True)
    address = models.CharField(verbose_name='Адрес доставки',
                               max_length=100,
                               db_index=True)
    processed_order = models.BooleanField(verbose_name='Заказ обработан',
                                          default=False)
    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.firstname} {self.lastname}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              verbose_name='Заказ',
                              on_delete=models.CASCADE,
                              related_name='items')
    product = models.ForeignKey(Product,
                                verbose_name='Позиция в заказе',
                                related_name='order_items',
                                on_delete=models.SET_NULL,
                                null=True)
    quantity = models.IntegerField(verbose_name='Количество')
    price = models.DecimalField(verbose_name='Цена',
                                default=0,
                                max_digits=8,
                                decimal_places=2,
                                validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'Позиция в заказе'
        verbose_name_plural = 'Позиции в заказе'

    def __str__(self):
        return f'{self.product} - {self.quantity}'
