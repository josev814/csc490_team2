"""
Models for the application are stored here
"""
from django.db import models
from users.models import Users
from datetime import datetime

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


    def create_rule(self, name:str, status:int=1):
        """ 
        Use this to create a rule
        """

        if name is None:
            raise TypeError('Each rule must have a name.')
        if status not in (0, 1):
            raise ValueError("Status must be 0 (inactive) or 1 (active).")
        if status != 1:
            raise TypeError('Rule must be active.')
        
        self.create_date = datetime.now()
        self.updated_date = datetime.now()
        
        rule = rule(name=name, status=status, create_date=self.create_date, updated_date=self.updated_date)
        
        # self.name = name
        # self.status = status
        # self.create_date = create_date
        # self.updated_date = updated_date 
        
        rule.save(using=self._db)  # Save the rule to the database
        self.rules[name] = rule

        return rule