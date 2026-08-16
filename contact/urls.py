"""
URL configuration for the contact app.

This module defines the URL patterns for the contact page.
"""

from django.urls import path
from contact import views as contact

urlpatterns = [
    path('', contact.contact_page, name='contact'),
]
