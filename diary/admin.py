from django.contrib import admin
from .models import EventDay


@admin.register(EventDay)
class EventDayAdmin(admin.ModelAdmin):
    """
    Admin configuration for the EventDay model.

    This class customizes the admin interface for the EventDay model,
    including the fields displayed, filters, search functionality, and
    ordering.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
        list_filter (tuple): Fields to filter by in the admin interface.
        search_fields (tuple): Fields to enable search functionality.
        ordering (list): Default ordering for the admin list view.
    """
    list_display = ('day_date', 'day_title')
    list_filter = ('day_date', 'day_title')
    search_fields = ('day_date', 'day_title')
    ordering = ['day_date']
