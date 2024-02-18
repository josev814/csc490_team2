"""
Application Configurations
"""
from django.apps import AppConfig


class PullstocksConfig(AppConfig):
    """
    Adds metadata for the Stocks app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stocks'
