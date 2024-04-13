from django.urls import path
from . import views

urlpatterns = [
    path('order/new_order', views.new_order, name='new_order'),
    path('orders', views.orders, name='orders'),
    
]