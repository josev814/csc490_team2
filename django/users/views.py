"""
The viewsets needed for the Users app
"""
import json
import requests

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.decorators import api_view, action

from users.serializers import UserSerializer
from users.models import Users
from django.http import JsonResponse


class UserViewSet(viewsets.ModelViewSet):
    """
    The User ViewSet that queries the Users database
    """
    kwargs = {}
    http_method_names = ['get', 'post']
    queryset = Users.objects.all().order_by('-email')
    serializer_class = UserSerializer
    # permission_classes = (IsAuthenticated,)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['updated']
    ordering = ['-updated']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Users.objects.all()
        return Users.objects.none()

    def get_object(self):
        queryset = super().get_queryset()
        # Perform your filtering here based on a specific column
        column_name = self.lookup_field
        queryset = queryset.filter(column_name=self.kwargs[self.lookup_field])
        return queryset

    # def get_object(self):
    #     lookup_field_value = self.kwargs[self.lookup_field]

    #     obj = Users.objects.get(lookup_field_value)
    #     self.check_object_permissions(self.request, obj)

    #     return 
    
    def search(self, search_value:str, search_column:str='email', limit=20) -> dict:
        """
        This method allows to search for a string or symbol and return the results
        
        params: 
        """
        self.lookup_field = search_column
        self.kwargs[search_column] = search_value
        return self.get_object()

    def find_user(self, request):
        print(request)
        jsonBody = json.loads(request.content.decode('utf-8'))
        if 'email' not in jsonBody:
            return JsonResponse(
                {'errors': ['Missing required parameter']},
                status_code=400
            )
        uvs = UserViewSet()
        results = uvs.search(jsonBody['email'])
        return JsonResponse(results)

    @action(detail=False, methods=['post'])
    def login_user(self, request):
        print(request.body)
        jsonBody = json.loads(request.body.decode('utf-8'))
        if 'email' not in jsonBody or 'password' not in jsonBody:
            return JsonResponse(
                {'errors': ['Missing required parameter']},
                status_code=400
            )
        user_obj = self.search(jsonBody['email'])
        if not user_obj.check_password(jsonBody['password']):
            return JsonResponse(
                {'errors': ['Invalid Credentials']},
                status_code=401
            )
        return JsonResponse({
            'access_token': user_obj.access_token,
            'refresh_token': user_obj.refresh_token
        }, status_code = 200)
