from django.db import models
from django.utils import timezone
from shop.models import Product
from django.contrib.auth.models import User

# Create your models here.

class OrderitemQuerySet(models.QuerySet):
    def total_price(self):
        return sum(cart.get_total_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Order(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Name')
    phone_number = models.CharField(max_length=15, verbose_name='Phone Number')
    requires_delivery = models.BooleanField(default=False, verbose_name='Requires Delivery')
    delivery_address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Delivery Address')
    payment_on_get = models.BooleanField(default=False, verbose_name='Payment on Get')
    is_paid = models.BooleanField(default=False, verbose_name='Is Paid')
    status = models.CharField(max_length=50, default='Processing', verbose_name='Status')

    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='Товар без назви', verbose_name='Product Name')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Quantity')
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'order_items'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    objects = OrderitemQuerySet.as_manager()

    def get_total_price(self):
        return round(self.product.price * self.quantity, 2)
