from django.contrib import admin
from .models import PetCategory, Pet,PetBreed

admin.site.register(PetCategory)
admin.site.register(Pet)
admin.site.register(PetBreed)