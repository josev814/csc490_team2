"""
Models for the application are stored here
"""
import sys
import logging
from datetime import datetime, timedelta

from django.db import models, IntegrityError


class Stocks(models.Model):
    """
    Model for a Stocks table
    """
    SKIP_STOCK_TYPES = ['option', 'futures', 'cryptocurrency']
    ticker = models.CharField(max_length=12)
    name = models.CharField(max_length=75)
    exchange_name = models.CharField(max_length=50)
    exchange = models.CharField(max_length=10)
    stock_type = models.CharField(max_length=25)
    create_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        """
        Adding indexes for the table
        """
        unique_together = ['ticker', 'name']

    def __str__(self):
        """Default return of the class

        :return: Returns the ticker
        :rtype: str
        """
        return f'{self.ticker}'

    def save_search_results(self, yahoo_data:dict) -> dict:
        """_summary_

        :param yahoo_data: _description_
        :type yahoo_data: dict
        :return: _description_
        :rtype: dict
        """
        records = []
        try:
            for entry in yahoo_data:
                if entry['typeDisp'].lower() in self.SKIP_STOCK_TYPES:
                    continue
                if 'longname' not in entry:
                    if 'shortname' not in entry:
                        continue
                    entry['longname'] = entry['shortname']
                record = {
                    'ticker': entry['symbol'],
                    'name': entry['longname'],
                    "exchange": entry['exchange'],
                    "exchange_name": entry['exchDisp'],
                    'stock_type': entry['typeDisp']
                }
                records.append(record)
                existing_tickers = set(Stocks.objects.values_list('ticker', flat=True))
                unique_records = [r for r in records if r['ticker'] not in existing_tickers]
                if unique_records:
                    Stocks.objects.bulk_create([Stocks(**record) for record in unique_records])
        except KeyError as e:
            error = f'KeyError when attempting to save stock results: {e}'
            return {'status': False, 'errors': [error]}
        except IntegrityError as e:
            error = f'IntegrityError when attempting to save stock results: {e}'
            return {'status': False, 'errors': [error]}
        return {'status': True, 'errors': None}



