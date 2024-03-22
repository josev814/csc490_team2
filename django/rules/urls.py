"""
The routes needed for the rules endpoints
"""
from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import RuleViewSet

routes = DefaultRouter()

# RULES
routes.register(r'', RuleViewSet)


urlpatterns = [
    path('', include(routes.urls))
]
