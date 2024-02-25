from users.models import Users
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['id', 'email', 'token', 'is_active', 'created', 'updated']
        read_only_field = ['token', 'is_active', 'created', 'updated']