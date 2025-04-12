from django.contrib import admin
from .models import EventDay


@admin.register(EventDay)
class EventDayAdmin(admin.ModelAdmin):
    list_display = ('day_date', 'day_title')
    list_filter = ('day_date', 'day_title')
    search_fields = ('day_date', 'day_title')
    ordering = ['day_date']
