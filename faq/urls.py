"""
URL configuration for the FAQ app.

This module defines the URL patterns for the FAQ page.
"""

from django.urls import path
from faq import views as faq

urlpatterns = [
    path('', faq.faq_page, name='faq'),
]
