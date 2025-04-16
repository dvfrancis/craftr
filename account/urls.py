"""
URL configuration for the account app.

This module defines the URL patterns for the account-related views, including
user details, logout, and account deletion. It also specifies custom error
handlers for 404 and 500 HTTP errors.

Attributes:
    handler404 (str): Path to the custom 404 error handler view.
    handler500 (str): Path to the custom 500 error handler view.
    urlpatterns (list): List of URL patterns for the account app.
"""

from django.urls import path
from account import views as account
from .views import custom_logout

handler404 = 'craftr.views.custom_404'
handler500 = 'craftr.views.custom_500'

urlpatterns = [
    path("logout/", custom_logout, name="logout"),
    path('', account.user_details, name='account'),
    path("delete_account/", account.delete_account, name="delete_account"),
]
