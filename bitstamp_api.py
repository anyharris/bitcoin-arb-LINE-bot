# bitstamp_api.py
import requests


class Bitstamp:
    API_HOST = 'https://www.bitstamp.net/api/'

    def _get(self, path):
        uri = self.API_HOST + path
        response = requests.get(uri)
        return response

    def get_ticker(self):
        path = 'ticker/'
        response = self._get(path)
        return response
