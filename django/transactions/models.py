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
    def add_transaction(self, ticker, rule_id, action, qty, price, trx_timestamp):
        """Adds a transaction to the database

        :param ticker: 
        :type ticker: ticker
        :param rule_id: 
        :type rule_id: int
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
            'ticker': ticker,
            'rule': rule_id,
            'action': action,
            'quantity': qty,
            'price': price,
            'timestamp': trx_timestamp
        }
        self.create(**record)

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
