"""
The serializer for the transactions
This contains the fields that we'll return back on api calls
"""
from rest_framework import serializers
from .models import Transactions
from rules.serializers import RuleSerializer

class TransactionSerializer(serializers.ModelSerializer):
    """
    The Transaction Serializer itself
    """
    rule = RuleSerializer()

    class Meta:
        """
        The metadata for the serializer
        says to use the Transactions model and the fields to return
        """
        model = Transactions
        
        fields = [
            'rule','id', 'ticker', 
            'action', 'quantity', 'price', 
            'timestamp', 'total_shares',
            'balance', 'initial_investment',
            'current_profit_loss'
        ]
