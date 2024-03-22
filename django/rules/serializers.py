"""
The serializer for the rules
This contains the fields that we'll return back on api calls
"""
from rest_framework import serializers

from rules.models import Rules

class RuleSerializer(serializers.HyperlinkedModelSerializer):
    """
    The Rule Serializer itself
    """

    class Meta:
        """
        The metadata for the serializer
        says to use the Rules model and the fields to return
        """
        model = Rules
        fields = ['id', 'name', 'status', 'growth', 'profit', 'created', 'updated']
        read_only_field = ['growth', 'profit', 'created', 'updated']

    def __init__(self, instance=None, data=serializers.empty, **kwargs):
        """_summary_
        :param instance: _description_, defaults to None
        :type instance: _type_, optional
        :param data: _description_, defaults to serializers.empty
        :type data: _type_, optional
        """
        kwargs['context'] = {'request': kwargs.get('request')}
        super().__init__(instance, data, **kwargs)
