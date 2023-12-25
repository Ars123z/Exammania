from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import UserProfile

@receiver(user_logged_in)
def initialize_user_profile(sender, request, user, **kwargs):
    # Check if the user has a UserProfile
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        # If UserProfile doesn't exist, create one and initialize with default values
        user_profile = UserProfile(user=user)
        user_profile.save()