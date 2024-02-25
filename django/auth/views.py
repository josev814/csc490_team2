from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from . import serializers
import json


class LoginViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = serializers.LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.body)

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
            body = json.loads(request.body.decode(encoding='utf-8'))
        except Exception:
            return JsonResponse(
                data={
                    'errors': [
                        'Invalid Request'
                    ]
                }, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=body)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        res = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return JsonResponse(
            data={
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
            return JsonResponse(
                data={
                    'errors': [
                        'Invalid Request'
                    ]
                }, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=body)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return JsonResponse(
            serializer.validated_data, 
            status=status.HTTP_200_OK
        )
