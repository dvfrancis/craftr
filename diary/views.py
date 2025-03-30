from django.shortcuts import render
from diary.models import EventDay
from details.models import EventClass


def diary_list(request):
    # Fetch all EventDay objects with related EventClass objects
    days = EventDay.objects.prefetch_related("event_day").all()
    classes = EventClass.objects.all()  # Fetch all EventClass objects

    return render(
        request,
        "diary/diary.html",
        {"days": days, "classes": classes}
    )