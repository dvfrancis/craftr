"""
URL configuration for the details app.

This module defines the URL patterns for class enrolment and withdrawal
functionality. It also specifies custom error handlers for 404 and 500 HTTP
errors.
"""

from django.urls import path
from details import views as details

handler404 = 'craftr.views.custom_404'
handler500 = 'craftr.views.custom_500'

urlpatterns = [
    path('<int:class_id>/', details.enrol, name='details'),
    path(
        "remove_enrolment/<int:class_id>/",
        details.remove_enrolment,
        name="remove_enrolment",
    ),
]
