"""
URL configuration for Transactions
"""
from rest_framework.routers import DefaultRouter
from django.urls import path

from . import views

routes = DefaultRouter()

urlpatterns = [
    path('<int:rule>/', views.ListAPIView.as_view())
]
