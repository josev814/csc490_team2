"""
URL configuration for Transactions
"""
from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import TransactionViewSet

routes = DefaultRouter()

routes.register(r'', TransactionViewSet)

urlpatterns = [
    path('', include(routes.urls))
]
