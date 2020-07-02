# bitstamp_api.py
"""
Bitstamp exchange public API
"""

import requests


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
