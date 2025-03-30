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
            # Create the associated profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # Log in the user
            login(request, user)
            # Replace "home" with your desired redirect
            return redirect("account/account.html")
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(
        request,
        "register/register.html",
        {"user_form": user_form, "profile_form": profile_form}
    )
