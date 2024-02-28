"""
The routes needed for the users endpoints
"""
from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import UserViewSet

routes = DefaultRouter()

# USER
routes.register(r'', UserViewSet)


urlpatterns = [
    path('', include(routes.urls))
]
