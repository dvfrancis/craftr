from django.shortcuts import render
from diary.models import EventDay
from details.models import EventClass


def diary_details(request):
    """
    Render the diary details page.

    This view fetches and displays a list of event days and their associated
    event classes, sorted by date and time.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered diary details page with event days and
        classes.
    """
    days = EventDay.objects.order_by("day_date")
    classes = EventClass.objects.select_related("event_day") \
        .order_by("event_day__class_date", "start_time")
    return render(
        request,
        "diary/diary.html",
        {"days": days, "classes": classes}
    )