class StockData(models.Model):
    """
    Model for the stock data
    """
    ticker = models.ForeignKey(
        'Stocks',
        on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(null=True, blank=True)
    high = models.FloatField(default=0.0, max_length=28)
    low = models.FloatField(default=0.0, max_length=28)
    open = models.FloatField(default=0.0, max_length=28)
    close = models.FloatField(default=0.0, max_length=28)
    granularity = models.CharField(max_length=4)
    day_open = models.FloatField(default=0.0, max_length=28)
    day_close = models.FloatField(null=True, blank=True, max_length=28)
    create_date = models.DateTimeField(auto_now_add=True)
    exchange_open = models.TimeField(null=True, blank=True)
    exchange_close = models.TimeField(null=True, blank=True)
    exchange_gmtoffset = models.IntegerField(default=-14400)
    
    class Meta:
        """
        Adding indexes for the table
        """
        unique_together = ['ticker', 'timestamp', 'granularity']
    
    def save_stock_results(self, yahoo_data:dict) -> dict:
        """Parses the yahoo chart results and saves the results to our database

        :param yahoo_data: The yahoo chart results
        :type yahoo_data: dict
        :return: Returns if we were able to successfully save the record
        :rtype: bool
        """
        try:
            ticker = yahoo_data['meta']['symbol']
            ticker_reference = Stocks.objects.filter(**{'ticker': ticker}).get().pk
            granularity = yahoo_data['meta']['dataGranularity']
            if 'timestamp' not in yahoo_data:
                return {'status': False, 'errors': ['YahooData: No data']}
            trading_periods = self.get_trading_times(yahoo_data)
            for i in range(len(yahoo_data['timestamp'])):
                record = self.process_record(
                    yahoo_data, i, trading_periods, ticker_reference, granularity
                )
                if record:
                    try:
                        StockData.objects.create(**record)
                    except IntegrityError as e:
                        if 'Duplicate entry' in str(e.args):
                            #print('skipping duplicate record entry')
                            pass
                        else:
                            return {
                                'status': False,
                                'errors': [f'IntegrityError: Failed to save record: {e}']
                            }
        except KeyError as e:
            return {'status': False, 'errors': [f'KeyError: Failed to save record: {e}']}
        except Exception:
            ex_type, ex, tb = sys.exc_info()
            logging.debug(tb)
            return {'status': False, 'errors': [f'{ex_type}: Failed to save record: {ex}']}
        return {'status': True, 'errors': None}

    def process_record(self, yahoo_data, i, trading_periods, ticker_reference, granularity):
        """
        Verifies that a tickers entry is in the trading window
        if so it will check for the correct keys
        then it will build out the record that gets inserted into the db
        """
        entry_datetime = yahoo_data['timestamp'][i]
        # only add entries that are within the trading window fo the stock exchange
        if not self.is_in_trading_window(trading_periods, entry_datetime):
            return False
        quote_volumes = yahoo_data['indicators']['quote'][0]
        cont = False
        for keys in ['high', 'low', 'open', 'close']:
            if quote_volumes[keys][i] is None:
                cont = True
                break
        if cont:
            return False
        return {
                'ticker_id': ticker_reference,
                'granularity': granularity,
                'timestamp': datetime.fromtimestamp(entry_datetime),
                'high': quote_volumes['high'][i],
                'low': quote_volumes['low'][i],
                'open': quote_volumes['open'][i],
                'close': quote_volumes['close'][i],
                **trading_periods
            }

    def get_trading_times(self, yahoo_data):
        """
        Getting the Stock's trading times for the exhange
        """
        trading_periods = yahoo_data['meta']['tradingPeriods']['regular'][0][0]
        trading_gmt_start = self.get_time_from_timestamp(trading_periods['start'])
        trading_gmt_end = self.get_time_from_timestamp(trading_periods['end'])
        trading_timezone_offset = trading_periods['gmtoffset']
        return {
            'exchange_open': trading_gmt_start,
            'exchange_close': trading_gmt_end,
            'exchange_gmtoffset': trading_timezone_offset
        }
    
    def get_time_from_timestamp(self, timestamp):
        """
        Gets the time from a POSIX timestamp
        """
        dt = datetime.fromtimestamp(timestamp)
        hour = dt.hour
        minutes = dt.minute
        secs = dt.second
        time_parts = [hour, minutes, secs]
        for i in range(len(time_parts)):
            if time_parts[i] < 10:
                time_parts[i] = f'0{time_parts[i]}'
        hour, minutes, secs = time_parts
        return f'{hour}:{minutes}:{secs}'
    
    def is_in_trading_window(self, trading_periods: dict, entry_datetime:int) -> bool:
        """
        Compare the entry_datetime with the trading_period
        We first get the time in a string format
        Then we convert to be the same date to do a comparison
        """
        entry_time = datetime.strptime(self.get_time_from_timestamp(entry_datetime), '%H:%M:%S')
        start_time = datetime.strptime(trading_periods['exchange_open'], '%H:%M:%S')
        end_time = datetime.strptime(trading_periods['exchange_close'], '%H:%M:%S')
        if entry_time >= start_time and entry_time <= end_time:
            return True
        return False

    def get_stock_data(
            self, ticker_id: int, column, operator, 
            value, condition, timestamp=None, data=None
            ):
        """
        Gets stock data matching the query
        """
        if column == 'price':
            column = 'low'
        
        if condition == 'if':
            if operator == 'eq':
                data = StockData.objects.filter(**{'ticker_id': ticker_id, f'{column}': value})
            else:
                data = StockData.objects.filter(**{
                    'ticker_id': ticker_id,
                    f'{column}__{operator}': value
                })
        elif condition == 'and':
            if operator == 'eq':
                data = data.filter(**{'ticker_id': ticker_id, f'{column}': value})
            else:
                data = data.filter(**{'ticker_id': ticker_id, f'{column}__{operator}': value})
        if timestamp:
            data = data.filter(**{'timestamp__gte': timestamp})

        return data


class StockSearch(models.Model):
    """
    Stores historical searches for Yahoo
    """
    search_phrase = models.CharField(max_length=75)
    search_args = models.CharField(max_length=512, null=True)
    updated_date = models.DateTimeField(auto_now=True)
    search_refresh = datetime.now() - timedelta(days=1)


    class Meta:
        """
        Adding indexes for the table
        """
        unique_together = ['search_phrase', 'search_args']
    
    def set_search_refresh(self, delta_name:str, delta_value:int):
        """sets the refresh date

        :param delta_name: _description_
        :type delta_name: str
        :param delta_value: _description_
        :type delta_value: int
        """
        self.search_refresh = datetime.now() - timedelta(**{delta_name:delta_value})

    def does_search_record_exist(self, phrase:str, args:str|dict) -> bool:
        """Determines is the search to Yahoo exists or not

        :param phrase: The ticker or company that is being searched for
        :type phrase: str
        :param args: The arguments passed to yahoo
        :type args: str
        :return: Returns if the record existed or not
        :rtype: bool
        """
        search_filter = {
            'search_phrase': phrase,
            'updated_date__gte': self.search_refresh
        }
        if isinstance(args, (str, dict)):
            search_filter['search_args'] = args
        records = StockSearch.objects.filter(**search_filter)
        return records.count() > 0
    
    def get_search_record(self, phrase:str, args:str|dict) -> object|None:
        """_summary_

        :param phrase: _description_
        :type phrase: str
        :param args: _description_
        :type args: str
        :return: _description_
        :rtype: object
        """
        if self.does_search_record_exist(phrase, args) is False:
            return None
        search_filter = {
            'search_phrase': phrase,
            'updated_date__gte': self.search_refresh
        }
        if isinstance(args, (str, dict)):
            search_filter['search_args'] = args
        record = StockSearch.objects.filter(**search_filter)
        # This is how to print the query being performed
        # logging.error(record.query)
        return record
    
    def save_search_request(self, phrase:str, args:str|None=None) -> dict:
        """Determines is the search to Yahoo exists or not

        :param phrase: The ticker or company that is being searched for
        :type phrase: str
        :param args: Additional arguments passed to yahoo
        :type args: str|None
        :return: Returns if the record was saved
        :rtype: bool
        """
        try:
            kwargs = {
                'search_args': args,
                'search_phrase': phrase
            }
            StockSearch.objects.create(**kwargs)
        except IntegrityError as e:
            return {'status': False, 'IntegrityError': f'Failed to save record: {e}'}
        except Exception as e:
            return {'status': False, 'errors': f'Failed to save record: {e}'}
        return {'status': True, 'errors': None}
    
    def save_search_results(self, yahoo_results: dict) -> dict:
        """a wrapper for saving search results

        :param yahoo_results: _description_
        :type yahoo_results: dict
        :return: _description_
        :rtype: dict
        """
        if 'chart' in yahoo_results:
            return StockData().save_stock_results(yahoo_results['chart']['result'][0])
        if 'quotes' in yahoo_results and len(yahoo_results['quotes']) > 0:
            return Stocks().save_search_results(yahoo_results['quotes'])
        msg = 'Unhandled option in save_search_results'
        return {'status': True, 'errors': [msg]}
