from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'experience', 'photograph')
    list_filter = ('user', 'location', 'experience')
    search_fields = ('user__username', 'location', 'experience')
    ordering = ('user__username', 'location', 'experience')
