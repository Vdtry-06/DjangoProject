from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path
from . import views
from .api_views import get_user, create_user, user_detail

urlpatterns = [
    path('', views.home, name = 'home'),
    path('home/<str:sort_type>/<str:sort_order>/', views.home, name='home'),
    path('register/', views.register, name = 'register'),
    path('login/', views.loginPage, name = 'login'),
    path('logout/', views.logoutPage, name = 'logout'),
    path('search/', views.search, name = 'search'),
    path('image_search/', views.image_search, name='image_search'),
    path('category/', views.category, name = 'category'),
    path('detail/', views.detail, name = 'detail'),
    path('cart/', views.cart, name = 'cart'),
    path('update_item/', views.updateItem, name = 'checkout'),
    path('useraccount/', views.useraccount, name = 'useraccount'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('endpage/', views.endpage, name = 'endpage'),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    
    # API
    path('users/', get_user, name = 'get_user'),
    path('users/create', create_user, name = 'create_user'),
    path('users/<int:pk>', user_detail, name = 'user_detail'),
]