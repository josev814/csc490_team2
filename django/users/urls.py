"""
The routes needed for the users endpoints
"""
from rest_framework.routers import SimpleRouter

from .views import UserViewSet

routes = SimpleRouter()

# USER
routes.register(r'user', UserViewSet, basename='user')


urlpatterns = [
    *routes.urls
]
