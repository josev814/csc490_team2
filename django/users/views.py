"""
The viewsets needed for the Users app
"""
import json
import datetime
import logging
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, status
# from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework import filters
# from rest_framework.decorators import api_view
from rest_framework.decorators import action
from rest_framework.response import Response
# from rest_framework import renderers
# from rest_framework.renderers import JSONRenderer



from users.serializers import UserSerializer
from users.models import Users
# from django.utils import timezone


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
        """
        Returns all objects from the database

        :return: _description_
        :rtype: _type_
        """
        if self.request.user.is_superuser:
            return Users.objects.all()
        return Users.objects.none()

    def get_object(self):
        """
        Retrieves a data object from the database
        """
        column_name = self.lookup_field
        object_filter = {column_name: self.kwargs[column_name]}
        try:
            result = Users.objects.filter(**object_filter).get()
        except ObjectDoesNotExist:
            result = None
        return result
    
    def search(self, search_value:str, search_column:str='email', limit=20) -> dict:
        """
        This method allows to search for a string or symbol and return the results
        
        params: 
        """
        self.lookup_field = search_column
        self.kwargs[search_column] = search_value
        logging.info(f'object limit set to {limit}')
        return self.get_object()

    def find_user(self, request):
        """
        Searches for a user based on the email
        """
        json_body = json.loads(request.content.decode('utf-8'))
        if 'email' not in json_body:
            return Response(
                {'errors': ['Missing required parameter']},
                status=400
            )
        uvs = UserViewSet()
        results = uvs.search(json_body['email'])
        return Response(results)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login_user(self, request):
        """
        Logs in the user
        """
        json_body = json.loads(request.body.decode('utf-8'))
        if 'email' not in json_body or 'password' not in json_body:
            return Response(
                {'errors': ['Missing required parameter']},
                status=status.HTTP_400_BAD_REQUEST
            )
        user_obj = self.search(json_body['email'])
        posted_pass = json_body['password']
        if user_obj is None \
                or not user_obj.check_password(posted_pass) \
                or not user_obj.is_active:
            return Response(
                {'errors': ['Invalid Credentials']},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user_obj = Users.objects.filter(**{'email':json_body['email']})[0]
        user_obj.last_login = datetime.datetime.now()
        user_obj.save()

        # user_obj.last_login = timezone.now()
        # user_obj.save() 
        
        return Response({
            'email': user_obj.email,
            'is_active': user_obj.is_active,
            'last_login': user_obj.last_login
        }, status=status.HTTP_200_OK)
