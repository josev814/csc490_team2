"""
Application Configurations
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Adds metadata for the Users app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
