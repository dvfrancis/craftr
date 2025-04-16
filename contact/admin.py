from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Contact model.

    This class customizes the admin interface for the Contact model,
    including the fields displayed, filters, search functionality, and
    ordering.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
        list_filter (tuple): Fields to filter by in the admin interface.
        search_fields (tuple): Fields to enable search functionality.
        ordering (list): Default ordering for the admin list view.
    """
    list_display = ('message', 'first_name', 'last_name', 'email')
    list_filter = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email', 'message')
    ordering = ['first_name', 'last_name', 'email']
