from django.urls import path
from . import views


urlpatterns = [
    path('chat/', views.chat_view, name='chat'),
    path('admin/chats/', views.admin_chat_list, name='admin_chat_list'),
    path('admin/chats/<int:chat_id>/', views.admin_chat_detail, name='admin_chat_detail'),
]