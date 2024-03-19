"""
Models for the application are stored here
"""
from django.db import models
from users.models import Users

# Create your models here.

class Rules(models.Model):
    """
    model for the rules
    """

    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length=175)
    status = models.BooleanField(default=True)
    growth = models.FloatField(max_length=9, default=0.0)
    profit = models.FloatField(max_length=20, default=0.0)
    create_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    rule = models.JSONField()
