"""
Module used to display models in the admin panel
Can also be used to customize the admin panel
"""
from django.contrib import admin
from users.models import Users

# Register your models here.

admin.site.register(Users)
