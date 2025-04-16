from django.contrib import admin
from .models import EventClass, Enrolment


@admin.register(EventClass)
class EventClassAdmin(admin.ModelAdmin):
    """
    Admin configuration for the EventClass model.

    This class customizes the admin interface for the EventClass model,
    including the fields displayed, filters, search functionality, and
    ordering.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
        list_filter (tuple): Fields to filter by in the admin interface.
        search_fields (tuple): Fields to enable search functionality.
        ordering (tuple): Default ordering for the admin list view.
    """
    list_display = (
        'event_day', 'class_title', 'start_time', 'end_time',
        'difficulty', 'instructor',
    )
    list_filter = (
        'event_day', 'start_time', 'end_time',
        'difficulty', 'instructor',
    )
    search_fields = (
        'event_day', 'class_title', 'start_time', 'end_time',
        'class_description', 'difficulty', 'instructor', 'instructor_bio')
    ordering = ('event_day', 'class_title', 'start_time', 'end_time',
                'difficulty', 'instructor')


@admin.register(Enrolment)
class EnrolmentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Enrolment model.

    This class customizes the admin interface for the Enrolment model,
    including the fields displayed, filters, search functionality, and
    ordering.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
        list_filter (list): Fields to filter by in the admin interface.
        search_fields (tuple): Fields to enable search functionality.
        ordering (list): Default ordering for the admin list view.
    """
    list_display = ('user', 'enrolled_class')
    list_filter = ['enrolled_class']
    search_fields = ('user', 'enrolled_class')
    ordering = ['user', 'enrolled_class']
