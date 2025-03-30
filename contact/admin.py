from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('message', 'first_name', 'last_name', 'email')
    list_filter = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email', 'message')
    ordering = ['first_name', 'last_name', 'email']
