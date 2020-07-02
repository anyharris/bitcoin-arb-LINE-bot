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

    def get_forex(self):
        path = f'/latest?access_key={self.API_KEY}&symbols=USD,THB'
        response = self._get(path)
        return response
