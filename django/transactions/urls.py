"""
URL configuration for Transactions
"""
from rest_framework.routers import DefaultRouter
from django.urls import path

from . import views

routes = DefaultRouter()

urlpatterns = [
    path('rule/<int:rule>/', views.ListRuleTransactionsAPIView.as_view()),
    path('<int:pk>/', views.GetAPIView.as_view())
]
