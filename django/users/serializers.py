"""
The serializer for the user
This contains the fields that we'll return back on api calls
"""
from rest_framework import serializers

from users.models import Users

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    The User Serializer itself
    """

    class Meta:
        """
        The metadata for the serializer
        says to use the Users model and the fields to return
        """
        model = Users
        fields = ['id', 'email', 'token', 'is_active', 'created', 'updated', 'last_login']
        read_only_field = ['token', 'is_active', 'created', 'updated', 'last_login']

    def __init__(self, instance=None, data=serializers.empty, **kwargs):
        """_summary_
        :param instance: _description_, defaults to None
        :type instance: _type_, optional
        :param data: _description_, defaults to serializers.empty
        :type data: _type_, optional
        """
        kwargs['context'] = {'request': kwargs.get('request')}
        super().__init__(instance, data, **kwargs)
