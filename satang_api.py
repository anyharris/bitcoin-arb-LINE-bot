# satang_api.py
import requests


class Satang:
    API_HOST = 'https://api.tdax.com/api/v3/'

    def _get(self, path):
        uri = self.API_HOST + path
        response = requests.get(uri)
        return response

    def get_ticker(self, symbol):
        path = f'ticker/24hr?symbol={symbol}'
        response = self._get(path)
        return response
