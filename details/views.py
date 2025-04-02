from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Enrolment, EventClass
from .models import EventDay


def diary_page(request):
    days = EventDay.objects.prefetch_related('event_day').all()
    return render(request, "diary/diary.html", {"days": days})


@login_required
def enrol(request, class_id):
    # Retrieve the specific class using the class_id
    event_class = get_object_or_404(EventClass, id=class_id)

    # Check if the user is enrolled in this class
    is_enrolled = Enrolment.objects.filter(user=request.user, enrolled_class=event_class).exists()

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "enrol" and not is_enrolled:
            Enrolment.objects.create(user=request.user, enrolled_class=event_class)
            messages.success(request, "You have successfully enrolled in this class!")
        elif action == "remove" and is_enrolled:
            Enrolment.objects.filter(user=request.user, enrolled_class=event_class).delete()
            messages.success(request, "Your enrolment has been removed!")
        else:
            messages.warning(request, "Invalid action or no changes made.")

        # Redirect back to the same page
        return redirect("details", class_id=class_id)

    return render(
        request,
        "details/details.html",
        {
            "event_class": event_class,
            "is_enrolled": is_enrolled,  # Pass enrolment status to the template
        },
    )


@login_required
def remove_enrolment(request, class_id):
    event_class = get_object_or_404(EventClass, id=class_id)
    if request.method == "POST":
        Enrolment.objects.filter(user=request.user, enrolled_class=event_class).delete()
        messages.success(request, "Your enrolment has been removed!")
    return redirect("account")  # Redirect to account page instead of details
