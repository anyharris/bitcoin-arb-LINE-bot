# line_requests.py
import os
import requests
from dotenv import load_dotenv


class Line:
    API_HOST = 'https://api.line.me/v2/bot/'

    def __init__(self):
        load_dotenv()
        self.CHANNEL_ACCESS_TOKEN = os.getenv('CHAN_ACCESS_TOKEN')
        self.CHANNEL_SECRET = os.getenv('CHAN_SECRET')

    def _headers(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.CHANNEL_ACCESS_TOKEN}'
        }
        return headers

    def _post(self, path, headers, data):
        uri = self.API_HOST + path
        response = requests.post(uri, headers=headers, data=data)
        return response

    def post_broadcast(self, message):
        """
        Sends a broadcast message to everyone who has a chat open with the bot

        :param message: 'Satang/Bitstamp spread is 0.63%'
        :return: {}
        """
        headers = self._headers()
        path = 'message/broadcast'
        data = '{"messages": [{"type": "text", "text": "%s"}]}' % message
        print(data)
        response = self._post(path=path, headers=headers, data=data)
        return response
