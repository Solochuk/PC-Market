from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

app_name = 'shop'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('', views.index, name='main_page'),
    path('add_product', views.add_product, name='add_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('<slug:category_slug>/', views.catalog, name='catalog_page'),
    path('product/<slug:product_slug>/', views.product_page, name='product_page'),
]    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
