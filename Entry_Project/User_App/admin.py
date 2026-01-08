from django.contrib import admin
from .models import *

admin.site.register(FoodCart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)