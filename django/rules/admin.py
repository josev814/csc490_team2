"""Adding the Rules model to the Django Admin Portal"""
from django.contrib import admin

# Register your models here.
from .models import Rules

admin.site.register(Rules)
