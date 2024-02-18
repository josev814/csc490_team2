"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.views.decorators.cache import cache_page

from . import views
from .management import utils

cache_time = 60 * 5  # time to cache a page for

urlpatterns = [
    path('', views.index, name='index'),
    path('clear_cache', utils.clear_cache),  # clear the cache
    path('ticker/find/<str:search>/', cache_page(cache_time)(views.find_ticker)),
    path('ticker/<str:symbol>/news/', cache_page(cache_time)(views.get_ticker_news)),
    path('ticker/<str:symbol>/', cache_page(cache_time)(views.get_ticker)),
]
