from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for the UserProfile model.

    This class customizes the admin interface for the UserProfile model,
    including the fields displayed, filters, search functionality, and
    ordering.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
        list_filter (tuple): Fields to filter by in the admin interface.
        search_fields (tuple): Fields to enable search functionality.
        ordering (list): Default ordering for the admin list view.
    """
    list_display = ('user', 'location', 'experience')
    list_filter = ('user', 'location', 'experience')
    search_fields = ('user__username', 'location', 'experience')
    ordering = ['user__username', 'location', 'experience']
