from django.contrib import admin
from .models import EventDay


@admin.register(EventDay)
class EventDayAdmin(admin.ModelAdmin):
    list_display = ('class_date', 'event_title')
    list_filter = ('class_date', 'event_title')
    search_fields = ('class_date', 'event_title')
    ordering = ['class_date']
