"""
Models for the application are stored here
"""
import sys
#import logging
from datetime import datetime, timedelta

from django.db import models, IntegrityError


class Stocks(models.Model):
    """
    Model for a Stocks table
    """
    ticker = models.CharField(max_length=12)
    name = models.CharField(max_length=75)
    exchange_name = models.CharField(max_length=50)
    exchange = models.CharField(max_length=10)
    stock_type = models.CharField(max_length=12)
    create_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        """
        Adding indexes for the table
        """
        indexes = [
            models.Index(fields=['ticker', 'name'])
        ]

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
                if entry['typeDisp'].lower() in ['option']: # skip options
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
    timestamp = models.DateTimeField(auto_now=True)
    high = models.FloatField(default=0.0, max_length=28)
    low = models.FloatField(default=0.0, max_length=28)
    open = models.FloatField(default=0.0, max_length=28)
    close = models.FloatField(default=0.0, max_length=28)
    granularity = models.CharField(max_length=4)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Adding indexes for the table
        """
        indexes = [
            models.Index(fields=['ticker', 'timestamp', 'granularity']),
        ]
    
    def save_stock_results(self, yahoo_data:dict) -> dict:
        """Parses the yahoo chart results and saves the results to our database

        :param yahoo_data: The yahoo chart results
        :type yahoo_data: dict
        :return: Returns if we were able to successfully save the record
        :rtype: bool
        """
        records = []
        try:
            ticker = yahoo_data['meta']['symbol']
            granularity = yahoo_data['meta']['dataGranularity']
            if 'timestamp' not in yahoo_data:
                return {'status': False, 'errors': ['YahooData: No data']}
            for i in range(len(yahoo_data['timestamp'])):
                quote_volumes = yahoo_data['indicators']['quote'][0]
                cont = False
                for keys in ['high', 'low', 'open', 'close']:
                    if quote_volumes[keys][i] is None:
                        cont = True
                        break
                if cont:
                    continue
                records.append(
                    {
                        'ticker_id': Stocks.objects.filter(**{'ticker': ticker}).get().pk,
                        'granularity': granularity,
                        'timestamp': datetime.fromtimestamp(yahoo_data['timestamp'][i]),
                        'high': quote_volumes['high'][i],
                        'low': quote_volumes['low'][i],
                        'open': quote_volumes['open'][i],
                        'close': quote_volumes['close'][i]
                    }
                )
            StockData.objects.bulk_create([StockData(**record) for record in records])
        except IntegrityError as e:
            return {'status': False, 'errors': [f'IntegrityError: Failed to save record: {e}']}
        except KeyError as e:
            return {'status': False, 'errors': [f'KeyError: Failed to save record: {e}']}
        except Exception:
            ex_type, ex, tb = sys.exc_info()
            print(tb)
            return {'status': False, 'errors': [f'{ex_type}: Failed to save record: {ex}']}
        return {'status': True, 'errors': None}



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
        indexes = [
            models.Index(fields=['search_phrase']),
            models.Index(fields=['search_args'])
        ]
    
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
        if isinstance(args, str) or isinstance(args, dict):
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
        if isinstance(args, str) or isinstance(args, dict):
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
