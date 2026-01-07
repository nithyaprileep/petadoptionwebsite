from django.contrib.auth.models import User
from .models import Profile

def create_user_with_profile(**kwargs):
    user = User.objects.create_user(
        username=kwargs['username'],
        email=kwargs.get('email'),
        password=kwargs['password']
    )

    Profile.objects.create(
        user=user,
        phone=kwargs.get('phone', ''),
        address=kwargs.get('address', '')
    )

    return user
