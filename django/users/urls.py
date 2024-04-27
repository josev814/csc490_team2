"""
The routes needed for the users endpoints
"""
from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import UserViewSet, GetUserProfit

routes = DefaultRouter()

# USER
routes.register(r'', UserViewSet)


urlpatterns = [
    path('get_profit_loss/', GetUserProfit.as_view()),
    path('', include(routes.urls)),
]
