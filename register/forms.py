from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegistrationForm(UserCreationForm):
    """
    A form for registering new users.

    Extends the default Django UserCreationForm to include an email field
    as a required field.

    Attributes:
        email (EmailField): A required email field.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={"placeholder": "Enter your username"}
            ),
            "first_name": forms.TextInput(
                attrs={"placeholder": "Enter your first name"}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": "Enter your last name"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Enter your email address"}
            ),
            "password1": forms.PasswordInput(
                attrs={"placeholder": "Enter your password"}
            ),
            "password2": forms.PasswordInput(
                attrs={"placeholder": "Confirm your password"}
            ),
        }


class UserUpdateForm(forms.ModelForm):
    """
    A form for updating user account details.

    Allows users to update their first name, last name, and email address.
    """
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class UserProfileForm(forms.ModelForm):
    """
    A form for updating user profile details.

    Allows users to update their location, experience level, and profile
    photograph.
    """
    class Meta:
        model = UserProfile
        fields = ["location", "experience", "photograph"]
        widgets = {
            "location": forms.TextInput(
                attrs={"placeholder": "Enter your location"}
            ),
        }
