#!/usr/bin/python3
# -*- coding: utf-8 -*-

# from slay_the_kraken.dashboard.price_viewer import plot_prices_continuously
from datetime import datetime
import time
from slay_the_kraken.kraken.api import API
import calendar

# def main():
#     plot_prices_continuously()


if __name__ == '__main__':
    api = API()

    # data = api.OHLC('XXBTZUSD', interval=1)

    print(api.OHLC('XXBTZUSD'))
    api.OHLC('XXBTZUSD', interval=1)
    api.OHLC('XXBTZUSD', interval=5)
    # api.OHLC('XXBTZUSD', interval=1, since=time.time() - 10*60)

    # print(data['result'].keys())
    # print(len(data['result']['XXBTZUSD']))
    # date = datetime.utcfromtimestamp(data['result']['last'])  # .strftime('%Y-%m-%d %H:%M:%S')
    # date = time.gmtime(data['result']['last'])
    # print(date)
    # datestr = time.strftime('%Y-%m-%d %H:%M:%S', date)
    # print(datestr)
    # unixtime = calendar.timegm(date)
    # print(data['result']['last'], date, unixtime, unixtime - data['result']['last'])
