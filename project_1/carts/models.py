from django.db import models


class CartQuerySet(models.QuerySet):
    def total_price(self):
        return sum(cart.get_total_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True, verbose_name='User')
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='cart_items', verbose_name='Product')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Quantity')
    session_key = models.CharField(max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')

    class Meta:
        db_table = 'cart'
        verbose_name = 'Cart'
        verbose_name_plural = 'Cart'

    objects = CartQuerySet.as_manager()

    def get_total_price(self):
        return round(self.product.price * self.quantity, 2)
