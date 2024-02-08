from django.db import models

# Create your models here.
class Stocks(models.Model):
    ticker = models.CharField(max_length=12)
    name = models.CharField(max_length=75)
    create_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['ticker', 'name'])
        ]

    def __str__(self):
        return self.ticker

class Stock_Data(models.Model):
    ticker = models.ForeignKey(
        'Stocks',
        on_delete=models.CASCADE,
    )
    data = models.JSONField()