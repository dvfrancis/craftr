"""
URL configuration for the home app.

This module defines the URL patterns for the home page and specifies
custom error handlers for 404 and 500 HTTP errors.
"""

from django.urls import path
from home import views as home

handler404 = 'craftr.views.custom_404'
handler500 = 'craftr.views.custom_500'

urlpatterns = [
    path('', home.home_page, name='home'),
]
