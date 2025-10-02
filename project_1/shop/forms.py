from django import forms
from .models import Category, Product

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug','description', 'price', 'stock', 'category']
