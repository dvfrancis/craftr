from django.contrib import admin
from .models import EventClass, Enrolment


@admin.register(EventClass)
class EventClassAdmin(admin.ModelAdmin):
    list_display = (
        'event_day', 'class_title', 'start_time', 'end_time',
        'class_description', 'difficulty'
    )
    list_filter = ('difficulty', 'event_day')
    search_fields = ('class_title', 'class_description')
    ordering = ('event_day', 'class_title', 'start_time', 'end_time',
                'difficulty')


@admin.register(Enrolment)
class EnrolmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'enrolled_class')
    list_filter = ['enrolled_class']
    search_fields = ('user', 'enrolled_class')
    ordering = ['user', 'enrolled_class']
