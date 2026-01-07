
from django.urls import path
from . import views

urlpatterns = [
    path('owner_register/', views.owner_register, name='owner_register'),
    path('owner_login/', views.owner_login, name='owner_login'),  # uncommented
    path('owner_dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('logout/', views.owner_logout, name='owner_logout'),
     path('pets/', views.owner_pet_list, name='owner_pet_list'),
    path('pets/<int:pk>/', views.owner_pet_detail, name='owner_pet_detail'),
    path('pets/<int:pk>/edit/', views.owner_pet_edit, name='owner_pet_edit'),
    path('pets/<int:pk>/delete/', views.owner_pet_delete, name='owner_pet_delete'),
    path('owner_profile/', views.owner_profile, name='owner_profile'),
    # Pet management
    path('add-pet/', views.add_pet, name='add_pet'),
    path('edit-pet/<int:pk>/', views.edit_pet, name='edit_pet'),
    path('delete-pet/<int:pk>/', views.delete_pet, name='delete_pet'),

    # Adopted pets
    path('adopted-pets/', views.adopted_pets, name='adopted_pets'),

    # Adoption requests
    path('adoptions/grant/<int:request_id>/', views.owner_grant_request, name='owner_grant_request'),
    path('adoptions/reject/<int:request_id>/', views.owner_reject_request, name='owner_reject_request'),

    # Optional: list owner adoption requests
    path('adoptions/requests/', views.owner_adoption_requests, name='owner_adoption_requests'),
]

