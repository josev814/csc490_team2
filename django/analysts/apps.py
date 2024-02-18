"""
Application Configurations
"""
from django.apps import AppConfig


class AnalystsConfig(AppConfig):
    """
    Adds metadata for the application
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analysts'
