from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Enrolment, EventClass
from django.conf import settings


def enrol(request, class_id):
    """
    Handle enrolment and withdrawal for a specific class.

    This view allows users to enrol in or withdraw from a specific class.
    It also checks the enrolment status and renders the class details page.

    Args:
        request: The HTTP request object.
        class_id (int): The ID of the class to enrol in or withdraw from.

    Returns:
        HttpResponse: The rendered class details page or a redirect after
        processing the enrolment/withdrawal.
    """
    cloud_name = settings.CLOUDINARY_STORAGE["CLOUD_NAME"]
    placeholder = (
        f"https://res.cloudinary.com/{cloud_name}/image/upload/placeholder"
    )
    # Retrieve the specific class using the class_id
    event_class = get_object_or_404(EventClass, id=class_id)
    # Check if the user is enrolled in this class
    if request.user.is_authenticated:
        is_enrolled = Enrolment.objects.filter(
            user=request.user, enrolled_class=event_class
        ).exists()
    else:
        is_enrolled = False  # Default for non-logged-in users
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "enrol" and not is_enrolled:
            Enrolment.objects.create(
                user=request.user, enrolled_class=event_class
            )
            messages.success(
                request, "You have successfully enrolled for this class"
            )
        elif action == "remove" and is_enrolled:
            Enrolment.objects.filter(
                user=request.user, enrolled_class=event_class
            ).delete()
            messages.success(request, "Your enrolment has been withdrawn")
        else:
            messages.warning(request, "Error - unable to process your request")
        # Redirect back to the same page
        return redirect("details", class_id=class_id)

    return render(
        request,
        "details/details.html",
        {
            "event_class": event_class,
            "is_enrolled": is_enrolled,
            "placeholder": placeholder,
        },
    )


@login_required
def remove_enrolment(request, class_id):
    """
    Handle enrolment removal for a specific class.

    This view allows logged-in users to withdraw their enrolment from a class.

    Args:
        request: The HTTP request object.
        class_id (int): The ID of the class to withdraw from.

    Returns:
        HttpResponse: A redirect to the account page after processing the
        withdrawal.
    """
    event_class = get_object_or_404(EventClass, id=class_id)
    if request.method == "POST":
        Enrolment.objects.filter(
            user=request.user, enrolled_class=event_class
        ).delete()
        messages.success(request, "Your enrolment has been withdrawn")
    return redirect("account")  # Redirect to account page instead of details
