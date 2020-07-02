# mckee_tasks.py
'''
celery -A mckee_tasks worker -l info
'''

from celery import Celery, chord, chain
from celery.utils.log import get_task_logger
from celery.schedules import crontab
from line_requests import Line
from satang_api import Satang
from bitstamp_api import Bitstamp
from fixer_api import Fixer
import time

mckee_app = Celery('tasks', backend='redis://localhost:6379/0', broker='pyamqp://guest@localhost//')
logger = get_task_logger(__name__)

bstamp = Bitstamp()
satang = Satang()
line = Line()
fixer = Fixer()

mckee_app.conf.beat_schedule = {
    'check-rate-spread': {
        'task': 'mckee_tasks.rate_spread',
        'schedule': crontab(minute='*/1', hour='*', day_of_week='*'),
    },
    'check-forex-rate': {
        'task': 'mckee_tasks.fx_rate',
        'schedule': crontab(minute='01', hour='*', day_of_week='*'),
    },
    'status-update': {
        'task': 'mckee_tasks.status_update',
        'schedule': crontab(minute='00', hour='7', day_of_week='*'),
    }
}


@mckee_app.task(name='mckee_tasks.status_update')
def status_update():
    message = f'I am still working'
    return line.post_broadcast(message)


@mckee_app.task(name='mckee_tasks.fx_rate')
def fx_rate():
    global xe
    # sleep a little bit so that it doesn't interfere with the every minute checks
    time.sleep(20)
    print('Getting exchange rate')
    fx = fixer.get_forex().json()
    xe = fx['rates']['THB'] / fx['rates']['USD']
    return xe


@mckee_app.task(name='mckee_tasks.satang_rate')
def satang_rate():
    symbol = 'btc_thb'
    response = satang.get_ticker(symbol).json()
    satang_price = float(response['bidPrice'])
    return satang_price


@mckee_app.task(name='mckee_tasks.bstamp_rate')
def bstamp_rate():
    response = bstamp.get_ticker().json()
    bstamp_price = float(response['ask'])
    return bstamp_price


@mckee_app.task(name='mckee_tasks.calc_spread')
def calc_spread(data):
    global old_spread
    global last_update_time
    print(old_spread)
    if data[0] > data[1]:
        satang_price = data[0]
        bstamp_price = data[1]
    else:
        satang_price = data[1]
        bstamp_price = data[0]
    spread = (satang_price - (bstamp_price * xe))/(bstamp_price * xe)
    if spread >= 0.01:
        if old_spread < 0.01:
            message = f'The Satang price is greater than Bitstamp by {spread:.2%}'
            last_update_time = time.time()
            line.post_broadcast(message)
        elif (time.time() - last_update_time) > 60*30:
            message = f'The Satang price is still greater than Bitstamp, now by {spread:.2%}'
            last_update_time = time.time()
            line.post_broadcast(message)
        else:
            message = 'Spread greater but there was a recent message, no action'
    elif old_spread >= 0.01:
        message = f'The spread fell below the cutoff (currently {spread:.2%})'
        line.post_broadcast(message)
    else:
        message = 'Spread still lesser, no action'
    old_spread = spread
    return [spread, message]


@mckee_app.task(name='mckee_tasks.rate_spread')
def rate_spread():
    return chord([satang_rate.s(), bstamp_rate.s()])(calc_spread.s())


# Global variables to keep track of things
xe = None
old_spread = 0
last_update_time = 0
fx_rate()
