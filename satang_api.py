# satang_api.py
"""
Satang exchange public API
"""

import requests


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
