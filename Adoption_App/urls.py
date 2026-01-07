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
from .import views
urlpatterns = [
    path('status/<int:request_id>/', views.adoption_request_status,name='adoption_request_status'),
    path('admin/requests/',views.admin_adoption_requests,name='admin_adoption_requests'),
    
    path('admin/approve/<int:request_id>/',views.admin_approve_request, name='admin_approve_request'),
    path('request/<int:pet_id>/',views.send_adoption_request,name='send_adoption_request'),
    path('admin/reject/<int:request_id>/',views.admin_reject_request,name='admin_reject_request'),
    path('owner/requests/',views.owner_adoption_requests,name='owner_adoption_requests'),

    path('owner/grant/<int:request_id>/',views.owner_grant_request,name='owner_grant_request'),
    

    path("adopt/<int:pet_id>/", views.send_adoption_request, name="send_adoption_request"),

    path('owner/reject/<int:request_id>/',views.owner_reject_request,name='owner_reject_request'),
    path('admin/delete-request/<int:request_id>/',views.admin_delete_request, name='admin_delete_request'),

]
