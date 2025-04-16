from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from details.models import Enrolment
from django.conf import settings


@login_required
def user_details(request):
    """
    Display user account details and enrolments.

    This view retrieves the user's enrolments and displays them along with
    their account details on the account page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered account page with user details and
        enrolments.
    """
    cloud_name = settings.CLOUDINARY_STORAGE['CLOUD_NAME']
    default_profile_url = (
        (
            f"https://res.cloudinary.com/{cloud_name}/image/upload/"
            f"placeholder"
        )
    )
    user_enrolments = Enrolment.objects.filter(
        user=request.user
    ).select_related("enrolled_class").order_by(
        "enrolled_class__event_day__day_date",
        "enrolled_class__start_time"
    )
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
    """
    Log out the user and redirect to the login page.

    This view logs out the user, displays a success message, and redirects
    them to the login page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponseRedirect: A redirect to the login page.
    """
    logout(request)
    messages.success(
            request,
            "You have been logged out successfully"
        )
    return redirect('login')


@login_required
def delete_account(request):
    """
    Delete the user's account and associated enrolments.

    This view handles account deletion. It deletes the user's enrolments
    and their account, displays a success message, and redirects to the
    home page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponseRedirect: A redirect to the home page after deletion.
    """
    if request.method == "POST":
        user = request.user
        Enrolment.objects.filter(user=user).delete()
        user.delete()
        messages.success(
            request,
            "Your account (and any enrolments) have been deleted"
        )
        return redirect("home")
    return redirect("account")
