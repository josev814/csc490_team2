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

    class Meta:
        """
        Adding indexes for table
        """
        indexes = [
            models.Index(
                fields=['rule']
            )
        ]
