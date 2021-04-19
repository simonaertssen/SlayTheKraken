#!/usr/bin/python3
# -*- coding: utf-8 -*-

import io
import time
import json
import matplotlib.pyplot as plt

from matplotlib.figure import Figure

from slay_the_kraken.kraken.api import API

# plt.ion()
# for i in range(100):
#     x = range(i)
#     y = range(i)
#     # plt.gca().cla() # optionally clear axes
#     plt.plot(x, y)
#     plt.title(str(i))
#     plt.draw()
#     plt.pause(0.001)

# plt.show(block=False) # block=True lets the window stay open at the end of the animation.
# plt.close()


def plot_prices_continuously():
    fig = Figure(figsize=(5, 5), dpi=100, frameon=False)
    axes = fig.gca()

    axes.set_xlim(0, 0.5)
    axes.set_ylim(0, 0.5)

    axes.set_xlabel('$Time$')
    axes.set_ylabel('$Price$')

    now = 0
    then = now - 7*24*60*30  # 30 days ago
    interval = (now - then) / 720
    print('interval', interval)

    krakenapi = API()
    with open('slay_the_kraken/trading/asset_pairs.json', 'r') as myfile:
        asset_pair = json.load(myfile)
        print(type(asset_pair))
    def get_price_data():
        (key, value), = asset_pair.items()
        data = {'pair': key, 'interval': 1, 'since': then}
        query = krakenapi.public_query('OHLC', data=data, timeout=1.0)
        return query['result'][value]

    data = get_price_data()
    for time, opn, high, low, close, _, _, _ in data:
        plot_data = axes.plot([time, time], [low, high])[0]
