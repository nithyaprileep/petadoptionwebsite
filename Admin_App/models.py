# admin_app/models.py
from django.db import models
from django.contrib.auth.models import User
from Pets_App.models import Pet, PetFood
from Adoption_App.models import AdoptionRequest

# Optional: Extend User with roles if needed
class ShelterAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    shelter_name = models.CharField(max_length=100)

class FoodOrder(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class FoodOrderItem(models.Model):
    order = models.ForeignKey(
        FoodOrder,
        related_name='items',
        on_delete=models.CASCADE
    )
    food = models.ForeignKey(PetFood, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.food.name} ({self.quantity})"
