from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'), 
    path('register/', views.register, name = 'register'),
    path('login/', views.loginPage, name = 'login'),
    path('logout/', views.logoutPage, name = 'logout'),
    path('search/', views.search, name = 'search'),
    path('category/', views.category, name = 'category'),
    path('detail/', views.detail, name = 'detail'),
    path('add_item/', views.updateItem, name = 'cart'),
    path('cart/', views.cart, name = 'cart'),
    path('update_item/', views.updateItem, name = 'checkout'),
    path('checkout/', views.checkout, name = 'checkout'),
]