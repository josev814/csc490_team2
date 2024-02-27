"""
The viewsets needed for the Users app
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from users.serializers import UserSerializer
from users.models import Users
import requests
from django.http import JsonResponse


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
    
    def search(self, search_param:str, retrieve:str='quotes', limit=20) -> dict:
        """
        This method allows to search for a string or symbol and return the results
        
        params: retrieve str options are quotes, news, lists
        """
        params = {
            'quotesCount': 0,
            'newsCount': 0,
            'listsCount': 0,
        }

def find_user(request, entry:str):
    print(request)
    uvs = UserViewSet()
    results = uvs.search(entry, 'user')
    return JsonResponse(results)