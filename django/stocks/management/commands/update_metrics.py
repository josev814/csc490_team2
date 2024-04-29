"""
The job collects the metrics from the database that we should be pulling
"""
from math import ceil
import time
import traceback
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError

from stocks.models import Stocks, StockData
from stocks.views import YahooFinance, StockSearch
from rules.models import Rules

class Command(BaseCommand):
    """
    The command that executes when this job is ran
    """
    help = 'Update metrics for all stock symbols'
    refresh = datetime.now() - timedelta(minutes=10)
    record_limit = 100

    def handle(self, *args, **options):
        try:
            start_time = datetime.now()
            self.stdout.writelines([
                '#### Update Metrics Job #####',
                f'Start Time: {start_time}'
            ])
            # Query all symbols from the Stocks table
            symbol_count = Stocks.objects.filter(
                is_active=1,
                updated_date__lte=self.refresh
            ).count()
            max_page = ceil(symbol_count/self.record_limit)
            self.stdout.write(f'Records: {symbol_count}, MaxPage: {max_page}')
            for page_num in range(max_page):
                start = page_num * self.record_limit
                self.stdout.write(
                    f'Page: {page_num}, Start: {start}, End: {start + self.record_limit}'
                )
                symbols = Stocks.objects.values_list(
                    'ticker', 'id'
                ).filter(
                    is_active=1,
                    updated_date__lte=self.refresh
                ).all()[0:self.record_limit]
                # Iterate over each symbol and update metrics in StocksData table
                for ticker, ticker_id in symbols:
                    self.process_ticker(ticker, ticker_id)
                    self.remove_ticker_no_data(ticker_id)
        except Exception as err:
            raise CommandError(f'Error: {err}') from err
        end_time = datetime.now()
        self.stdout.writelines([
            f'End Time: {end_time}',
            f'Run Time: {end_time - start_time}',
            '#### End Update Metrics Job #####'
        ])
    
    def process_ticker(self, ticker, ticker_id):
        """Process pulling metrics for a ticker

        :param ticker: the ticker name
        :type ticker: str
        :param ticker_id: the ticker's id from our database
        :type ticker_id: int
        """
        try:
            start_date = self.get_start_date()
            try:
                last_updated = Stocks.objects.filter(pk__exact=ticker_id).first().updated_date
                start_date = max(start_date, last_updated)
            except:
                # No record
                pass
            
            current_datetime = datetime.now()
            while start_date < current_datetime:
                end_date = start_date + timedelta(days=7)

                yf = YahooFinance()
                start_posix = int(start_date.timestamp())
                end_posix = int(end_date.timestamp())
                chart = yf.get_chart(ticker, period1=start_posix, period2=end_posix)
                if 'chart' not in chart:
                    self.output_error(
                        f'No data for {ticker} on {start_date}'
                    )
                    # move forward one day
                    start_date = start_date + timedelta(days=1)
                    time.sleep(.5)
                    continue
                chart_metrics = chart['chart']['result'][0]
                
                # Create or update StocksData entry for the symbol
                dict_resp = StockData().save_stock_results(chart_metrics)
                if dict_resp['status']:
                    self.output_success(
                        f'Successfully added metrics for {ticker}'
                    )
                    # update the symbol for when was last saved it
                    StockSearch().save_search_request(ticker)
                    stock = Stocks.objects.filter(id=ticker_id, is_active=1).get()
                    stock.updated_date = datetime.now()
                    stock.save()
                else:
                    errors = dict_resp['errors']
                    self.output_error(
                        f'Failed adding metrics for {ticker} with error: {errors}'
                    )
                start_date = end_date + timedelta(minutes=1)
        except Exception as e:
            self.output_error(traceback.print_exc())
            self.output_error(f'Error updating metrics for {ticker}: {e}')
    
    def remove_ticker_no_data(self, ticker_id):
        """
        Removes a ticker if we don't have any data for them
        """
        if StockData.objects.filter(ticker_id__exact=ticker_id).count() > 0:
            return
        # cleanup the ticker, since we haven't gotten any data from them.
        Stocks.objects.filter(pk__exact=ticker_id).delete()

    
    def get_start_date(self):
        """
        Get the oldest rule start date or default to beginning of the year
        """
        oldest_date = datetime.now() - timedelta(days=30) + timedelta(minutes=1)
        # try:
        #     rule = Rules.objects.order_by('-start_date').first()
        #     rule_oldest_date = datetime.combine(rule.start_date, datetime.min.time())
        #     if rule_oldest_date < oldest_date:
        #         oldest_date = rule_oldest_date
        # except:
        #     pass
        return oldest_date

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
