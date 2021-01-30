from django.urls import path
from . import views

urlpatterns = [
    path('', views.who, name='who'),
    path('chat_home/', views.chat_home, name='chat_home'),
    path('create/<personp>/<personp2>/', views.create, name='create'),
    path('ajax_update/<personp>/<personp2>/', views.ajax_update, name='ajax_update'),
    path('check_username/', views.check_username, name='check_username'),
    path('register/', views.register, name='register'),
]