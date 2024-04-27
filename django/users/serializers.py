"""
The serializer for the user
This contains the fields that we'll return back on api calls
"""
from rest_framework import serializers
from django.db.models import Sum

from users.models import Users
from rules.models import Rules

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


class UserProfitSerializer(serializers.ModelSerializer):
    """
    Serializer for User model with profit sum from rules
    """

    total_profit = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    def to_representation(self, instance):
        """
        Set the way the data should be returned for the profit
        """
        total_profit = instance['total_profit']
        return {'total_profit': total_profit}

    def get_total_profit(self, user):
        """
        Calculate the total profit for the given user
        """
        total_profit = Rules.objects.filter(user=user).aggregate(total_profit=Sum('profit'))['total_profit']
        return total_profit if total_profit is not None else float('0.00')
