"""
The serializer for stocks
This contains the fields that we'll return back on api calls
"""
from rest_framework import serializers

from stocks.models import Stocks

class StockSerializer(serializers.HyperlinkedModelSerializer):
    """
    The Stock Serializer itself
    """

    class Meta:
        """
        The metadata for the serializer
        says to use the Stocks model and the fields to return
        """
        model = Stocks
        fields = ['id', 'ticker', 'name', 'create_date', 'updated_date']
