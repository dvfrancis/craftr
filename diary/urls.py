"""
URL configuration for the diary app.

This module defines the URL patterns for the diary details page and specifies
custom error handlers for 404 and 500 HTTP errors.
"""

from django.urls import path
from diary import views as diary

handler404 = 'craftr.views.custom_404'
handler500 = 'craftr.views.custom_500'

urlpatterns = [
    path('', diary.diary_details, name='diary'),
]
