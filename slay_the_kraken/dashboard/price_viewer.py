#!/usr/bin/python3
# -*- coding: utf-8 -*-

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

    now = time()
    period = 60*60  # in seconds
    then = time() - period
    print(ctime(now), ctime(then))

    krakenapi = API()
    with open('slay_the_kraken/trading/asset_pairs.json', 'r') as myfile:
        asset_pair = json.load(myfile)

    def get_price_data(interval):
        if interval not in [1, 5, 15, 30, 60, 240, 1440, 10080, 21600]:
            interval = 1
        (key, value), = asset_pair.items()
        data = {'pair': key, 'interval': interval, 'since': then}
        query = krakenapi.public_query('OHLC', data=data, timeout=1.0)
        return query['result'][value]

    data = get_price_data(1)
    print(len(data))

    fig, ax = plt.subplots(1, figsize=(12, 6))
    for t, opn, high, low, close, _, _, _ in data:
        plt.plot([t, t], [float(low), float(high)])

    # plt.xlim([ctime(now), ctime(then)])
    plt.xticks([then:now], rotation=30)
    plt.xlabel('$Time$')
    plt.ylabel('$Price$')

    plt.show(block=False)
    plt.pause(5)
    plt.close()
