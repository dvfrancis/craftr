from django.apps import AppConfig


class RegisterConfig(AppConfig):
    """
    Configuration class for the 'register' app.

    This class defines the default settings for the 'register' app, including
    the app name and the default primary key field type.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'register'
