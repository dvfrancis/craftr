from django.contrib import admin
from .models import EventClass, Enrolment


@admin.register(EventClass)
class EventClassAdmin(admin.ModelAdmin):
    list_display = (
        'event_day', 'class_title', 'start_time', 'end_time',
        'difficulty', 'instructor',
    )
    list_filter = ('event_day', 'start_time', 'end_time',
                   'difficulty', 'instructor')
    search_fields = ('event_day', 'class_title', 'start_time', 'end_time',
                     'class_description', 'difficulty', 'instructor', 'instructor_bio')
    ordering = ('event_day', 'class_title', 'start_time', 'end_time',
                'difficulty', 'instructor')


@admin.register(Enrolment)
class EnrolmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'enrolled_class')
    list_filter = ['enrolled_class']
    search_fields = ('user', 'enrolled_class')
    ordering = ['user', 'enrolled_class']
