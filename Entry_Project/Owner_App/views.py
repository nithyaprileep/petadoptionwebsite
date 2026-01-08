from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from Owner_App.Forms import PetForm
from User_App.models import Profile, ProfileRole
from Pets_App.models import Pet, PetCategory, PetBreed
from Adoption_App.models import AdoptionRequest


# ================= OWNER REGISTER =================
def owner_register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('owner_register')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if password != confirm_password:
            return render(request, 'Owner_App/register.html', {
                'error': 'Passwords do not match'
            })

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        profile = Profile.objects.create(
            user=user,
            phone=phone,
            address=address
        )

        owner_role = ProfileRole.objects.get(name='owner')
        profile.roles.add(owner_role)

        return redirect('login1')

    return render(request, 'Owner_App/register.html')


# ================= OWNER LOGIN =================
def owner_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)

        if user and user.profile.roles.filter(name='owner').exists():
            login(request, user)
            return redirect('owner_dashboard')

        return render(request, 'Owner_App/login.html', {
            'error': 'Invalid owner credentials'
        })

    return render(request, 'Owner_App/login.html')


# ================= OWNER DASHBOARD =================

@login_required
def owner_dashboard(request):
    if not request.user.profile.roles.filter(name='owner').exists():
        return redirect('home')

    # Pets added by owner, waiting for admin approval
    pending_pets = Pet.objects.filter(owner=request.user, approval_status='Pending')

    # Adoption requests for owner's pets, waiting for admin approval
    pending_requests = AdoptionRequest.objects.filter(owner=request.user, status='pending_admin')

    # Adopted pets count
    adopted_pets_count = Pet.objects.filter(owner=request.user, availability='Adopted').count()

    return render(request, 'Owner_App/dashboard.html', {
        'pending_pets': pending_pets,
        'pending_requests': pending_requests,
        'adopted_pets_count': adopted_pets_count,
    })

# ================= LOGOUT =================
@login_required
def owner_logout(request):
    logout(request)
    request.session.flush()
    messages.success(request, "Logged out successfully")
    return redirect('login')


# ================= ADD PET =================
@login_required
def add_pet(request):
    if not request.user.profile.roles.filter(name='owner').exists():
        return redirect('login')

    categories = PetCategory.objects.all()
    breeds = PetBreed.objects.all()

    if request.method == 'POST':
        category_id = request.POST.get('category')
        breed_id = request.POST.get('breed')
        custom_breed = request.POST.get('custom_breed', '').strip()

        if not category_id:
            messages.error(request, "Category is required.")
            return redirect('add_pet')

        category = get_object_or_404(PetCategory, id=category_id)

        # ✅ Handle breed logic
        if breed_id == "other":
            if not custom_breed:
                messages.error(request, "Please enter the breed name.")
                return redirect('add_pet')

            # Create or reuse breed
            breed, created = PetBreed.objects.get_or_create(
                name__iexact=custom_breed,
                category=category,
                defaults={'name': custom_breed}
            )

        else:
            if not breed_id:
                messages.error(request, "Please select a breed.")
                return redirect('add_pet')

            breed = get_object_or_404(PetBreed, id=breed_id,category=category)

        Pet.objects.create(
        owner=request.user,
        category=category,
        breed=breed,
        name=request.POST.get('name'),
        age=request.POST.get('age') or 'Unknown',
        gender=request.POST.get('gender'),
        colour=request.POST.get('colour'),
        description=request.POST.get('description'),
        photo=request.FILES.get('photo'),
        availability='Available',
        approval_status='Pending'    # set pending status
        )

        messages.success(request, "Pet added. Waiting for admin approval.")
        # return redirect('owner_dashboard')

    return render(request, 'Owner_App/owner_add_pet.html', {
        'categories': categories,
        'breeds': breeds
    })
@login_required
def owner_pet_delete(request, pk):
    pet = get_object_or_404(Pet, id=pk, owner=request.user)

    if request.method == 'POST':
        pet.delete()
        return redirect('owner_pet_list')

    return render(request, 'Owner_App/pet_confirm_delete.html', {'pet': pet})

@login_required
def owner_pet_edit(request, pk):
    pet = get_object_or_404(Pet, id=pk, owner=request.user)

    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('owner_pet_list')
    else:
        form = PetForm(instance=pet)

    return render(request, 'Owner_App/pet_edit.html', {'form': form})


@login_required
def owner_pet_detail(request, pk):
    pet = get_object_or_404(Pet, id=pk, owner=request.user)
    return render(request, 'Owner_App/pet_detail.html', {'pet': pet})

@login_required
def owner_pet_list(request):
    pets = Pet.objects.filter(owner=request.user).order_by('-created_at') 
    return render(request, 'Owner_App/owner_pet_list.html', {'pets': pets})

# ================= EDIT PET =================
@login_required
def edit_pet(request, pk):
    pet = get_object_or_404(Pet, id=pk, owner=request.user)

    if pet.approval_status != 'pending':
        messages.error(request, "Cannot edit after approval.")
        return redirect('owner_dashboard')

    if request.method == 'POST':
        pet.name = request.POST.get('name')
        pet.age = request.POST.get('age')
        pet.gender = request.POST.get('gender')
        pet.colour = request.POST.get('colour')
        pet.description = request.POST.get('description')

        if request.FILES.get('photo'):
            pet.photo = request.FILES.get('photo')

        pet.save()
        messages.success(request, "Pet updated.")
        return redirect('owner_dashboard')

    return render(request, 'Owner_App/edit_pet.html', {'pet': pet})


# ================= DELETE PET =================
@login_required
def delete_pet(request, pk):
    pet = get_object_or_404(Pet, id=pk, owner=request.user)

    if pet.approval_status != 'pending':
        messages.error(request, "Cannot delete after approval.")
        return redirect('owner_dashboard')

    pet.delete()
    messages.success(request, "Pet deleted.")
    return redirect('owner_dashboard')


# ================= OWNER GRANT ADOPTION =================
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

    adoption.pet.availability = 'Adopted'
    adoption.pet.save()

    return redirect('owner_requests')


# ================= OWNER REJECT ADOPTION =================
@login_required
def owner_reject_request(request, request_id):
    adoption = get_object_or_404(
        AdoptionRequest,
        id=request_id,
        owner=request.user
    )

    adoption.status = 'rejected'
    adoption.save()

    adoption.pet.availability = 'Available'
    adoption.pet.save()

    return redirect('owner_requests')


# ================= ADOPTED PETS =================
@login_required
def adopted_pets(request):
    pets = Pet.objects.filter(
        owner=request.user,
        availability='Adopted'
    )
    return render(request, 'Owner_App/adopted_pets.html', {'pets': pets})

@login_required
def owner_adoption_requests(request):
    """
    Show all adoption requests for this owner
    grouped by status.
    """
    pending_requests = AdoptionRequest.objects.filter(
        owner=request.user,
        status='pending_admin'
    ).select_related('pet', 'user').order_by('-created_at')

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

    return render(request, 'Owner_App/owner_requests.html', {
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'granted_requests': granted_requests,
        'rejected_requests': rejected_requests,
    })

from User_App.forms import UserForm, ProfileForm

@login_required
def owner_profile(request):
    user = request.user
    profile = user.profile

    # Ensure only owner can access
    if not profile.roles.filter(name='owner').exists():
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Owner profile updated successfully ✅")
            return redirect('owner_edit_profile')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'Owner_App/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })