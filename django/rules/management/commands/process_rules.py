from datetime import datetime
from math import floor
from typing import Any

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from rules.models import Rules, RuleJobs
from stocks.models import StockData
from transactions.models import Transactions
#from users.models import Users
#from django.core.exceptions import ValidationError


class Command(BaseCommand):
    """
    The command that executes when this job is ran
    """
    help = 'Runs the rules against out database'
    START_TIME = datetime.now()

    def handle(self, *args: Any, **options: Any):
        # // Get last runtime
        last_runtime = self.get_last_runtime()
        rules = self.get_rules(last_runtime)
        for rule in rules:
            # only process rule if active and filled in
            if rule.status and rule.rule is not None \
                  and 'conditions' in rule.rule and 'action' in rule.rule \
                  and rule.initial_investment > 0:
                self.perform_action(rule, last_runtime)
                Rules.set_last_runtime(
                    rule_id = rule.id,
                    last_runtime = last_runtime
                )
        # update this jobs last runtime
        self.set_last_runtime(self.START_TIME)
    
    def get_last_runtime(self):
        """
        Get the last time this job ran
        """
        job = RuleJobs.objects.first()
        if job is not None and job.last_ran_timestamp is not None:
            return job.last_ran_timestamp
        return self.START_TIME

    def set_last_runtime(self, last_runtime):
        """
        Set the last time this job ran
        """
        job = RuleJobs()
        job.set_last_runtime(last_runtime)

    def get_rules(self, last_runtime):
        """
        Get all rules that haven't ran OR are gte the current time
        """
        rule_filter = Q(last_ran_timestamp__lte=last_runtime) | Q(last_ran_timestamp=None)
    
        rules = Rules.objects.filter(rule_filter) # add filters here to get rules
    
        return rules

    def run_conditions(self, conditions, last_runtime):
        qs = None
        for condition in conditions:
            if condition['data'] == 'price':
                condition['data'] = 'low'
            if not qs:
                qs = StockData().get_stock_data(
                    ticker_id = condition['symbol']['id'],
                    column = condition['data'],
                    operator = condition['operator'],
                    value = condition['value'],
                    condition = condition['condition'],
                    timestamp=last_runtime
                )
            else:
                qs = StockData().get_stock_data(
                    ticker_id = condition['symbol']['id'],
                    column = condition['data'],
                    opertor = condition['operator'],
                    value = condition['value'],
                    condition = condition['condition'],
                    data=qs
                )
        return qs

    def perform_action(self, rule, last_runtime):
        """
        Run the action portion of the rule to log the transactions
        """
        matched_records = self.run_conditions(rule.rule['conditions'], last_runtime)
        print(matched_records)
        if matched_records is None or matched_records.count == 0:
            return

        action = rule.rule['action']

        number_of_shares = rule.shares
        balance = rule.balance

        profit_loss = 0
        # initial_investment = 0 
        #current_price = (action['quantity'] * action['value'])  
        # sale_income = (action['quantity'] * action['value'])
        # transaction = Transactions.objects.filter(timestamp)

        for matched_record in matched_records:
            if action['method'] == 'buy':
                if balance == 0: # we can't buy anything at this point
                    break
                if action['data'] == 'shares':
                    balance, profit_loss, number_of_shares = self.purchase_by_shares(
                        rule, action, matched_record, balance, profit_loss, number_of_shares
                    )
                elif action['data'] == 'price':
                    # TODO: create the purchase_by_price method and logic
                    # return balance, profit_loss, number_of_shares
                    balance, profit_loss, number_of_shares = self.purchase_by_price(
                        rule, action, matched_record, balance, profit_loss, number_of_shares
                    )
            elif action['method'] == 'sell':
                if number_of_shares < 1:
                    break
                if action['data'] == 'shares':
                    balance, profit_loss, number_of_shares = self.sell_by_shares(
                        rule, action, matched_record, balance, profit_loss, number_of_shares
                    )
                elif action['data'] == 'price':
                    # TODO port to a function of sell_by_price
                    # finish the logic for this and verify it
                    balance, profit_loss, number_of_shares = self.sell_by_price(

                    )
            else:
                self.output_error('Unsupported action: ', action)
        
        growth = ((balance - rule.initial_investment)/rule.initial_investment)*100
        profit_loss = (balance - rule.initial_investment)
        Rules().update_balance(
            rule_id = rule.id,
            shares = number_of_shares,
            balance = balance,
            growth = growth,
            profit = profit_loss
        )
    
    def purchase_by_price(self, rule, action, matched_record, balance, profit_loss, number_of_shares):
        """
        """

        wanted_price = action['qty']
        current_share_price = matched_record['low']
        wanted_shares = int ( wanted_price // current_share_price )

        if balance > wanted_price and wanted_shares > 0: # filling full order
            total_shares_cost = wanted_shares * current_share_price

            Transactions.add_transaction(
                ticker_id = action['symbol']['id'],
                rule_id = rule.id,
                action = action['method'],
                qty = action['qty'],
                price = matched_record['low'],
                trx_timestamp = matched_record['timestamp']
            )
            number_of_shares += wanted_shares
            profit_loss -= total_shares_cost

        elif balance >= current_share_price: # filling partial order
            number_of_affordable_shares = int( wanted_price // current_share_price )
            total_shares_cost =  current_share_price * number_of_affordable_shares

            Transactions.add_transaction(
                ticker_id = action['symbol']['id'],
                rule_id = rule.id,
                action = action['method'],
                qty = number_of_affordable_shares,
                price = matched_record['low'],
                trx_timestamp = matched_record['timestamp']
            )
            profit_loss -= total_shares_cost
            number_of_shares += number_of_affordable_shares

        else:
            self.output_error("Insufficient balance to make the purchase")
        balance += profit_loss
        return [balance, profit_loss, number_of_shares]
    
        
    
    def sell_by_shares(self, rule, action, matched_record, balance, profit_loss, number_of_shares):
        """
        Sells the number of shares we have or qty requested when we have a matched record
        """
        if number_of_shares > action['qty']: # sell what was asked
            profit_loss += action['qty'] * matched_record['low']
            number_of_shares -= action['qty']
            Transactions.add_transaction(
                ticker_id=action['ticker_id'],
                rule_id=rule.id,
                action=action['method'],
                qty=action['qty'],
                price=action['value'],
                trx_timestamp=matched_record['timestamp']
            )
        elif number_of_shares >= 1: # sell our remaining shares
            sellable_shares = int( number_of_shares // 1 )
            profit_loss += sellable_shares * matched_record['low']
            Transactions.add_transaction(
                ticker_id=action['ticker_id'],
                rule_id=rule.id,
                action=action['method'],
                qty=number_of_shares,
                price=action['value'],
                trx_timestamp=matched_record['timestamp']
            )
            number_of_shares -= sellable_shares
        else:
            self.output_error("Insufficient quantity to make the sale")
        balance += profit_loss
        return [balance, profit_loss, number_of_shares]
    
    def purchase_by_shares(self, rule, action, matched_record, balance, profit_loss, number_of_shares):
        current_share_price = matched_record['low']
        total_shares_cost = action['qty'] * current_share_price
        if balance >= total_shares_cost: # make full purchase
            profit_loss -= total_shares_cost
            # balance -= sale_income
            number_of_shares += action['qty']
            
            Transactions.add_transaction(
                ticker_id = action['ticker_id'],
                rule_id = rule.id,
                action = action['method'],
                qty = action['qty'],
                price = matched_record['low'],
                trx_timestamp = matched_record['timestamp']
            )
        elif balance >= current_share_price: # buy what we can
            number_of_affordable_shares = int( current_share_price // balance )
            total_shares_cost =  current_share_price * number_of_affordable_shares
            profit_loss -= total_shares_cost
            # balance -= sale_income
            number_of_shares += number_of_affordable_shares
            
            Transactions.add_transaction(
                ticker_id = action['ticker_id'],
                rule_id = rule.id,
                action = action['method'],
                qty = number_of_affordable_shares,
                price = matched_record['low'],
                trx_timestamp = matched_record['timestamp']
            )
        else:
            self.output_error("Insufficient balance to make the purchase")
        return [balance, profit_loss, number_of_shares]

    def sell_by_price(self, rule, action, matched_record, balance, profit_loss, number_of_shares):
        """
        
        """
        wanted_price = action['qty']
        sellable_shares = int (wanted_price // matched_record['low']) # gets the floor whole number of sellable_shares 

        if number_of_shares > 0 and sellable_shares > 0: # has to have at least 1 share
            
            if sellable_shares > number_of_shares: # ERROR, trying to sell more shares than you own
                sellable_shares = number_of_shares # sets sellable_shares = number_of_shares so you can not oversell
            
            Transactions.add_transaction(
                ticker_id=action['ticker_id'],
                rule_id=rule.id,
                action=action['method'],
                qty=action['qty'],
                price=action['value'],
                trx_timestamp=matched_record['timestamp']
            )
            number_of_shares -= sellable_shares # sells shares
            profit_loss += (sellable_shares * matched_record['low']) # adds the profit_loss

        elif number_of_shares > 0:
            self.output_error("Insufficient quantity to make the sale")
        else:
            self.output_error("Not enough shares to sell at the price specified")
        balance += profit_loss
        return [balance, profit_loss, number_of_shares]


        # if balance > action['qty']:
        #     floor(action['qty']/matched_record['low'])
        #     income += action['qty'] * matched_record['low']
        #     balance += sale_income
        #     number_of_shares -= action['qty']

        #     Transactions.add_transaction(
        #         ticker_id=action['ticker_id'],
        #         rule_id='rule',
        #         action=action['action'['method']],
        #         qty=action['action'['qty']],
        #         price=action['condition'['value']],
        #         trx_timestamp=row.timestamp
        #     )

    def output_error(self, error_msg) -> None:
        """Outputs an error message

        :param error_msg: the error message to output
        :type error_msg: str
        """
        self.stdout.write(
            self.style.ERROR(
                error_msg
            )
        )
    
    def output_success(self, success_msg) -> None:
        """Outputs a success message

        :param success_msg: the message to output
        :type success_msg: str
        """
        self.stdout.write(
            self.style.SUCCESS(
                success_msg
            )
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
    