"""
The serializer for stocks
This contains the fields that we'll return back on api calls
"""
from rest_framework import serializers

from stocks.models import Stocks, StockData, StockSearch

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
        fields = '__all__'

    def __init__(self, instance=None, data=serializers.empty, **kwargs):
        """_summary_

        :param instance: _description_, defaults to None
        :type instance: _type_, optional
        :param data: _description_, defaults to serializers.empty
        :type data: _type_, optional
        """
        kwargs['context'] = {'request': kwargs.get('request')}
        super().__init__(instance, data, **kwargs)


class StockSearchSerializer(serializers.ModelSerializer):
    """
    The StockSearch Serializer
    """

    class Meta:
        """
        The metadata for the serializer
        says to use the StockData model and the fields to return
        """
        model = StockSearch
        fields = '__all__'

    def __init__(self, instance=None, data=serializers.empty, **kwargs):
        """_summary_

        :param instance: _description_, defaults to None
        :type instance: _type_, optional
        :param data: _description_, defaults to serializers.empty
        :type data: _type_, optional
        """
        kwargs['context'] = {'request': kwargs.get('request')}
        super().__init__(instance, data, **kwargs)


class StockDataSerializer(serializers.ModelSerializer):
    """
    The StockData Serializer itself
    """

    class Meta:
        """
        The metadata for the serializer
        says to use the StockData model and the fields to return
        """
        model = StockData
        fields = '__all__'

    def __init__(self, instance=None, data=serializers.empty, **kwargs):
        """_summary_

        :param instance: _description_, defaults to None
        :type instance: _type_, optional
        :param data: _description_, defaults to serializers.empty
        :type data: _type_, optional
        """
        kwargs['context'] = {'request': kwargs.get('request')}
        super().__init__(instance, data, **kwargs)
