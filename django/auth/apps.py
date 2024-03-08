"""
Defines the micro app for Django
"""
from django.apps import AppConfig


class AuthConfig(AppConfig):
    """_summary_

    :param AppConfig: _description_
    :type AppConfig: _type_
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth'
