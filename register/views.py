from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm, UserProfileForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def register_user(request):
    """
    Handles user registration

    This view handles the registration of a new user, including creating
    a user account and associated profile. If the registration is successful,
    the user is logged in and redirected to the specified 'next' URL or the
    account page by default.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the registration page or redirects after
        successful registration.
    """
    next_url = (
        request.POST.get("next") or
        request.GET.get("next") or
        "account"  # Capture 'next' URL
    )

    user_form = UserRegistrationForm()
    profile_form = UserProfileForm()

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
            messages.success(request, "Account created, and logged in")

            # Log in user after successful registration
            login(request, user)

            # Redirect to the original page (class details)
            # or account page, if missing
            return redirect(next_url)
        else:
            # Show validation errors when passwords don't match or are missing
            if user_form.errors:
                messages.error(
                    request,
                    (
                        "The passwords do not match, or have not been entered."
                        " Please enter them again."
                    ))

    return render(
        request,
        "register/register.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "next": next_url,
        },
    )


@login_required
def update_profile(request):
    user = request.user
    profile = request.user.profile  # Get the user's profile

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated")
            return redirect("account")  # Redirect to the account page

    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(
        request,
        "account/update_profile.html",
        {"user_form": user_form, "profile_form": profile_form}
    )
