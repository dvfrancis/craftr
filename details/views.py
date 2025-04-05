from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Enrolment, EventClass
from .models import EventDay
from django.conf import settings


def diary_page(request):
    days = EventDay.objects.prefetch_related('event_day').all()
    return render(request, "diary/diary.html", {"days": days})


def enrol(request, class_id):
    cloud_name = settings.CLOUDINARY_STORAGE['CLOUD_NAME']

    default_class_image = (
        (
            f"https://res.cloudinary.com/{cloud_name}/image/upload/"
            f"default_class_image"
        )
    )

    default_instructor_image = (
        (
            f"https://res.cloudinary.com/{cloud_name}/image/upload/"
            f"default_instructor_image"
        )
    )

    # Retrieve the specific class using the class_id
    event_class = get_object_or_404(EventClass, id=class_id)

    # Check if the user is enrolled in this class

    if request.user.is_authenticated:
        is_enrolled = Enrolment.objects.filter(user=request.user, enrolled_class=event_class).exists()
    else:
        is_enrolled = False  # Default for non-logged-in users

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "enrol" and not is_enrolled:
            Enrolment.objects.create(user=request.user, enrolled_class=event_class)
            messages.success(request, "You have successfully enrolled for this class")
        elif action == "remove" and is_enrolled:
            Enrolment.objects.filter(user=request.user, enrolled_class=event_class).delete()
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
            "is_enrolled": is_enrolled,  # Pass enrolment status to the template
            "default_class_image": default_class_image,
            "default_instructor_image": default_instructor_image,
        },
    )


@login_required
def remove_enrolment(request, class_id):
    event_class = get_object_or_404(EventClass, id=class_id)
    if request.method == "POST":
        Enrolment.objects.filter(user=request.user, enrolled_class=event_class).delete()
        messages.success(request, "Your enrolment has been withdrawn")
    return redirect("account")  # Redirect to account page instead of details
