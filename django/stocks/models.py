"""
Models for the application are stored here
"""
from django.db import models

# Create your models here.
class Stocks(models.Model):
    """
    Model for a Stocks table
    """
    ticker = models.CharField(max_length=12)
    name = models.CharField(max_length=75)
    create_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Adding indexes for the table
        """
        indexes = [
            models.Index(fields=['ticker', 'name'])
        ]

    def __str__(self):
        return str(self.ticker)

class StockData(models.Model):
    """
    Model for the stock data
    """
    ticker = models.ForeignKey(
        'Stocks',
        on_delete=models.CASCADE,
    )
    data = models.JSONField()
