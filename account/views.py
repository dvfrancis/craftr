from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from details.models import Enrolment
from django.conf import settings


@login_required
def user_details(request):
    cloud_name = settings.CLOUDINARY_STORAGE['CLOUD_NAME']
    default_profile_url = (
        (
            f"https://res.cloudinary.com/{cloud_name}/image/upload/"
            f"placeholder"
        )
    )
    user_enrolments = Enrolment.objects.filter(
        user=request.user
    ).select_related("enrolled_class").order_by("enrolled_class__event_day__class_date", "enrolled_class__start_time")
    return render(
        request,
        "account/account.html",
        {
            "user": request.user,
            "enrolments": user_enrolments,
            "default_profile_url": default_profile_url,
        }
    )


def custom_logout(request):
    logout(request)
    return redirect('home')


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user

        # Delete associated enrolments
        Enrolment.objects.filter(user=user).delete()

        # Delete the user account
        user.delete()

        messages.success(
            request,
            "Your account and enrolments have been successfully deleted."
        )
        return redirect("home")  # Redirect to the home page after deletion

    return redirect("account")
    # Redirect back to account page for GET requests
