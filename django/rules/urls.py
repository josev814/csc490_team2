"""
The routes needed for the rules endpoints
"""
from rest_framework.routers import DefaultRouter
from django.urls import path

from . import views

routes = DefaultRouter()

# RULES
urlpatterns = [
    path('', views.CreateAPIView.as_view()),
    path('list/', views.ListAPIView.as_view()),
    path('<int:pk>/', views.DetailAPIView.as_view()),
    path('<int:pk>', views.DestroyAPIView.as_view())
]
