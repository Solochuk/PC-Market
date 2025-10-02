from django.shortcuts import render, redirect
from .forms import OrderForm
from carts.models import Cart
from .models import Order, OrderItem

def create_order(request):
    user = request.user if request.user.is_authenticated else None
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_items = Cart.objects.filter(user=user) if user else Cart.objects.filter(session_key=session_key)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            name = user.username if user else form.cleaned_data['name']

            order = Order.objects.create(
                user=user,
                name=name,
                phone_number=form.cleaned_data['phone_number'],
                requires_delivery=form.cleaned_data['requires_delivery'],
                payment_on_get=form.cleaned_data['payment_on_get']
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    name=item.product.name,
                    price=item.product.price,
                    quantity=item.quantity
                )
            cart_items.delete()
            return redirect('orders:order_success')
    else:
        initial = {'name': user.username} if user else {}
        form = OrderForm(initial=initial)

    return render(request, 'orders/create_order.html', {
        'form': form,
        'cart_items': cart_items
    })

def order_success(request):
    return render(request, 'orders/order_success.html')
