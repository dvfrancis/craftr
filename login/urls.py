"""
URL configuration for the login app.

This module defines the URL patterns for the login functionality.
"""

from django.urls import path
from .views import CustomLoginView

urlpatterns = [
    path(
        "",
        CustomLoginView.as_view(template_name="login/login.html"),
        name="login",
    ),
]
