# mckee_tasks.py
"""
I used celery to get some practice and to save a bit of time for when multiple API calls can be done simultaneously.
I also like the built in crontab scheduling.

To start the app:
    celery -A mckee_tasks worker -l -B info
"""

from celery import Celery, chord
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

SPREAD_THRESHOLD = 0.01     # Broadcast if the price difference [(a - b)/b] is greater than this
REST_TIME = 60*30           # If the price stays above the threshold wait this long to broadcast again


mckee_app.conf.beat_schedule = {
    """
    Check the rate spread every minute
    Update the fx rate every hour
    Send a ping every day so that people know it's still working
    """
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
    """
    A ping to show users that the app is still alive

    :return: {}
    """
    message = f'I am still working'
    return line.post_broadcast(message)


@mckee_app.task(name='mckee_tasks.fx_rate')
def fx_rate():
    """
    Keeps the global xe rate variable up to date for the calc_spread task to use
    Uses the fixer.io free tier forex API which only has EUR as the base pair so we need to do some division

    :return: 31.019741608682857
    """
    global xe
    # sleep a little bit so that it doesn't interfere with the every minute checks
    time.sleep(20)
    print('Getting exchange rate')
    fx = fixer.get_forex('USD', 'THB').json()
    xe = fx['rates']['THB'] / fx['rates']['USD']
    return xe


@mckee_app.task(name='mckee_tasks.satang_rate')
def satang_rate():
    """
    Uses the Satang API to get the current bid price

    :return: 288700.0
    """
    symbol = 'btc_thb'
    response = satang.get_ticker(symbol).json()
    satang_price = float(response['bidPrice'])
    return satang_price


@mckee_app.task(name='mckee_tasks.bstamp_rate')
def bstamp_rate():
    """
    Uses the Bitstamp API to get the current ask price

    :return: 9245.38
    """
    response = bstamp.get_ticker().json()
    bstamp_price = float(response['ask'])
    return bstamp_price


@mckee_app.task(name='mckee_tasks.calc_spread')
def calc_spread(data):
    """
    Takes as input the returns from satang_rate() and bstamp_rate()
    The order of those returns is random so it checks first to see which is which
    A message is broadcast on LINE if an arbitrage opportunity is present

    :param data: [9245.38, 288700.0]
    :return: [0.00633688792936527, 'Spread still lesser, no action']
    """
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
    """
    Runs the celery task chord that determines the rate spread and sends LINE messages

    :return: <AsyncResult: ff626389-e044-428b-b02f-f58cd08c438e>
    """
    return chord([satang_rate.s(), bstamp_rate.s()])(calc_spread.s())


# Global variables to keep track of things
xe = None
old_spread = 0
last_update_time = 0

# Get the xe rate when the app starts
fx_rate()
