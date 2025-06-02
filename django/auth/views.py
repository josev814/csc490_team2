"""
Defines the viewsets that will be access for authentication purposes
"""
import json
import logging

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from . import serializers


class LoginViewSet(ModelViewSet, TokenObtainPairView):
    """_summary_

    :param ModelViewSet: _description_
    :type ModelViewSet: _type_
    :param TokenObtainPairView: _description_
    :type TokenObtainPairView: _type_
    :raises InvalidToken: _description_
    :return: _description_
    :rtype: _type_
    """
    serializer_class = serializers.LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """Overrides the default create from the modelViewset

        :param request: _description_
        :type request: _type_
        :raises InvalidToken: _description_
        :return: _description_
        :rtype: _type_
        """
        try:
            json_body = json.loads(request.body.decode(encoding='utf-8'))
        except Exception:
            return Response(
                {'errors': ['Invalid Request']},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=json_body)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as err:
            raise InvalidToken(err.args[0]) from err

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RegistrationViewSet(ModelViewSet, TokenObtainPairView):
    """_summary_

    :param ModelViewSet: _description_
    :type ModelViewSet: _type_
    :param TokenObtainPairView: _description_
    :type TokenObtainPairView: _type_
    :return: _description_
    :rtype: _type_
    """
    serializer_class = serializers.RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']
    request = None
    format_kwarg = None

    def create(self, request, *args, **kwargs):
        """Overrides the create method so we can register a user

        :param request: _description_
        :type request: _type_
        :return: _description_
        :rtype: _type_
        """
        try:
            decoded_body = request.body.decode(encoding='utf-8').strip()
        except Exception:
            return Response(
                {'errors': ['Unable to decode']},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not decoded_body:
            # Handle empty decoded_body
            return Response(
                {'errors': ['Empty request body']},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            json_body = json.loads(decoded_body)
        except Exception:
            return Response(
                {
                    'errors': [
                        'Invalid Request'
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=json_body)

        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            res = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

            return Response(
                {
                    "user": serializer.data,
                    "refresh": res["refresh"],
                    "token": res["access"]
                }, status=status.HTTP_201_CREATED
            )
        except Exception as err:
            print(err)
            return Response(
                    {
                        "errors": [
                            'User already exists'
                        ],
                    }, status=status.HTTP_409_CONFLICT
                )



class RefreshViewSet(ViewSet, TokenRefreshView):
    """Refreshes a users token

    :param ViewSet: _description_
    :type ViewSet: _type_
    :param TokenRefreshView: _description_
    :type TokenRefreshView: _type_
    :raises InvalidToken: _description_
    :return: _description_
    :rtype: _type_
    """
    permission_classes = (AllowAny,)
    http_method_names = ['post']
    request = None
    format_kwarg = None

    def create(self, request, *args, **kwargs):
        """Refreshes the user's token

        :param request: _description_
        :type request: _type_
        :raises InvalidToken: _description_
        :return: _description_
        :rtype: _type_
        """
        logging.info(f'RefreshToken create args: {args}')
        logging.info(f'RefreshToken create kwargs: {kwargs}')
        
        try:
            body = json.loads(request.body.decode(encoding='utf-8'))
        except Exception:
            return Response(
                {'errors': ['Invalid Request']},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=body)
        
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as err:
            raise InvalidToken(err.args[0]) from err

        return Response(
            serializer.validated_data, 
            status=status.HTTP_200_OK
        )
