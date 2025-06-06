"""
Models for the application are stored here
"""
from django.db import models
from django.conf import settings
from users.models import Users
# from stocks.models import Stocks
# from django.core.exceptions import ObjectDoesNotExist

User = settings.AUTH_USER_MODEL # auth.User

class RuleQuerySet(models.QuerySet):
    """
    Adding the option to do a search
    """
    def search(self, name=None, status=None, user=None):
        """A search method so we can attempt to filter the rules"""
        if user is None: # returning none object
            return self.filter(user=user).none()
        qs = self.filter(user=user)
        if name:
            qs = qs.filter(models.Q(name__icontains=name))
        if status and status in [0|1]:
            qs = qs.filter(models.Q(status=status))
        return qs

class RuleManager(models.Manager):
    """
    Overriding some of the default manager
    """
    def get_queryset(self):
        """
        returns a query set for the model
        """
        return RuleQuerySet(self.model, using=self._db)

    def search(self, user=None, **kwargs):
        """
        Here we search the queryset based on our user
        """
        return self.get_queryset().search(user=user, **kwargs)

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
    shares = models.IntegerField(default=0)
    balance = models.FloatField(max_length=20, default=0.0)
    create_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    start_date = models.DateField(blank=True, null=True)
    last_ran_timestamp = models.DateTimeField(blank=True, null=True)
    initial_investment = models.FloatField(max_length=20, default=0.0)
    rule = models.JSONField()

    objects = RuleManager()

    def get_absolute_url(self):
        """
        Sets the absolute url for a rule based on it's primary key
        """
        return f"/rules/{self.pk}/"

    @property
    def endpoint(self):
        """
        Gets the rules endpoint url
        """
        return self.get_absolute_url()

    @property
    def path(self):
        """
        Sets the absolute url for a rule based on it's primary key
        """
        return f"/rules/{self.pk}/"

    def update_balance(self, shares, balance, growth, profit):
        """
        Update the object's values that we need to update
        Then save the record
        """
        self.shares = shares
        self.balance = balance
        self.growth = growth
        self.profit = profit
        self.save()
    
    def set_last_runtime(self, last_runtime):
        """
        Pull the record with the rule id
        Update the object's last runtime
        Then save the record
        """
        self.last_ran_timestamp = last_runtime
        self.save()
