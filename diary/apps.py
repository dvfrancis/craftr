"""
Configuration class for the 'diary' app.

This class defines the default settings for the 'diary' app, including
the app name and the default primary key field type.
"""

from django.apps import AppConfig


class DiaryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'diary'
