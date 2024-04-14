from datetime import datetime
from math import floor
from typing import Any

from django.core.management.base import BaseCommand, CommandError
from rules.models import Rules, RulesPayment
from stocks.models import StockData
from transactions.models import Transactions
from users.models import Users
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    """
    The command that executes when this job is ran
    """
    help = 'Runs the rules against out database'
    CUR_TIME = datetime.now()

    def handle(self, *args: Any, **options: Any):
        rules = self.get_rules()
        for rule in rules:
            self.perform_action(rule)

    def get_rules(self):
        """
        Get all rules that haven't ran OR are gte the current time
        """
        rules = Rules.objects.filter(**{last_ran__gte: self.CUR_TIME}) # add filters here to get rules
    
        for rule in rules:
            matched_records = run_conditions(rule['conditions'])
            if matched_records.count > 0:
                perform_action(rule['action'])
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

    def perform_action(self, action, matched_records):
        """
        Run the action portion of the rule to log the transactions
        """
        cond = self.run_conditions(rule['conditions'])
        if cond is None or cond.count == 0:
            return

        

        number_of_shares = RulesPayment['shares_available']
        balance = RulesPayment['balance']
        income = 0
        initial_investment = 0
        current_price = (action['quantity'] * action['value'])  
        sale_income = (action['quantity'] * action['value'])
        transaction = Transactions.objects.filter(timestamp)

        for matched_records in matched_records:
            if transaction.action['action'['method']] == 'buy':
                if action['data'] == 'shares':
                    if balance > current_price:
                        income -= (action['qty'] * matched_records['low'])
                        balance -= sale_income 
                        number_of_shares += action['qty']
                        
                        Transactions.add_transaction(
                        ticker_id=action['ticker_id'],
                        rule_id='rule',
                        action=action['action'['method']],
                        qty=action['action'['qty']],
                        price=action['condition'['value']],
                        trx_timestamp=row.timestamp
                        )
                else:
                    raise ValidationError("Insufficient balance to make the purchase")
                
            if transaction.action['action'['method']] == 'sell':
                if action['data'] == 'shares':
                    if number_of_shares > action['qty']:
                        income += action['qty'] * matched_records['low']
                        balance += sale_income 
                        number_of_shares -= action['qty']
                        
                        Transactions.add_transaction(
                        ticker_id=action['ticker_id'],
                        rule_id='rule',
                        action=action['action'['method']],
                        qty=action['action'['qty']],
                        price=action['condition'['value']],
                        trx_timestamp=row.timestamp
                        )
                        
                else:
                    raise ValidationError("Insufficient quantity to make the sale")
            
            if action['data'] == 'price':
                if balance > action['qty']:
                    floor(action['qty']/matched_records['low'])
                    income += action['qty'] * matched_records['low']
                    balance += sale_income
                    number_of_shares -= action['qty']

                    Transactions.add_transaction(
                        ticker_id=action['ticker_id'],
                        rule_id='rule',
                        action=action['action'['method']],
                        qty=action['action'['qty']],
                        price=action['condition'['value']],
                        trx_timestamp=row.timestamp
                        )

        growth = ((balance-initial_investment)/initial_investment)*100
        #growth = (1 - (100/(initial_investment + sale_income))) * 100
        RulesPayment.update_balance(
            ticker= ['ticker_id'],
            number_of_shares=  number_of_shares,
            balance= balance,
            growth = growth,
            trx_timestamp= row_timestamp
            )


                        



        # initial_investment = 0
        # transaction = Transactions.objects.filter(timestamp)
        # current_price = (rule['quantity'] * rule['value'])
        # number_of_shares = RulesPayment.object.filter(number_of_shares)

        # query = None
        # for actions in rule['action']:
        #     # get the method
        #     try:
        #         if transaction.rule['action'['method']] == 'buy':

        #     # if buying, check that the user has enough money to buy
        #             if initial_investment < current_price:
        #                 raise ValidationError("Insufficient balance to make the purchase")
                    
        #     # add_transaction for buy
        #             Transactions.add_transaction(
        #                 ticker_id=actions['ticker_id'],
        #                 rule_id='rule',
        #                 action=rule['action'['method']],
        #                 qty=rule['action'['quantity']],
        #                 price=rule['condition'['value']],
        #                 trx_timestamp=row.timestamp
        #             )
        #             RulesPayment.update_balance(
        #                 ticker= ['ticker_id'],
        #                 user= user_id,
        #                 number_of_shares=  number_of_shares,
        #                 balance= (initial_investment - current_price),
        #                 growth= (current_price),
        #                 profit= (current_price - initial_investment),
        #                 initial_investment= initial_investment,
        #                 trx_timestamp= row_timestamp
        #                 )
        #     # if selling, check that the user has enough to sell of the shares
        #         elif transaction.rule['action'['method']] == 'sell':
        #             if number_of_shares < rule['quantity']:
        #                 raise ValidationError("Insufficient quantity to make the sale")

        #         # add_transaction for sell
        #             Transactions.add_transaction(
        #                 ticker_id=actions['ticker_id'],
        #                 rule_id='rule',
        #                 action=rule['action'['method']],
        #                 qty=rule['action'['quantity']],
        #                 price=rule['condition'['value']],
        #                 trx_timestamp=row.timestamp
        #             )

        #     except ValidationError as e:
        #         print(e)
            

        #         # Transactions.add_transaction(
        #         #     ticker_id=actions['ticker_id'],
        #         #     rule_id='rule',
        #         #     action=action['method'],
        #         #     qty=action['quantity'],
        #         #     price=condition['value'],
        #         #     trx_timestamp=row.timestamp
        #         # )

    # def update_balance(self, request, rule, action):
    #     """
    #     Update user balance after each transaction
    #     """
    #     initial_investment = 0
    #     # user = self.request.user.id
    #     # user_obj = Users.objects.filter(user=user)
    #     transaction = Transactions.objects.filter(timestamp)
    #     balance = user_obj.balance
    #     number_of_shares = user_obj.number_of_shares
    #     current_price = (rule['quantity'] * rule['value'])
        

    #     # Calculate the change in balance based on transactions
    #     for transaction in action:
    #         try:
    #             if transaction.rule[action['method']] == 'buy':
    #                 if balance < current_price:
    #                     raise ValidationError("Insufficient balance to make the purchase")
    #                 balance -= current_price
    #                 number_of_shares += rule['quantity']
    #             elif transaction.rule[action['method']] == 'sell':
    #                 if number_of_shares < rule['quantity']:
    #                     raise ValidationError("Insufficient quantity to make the sale")
    #                 balance += current_price
    #                 number_of_shares -= rule['quantity']
    #         except ValidationError as e:
    #             print(e)

    #     # Update user's balance in the database
    