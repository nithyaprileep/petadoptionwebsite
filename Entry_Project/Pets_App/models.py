from django.db import models
from django.contrib.auth.models import User


class PetCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class PetBreed(models.Model):
    category = models.ForeignKey(
        PetCategory,
        on_delete=models.CASCADE,
        related_name="breeds"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.category.name}"


class Pet(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    AVAILABILITY_CHOICES = (
        ('available', 'Available'),
        ('adopted', 'Adopted'),
    )

    APPROVAL_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    category = models.ForeignKey(
        PetCategory,
        on_delete=models.CASCADE,
        related_name="pets",
        null=True,
        blank=True
    )

    breed = models.ForeignKey(
        PetBreed,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=150)
    age = models.CharField(max_length=50, default='Unknown')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    colour = models.CharField(max_length=50, default="Unknown")
    description = models.TextField(blank=True)

    photo = models.ImageField(upload_to="pet_images/", null=True, blank=True)

    availability = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default='available'
    )

    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class PetFood(models.Model):
    FOOD_TYPES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
    ]

    name = models.CharField(max_length=200)
    food_type = models.CharField(max_length=20, choices=FOOD_TYPES)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='pet_foods/')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
# Services_App/models.py

class GroomingBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet_name = models.CharField(max_length=100)
    service_date = models.DateField()
    services = models.TextField()
    total_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet_name} - {self.service_date}"
