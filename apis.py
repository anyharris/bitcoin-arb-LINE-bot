# apis.py
"""
API wrappers for fixer.io, satang.pro, and bitstamp
"""
import requests
from dotenv import load_dotenv
import os


class Fixer:
    API_HOST = 'http://data.fixer.io/api/'

    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv('FIXER_KEY')

    def _get(self, path):
        uri = self.API_HOST + path
        response = requests.get(uri)
        return response

    def get_forex(self, curr1, curr2):
        """
        Returns forex rate with EUR base pair for both currencies
        Needs to be done this way with the free tier of this API

        :param curr1: 'USD'
        :param curr2: 'THB'
        :return:
        {
        'success': True,
        'timestamp': 1593663365,
        'base': 'EUR',
        'date': '2020-07-02',
        'rates': {
            'USD': 1.126342,
            'THB': 35.006608
            }
        }
        """
        path = f'/latest?access_key={self.API_KEY}&symbols={curr1},{curr2}'
        response = self._get(path)
        return response


class Satang:
    API_HOST = 'https://api.tdax.com/api/v3/'

    def _get(self, path):
        uri = self.API_HOST + path
        response = requests.get(uri)
        return response

    def get_ticker(self, symbol):
        """
        Returns 24hr market data for the specified symbol

        :param symbol: 'btc_tbh'
        :return:
        {
        'symbol': 'btc_thb',
        'priceChange': '2306.07230023732',
        'priceChangePercent': '0.803383198117939807',
        'weightedAvgPrice': '286945.1634908135254153',
        'prevClosePrice': '285236.5579636',
        'lastPrice': '289351.19667422',
        'lastQty': '0.11781495',
        'bidPrice': '288700',
        'askPrice': '289339.64201777',
        'openPrice': '285251.31463336',
        'highPrice': '289728.81624311',
        'lowPrice': '284100.33',
        'volume': '107.22939527',
        'quoteVolume': '30768956.3567712165306242',
        'openTime': 1593566892528,
        'closeTime': 1593653085780,
        'firstId': 1396940,
        'lastId': 1398439,
        'count': 1501
        }
        """
        path = f'ticker/24hr?symbol={symbol}'
        response = self._get(path)
        return response


class Bitstamp:
    API_HOST = 'https://www.bitstamp.net/api/'

    def _get(self, path):
        uri = self.API_HOST + path
        response = requests.get(uri)
        return response

    def get_ticker(self):
        """
        With no specified ticker this will return BTC_USD 24hr market data

        :return:
        {
        'high': '9300.00000000',
        'last': '9240.58',
        'timestamp': '1593652929',
        'bid': '9232.67',
        'vwap': '9212.05',
        'volume': '4211.92053379',
        'low': '9096.62000000',
        'ask': '9236.99',
        'open': 9230.97
        }
        """
        path = 'ticker/'
        response = self._get(path)
        return response
