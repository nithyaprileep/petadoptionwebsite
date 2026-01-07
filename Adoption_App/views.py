# Adoption_App/views.py
# Adoption_App/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from Adoption_App.models import AdoptionRequest
from Pets_App.models import Pet


@login_required
def adopt_pet(request, pet_id):
    # session username can be accessed
    username = request.session.get('username')
    # Your logic to submit adoption request
    return render(request, 'Adoption_App/adopt_pet.html', {'username': username})

@login_required
def adoption_request_status(request, request_id):
    adoption_request = get_object_or_404(
        AdoptionRequest,
        id=request_id,
        user=request.user
    )

    return render(
        request,
        'Adoption_App/request_status.html',
        {'request': adoption_request}
    )
@staff_member_required
def admin_adoption_requests(request):
    requests = AdoptionRequest.objects.filter(status='pending_admin')  # matches model value
    return render(
        request,
        'Adoption_App/admin_requests.html',
        {'requests': requests}
    )
@staff_member_required
def admin_approve_request(request, request_id):
    adoption = get_object_or_404(
        AdoptionRequest,
        id=request_id,
        status='pending_admin'
    )

    # Update request status
    adoption.status = 'approved_by_admin'
    adoption.save()

    # Optional: mark the pet as pending/granted
    adoption.pet.availability = 'Pending'
    adoption.pet.save()

    messages.success(
        request,
        f"Adoption request for {adoption.pet.name} approved and sent to the pet owner."
    )

    return redirect('admin_adoption_requests')

@staff_member_required
def admin_reject_request(request, request_id):
    adoption = get_object_or_404(
        AdoptionRequest,
        id=request_id
    )

    adoption.status = 'rejected'
    adoption.save()

    # Make pet available again if it was pending
    adoption.pet.availability = 'Available'
    adoption.pet.save()

    messages.error(
        request,
        f"Adoption request for {adoption.pet.name} rejected."
    )

    return redirect('admin_adoption_requests')

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
@login_required
def send_adoption_request(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    
    # Owner cannot request own pet
    if pet.owner == request.user:
        messages.error(request, "You cannot request adoption for your own pet.")
        return redirect('user_pet_detail', pet_id=pet.id)

    # Already requested by this user
    if AdoptionRequest.objects.filter(user=request.user, pet=pet).exists():
        messages.warning(request, "You have already requested this pet.")
        return redirect('user_pet_detail', pet_id=pet.id)

    # Pet not available
    if pet.availability != "Available":
        messages.error(request, "This pet is not available for adoption.")
        return redirect('user_pet_detail', pet_id=pet.id)

    # Create adoption request
    AdoptionRequest.objects.create(
        user=request.user,
        pet=pet,
        owner=pet.owner,
        status='pending_admin'  # must match model choice exactly
    )

    # Mark pet as pending
    pet.availability = "Pending"
    pet.save()

    messages.success(request, "Adoption request sent successfully! Please wait for admin approval.")
    return redirect('dashboard')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from Pets_App.models import Pet
from Adoption_App.models import AdoptionRequest

@login_required
def owner_adoption_requests(request):
    # Newly added pets waiting for admin approval
    pending_pets = Pet.objects.filter(owner=request.user, approval_status='Pending')

    # Adoption requests for owner's pets waiting for admin approval
    pending_requests = AdoptionRequest.objects.filter(
        owner=request.user,
        status='pending_admin'
    ).select_related('pet', 'user').order_by('-created_at')

    # Other adoption request statuses
    approved_requests = AdoptionRequest.objects.filter(
        owner=request.user,
        status='approved_by_admin'
    ).select_related('pet', 'user').order_by('-created_at')

    granted_requests = AdoptionRequest.objects.filter(
        owner=request.user,
        status='granted_by_owner'
    ).select_related('pet', 'user').order_by('-created_at')

    rejected_requests = AdoptionRequest.objects.filter(
        owner=request.user,
        status='rejected'
    ).select_related('pet', 'user').order_by('-created_at')

    return render(request, 'Adoption_App/owner_requests.html', {
        'pending_pets': pending_pets,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'granted_requests': granted_requests,
        'rejected_requests': rejected_requests,
    })
@login_required
def owner_grant_request(request, request_id):
    adoption = get_object_or_404(
        AdoptionRequest,
        id=request_id,
        owner=request.user,
        status='approved_by_admin'
    )

    adoption.status = 'granted_by_owner'
    adoption.save()

    pet = adoption.pet
    pet.availability = 'Adopted'
    pet.save()

    messages.success(
        request,
        f"Adoption approved successfully! {pet.name} has been adopted."
    )

    # return redirect('adoption:owner_adoption_requests')
    return redirect('owner_adoption_requests')


@login_required
def owner_reject_request(request, request_id):
    adoption = get_object_or_404(
        AdoptionRequest,
        id=request_id,
        owner=request.user
    )

    adoption.status = 'rejected'
    adoption.save()

    pet = adoption.pet
    pet.availability = 'Available'
    pet.save()

    messages.error(
        request,
        f"Adoption request for {pet.name} has been rejected."
    )

    return redirect('adoption:owner_adoption_requests')

@staff_member_required
def admin_delete_request(request, request_id):
    adoption = get_object_or_404(AdoptionRequest, id=request_id)

    pet_name = adoption.pet.name
    adoption.delete()

    messages.success(
        request,
        f"Adoption request for {pet_name} has been deleted successfully."
    )

    return redirect('admin_dashboard')

