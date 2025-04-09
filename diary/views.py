from django.shortcuts import render
from diary.models import EventDay
from details.models import EventClass


def diary_details(request):
    # Fetch EventDay objects sorted by date
    days = EventDay.objects.order_by("class_date")

    # Fetch EventClass objects, ensuring sorting by event day first,
    # then start time
    classes = EventClass.objects.select_related("event_day") \
        .order_by("event_day__class_date", "start_time")

    return render(
        request,
        "diary/diary.html",
        {"days": days, "classes": classes}
    )
