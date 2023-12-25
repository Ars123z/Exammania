from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['city', 'state', 'country', 'standard', 'phone_no']  # List the fields you want to include in the form

    # You can add additional customization here, such as widgets, labels, or validators
