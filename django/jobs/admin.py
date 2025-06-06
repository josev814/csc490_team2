"""
Adding to the django admin panel as Jobs so we can utilize that to view content
"""
from django.contrib import admin

from .models import Jobs

admin.site.register(Jobs)
