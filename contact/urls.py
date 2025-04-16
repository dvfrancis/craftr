"""
URL configuration for the contact app.

This module defines the URL patterns for the contact page and specifies
custom error handlers for 404 and 500 HTTP errors.
"""

from django.urls import path
from contact import views as contact

handler404 = 'craftr.views.custom_404'
handler500 = 'craftr.views.custom_500'

urlpatterns = [
    path('', contact.contact_page, name='contact'),
]
