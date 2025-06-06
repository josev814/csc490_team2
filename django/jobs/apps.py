"""
App that is configuring jobs
"""
from django.apps import AppConfig


class JobsConfig(AppConfig):
    """Naming the app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobs'
