from rest_framework.routers import SimpleRouter
from .views import LoginViewSet, RegistrationViewSet, RefreshViewSet


routes = SimpleRouter()

# AUTHENTICATION
routes.register(r'login', LoginViewSet, basename='auth-login')
routes.register(r'register', RegistrationViewSet, basename='auth-register')
routes.register(r'refresh', RefreshViewSet, basename='auth-refresh')

urlpatterns = [
    *routes.urls
]