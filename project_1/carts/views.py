# from django.shortcuts import render, redirect

# from carts.models import Cart
# from shop.models import Product


# def cart_add(request, product_slug):
#     product = Product.objects.get(slug=product_slug)
#     if request.user.is_authenticated:
#         carts = Cart.objects.filter(user=request.user, product=product)

#         if carts.exists():
#             cart = carts.first()
#             if cart:
#                 cart.quantity += 1
#                 cart.save()
#         else:
#             Cart.objects.create(user=request.user, product=product, quantity=1)
#     else:
#         carts = Cart.objects.filter(session_key=request.session.session_key, product=product)

#         if carts.exists():
#             cart = carts.first()
#             if cart:
#                 cart.quantity += 1
#                 cart.save()
#         else:
#             Cart.objects.create(session_key=request.session.session_key, product=product, quantity=1)

#     return redirect(request.META.get('HTTP_REFERER', '/'))

# def cart_remove(request, cart_id):
#     cart = Cart.objects.get(id=cart_id)
#     cart.delete()
#     return redirect(request.META.get('HTTP_REFERER', '/'))

# def cart_change(request, cart_id):
#     cart = Cart.objects.get(id=cart_id)
#     if request.method == "POST":
#         quantity = int(request.POST.get("quantity", 1))
#         if quantity > 0:
#             cart.quantity = quantity
#             cart.save()
#         else:
#             cart.delete()
#     return redirect(request.META.get('HTTP_REFERER', '/'))

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart
from shop.models import Product


def cart_view(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart_items = Cart.objects.filter(session_key=request.session.session_key)

    return render(request, "carts/carts.html", {
        "cart_items": cart_items,
        "cart_total": cart_items.total_price(),
        "cart_quantity": cart_items.total_quantity(),
    })


def cart_add(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user, product=product,
            defaults={"quantity": 1}
        )
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(
            session_key=request.session.session_key, product=product,
            defaults={"quantity": 1}
        )

    if not created:
        cart.quantity += 1
        cart.save()

    return redirect(request.META.get("HTTP_REFERER", "/"))


def cart_remove(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)
    cart.delete()
    return redirect(request.META.get("HTTP_REFERER", "/"))


def cart_change(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)
    if request.method == "POST":
        try:
            quantity = int(request.POST.get("quantity", 1))
            if quantity > 0:
                cart.quantity = quantity
                cart.save()
            else:
                cart.delete()
        except (TypeError, ValueError):
            pass
    return redirect(request.META.get("HTTP_REFERER", "/"))
