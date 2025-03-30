from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm, UserProfileForm


def register_user(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the user
            user = user_form.save()
            profile = user.profile  # Access the profile created by the signal
            profile.location = profile_form.cleaned_data['location']
            profile.experience = profile_form.cleaned_data['experience']
            profile.photograph = profile_form.cleaned_data['photograph']
            profile.save()

            # Log in the user
            login(request, user)
            return redirect("account")
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(
        request,
        "register/register.html",
        {"user_form": user_form, "profile_form": profile_form}
    )
