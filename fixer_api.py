# fixer_api.py
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
        #path = f'/latest?access_key={self.API_KEY}&symbols=USD,THB'
        path = f'/latest?access_key={self.API_KEY}&symbols={curr1},{curr2}'
        response = self._get(path)
        return response
