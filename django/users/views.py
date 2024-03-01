"""
The viewsets needed for the Users app
"""
import json
import requests

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from users.serializers import UserSerializer
from users.models import Users


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
    ordering_fields = ['updated','email']
    ordering = ['-updated', '-email']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Users.objects.all()
        return Users.objects.none()

    def get_object(self):
        # Perform your filtering here based on a specific column
        column_name = self.lookup_field
        object_filter = {column_name: self.kwargs[column_name]}
        obj = Users.objects.filter(**object_filter).get()
        return obj

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
        jsonBody = json.loads(request.content.decode('utf-8'))
        if 'email' not in jsonBody:
            return Response(
                {'errors': ['Missing required parameter']},
                status=400
            )
        uvs = UserViewSet()
        results = uvs.search(jsonBody['email'])
        return Response(results)

    @action(detail=False, methods=['post'])
    def login_user(self, request):
        jsonBody = json.loads(request.body.decode('utf-8'))
        if 'email' not in jsonBody or 'password' not in jsonBody:
            return Response(
                {'errors': ['Missing required parameter']},
                status=status.HTTP_400_BAD_REQUEST
            )
        user_obj = self.search(jsonBody['email'])
        if not user_obj.check_password(jsonBody['password']) or not user_obj.is_active:
            return Response(
                {'errors': ['Invalid Credentials']},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response({
            'email': user_obj.email,
            'is_active': user_obj.is_active,
            'last_login': user_obj.last_login
        }, status=status.HTTP_200_OK)
