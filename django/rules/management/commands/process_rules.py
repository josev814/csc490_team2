from datetime import datetime
from typing import Any

from django.core.management.base import BaseCommand, CommandError
from rules.models import Rules
from stocks.models import StockData
from transactions.models import Transactions

class Command(BaseCommand):
    """
    The command that executes when this job is ran
    """
    help = 'Runs the rules against out database'
    CUR_TIME = datetime.now()

    def handle(self, *args: Any, **options: Any):
        rules = self.get_rules()
        for rule in rules:
            self.parse_rule(rule)

    def get_rules(self):
        """
        Get all rules that haven't ran OR are gte the current time
        """
        rules = Rules.objects.filter(**{last_ran__gte: self.CUR_TIME}) # add filters here to get rules
        return rules

    def run_conditions(self, conditions):
        qs = None
        for condition in conditions:
            if not qs:
                qs = StockData.get_stock_data(
                    condition['ticker_id'],
                    condition['column_name'],
                    condition['operator'],
                    condition['value'],
                    timestamp
                )
            else:
                qs = StockData.get_stock_data(
                    condition['ticker_id'],
                    condition['column_name'],
                    condition['operator'],
                    condition['value'],
                    data=qs
                )
        return qs

    def perform_action(self, action):
        """
        Run the action portion of the rule to log the transactions
        """
        # Transactions.add_transaction()

    def parse_rule(self, rule, timestamp):
        """parsing through the rule logic

        :param rule: 
        :type rule: 
        """
        symbol = rule['ticker']

        # if symbol price > value then perform action
        if rule['condition'] == 'if':
            if symbol[rule['price']] > rule['value']:
                perform(rule['action'])
            
            #continues with condition == 'and' and greater than
            if rule['condition'] == 'and':
                if symbol[rule['price']] > rule['value']:
                    perform(rule['action'])

            #continues with condition == 'and' and less than
            if rule['condition'] == 'and':
                if symbol[rule['price']] < rule['value']:
                    perform(rule['action'])


        # if symbol price < value then perform action
        if rule['condition'] == 'if':
            if symbol[rule['price']] < rule['value']:
                perform(rule['action'])
            
            #continues with condition == 'and' and greater than
            if rule['condition'] == 'and':
                if symbol[rule['price']] > rule['value']:
                    perform(rule['action'])

            #continues with condition == 'and' and less than
            if rule['condition'] == 'and':
                if symbol[rule['price']] < rule['value']:
                    perform(rule['action'])


    def calculate_rule(self, rule, checkout):
        """function to calculate the action of the rule

        :param rule: _description_
        :type rule: _type_
        :param checkout: _description_
        :type checkout: _type_
        """
        # if method == buy then "amount" needs to go UP by quantity
        if rule['method'] == 'buy':
            amount += rule['quantity']
            
        
        # if method == sell then "amount" needs to go DOWN by quantity
        # this would always sell the available amount of "quantity",
            # but raises an error when "amount" goes below 0 (into the negatives)
        if rule['method'] == 'sell':
            try:
                amount -= rule['quantity']
                if amount < 0:
                    raise ValueError("Selling quantity exceeds available amount.")
            except ValueError as e:
                print(e)
                return 0
