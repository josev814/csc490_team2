"""
Logic for the stocks app
"""
#from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
def index(request):
    """
    This is the main endpoint that gets hit
    """
    print(request)
    resp = {
        'error': {
            'msg': 'Unauthorized Access',
            'status_code': '403'
        }
    }
    return JsonResponse(resp)


def find_ticker(request, search: str):
    """
    This endpoint allows us to search for a ticker using the search parameter
    """
    print(request)
    search_query = f'https://query1.finance.yahoo.com/v1/finance/{search}' \
        '?q=amazon&lang=en-US&region=US&quotesCount=6&newsCount=0&listsCount=0'
    print(search_query)
    results = {
        "count": 6,
        "quotes": [
            {
                "exchange": "NMS",
                "shortname": "Amazon.com, Inc.",
                "quoteType": "EQUITY",
                "symbol": "AMZN",
                "index": "quotes",
                "score": 299173,
                "typeDisp": "Equity",
                "longname": "Amazon.com, Inc.",
                "exchDisp": "NASDAQ",
                "sector": "Consumer Cyclical",
                "sectorDisp": "Consumer Cyclical",
                "industry": "Internet Retail",
                "industryDisp": "Internet Retail",
                "dispSecIndFlag": True,
                "isYahooFinance": True
            },
            {
                "exchange": "NEO",
                "shortname": "AMAZON.COM CDR (CAD HEDGED)",
                "quoteType": "EQUITY",
                "symbol": "AMZN.NE",
                "index": "quotes",
                "score": 20387,
                "typeDisp": "Equity",
                "longname": "Amazon.com, Inc.",
                "exchDisp": "NEO",
                "sector": "Consumer Cyclical",
                "sectorDisp": "Consumer Cyclical",
                "industry": "Internet Retail",
                "industryDisp": "Internet Retail",
                "isYahooFinance": True
            },
            {
                "exchange": "GER",
                "shortname": "AMAZON.COM INC.  DL-,01",
                "quoteType": "EQUITY",
                "symbol": "AMZ.DE",
                "index": "quotes",
                "score": 20250,
                "typeDisp": "Equity",
                "longname": "Amazon.com, Inc.",
                "exchDisp": "XETRA",
                "sector": "Consumer Cyclical",
                "sectorDisp": "Consumer Cyclical",
                "industry": "Internet Retail",
                "industryDisp": "Internet Retail",
                "isYahooFinance": True
            },
            {
                "exchange": "SAO",
                "shortname": "AMAZON      DRN",
                "quoteType": "EQUITY",
                "symbol": "AMZO34.SA",
                "index": "quotes",
                "score": 20150,
                "typeDisp": "Equity",
                "longname": "Amazon.com, Inc.",
                "exchDisp": "São Paulo",
                "sector": "Consumer Cyclical",
                "sectorDisp": "Consumer Cyclical",
                "industry": "Internet Retail",
                "industryDisp": "Internet Retail",
                "isYahooFinance": True
            },
            {
                "exchange": "FRA",
                "shortname": "AMAZON COM INC",
                "quoteType": "EQUITY",
                "symbol": "AMZ.F",
                "index": "quotes",
                "score": 20078,
                "typeDisp": "Equity",
                "longname": "Amazon.com, Inc.",
                "exchDisp": "Frankfurt",
                "sector": "Consumer Cyclical",
                "sectorDisp": "Consumer Cyclical",
                "industry": "Internet Retail",
                "industryDisp": "Internet Retail",
                "isYahooFinance": True
            },
            {
                "exchange": "DUS",
                "shortname": "AMAZON COM INC",
                "quoteType": "EQUITY",
                "symbol": "AMZ.DU",
                "index": "quotes",
                "score": 20071,
                "typeDisp": "Equity",
                "longname": "Amazon.com Inc",
                "exchDisp": "Dusseldorf Stock Exchange",
                "sector": "Consumer Cyclical",
                "sectorDisp": "Consumer Cyclical",
                "industry": "Internet Retail",
                "industryDisp": "Internet Retail",
                "isYahooFinance": True
            }
        ],
        "news": [],
        "nav": [],
        "lists": [],
        "researchReports": [],
        "screenerFieldResults": [],
        "totalTime": 71,
        "timeTakenForQuotes": 445,
        "timeTakenForNews": 0,
        "timeTakenForAlgowatchlist": 400,
        "timeTakenForPredefinedScreener": 400,
        "timeTakenForCrunchbase": 0,
        "timeTakenForNav": 400,
        "timeTakenForResearchReports": 0,
        "timeTakenForScreenerField": 0,
        "timeTakenForCulturalAssets": 0
    }
    return JsonResponse(results)


def get_ticker(request, symbol:str):
    """
    Gets a ticker's chart data
    """
    print(request)
    query_uri = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}' \
        '?interval=1d&includePrePost=true&lang=en-US&region=US'
    print(query_uri)
    ticker = {
        "chart": {
            "result": [
                {
                    "meta": {
                        "currency": "USD",
                        "symbol": "TSP",
                        "exchangeName": "NMS",
                        "instrumentType": "EQUITY",
                        "firstTradeDate": 1618493400,
                        "regularMarketTime": 1707166801,
                        "gmtoffset": -18000,
                        "timezone": "EST",
                        "exchangeTimezoneName": "America/New_York",
                        "regularMarketPrice": 0.265,
                        "chartPreviousClose": 0.3009,
                        "priceHint": 4,
                        "currentTradingPeriod": {
                            "pre": {
                                "timezone": "EST",
                                "start": 1707123600,
                                "end": 1707143400,
                                "gmtoffset": -18000
                            },
                            "regular": {
                                "timezone": "EST",
                                "start": 1707143400,
                                "end": 1707166800,
                                "gmtoffset": -18000
                            },
                            "post": {
                                "timezone": "EST",
                                "start": 1707166800,
                                "end": 1707181200,
                                "gmtoffset": -18000
                            }
                        },
                        "dataGranularity": "1d",
                        "range": "1d",
                        "validRanges": [
                            "1d",
                            "5d",
                            "1mo",
                            "3mo",
                            "6mo",
                            "1y",
                            "2y",
                            "5y",
                            "ytd",
                            "max"
                        ]
                    },
                    "timestamp": [
                        1707166801
                    ],
                    "indicators": {
                        "quote": [
                            {
                                "high": [
                                    0.28630000352859497
                                ],
                                "low": [
                                    0.2574000060558319
                                ],
                                "volume": [
                                    2500306
                                ],
                                "close": [
                                    0.26499998569488525
                                ],
                                "open": [
                                    0.2808000147342682
                                ]
                            }
                        ],
                        "adjclose": [
                            {
                                "adjclose": [
                                    0.26499998569488525
                                ]
                            }
                        ]
                    }
                }
            ],
            "error": None
        }
    }
    return JsonResponse(ticker)
