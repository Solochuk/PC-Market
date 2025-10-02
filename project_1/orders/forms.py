from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['phone_number', 'requires_delivery', 'payment_on_get']

    name = forms.CharField()
    delivery_address = forms.CharField()
