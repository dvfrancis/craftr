"""
URL configuration for the diary app.

This module defines the URL patterns for the diary details page.
"""

from django.urls import path
from diary import views as diary

urlpatterns = [
    path('', diary.diary_details, name='diary'),
]
