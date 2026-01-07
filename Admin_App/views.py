from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from Adoption_App.models import AdoptionRequest
from Pets_App.models import GroomingBooking, Pet, PetFood
from Admin_App.models import FoodOrder
from User_App.models import User
from Owner_App.models import Owner

@staff_member_required
def admin_dashboard(request):
    context = {
        # Users
        'users_count': User.objects.count(),
        'owners_count': Owner.objects.count(),

        # Pets summary
        'total_pets': Pet.objects.count(),
        'available_pets': Pet.objects.filter(availability='Available').count(),
        'adopted_pets': Pet.objects.filter(availability='Adopted').count(),

        # Adoption requests (USER → ADMIN)
        'pending_adoption_requests': AdoptionRequest.objects.filter(
            status='pending_admin'
        ).count(),

        # Owner added pets (OWNER → ADMIN)
        'pending_owner_pets_count': Pet.objects.filter(
            approval_status='Pending'
        ).count(),
    }

    return render(request, 'Admin_App/dashboard.html', context)


@staff_member_required
def set_pet_status(request, pet_id, status):
    print("VIEW HIT", pet_id, status, request.method)

    if request.method == 'POST' and status in ['Approved', 'Rejected']:
        pet = get_object_or_404(Pet, id=pet_id)
        pet.approval_status = status
        pet.save()
        print("STATUS UPDATED")

    return redirect('admin_owner_pets')


@staff_member_required
def admin_owner_requests(request):
    owners = AdoptionRequest.objects.select_related(
        'user', 'pet', 'owner'
    ).filter(
        status='pending_admin'
    ).order_by('-created_at')

    return render(
        request,
        'Admin_App/owner_requests.html',
        {'owners': owners}
    )
@staff_member_required
def admin_approve_request(request, request_id):
    adoption = get_object_or_404(
        AdoptionRequest,
        id=request_id,
        status='pending_admin'
    )

    adoption.status = 'approved_by_admin'
    adoption.save()

    messages.success(request, "Adoption request approved successfully.")
    return redirect('admin_owner_requests')
@staff_member_required
def admin_reject_request(request, request_id):
    adoption = get_object_or_404(
        AdoptionRequest,
        id=request_id,
        status='pending_admin'
    )

    adoption.status = 'rejected'
    adoption.save()

    messages.error(request, "Adoption request rejected.")
    return redirect('admin_owner_requests')
@staff_member_required
def admin_food_list(request):
    foods = PetFood.objects.all()
    return render(request, 'Admin_App/admin_food_list.html', {'foods': foods})

@staff_member_required
def add_pet_food(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        brand = request.POST.get('brand')
        food_type = request.POST.get('food_type')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description', '')
        image = request.FILES.get('image')
        is_available = request.POST.get('is_available') == 'on'

        if not all([name, brand, food_type, price, stock, image]):
            messages.error(request, "Please fill all required fields.")
        else:
            PetFood.objects.create(
                name=name,
                brand=brand,
                food_type=food_type,
                price=price,
                stock=stock,
                description=description,
                image=image,
                is_available=is_available
            )
            messages.success(request, "🐾 Pet Food added successfully!")
            return redirect('admin_food_list')

    return render(request, 'Admin_App/add_pet_food.html')
@staff_member_required
def edit_pet_food(request, food_id):
    food = get_object_or_404(PetFood, id=food_id)

    if request.method == 'POST':
        food.name = request.POST.get('name')
        food.description = request.POST.get('description')
        food.price = request.POST.get('price')
        food.save()
        return redirect('admin_food_list')

    return render(request, 'Admin_App/edit_pet_food.html', {'food': food})
@staff_member_required
def delete_pet_food(request, food_id):
    food = get_object_or_404(PetFood, id=food_id)
    food.delete()
    return redirect('admin_food_list')
@staff_member_required
def admin_orders(request):
    orders = FoodOrder.objects.all().order_by('-created_at')
    return render(request, 'Admin_App/orders.html', {'orders': orders})
@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(FoodOrder, id=order_id)

    if request.method == 'POST':
        order.status = request.POST.get('status')
        order.save()

    return redirect('admin_orders')
@staff_member_required
def admin_owner_pets(request):
    pets = Pet.objects.filter(approval_status='pending').order_by('-created_at')
    return render(request, 'Admin_App/owner_pets.html', {'pets': pets})
@staff_member_required
def admin_grooming_bookings(request):
    bookings = GroomingBooking.objects.all().order_by("-created_at")
    return render(request, "Admin_App/grooming_bookings.html", {
        "bookings": bookings
    })
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from Pets_App.models import Pet


@staff_member_required
def admin_adopted_pets(request):
    adopted_pets_qs = Pet.objects.filter(availability='Adopted').select_related('breed', 'owner')

    adopted_pets = []
    for pet in adopted_pets_qs:
        # Get the adoption request where owner granted adoption
        adoption = AdoptionRequest.objects.filter(pet=pet, status='granted_by_owner').first()
        adopted_pets.append({
            'pet': pet,
            'adopted_by': adoption.user if adoption else None,
            'adopted_on': adoption.created_at if adoption else None,
        })

    return render(request, 'Admin_App/adopted_pets.html', {
        'adopted_pets': adopted_pets
    })