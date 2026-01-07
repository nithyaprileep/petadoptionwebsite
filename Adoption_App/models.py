from Pets_App.models import Pet
from django.contrib.auth.models import User
from django.db import models
class AdoptionRequest(models.Model):
    STATUS_CHOICES = (
        ('pending_admin', 'Pending Admin Approval'),
        ('approved_by_admin', 'Approved by Admin'),
        ('granted_by_owner', 'Granted by Owner'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner_requests'
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='pending_admin'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.pet.name}"
