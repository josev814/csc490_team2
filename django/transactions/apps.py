"""
Application Configurations
"""
from django.apps import AppConfig


class TransactionsConfig(AppConfig):
    """
    Adds metadata for the app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transactions'
