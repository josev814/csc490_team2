"""
The serializer for the rules
This contains the fields that we'll return back on api calls
"""
from rest_framework import serializers
from .models import Rules

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
        
        fields = [
            'user','id', 'name', 
            'initial_investment', 'balance',
            'status', 'growth', 'profit', 
            'create_date', 'updated_date', 'start_date',
            'rule'
        ]
        read_only_fields = ['growth', 'profit', 'create_date', 'updated_date']

    def create(self, validated_data):
        """
        Makes the call to the Rules model to save the data
        """
        rule = Rules.objects.create(**validated_data)
        return rule
