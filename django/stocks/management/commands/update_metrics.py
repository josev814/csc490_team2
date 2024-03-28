"""
The job collects the metrics from the database that we should be pulling
"""
from math import ceil
import traceback
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from stocks.models import Stocks, StockData
from stocks.views import YahooFinance, StockSearch

class Command(BaseCommand):
    """
    The command that executes when this job is ran
    """
    help = 'Update metrics for all stock symbols'
    refresh = datetime.now() - timedelta(hours=1)
    record_limit = 10

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
            stock_search = StockSearch()
            StockSearch.objects.values_list(
                'search_args'
            ).filter(
                search_phrase=ticker
            ).all()

            yf = YahooFinance()
            chart_metrics = yf.get_chart(ticker)['chart']['result'][0]
            
            # Create or update StocksData entry for the symbol
            dict_resp = StockData().save_stock_results(chart_metrics)
            
            if dict_resp['status']:
                self.output_success(
                    f'Successfully added metrics for {ticker}'
                )
                # update the symbol for when was last saved it
                stock_search.save_search_request(ticker)
                stock = Stocks.objects.filter(id=ticker_id, is_active=1).get()
                stock.updated_date = datetime.now()
                stock.save()
            else:
                errors = dict_resp['errors']
                self.output_error(
                    f'Failed adding metrics for {ticker} with error: {errors}'
                )
        except Exception as e:
            self.output_error(traceback.print_exc())
            self.output_error(f'Error updating metrics for {ticker}: {e}')

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
