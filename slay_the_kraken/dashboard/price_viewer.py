#!/usr/bin/python3
# -*- coding: utf-8 -*-

import io
import json
import datetime
import matplotlib.pyplot as plt

from time import time, ctime
from matplotlib.figure import Figure
from slay_the_kraken.kraken.api import API


def plot_prices_continuously():
    plt.figure()

    plt.xlabel('$Time$')
    plt.ylabel('$Price$')

    now = ctime()
    interval = 60*60 
    then = ctime(time() - interval)
    print(now, then)

    plt.xaxis([now, then])
    plt.ylabel('$Price$')

    krakenapi = API()
    with open('slay_the_kraken/trading/asset_pairs.json', 'r') as myfile:
        asset_pair = json.load(myfile)

    def get_price_data():
        (key, value), = asset_pair.items()
        data = {'pair': key, 'interval': 1, 'since': then}
        query = krakenapi.public_query('OHLC', data=data, timeout=1.0)
        return query['result'][value]

    data = get_price_data()
    print(len(data))
    for t, opn, high, low, close, _, _, _ in data:
        timestamp = time.ctime(t)
        plt.plot([timestamp, timestamp], [low, high])

    plt.show(block=False)
    plt.pause(2)
    plt.close()