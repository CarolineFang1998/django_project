from django.urls import path, include
from django.contrib import admin
from . import views

# home page is the empty string
urlpatterns = [
    path('', views.home, name='home'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('update_item/', views.updateItem, name='update_item'),
]