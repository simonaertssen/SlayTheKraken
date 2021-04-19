import io
import matplotlib.pyplot as plt

import os
print(os.getcwd())
from the_kraken.api import API
from matplotlib.figure import Figure
from matplotlib.finance import candlestick2_ohlc

plt.ion()
for i in range(100):
    x = range(i)
    y = range(i)
    # plt.gca().cla() # optionally clear axes
    plt.plot(x, y)
    plt.title(str(i))
    plt.draw()
    plt.pause(0.001)

plt.show(block=False) # block=True lets the window stay open at the end of the animation.
plt.close()

def plot_prices_continuously():
    self.figr = Figure(figsize=(5, 5), dpi=100, frameon=False)
    self.axes = self.fig.gca(projection='2d')

    self.axes.set_xlim(0, 0.5)
    self.axes.set_ylim(0, 0.5)

    self.axes.set_xlabel('$Time$')
    self.axes.set_ylabel('$Price$')

    now = time.time()
    then = now - 7*24*60*30  # 30 days ago
    interval = (now - then) / 720
    print('interval', interval)

    krakenapi = API()
    with open('trading/asset_pairs.json', 'r') as myfile:
        asset_pair = json.load(myfile)
    def get_price_data():
        data = {'pair': asset_pair.keys(0), 'interval': 1, 'since': then}
        query = krakenapi.public_query('OHLC', data=data, timeout=1.0)
        return query['result'][asset_pair.values(0)]

    data = get_price_data()
    for time, opn, high, low, close, _, _, _ in data:
        self.plot_data = self.axes.plot([time, time], [low, high])[0]

    # while(True):


def main():
    plot_prices_continuously()


if __name__ == '__main__':
    main()