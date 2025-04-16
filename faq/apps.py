"""
Configuration class for the 'faq' app.

This class defines the default settings for the 'faq' app, including
the app name and the default primary key field type.
"""

from django.apps import AppConfig


class FaqConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'faq'
