"""
URL configuration for the register app

This module defines the URL patterns for the user registration and profile
update views. It also specifies custom error handlers for 404 and 500 HTTP
errors.
"""
from django.urls import path
from register import views as registration

handler404 = 'craftr.views.custom_404'
handler500 = 'craftr.views.custom_500'

urlpatterns = [
    path('', registration.register_user, name='register'),
    path(
        'update_profile/',
        registration.update_profile,
        name="update_profile",
    ),
]
