from django.apps import AppConfig


class HomeConfig(AppConfig):
    """
    Configuration class for the 'home' app.

    This class defines the default settings for the 'home' app, including
    the app name and the default primary key field type.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
