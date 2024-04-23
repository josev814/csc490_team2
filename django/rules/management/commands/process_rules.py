from datetime import datetime
from math import floor
from typing import Any

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q, Sum, Func, Value, F
from rules.models import Rules, RuleJobs
from stocks.models import StockData, Stocks
from transactions.models import Transactions
#from users.models import Users
#from django.core.exceptions import ValidationError


class Command(BaseCommand):
    """
    The command that executes when this job is ran
    """
    help = 'Runs the rules against out database'
    START_TIME = datetime.now()
    LAST_RUNTIME = None

    def handle(self, *args: Any, **options: Any):
        # // Get last runtime
        self.get_last_runtime()
        rules = self.get_rules()
        for record in rules:
            # only process rule if active and filled in
            if record.rule is not None \
                  and 'conditions' in record.rule and 'action' in record.rule \
                  and record.initial_investment > 0:
                if record.last_ran_timestamp is None:
                    record.balance = record.initial_investment
                    record.save()
                print('Rule: ', record.pk)
                print('Runtime: ', record.last_ran_timestamp)
                print('Rule Info: ', record.rule)
                self.perform_action(record)
                record.set_last_runtime(self.START_TIME)
                print('New Runtime: ', record.last_ran_timestamp)
        # update this jobs last runtime
        self.set_last_runtime()
    
    def get_last_runtime(self):
        """
        Get the last time this job ran
        """
        job = RuleJobs.objects.first()
        if job is not None and job.last_ran_timestamp is not None:
            self.LAST_RUNTIME = job.last_ran_timestamp
        self.LAST_RUNTIME = self.START_TIME

    def set_last_runtime(self):
        """
        Set the last time this job ran base on the start time
        """
        RuleJobs.objects.first().set_last_runtime(
            self.START_TIME
        )

    def get_rules(self):
        """
        Get all rules that haven't ran OR are lte the current time
        Make sure the rule is active
        """
        rule_filter = Q(last_ran_timestamp__lte=self.LAST_RUNTIME) | Q(last_ran_timestamp=None)
        rules = Rules.objects.filter(
            rule_filter
        ).filter(
            status__exact = True
        )
        return rules

    def run_conditions(self, conditions):
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
                    timestamp = self.START_TIME
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

    def perform_action(self, record):
        """
        Run the action portion of the rule to log the transactions
        """

        stock_records = self.run_conditions(record.rule['conditions'])
        print(stock_records.query)
        if stock_records is None or stock_records.count() == 0:
            return
        print('Triggers: ', stock_records.count())

        action = record.rule['action']

        number_of_shares = record.shares
        balance = record.balance

        for stock_record in stock_records:
            if action['method'] == 'buy':
                if balance == 0: # we can't buy anything at this point
                    break
                if action['quantity_type'] == 'shares':
                    balance, number_of_shares = self.purchase_by_shares(
                        record, stock_record, balance, number_of_shares
                    )
                elif action['quantity_type'] == 'price':
                    # TODO: create the purchase_by_price method and logic
                    # return balance, profit_loss, number_of_shares
                    balance, number_of_shares = self.purchase_by_price(
                        record, stock_record, balance, number_of_shares
                    )
            elif action['method'] == 'sell':
                if number_of_shares < 1:
                    break
                if action['quantity_type'] == 'shares':
                    balance, number_of_shares = self.sell_by_shares(
                        record, stock_record, balance, number_of_shares
                    )
                elif action['quantity_type'] == 'price':
                    # TODO port to a function of sell_by_price
                    # finish the logic for this and verify it
                    balance, number_of_shares = self.sell_by_price(
                        
                    )
            else:
                self.output_error('Unsupported action: ', action)
        
        growth = self.get_rule_growth(balance, record)
        profit_loss = 0
        if number_of_shares > 0:
            profit_loss = self.get_profit_loss(record, number_of_shares)
        
        record.update_balance(
            shares = number_of_shares,
            balance = balance,
            growth = growth,
            profit = profit_loss
        )
    
    def get_profit_loss(self, record, number_of_shares):
        symbol_id = record.rule['action']['symbol']['id']
        current_stock_price = self.get_current_stock_price(
            symbol_id
        )
        average_cost = self.get_average_cost_of_stock(
            record.id,
            symbol_id
        )
        print('Current Stock Price: ', current_stock_price)
        print('AVG Cost: ', average_cost)
        print('SHARES: ', number_of_shares)
        total_investment = number_of_shares * average_cost
        current_value = number_of_shares * current_stock_price
        return current_value - total_investment

    def get_average_cost_of_stock(self, rule, ticker):
        trx_data_cost = Transactions.objects.filter(
            rule_id__exact=rule,
            ticker_id__exact=ticker
        ).aggregate(total_cost=Sum('price'))

        trx_data_shares = Transactions.objects.filter(
            rule_id__exact=rule,
            ticker_id__exact=ticker
        ).aggregate(total_shares=Sum('quantity'))
        
        average_cost = trx_data_cost['avg_cost'] // float(trx_data_shares['total_shares'])
        return average_cost

    def get_current_stock_price(self, stock_id):
        return StockData.objects.filter(
            ticker_id__exact=stock_id,
            granularity__exact='1m'
        ).order_by('-pk', ).first().low

    def get_stock_price_from_timestamp(self, stock_id, timestamp):
        qs = StockData.objects.filter(
            ticker_id__exact=stock_id,
            granularity__exact='1m'
        ).annotate(
            timestamp_difference=Func(
                F('timestamp') - Value(timestamp), function='ABS'
            )
        ).order_by('timestamp_difference')
        print(qs.query)
        return qs.first().low
    
    def get_rule_growth(self, balance:float, record:Rules.rule):
        """
        Calculates the growth for the rule

        :param balance: The updated balance of the user
        :type balance: float
        :param record: The record that was processed
        :type record: Rules.rule
        :return: The growth in a float number out of 100
        :rtype: float
        """
        if record.initial_investment == 0:
            return 0
        return (
            (
                balance - record.initial_investment
            ) / record.initial_investment
        ) * 100
    
    def purchase_by_price(self, record, stock_record, balance, number_of_shares):
        """
        """
        action = record.rule['action']

        wanted_price = action['quantity']
        current_share_price = stock_record.low
        wanted_shares = int ( wanted_price // current_share_price )

        if balance > wanted_price and wanted_shares > 0: # filling full order
            total_shares_cost = wanted_shares * current_share_price

            Transactions.objects.add_transaction(
                ticker_id = Stocks.objects.get(id=action['symbol']['id']),
                rule_id = record,
                action = action['method'],
                qty = action['quantity'],
                price = stock_record.low,
                trx_timestamp = stock_record.timestamp
            )
            number_of_shares += wanted_shares
            balance -= total_shares_cost

        elif balance >= current_share_price: # filling partial order
            number_of_affordable_shares = int( wanted_price // current_share_price )
            total_shares_cost =  current_share_price * number_of_affordable_shares

            Transactions.objects.add_transaction(
                ticker_id = Stocks.objects.get(id=action['symbol']['id']),
                rule_id = record.id,
                action = action['method'],
                qty = number_of_affordable_shares,
                price = stock_record.low,
                trx_timestamp = stock_record.timestamp
            )
            number_of_shares += number_of_affordable_shares
            balance -= total_shares_cost
        else:
            self.output_error("Insufficient balance to make the purchase")
        return [balance, number_of_shares]
    
    def sell_by_shares(self, record, stock_record, balance, number_of_shares):
        """
        Sells the number of shares we have or qty requested when we have a matched record
        """
        action = record.rule['action']

        if number_of_shares > action['quantity']: # sell what was asked
            number_of_shares -= action['quantity']
            Transactions.objects.add_transaction(
                ticker_id = Stocks.objects.get(id=action['symbol']['id']),
                rule_id = record.id,
                action = action['method'],
                qty = action['quantity'],
                price = action['value'],
                trx_timestamp = stock_record.timestamp
            )
            balance += (action['quantity'] * stock_record.low)
        elif number_of_shares >= 1: # sell our remaining shares
            sellable_shares = int( number_of_shares // 1 )
            Transactions.objects.add_transaction(
                ticker_id = Stocks.objects.get(id=action['symbol']['id']),
                rule_id = record.id,
                action = action['method'],
                qty = number_of_shares,
                price = action['value'],
                trx_timestamp = stock_record.timestamp
            )
            number_of_shares -= sellable_shares
            balance += (sellable_shares * stock_record.low)
        else:
            self.output_error("Insufficient quantity to make the sale")
        return [balance, number_of_shares]
    
    def purchase_by_shares(self, record, stock_record, balance, number_of_shares):
        action = record.rule['action']
        print(action)
        action_stock = Stocks.objects.get(id=action['symbol']['id'])
        current_share_price = self.get_stock_price_from_timestamp(
            action_stock.pk,
            stock_record.timestamp
        )
        total_shares_cost = float(action['quantity']) * current_share_price
        if balance >= total_shares_cost: # make full purchase
            # balance -= sale_income
            print(action)
            Transactions.objects.add_transaction(
                ticker = action_stock,
                rule_id = record,
                action = action['method'],
                qty = action['quantity'],
                price = current_share_price,
                trx_timestamp = stock_record.timestamp
            )
            number_of_shares += int(action['quantity'])
            balance -= (float(action['quantity']) * current_share_price)
        elif balance >= current_share_price: # buy what we can
            number_of_affordable_shares = int( current_share_price // balance )
            total_shares_cost =  current_share_price * float(number_of_affordable_shares)
            
            Transactions.objects.add_transaction(
                ticker = action_stock,
                rule_id = record.id,
                action = action['method'],
                qty = number_of_affordable_shares,
                price = stock_record.low,
                trx_timestamp = stock_record.timestamp
            )
            number_of_shares += number_of_affordable_shares
            balance -= (float(number_of_affordable_shares) * stock_record.low)
        else:
            self.output_error("Insufficient balance to make the purchase")
        return [balance, number_of_shares]

    def sell_by_price(self, record, stock_record, balance, number_of_shares):
        """
        
        """
        action = record.rule['action']
        wanted_price = action['quantity']
        sellable_shares = int (wanted_price // stock_record.low) # gets the floor whole number of sellable_shares 

        if number_of_shares > 0 and sellable_shares > 0: # has to have at least 1 share
            if sellable_shares > number_of_shares: # ERROR, trying to sell more shares than you own
                sellable_shares = number_of_shares # sets sellable_shares = number_of_shares so you can not oversell
            
            Transactions.objects.add_transaction(
                ticker_id = Stocks.objects.get(id=action['symbol']['id']),
                rule_id = record.id,
                action = action['method'],
                qty = action['quantity'],
                price = action['value'],
                trx_timestamp = stock_record.timestamp
            )
            number_of_shares -= sellable_shares # sells shares
            balance += (float(sellable_shares) * stock_record.low) # adds the profit_loss

        elif number_of_shares > 0:
            self.output_error("Insufficient quantity to make the sale")
        else:
            self.output_error("Not enough shares to sell at the price specified")
        return [balance, number_of_shares]

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
