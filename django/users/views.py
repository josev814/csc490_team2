"""
The viewsets needed for the Users app
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from users.serializers import UserSerializer
from users.models import Users


class UserViewSet(viewsets.ModelViewSet):
    """
    The User ViewSet that queries the Users database
    """
    http_method_names = ['get']
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['updated']
    ordering = ['-updated']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Users.objects.all()
        return Users.objects.none()

    def get_object(self):
        lookup_field_value = self.kwargs[self.lookup_field]

        obj = Users.objects.get(lookup_field_value)
        self.check_object_permissions(self.request, obj)

        return obj
