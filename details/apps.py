"""
Configuration class for the 'details' app.

This class defines the default settings for the 'details' app, including
the app name and the default primary key field type.
"""

from django.apps import AppConfig


class DetailsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'details'
