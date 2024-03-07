import json

from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from . import serializers


class LoginViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = serializers.LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        try:
            jsonBody = json.loads(request.body.decode(encoding='utf-8'))
        except Exception:
            return Response(
                {'errors': ['Invalid Request']},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=jsonBody)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RegistrationViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = serializers.RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']
    request = None
    format_kwarg = None

    def create(self, request, *args, **kwargs):
        try:
            decoded_body = request.body.decode(encoding='utf-8').strip()
        except Exception as err_msg:
            return Response(
                {'errors': ['Unable to decode', err_msg]},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not decoded_body:
            # Handle empty decoded_body
            return Response(
                {'errors': ['Empty request body']},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            jsonBody = json.loads(decoded_body)
        except Exception as err_msg:
            return Response(
                {
                    'errors': [
                        'Invalid Request',
                        err_msg,
                        decoded_body
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=jsonBody)

        serializer.is_valid(raise_exception=True)
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


class RefreshViewSet(ViewSet, TokenRefreshView):
    permission_classes = (AllowAny,)
    http_method_names = ['post']
    request = None
    format_kwarg = None

    def create(self, request, *args, **kwargs):
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
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(
            serializer.validated_data, 
            status=status.HTTP_200_OK
        )
