from django.apps import AppConfig


class AccountConfig(AppConfig):
    """
    Configuration class for the 'account' app.

    This class defines the default settings for the 'account' app, including
    the app name and the default primary key field type.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'
