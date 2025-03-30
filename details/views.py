from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Enrolment, EventClass
from django.contrib import messages


@login_required
def enrol_in_class(request, class_id):
    event_class = get_object_or_404(EventClass, id=class_id)

    # Check if the user is already enrolled
    existing_enrolment = Enrolment.objects.filter(
        user=request.user, enrolled_class=event_class
    ).exists()

    if not existing_enrolment:
        # Create a new enrolment
        Enrolment.objects.create(user=request.user, enrolled_class=event_class)
        messages.success(
            request, "You have successfully enrolled in the class!"
        )
    else:
        messages.info(request, "You are already enrolled for this class")

    return redirect("diary")
