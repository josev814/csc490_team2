"""
Module used to display models in the admin panel
Can also be used to customize the admin panel
"""
from stocks.models import Stocks
from django.contrib import admin

# Register your models here.
admin.site.register(Stocks)
