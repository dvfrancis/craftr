"""
URL configuration for the account app.

This module defines the URL patterns for the account-related views, including
user details, logout, and account deletion.

Attributes:
    urlpatterns (list): List of URL patterns for the account app.
"""

from django.urls import path
from account import views as account
from .views import custom_logout

urlpatterns = [
    path("logout/", custom_logout, name="logout"),
    path('', account.user_details, name='account'),
    path("delete_account/", account.delete_account, name="delete_account"),
]
