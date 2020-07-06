# tg_requests.py
import os
import requests
from dotenv import load_dotenv
# channel ID is 1297643126, -1001297643126


class Telegram:
    API_HOST = 'https://api.telegram.org'

    def __init__(self):
        load_dotenv()
        self.TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
        self.TG_CHANNEL_ID = os.getenv('TG_CHANNEL_ID')

    def _get(self, path, params):
        uri = self.API_HOST + path
        response = requests.get(uri, params=params)
        return response

    def broadcast(self, msg):
        path = f'/bot{self.TG_BOT_TOKEN}/sendMessage'
        params = {
            'chat_id': self.TG_CHANNEL_ID,
            'text': msg
        }
        response = self._get(path, params)
        return response
