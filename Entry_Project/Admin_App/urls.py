from django.urls import path
from . import views

urlpatterns = [
    # Admin Dashboard
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Pet approval
    path('pets/<int:pet_id>/status/<str:status>/',views.set_pet_status,name='set_pet_status'),

    # Adoption requests
    path('adoptions/requests/',views.admin_owner_requests,name='admin_owner_requests'),
    path('adoptions/approve/<int:request_id>/', views.admin_approve_request,name='admin_approve_request' ),
    path('adoptions/reject/<int:request_id>/',views.admin_reject_request,name='admin_reject_request'),
    path('admin/adopted-pets/', views.admin_adopted_pets, name='admin_adopted_pets'),

    # Pet food management
    path('foods/', views.admin_food_list, name='admin_food_list'),
    path('foods/add/', views.add_pet_food, name='add_pet_food'),
    path('foods/edit/<int:food_id>/', views.edit_pet_food, name='edit_pet_food'),
    path('foods/delete/<int:food_id>/', views.delete_pet_food, name='delete_pet_food'),

    # Food orders
    path('orders/', views.admin_orders, name='admin_orders'),
    path('orders/<int:order_id>/status/', views.update_order_status, name='update_order_status'),
    path('owner-pets/', views.admin_owner_pets, name='admin_owner_pets'),
    #grooming
    path('grooming-bookings/', views.admin_grooming_bookings, name='admin_grooming_bookings'),
]
