"""
The serializer for the user
This contains the fields that we'll return back on api calls
"""
from rest_framework import serializers

from users.models import Users

class UserSerializer(serializers.ModelSerializer):
    """
    The User Serializer itself
    """

    class Meta:
        """
        The metadata for the serializer
        says to use the Users model and the fields to return
        """
        model = Users
        fields = ['id', 'email', 'token', 'is_active', 'created', 'updated']
        read_only_field = ['token', 'is_active', 'created', 'updated']
