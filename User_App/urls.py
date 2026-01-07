"""
URL configuration for Pet_Adoption project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.common_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/',views.user_dashboard,name="dashboard"),
    path('', views.index, name='index'),
    
    path('test/', views.test, name='test'),
    path('home/', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('book-grooming/', views.book_grooming, name='book_grooming'),
     path('pet/<int:pet_id>/', views.user_pet_detail, name='user_pet_detail'),
    path('profile/', views.user_profile, name='profile'),
    # Adoption request submission
    path('pet/<int:pet_id>/request/', views.send_adoption_request, name='send_adoption_request'),
    #Food related paths
    path('foods/', views.pet_food_list, name='pet_food_list'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/decrease/<int:item_id>/',views.decrease_quantity,name='decrease_quantity'  ),
    path('cart/increase/<int:item_id>/',views.increase_quantity,name='increase_quantity' ),
    path('order-success/', views.order_success, name='order_success'),
    
   
]