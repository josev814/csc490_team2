from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist

from users.serializers import UserSerializer
from users.models import Users


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        user_serial = UserSerializer(self.user)
        data['user'] = user_serial.data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        update_last_login(None, self.user)
        return data

class RegisterSerializer(UserSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)
    email = serializers.EmailField(required=True, write_only=True, max_length=128)

    class Meta:
        model = Users
        fields = ['id', 'email', 'password', 'is_active', 'token']
        #, 'created', 'updated']

    def create(self, validated_data):
        try:
            user = Users.objects.filter(**{'email':validated_data['email']}).get()
        except ObjectDoesNotExist:
            user = Users.objects.create_user(**validated_data)
        return user
