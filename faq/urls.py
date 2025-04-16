"""
URL configuration for the FAQ app.

This module defines the URL patterns for the FAQ page and specifies
custom error handlers for 404 and 500 HTTP errors.
"""

from django.urls import path
from faq import views as faq

handler404 = 'craftr.views.custom_404'
handler500 = 'craftr.views.custom_500'

urlpatterns = [
    path('', faq.faq_page, name='faq'),
]
