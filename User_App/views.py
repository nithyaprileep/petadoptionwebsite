# User_App/views.py
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserForm, ProfileForm

from Adoption_App.models import AdoptionRequest
from User_App.models import User
from Owner_App.models import Owner


from User_App.utils import create_user_with_profile
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Cart, CartItem, Order, OrderItem, Profile, ProfileRole
from .models import FoodCart, CartItem

@login_required
def send_adoption_request(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, availability="Available")

    AdoptionRequest.objects.create(
        user=request.user,
        pet=pet,
        owner=pet.owner
    )

    pet.availability = "Pending"
    pet.save()
    messages.success(request,"Your adoption request has been sent for approval.")
    return redirect('user_pet_detail', pet_id=pet.id)


def user_pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    # Check if the current user already sent a pending request
    user_request_exists = False
    if request.user.is_authenticated:
        user_request_exists = AdoptionRequest.objects.filter(
            pet=pet, user=request.user, status='pending_admin'
        ).exists()

    related_pets = Pet.objects.filter(category=pet.category, availability="Available").exclude(id=pet.id)[:4]

    return render(request, "User_App/pet_detail.html", {
        "pet": pet,
        "user_request_exists": user_request_exists,
        "related_pets": related_pets,
    })

def user_register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        # Create User
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        # Create Profile
        profile = Profile.objects.create(user=user)

        # ADD ROLE (THIS IS WHERE .add() GOES)
        user_role, _ = ProfileRole.objects.get_or_create(name="user")
        profile.roles.add(user_role)

        messages.success(request, "Registration successful. Please login.")
        return redirect('login')

    return render(request, "User_App/register.html")

@login_required
def user_logout(request):
    logout(request)
    request.session.flush()
    messages.success(request, "Logged out successfully")
    return redirect('home')


def index(request):
    return render(request, 'index.html')



def test(request):
    return render(request, 'test.html')
from Pets_App.models import Pet, PetFood

@login_required
def user_dashboard(request):
    # Pets that are approved and NOT adopted
    available_pets = Pet.objects.filter(approval_status="Approved", availability="Available").order_by('-created_at')
   
    # Pets that are adopted
    adopted_pets = Pet.objects.filter(
        approval_status='approved',
        availability='Adopted'
    ).order_by('-created_at')

    return render(request, 'User_App/dashboard.html', {
        'available_pets': available_pets,
        'adopted_pets': adopted_pets,
    })

def home(request):
    if request.user.is_authenticated:
        profile = request.user.profile

        # Owner → Owner Dashboard
        if profile.roles.filter(name='owner').exists():
            return redirect('owner_dashboard')

        # Normal user → Home
        return render(request, 'User_App/dashboard.html')

    # Guest
    return render(request, 'home.html')

def services(request):
    return render(request, 'User_App/services.html')

def about(request):
    return render(request, 'User_App/about.html')

def contact(request):
    return render(request, 'User_App/contact.html')
def common_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'login.html', {'error': 'All fields are required'})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 1️⃣ ADMIN FIRST
            if user.is_staff or user.is_superuser:
                return redirect('admin_dashboard')

            # 2️⃣ ENSURE PROFILE EXISTS
            profile, created = Profile.objects.get_or_create(user=user)

            is_owner = profile.roles.filter(name='owner').exists()
            is_user = profile.roles.filter(name='user').exists()

            # 3️⃣ BOTH ROLES? → ASK USER
            if is_owner and is_user:
                return redirect('choose_role')   # 🔥 show selection page

            # 4️⃣ OWNER ONLY
            if is_owner:
                return redirect('owner_dashboard')

            # 5️⃣ NORMAL USER
            if is_user:
                return redirect('dashboard')

            # fallback
            return redirect('login')

        return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')
# def pet_list(request):
#     available_pets = Pet.objects.filter(
#         availability='available',
#         approval_status='approved'
#     )

#     adopted_pets = Pet.objects.filter(
#         availability='adopted',
#         approval_status='approved'
#     )

#     return render(request, 'User_App/pet_list.html', {
#         'available_pets': available_pets,
#         'adopted_pets': adopted_pets,
#     })
def pet_list(request):
    available_pets = Pet.objects.filter(approval_status="Approved", availability="Available").order_by('-created_at')
   
    # Pets that are adopted
    adopted_pets = Pet.objects.filter(
        approval_status='approved',
        availability='Adopted'
    ).order_by('-created_at')

    return render(request, 'User_App/petlist.html', {
        'available_pets': available_pets,
        'adopted_pets': adopted_pets,
    })


def pet_food_list(request):
    foods = PetFood.objects.filter(is_available=True, stock__gt=0)
    return render(request, 'User_App/food_list.html', {'foods': foods})

@login_required
def add_to_cart(request, food_id):
    food = get_object_or_404(PetFood, id=food_id)

# Get or create food cart for user
    food_cart, _ = FoodCart.objects.get_or_create(user=request.user)

# Get or create cart item
    item, created = CartItem.objects.get_or_create(
        cart=food_cart,
        food=food
    )

# If item already exists, increase quantity
    if not created:
        item.quantity += 1
    else:
        item.quantity = 1

    item.save()

    return redirect('view_cart')


@login_required(login_url='login')
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'User_App/cart.html', {
        'cart': cart,
        'total': cart.total_price()
    })
@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)

    if request.method == "POST":
        order = Order.objects.create(
            user=request.user,
            total_amount=cart.total_price(),
            is_paid=True   # later integrate real payment
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                food=item.food,
                quantity=item.quantity,
                price=item.food.price
            )
            item.food.stock -= item.quantity
            item.food.save()

        cart.items.all().delete()

        return redirect('order_success')

    return render(request, 'User_App/checkout.html', {'cart': cart})
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()   # remove item if quantity becomes 0

    return redirect('view_cart')

@login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.quantity += 1
    item.save()

    return redirect('view_cart')


@login_required
def order_success(request):
    return render(request, 'User_App/order_success.html')

def book_grooming(request):
    if request.method == 'POST':
        # Save to DB later (optional)
        messages.success(request, "Grooming service booked successfully!")
        return redirect('services')

@login_required
def send_adoption_request(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == "POST":
        # Prevent duplicate requests
        if AdoptionRequest.objects.filter(pet=pet, user=request.user, status='pending_admin').exists():
            messages.warning(request, "You already sent a request for this pet!")
            return redirect('user_pet_detail', pet_id=pet.id)

        # Create adoption request
        AdoptionRequest.objects.create(
            pet=pet,
            user=request.user,
            owner=pet.owner
        )

        messages.success(request, "Adoption request sent successfully!")
        return redirect('user_pet_detail', pet_id=pet.id)

    return redirect('user_pet_detail', pet_id=pet.id)


@login_required
def user_profile(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully ✅")
            return redirect('profile')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'User_App/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })