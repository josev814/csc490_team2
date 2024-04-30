"""
The job collects the metrics from the database that we should be pulling
"""
from math import ceil
import time
import traceback
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q, Func, F

from stocks.models import Stocks, StockData
from stocks.views import YahooFinance, StockSearch

class GetDateFromTS(Func):
    """
    Get the date from a timestamp
    """
    function = 'DATE'
    template = "%(function)s(%(expressions)s)"

class Command(BaseCommand):
    """
    The command that executes when this job is ran
    """
    help = 'Update metrics for all stock symbols or pass '
    help += '--ticker_id xxxx to process a specific ticker'
    refresh = datetime.now() - timedelta(minutes=10)
    record_limit = 100

    def add_arguments(self, parser):
        parser.add_argument('--ticker_id', type=int, help='ticker_id to process')
        parser.add_argument(
            '--ticker_ids',
            type=str,
            help='comma separated list of ticker_ids to process'
        )
        parser.add_argument(
            '--update_open_close',
            type=bool,
            help='Whether to update the open_close of stocks'
        )

    def handle(self, *args, **options):
        try:
            start_time = datetime.now()
            self.output_info([
                '#### Update Metrics Job #####',
                f'Start Time: {start_time}'
            ])
            if 'update_open_close' in options and options['update_open_close'] is not None:
                self.output_info('Only running day_open/day_close updates')
                self.update_open_close()
                end_time = datetime.now()
                self.output_info([
                    f'End Time: {end_time}',
                    f'Run Time: {end_time - start_time}',
                    '#### End Update Metrics Job #####'
                ])
                return
            if 'ticker_id' in options and options['ticker_id'] is not None:
                self.run_specific_ticker(
                    int(options['ticker_id'])
                )
            elif 'ticker_ids' in options and options['ticker_ids'] is not None:
                ticker_ids = options['ticker_ids'].split(',')
                for ticker_id in ticker_ids:
                    ticker_id = int(ticker_id)
                    try:
                        self.run_specific_ticker(
                            int(ticker_id)
                        )
                    except CommandError as ce:
                        self.output_error(ce)
                        pass
            else:
                self.run_all_tickers()
            self.update_open_close()
        except Exception as err:
            self.output_error(traceback.print_exc())
            raise CommandError(f'Error: {err}') from err
        end_time = datetime.now()
        self.output_info([
            f'End Time: {end_time}',
            f'Run Time: {end_time - start_time}',
            '#### End Update Metrics Job #####'
        ])
    
    def update_open_close(self):
        """
        Process all stocks to ensure that the open and close are set for the day
        """
        stocks = Stocks.objects.filter(is_active=1).values_list('pk', flat=True)
        if stocks.count() == 0:
            # no stocks
            return
        self.output_info('Updating any stock with missing day_open or day_close values')
        for stock_id in stocks:
            self.update_open(stock_id)
            self.update_close(stock_id)
    
    def get_exchange_open_val(self, ticker_id, proc_date):
        """
        Get the exchange open value based on the first record found for the day
        """
        return StockData.objects.filter(
                ticker_id=ticker_id,
                timestamp__date=proc_date
            ).values_list('open', flat=True).order_by('timestamp').first()

    def set_missing_day_open_val(self, ticker_id, proc_date, day_open_price):
        """
        Updates the stock's day with it's detected day open price
        """
        StockData.objects.filter(
                ticker_id=ticker_id,
                timestamp__date=proc_date
            ).filter(
                Q(day_open=0.0) | Q(day_open__isnull=True)
            ).update(day_open=day_open_price)
    
    def update_open(self, ticker_id):
        """
        Gets dates to process and then updates the day_open value
        """
        unique_dates = StockData.objects.filter(
            ticker_id=ticker_id
        ).filter(
            Q(day_open=0.0) | Q(day_open__isnull=True)
        ).annotate(
            date=GetDateFromTS('timestamp')
        ).values_list('date', flat=True).distinct()
        
        for unique_date in unique_dates:
            day_open_price = self.get_exchange_open_val(ticker_id, unique_date)
            self.set_missing_day_open_val(ticker_id, unique_date, day_open_price)

    def get_exchange_close_info(self, ticker_id, proc_date):
        """
        Get the exchange day close value based on the last record found for the day
        """
        return StockData.objects.filter(
            ticker_id=ticker_id,
            timestamp__date=proc_date,
            timestamp__time=F('exchange_close')
        ).values_list('close', flat=True).order_by('timestamp').first()
    
    def set_missing_day_close_val(self, ticker_id, proc_date, day_close_price):
        """
        Updates the stock's day with it's detected day close price
        """
        StockData.objects.filter(
                ticker_id=ticker_id,
                timestamp__date=proc_date
            ).filter(
                Q(day_close=0.0) | Q(day_close__isnull=True)
            ).update(day_close=day_close_price)
    
    def update_close(self, ticker_id):
        """
        Gets dates to process and then updates the day_close value
        """
        unique_dates = StockData.objects.filter(
            ticker_id=ticker_id
        ).filter(
            Q(day_close=0.0) | Q(day_close__isnull=True)
        ).annotate(
            date=GetDateFromTS('timestamp')
        ).values_list('date', flat=True).distinct()
        
        for unique_date in unique_dates:
            day_close_price = self.get_exchange_close_info(ticker_id, unique_date)
            if day_close_price:
                self.set_missing_day_close_val(ticker_id, unique_date, day_close_price)
    
    def run_specific_ticker(self, ticker_id):
        """
        Runs this job against a specific ticker
        """
        ticker_info = Stocks.objects.filter(
            is_active=1,
            updated_date__lte=self.refresh,
            pk__exact=ticker_id
        ).values_list(
            'ticker'
        )
        if ticker_info.count() == 0:
            ## already up to date
            self.output_success(f'Ticker with id {ticker_id} is already up to date')
            return
        ticker = ticker_info.get()[0]

        self.process_ticker(ticker, ticker_id)
    
    def run_all_tickers(self):
        """
        Runs the job against all tickers
        """
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
    
    def output_info(self, info_msg) -> None:
        """Outputs an informational message

        :param info_msg: the message to output
        :type info_msg: str|list
        """
        if isinstance(info_msg, list):
            formatted_msg = [self.style.NOTICE(line) for line in info_msg]
            self.stdout.writelines(
                formatted_msg
            )
        else:
            self.stdout.write(
                self.style.NOTICE(
                    info_msg
                )
            )
