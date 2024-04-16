"""
Setting required for the app
"""
from django.apps import AppConfig


class RulesConfig(AppConfig):
    """Naming the app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rules'
