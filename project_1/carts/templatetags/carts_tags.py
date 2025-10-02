from django import template
from carts.utils import get_user_cart

from carts.models import Cart

register = template.Library()

@register.simple_tag()
def user_carts(request):
    return get_user_cart(request)

# {% load carts_tags %}
# {% user_carts request as carts %}
