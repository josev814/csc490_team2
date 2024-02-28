"""
URL configuration for Stocks
"""
# from django.urls import path
# from django.views.decorators.cache import cache_page

# from . import views
# from .management import utils

# CACHE_TIME = 60 * 5  # time to cache a page for

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('clear_cache', utils.clear_cache),  # clear the cache
#     path('ticker/find/<str:search>/', cache_page(CACHE_TIME)(views.find_ticker)),
#     path('ticker/<str:symbol>/news/', cache_page(CACHE_TIME)(views.get_ticker_news)),
#     path('ticker/<str:symbol>/', cache_page(CACHE_TIME)(views.get_ticker)),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import StockViewSet

routes = DefaultRouter()

routes.register(r'', StockViewSet)

urlpatterns = [
    path('', include(routes.urls))
]