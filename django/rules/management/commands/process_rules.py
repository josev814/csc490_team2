"""
This job runs rules to see if transactions should be performed
"""
from datetime import datetime
# from math import floor
from typing import Any
import sys

from django.core.management.base import BaseCommand
from django.core.management import call_command
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

    def set_defaults(self):
        """
        Initialize this job
        """
        self.START_TIME = datetime.now()
        self.this_job = self.get_job_info()
        # Get the last runtime of this job
        self.LAST_RUNTIME = self.get_last_runtime()
        

    def handle(self, *args: Any, **options: Any):
        """
        Runs the job to process the rules in the db
        """
        self.set_defaults()

        rules = self.get_rules()
        for record in rules:
            # only process rule if filled in
            if self.is_rule_valid(record.rule) and record.initial_investment > 0:
                if record.last_ran_timestamp is None:
                    self.set_record_balance(record, record.initial_investment)
                print('Rule: ', record.pk)
                print('Runtime: ', record.last_ran_timestamp)
                print('Rule Info: ', record.rule)
                self.run_rule(record)
        #         self.set_record_last_run(record, self.START_TIME)
        #         print('New Runtime: ', record.last_ran_timestamp)
        # # update this jobs last runtime
        # self.set_last_runtime()
    
    def set_record_balance(self, record, balance):
        """
        Set the balance for the record
        """
        record.balance = balance
        record.save()
    
    def set_record_last_run(self, record):
        """
        Sets the last_ran_time for the record to be the start time of this process
        """
        record.last_ran_timestamp = self.START_TIME
        record.save()
    
    def is_rule_valid(self, rule):
        """
        Checks if the rule is properly defined
        """
        if rule is not None and all(key in rule for key in ['conditions', 'action', 'trigger']):
            return True
        return False
    
    def get_job_info(self):
        """
        Gets the job info from the database
        """
        return RuleJobs.objects.first()
    
    def get_last_runtime(self):
        """
        Get the last time this job ran
        """
        if self.this_job is not None and self.this_job.last_ran_timestamp is not None:
            return self.this_job.last_ran_timestamp
        return self.START_TIME

    def set_last_runtime(self):
        """
        Set the last time this job ran based on the start time
        """
        self.this_job.set_last_runtime(
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


    def get_referenced_symbols(self, rule):
        """
        Gets the symbols in the conditions and actions
        """
        symbols = self.get_conditions_symbols(rule['conditions'])
        action_symbol = self.get_action_symbols(rule['action'])
        for item_id, _ in action_symbol.items():
            if item_id not in symbols:
                symbols.update(action_symbol)
        return symbols
    
    def get_conditions_symbols(self, conditions):
        """
        Get the symbols that a rule references
        """
        symbols = {}
        for condition in conditions:
            symbol = condition['symbol']
            if symbol['id'] in symbols:
                # already in our dict
                continue
            symbols[symbol['id']] = symbol['ticker']
        return symbols
            
    
    def get_action_symbols(self, action):
        """
        Gets the symbol referenced in the action
        """
        return {action['symbol']['id']: action['symbol']['ticker']}

    def update_metrics_before_processing(self, record):
        """
        Runs the update metrics process before we run the rule
        """
        self.output_success(f'### Updating stocks pertaining to rule: {record.id} - {record.name}')
        symbols = self.get_referenced_symbols(record.rule)
        symbol_ids_csv = ','.join(symbols.keys())
        call_command('update_metrics', ticker_ids=symbol_ids_csv)
        self.output_success(f'### Updated stocks pertaining to rule: {record.id} - {record.name}')        

    def run_rule(self, record):
        """
        Run the rule
        """
        # get the records that passed the user's conditions
        start_date = self.get_start_from(record)
        self.update_metrics_before_processing(record)
        
        # ensure we have rules
        stock_records = self.run_conditions(record.rule['conditions'], start_date)
        if stock_records is None or stock_records.count() == 0:
            return
        print('Matching Stock Records: ', stock_records.count())

        action = record.rule['action']

        number_of_shares = record.shares
        balance = record.balance

        # get last transaction for rule
        last_transaction = Transactions.objects.get_last_transaction(record.id)
        print(action)
        print(number_of_shares)
        print(balance)
        print(last_transaction)
        sys.exit()

        # for stock_record in stock_records:
        #     print('STock record: ', stock_record)

        #     break

        #     if action['method'] == 'buy':
        #         if balance == 0: # we can't buy anything at this point
        #             break
        #         if action['quantity_type'] == 'shares':
        #             balance, number_of_shares = self.purchase_by_shares(
        #                 record, stock_record, balance, number_of_shares
        #             )
        #         elif action['quantity_type'] == 'price':
        #             # TODO: create the purchase_by_price method and logic
        #             # return balance, profit_loss, number_of_shares
        #             balance, number_of_shares = self.purchase_by_price(
        #                 record, stock_record, balance, number_of_shares
        #             )
        #     elif action['method'] == 'sell':
        #         if number_of_shares < 1:
        #             break
        #         if action['quantity_type'] == 'shares':
        #             balance, number_of_shares = self.sell_by_shares(
        #                 record, stock_record, balance, number_of_shares
        #             )
        #         elif action['quantity_type'] == 'price':
        #             # TODO port to a function of sell_by_price
        #             # finish the logic for this and verify it
        #             balance, number_of_shares = self.sell_by_price(
                        
        #             )
        #     else:
        #         self.output_error('Unsupported action: ', action)
        
        # growth = self.get_rule_growth(balance, record)
        # profit_loss = 0
        # if number_of_shares > 0:
        #     profit_loss = self.get_profit_loss(record, number_of_shares)
        
        # record.update_balance(
        #     shares = number_of_shares,
        #     balance = balance,
        #     growth = growth,
        #     profit = profit_loss
        # )
    
    def get_start_from(self, record):
        """
        Gets the date to start from
        """
        if record.last_ran_timestamp is not None:
            return record.last_ran_timestamp
        return record.start_date
    
    def run_conditions(self, conditions, start_from):
        """
        Queries the database based on the conditions the user set
        Additionally the start_from is when the user set for the start date
        """
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
                    timestamp = start_from
                )
            else:
                qs = StockData().get_stock_data(
                    ticker_id = condition['symbol']['id'],
                    column = condition['data'],
                    operator = condition['operator'],
                    value = condition['value'],
                    condition = condition['condition'],
                    data=qs
                )
        # Ensure to only pull records since this last ran
        qs = qs.filter(timestamp__lte=self.START_TIME)
        return qs
    
    def get_profit_loss(self, record, number_of_shares):
        """
        Calculates the profit loss for a rule
        """
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
        """
        Gets the average cost that the rule paid for the stock
        """
        trx_data_cost = Transactions.objects.filter(
            rule_id__exact=rule,
            ticker_id__exact=ticker,
            action__exact='buy'
        ).aggregate(total_cost=Sum('price'))

        trx_data_shares = Transactions.objects.filter(
            rule_id__exact=rule,
            ticker_id__exact=ticker,
            action__exact='buy'
        ).aggregate(total_shares=Sum('quantity'))
        
        average_cost = trx_data_cost['avg_cost'] // float(trx_data_shares['total_shares'])
        return average_cost

    def get_current_stock_price(self, stock_id):
        """
        Gets the most recent stock price
        """
        return StockData.objects.filter(
            ticker_id__exact=stock_id,
            granularity__exact='1m'
        ).order_by('-pk', ).first().low

    def get_stock_price_from_timestamp(self, stock_id, timestamp):
        """
        Gets the stock price that's closest to the timestamp given
        """
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
        Purchase the stock based on how much the user wants to spend
        """
        action = record.rule['action']

        wanted_price = action['quantity']
        current_share_price = stock_record.low
        wanted_shares = int ( wanted_price // current_share_price )

        if balance > wanted_price and wanted_shares > 0: # filling full order
            total_shares_cost = wanted_shares * current_share_price

            Transactions.objects.add_transaction(
                ticker = Stocks.objects.get(id=action['symbol']['id']),
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
                ticker = Stocks.objects.get(id=action['symbol']['id']),
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
                ticker = Stocks.objects.get(id=action['symbol']['id']),
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
                ticker = Stocks.objects.get(id=action['symbol']['id']),
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
        """
        Make a purchase of the stock based on shares that the user wants
        """
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
        Sell shares of the stock up to the price that the user wants to sell
        """
        action = record.rule['action']
        wanted_price = action['quantity']
        # gets the floor whole number of sellable_shares 
        sellable_shares = int (wanted_price // stock_record.low)

        if number_of_shares > 0 and sellable_shares > 0: # has to have at least 1 share
            sellable_shares = min(sellable_shares, number_of_shares) # prevent oversell
            
            Transactions.objects.add_transaction(
                ticker = Stocks.objects.get(id=action['symbol']['id']),
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
