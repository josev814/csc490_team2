"""
Models for the application are stored here
"""
#import sys
#import logging
#from datetime import datetime, timedelta

from django.db import models
from stocks.models import Stocks
from rules.models import Rules
#from django.db import IntegrityError

class TransactionsManager(models.Manager):
    """_summary_

    :param models: _description_
    :type models: _type_
    """
    def add_transaction(self, ticker_obj, rule_obj, action, qty, price, trx_timestamp):
        """Adds a transaction to the database

        :param ticker_obj: 
        :type ticker_obj: Stocks object
        :param rule_obj: 
        :type rule_obj: Rules Object
        :param action: Whether we buy or sell a stock
        :type action: str
        :param qty: 
        :type qty: (int|float)
        :param price: The price the transaction occurred at
        :type price: float
        :param trx_timestamp: Time that the transaction took place
        :type trx_timestamp: datetime
        """
        record = {
            'ticker': ticker_obj,
            'rule': rule_obj,
            'action': action,
            'quantity': qty,
            'price': price,
            'timestamp': trx_timestamp
        }
        self.create(**record)
    
    def get_last_transaction(self, rule_id):
        """
        Gets the most recent transaction that was performed by a rule
        """
        return self.filter(rule_id__exact=rule_id).order_by('-pk').first()

class Transactions(models.Model):
    """
    Model for a Transactions table
    """
    ticker = models.ForeignKey(
        Stocks,
        on_delete=models.CASCADE,
    )
    rule = models.ForeignKey(
        Rules,
        on_delete=models.CASCADE,
    )
    action = models.CharField(max_length=25)
    timestamp = models.DateTimeField()
    quantity = models.IntegerField()
    price = models.FloatField(max_length=28)
    total_shares = models.IntegerField()
    balance = models.FloatField(max_length=28)
    initial_investment = models.FloatField(max_length=28)


    objects = TransactionsManager()

    class Meta:
        """
        Adding indexes for table
        """
        indexes = [
            models.Index(
                fields=['rule']
            )
        ]

    def __str__(self):
        """
        Default return of the class

        :return: Returns the ticker, rule, action, quantity, price and timestamp
        :rtype: str
        """
        return f'{self.ticker, self.rule, self.action, self.quantity, self.price, self.timestamp}'
