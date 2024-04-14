"""
Models for the application are stored here
"""
from django.db import models
from django.conf import settings
from users.models import Users
from stocks.models import Stocks
from django.core.exceptions import ObjectDoesNotExist

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
            qs.filter(models.Q(name__icontains=name))
        if status and status in [0|1]:
            qs.filter(models.Q(status=status))
        return qs

class RuleManager(models.Manager):
    """
    Overriding some of the default manager
    """
    def get_queryset(self, *args,**kwargs):
        """
        returns a query set for the model
        """
        print(args)
        print(kwargs)
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
    create_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
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

class RulesPayment(models.Model, Rules):
    """
    Model for a table that has any field related to a user's payment (balance, number of shares, initial_investment, etc)
    """
    ticker = models.ForeignKey(
        Stocks,
        on_delete=models.CASCADE,
    )
    ticker_id = ticker

    # rule = models.ForeignKey(
    #     Rules,
    #     on_delete=models.CASCADE,
    # )
    # rule_id = rule

    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
    )
    user_id = user

    action = models.CharField(max_length=25)
    quantity = models.IntegerField()
    price = models.FloatField(max_length=28)
    number_of_shares = models.IntegerField(max_length=28)
    balance = models.FloatField(max_length=28)
    timestamp = models.DateTimeField()

    def get_object(self):
        """
        Retrieves a data object from the database
        """
        column_name = self.lookup_field
        object_filter = {column_name: self.kwargs[column_name]}
        try:
            result = Users.objects.filter(**object_filter).get()
        except ObjectDoesNotExist:
            result = None
        return result
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

        :return: Returns the    ticker_id, user_id, number_of_shares,
                                growth, profit, initial_investment, 
                                timestamp
        :rtype: str
        """
        return f'{self.ticker_id, self.user_id, self.number_of_shares, self.growth, self.profit, self.initial_investment, self.timestamp}'

    def update_balance(self, ticker_id, user_id, number_of_shares, balance, growth, profit, initial_investment, trx_timestamp):
        
        record = {
            'ticker': ticker_id,
            'user': user_id,
            'number_of_shares': number_of_shares,
            'balance': balance,
            'growth': growth,
            'profit': profit,
            'initial_investment': initial_investment,
            'timestamp': trx_timestamp
        }
        self.objects.create(**record)
