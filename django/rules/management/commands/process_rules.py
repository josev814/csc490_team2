from datetime import datetime
from typing import Any

from django.core.management.base import BaseCommand, CommandError
from rules.models import Rules
from stocks.models import StockData
from transactions.models import Transactions
from users.models import Users
from django.core.exceptions import ValidationError

"""
Get Rules
- for rule in rules
  - matched_records = check_rule_conditions(rule['conditions'])
  - if matched_records.count > 0
    - perform_action(rule['action'], matched_records)

- def check_rule_conditions(conditions)
  - for condition in conditions
    - query the stock data for the condition
    return records that match

- def perform_action(action, matched_records)
  - get action method (buy vs sell)
  - in the rules table check how many stocks we have and our rule balance (shares_available and balance should be new column in the rules table)
  - shares_avail = rules['shares_available']
  - bal = rules['balance']
  - income = 0
  - for matched_record in matched_records:
    - if action method == buy
      - documenting only the sell action, the buy action is the reverse
    - else //sell action
      - if action['data'] == 'shares'
        - if shares_available > action['qty']
          - sell action['qty'] shares at matched_record['low'] // this would be the current price at the timestamp
          - income += action['qty'] * matched_record['low']
          - bal += sale_income
          - shares_avail -= action['qty']
          - log transaction in the transactions table
        - elif shares_available > 0 //sell all the stocks we have left
          - sell action['qty'] shares at matched_record['low'] // this would be the current price at the timestamp
          - income += action['qty'] * matched_record['low']
          - bal += sale_income
          - shares_avail -= action['qty']
          - log transaction in the transactions table
        - else
          //no shares available, do not perform the transaction
    - elif action['data'] == 'price'
      - if bal > action['qty']
        - sell floor(action['qty']/matched_record['low']) gives share qty to sell // this would be the current price at the timestamp
        - income += action['qty'] * matched_record['low']
        - bal += sale_income
        - shares_avail -= action['qty']
        - log transaction in the transactions table
      - elif .... pretty much same logic as in the shares actions
    - update rules balance and shares
    - update the rule return by doing adding the initial balance with bal
    - update the rule growth
      - ex:
        - initial investment = 100
        - sale_income = 25
        - growth = (1 - (100/(100 + 25))) * 100
    
We'll need another job under the users app that will sum up the balance, growth and initial investment columns to that will update that information for the user

"""

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
        query = None
        for actions in action:
            if not query:
                query = StockData.get_stock_data(
                    actions['method'],              # for buy or sell
                    actions['quantity'],            # quantity 
                    actions['quantity_type'],       # quantity type
                    actions['ticker_id'],
                    timestamp
                )
            else:
                query = StockData.get_stock_data(
                    actions['method'],
                    actions['quantity'],
                    actions['quantity_type'],
                    actions['ticker_id'],
                    data=query
                )
        # return query

        Transactions.add_transaction()

    def update_balance(self, request, rule, action):
        """
        Update user balance after each transaction
        """
        user = self.request.user.id
        user_obj = Users.objects.filter(user=user)
        transaction = Transactions.objects.filter(user=user)
        balance = user_obj.balance
        number_of_shares = user_obj.number_of_shares
        current_price = (rule['quantity'] * rule['value'])
        

        # Calculate the change in balance based on transactions
        for transaction in action:
            try:
                if transaction.rule[action['method']] == 'buy':
                    if balance < current_price:
                        raise ValidationError("Insufficient balance to make the purchase")
                    balance -= current_price
                    number_of_shares += rule['quantity']
                elif transaction.rule[action['method']] == 'sell':
                    if number_of_shares < rule['quantity']:
                        raise ValidationError("Insufficient quantity to make the sale")
                    balance += current_price
                    number_of_shares -= rule['quantity']
            except ValidationError as e:
                print(e)

        # Update user's balance in the database
        user_obj.balance = balance
        user_obj.save()