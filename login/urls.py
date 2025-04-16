"""
URL configuration for the login app.

This module defines the URL patterns for the login functionality and specifies
custom error handlers for 404 and 500 HTTP errors.
"""

from django.urls import path
from .views import CustomLoginView

handler404 = 'craftr.views.custom_404'
handler500 = 'craftr.views.custom_500'

urlpatterns = [
    path(
        "",
        CustomLoginView.as_view(template_name="login/login.html"),
        name="login",
    ),
]
