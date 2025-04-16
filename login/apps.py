from django.apps import AppConfig


class LoginConfig(AppConfig):
    """
    Configuration class for the 'login' app.

    This class defines the default settings for the 'login' app, including
    the app name and the default primary key field type.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'login'
