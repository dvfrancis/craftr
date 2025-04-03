from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm, UserProfileForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def register_user(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = user.profile
            profile.location = profile_form.cleaned_data["location"]
            profile.experience = profile_form.cleaned_data["experience"]
            profile.photograph = profile_form.cleaned_data["photograph"]
            profile.save()

            # Log in user
            login(request, user)

            # Show success message
            messages.success(request, "User created successfully!")

            return redirect("account")

    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(
        request,
        "register/register.html",
        {"user_form": user_form, "profile_form": profile_form}
    )


@login_required
def update_profile(request):
    user = request.user
    profile = request.user.profile  # Get the user's profile

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("account")  # Redirect to the account page

    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(
        request,
        "account/update_profile.html",
        {"user_form": user_form, "profile_form": profile_form}
    )
