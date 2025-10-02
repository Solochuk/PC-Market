from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test


from django.shortcuts import render
from django.http import HttpResponse

from .models import ProductImage, Product, Category
from .forms import ProductForm

def admin_required(view_function):
    return user_passes_test(lambda u: u.is_superuser)(view_function)

def index(request):
    categories = Category.objects.all()
    data = Product.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(data, 15)
    current_page = paginator.page(int(page))
    return render(request, 'shop/base.html', {"data": current_page, "categories": categories})


def catalog(request, category_slug):
    categories = Category.objects.all()
    data = Product.objects.filter(category__slug=category_slug)

    page = request.GET.get('page', 1)
    paginator = Paginator(data, 15)
    current_page = paginator.page(int(page))

    return render(request, 'shop/base.html', {
        "data": current_page,
        "categories": categories
        })

def product_page(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    return render(request, 'shop/product_page.html', {"product": product})

@admin_required
def add_product(request):
    if request.method == 'POST':
        if "add" in request.POST:
            form = ProductForm(request.POST)
            if form.is_valid():
                product_instance = form.save()
                for img in request.FILES.getlist('product_images'):
                    ProductImage.objects.create(product=product_instance, image_file=img)
                return render(request, 'shop/add_product.html', {
                    "form": ProductForm(),
                    "success": True
                })
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {"form": form})

@admin_required
def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == "POST":
        if "edit" in request.POST:
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                for img in request.FILES.getlist("image_file[]"):
                    ProductImage.objects.create(product=product, image_file=img)
            return render(request, 'shop/edit_product.html', {"form": form, "success": True})
        elif "delet" in request.POST:
            product.delete()
            return redirect('/')
    else:
        form = ProductForm(instance=product)
        return render(request, 'shop/edit_product.html', {"form": form})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})
