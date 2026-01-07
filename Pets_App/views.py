from urllib import request
from django.shortcuts import redirect, render, get_object_or_404
from .models import GroomingBooking, Pet
from django.contrib.auth.decorators import login_required
from django.contrib import messages
def pet_list(request):
    available_pets = Pet.objects.filter(approval_status="Approved", availability="Available").order_by('-created_at')
   
    # Pets that are adopted
    adopted_pets = Pet.objects.filter(
        approval_status='approved',
        availability='Adopted'
    ).order_by('-created_at')

    return render(request, 'User_App/pet_list.html', {
        'available_pets': available_pets,
        'adopted_pets': adopted_pets,
    })



def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    return render(request, 'Pets_App/pet_detail.html', {'pet': pet})
@login_required
def book_grooming(request):
    if request.method == "POST":
        services = request.POST.getlist("services")

        GroomingBooking.objects.create(
            user=request.user,
            pet_name=request.POST["pet_name"],
            service_date=request.POST["service_date"],
            services=", ".join(services),
            total_price=request.POST["total_price"]
        )

        messages.success(request, "Grooming booked successfully!")
        return redirect("services")
