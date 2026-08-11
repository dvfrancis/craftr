from django.shortcuts import render
from diary.models import EventDay


def diary_details(request):
    """
    Render the diary details page.

    This view fetches and displays the list of event days. Each day's classes
    are reached in the template through the event_day reverse accessor, so
    they are not queried separately here.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered diary details page with event days.
    """
    days = EventDay.objects.order_by("day_date")
    return render(request, "diary/diary.html", {"days": days})
