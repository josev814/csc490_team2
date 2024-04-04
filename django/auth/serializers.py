"""
Classes that will serialize the data
"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist

from users.serializers import UserSerializer
from users.models import Users


class LoginSerializer(TokenObtainPairSerializer):
    """Serializer for logging in

    :param TokenObtainPairSerializer: _description_
    :type TokenObtainPairSerializer: _type_
    """
    def validate(self, attrs):
        """validates the user and returns their data and a token

        :param attrs: _description_
        :type attrs: _type_
        :return: _description_
        :rtype: _type_
        """
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        user_serial = UserSerializer(self.user)
        data['user'] = user_serial.data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        update_last_login(None, self.user)
        return data

class RegisterSerializer(UserSerializer):
    """The serilaizer for registration

    :param UserSerializer: _description_
    :type UserSerializer: _type_
    :return: _description_
    :rtype: _type_
    """
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)
    email = serializers.EmailField(required=True, max_length=128)

    class Meta:
        """database information for this class
        """
        model = Users
        fields = ['id', 'email', 'password', 'is_active', 'token']
        #, 'created', 'updated']

    def create(self, validated_data):
        """Created the user or returns their data in the db

        :param validated_data: _description_
        :type validated_data: _type_
        :return: _description_
        :rtype: _type_
        """
        try:
            user = Users.objects.filter(**{'email':validated_data['email']})
            if not user.get().check_password(validated_data['password']):
                user = None
            user = user.get()
        except ObjectDoesNotExist:
            user = Users.objects.create_user(**validated_data)
        return user
