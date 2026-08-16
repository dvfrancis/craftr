"""
URL configuration for the home app.

This module defines the URL patterns for the home page.
"""

from django.urls import path
from home import views as home

urlpatterns = [
    path('', home.home_page, name='home'),
]
