from django.apps import AppConfig


class ContactConfig(AppConfig):
    """
    Configuration class for the 'contact' app.

    This class defines the default settings for the 'contact' app, including
    the app name and the default primary key field type.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contact'
