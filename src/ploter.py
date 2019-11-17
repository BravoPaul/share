import pandas as pd
import matplotlib as mpl
from datetime import datetime
import matplotlib.dates as mdates

mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np


class MyPlot(object):
    def plot_close_value(self, data, start_date, end_date, scale='m'):
        # create some data to use for the plot
        data = data.sort_values(by=['trade_date'])
        length = len(data)
        if scale == 'm':
            scale_num = 30
        elif scale == 'w':
            scale_num = 7
        else:
            raise ValueError
        # t = np.arange(0, length, scale_num)
        t = data.iloc[::7, :]['trade_date'].map(lambda x: datetime.strptime(str(x), '%Y%m%d').date())
        s = data.iloc[::7, :]['close'].values

        print(len(t))
        plt.figure(figsize=(80,40))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=150))
        plt.plot(t, s)
        plt.gcf().autofmt_xdate()
        plt.show()


if __name__ == '__main__':
    path_data = '../data/data_market/market_value.csv'
    data = pd.read_csv(path_data)
    data = data[data['ts_code'] == '000300.SH']
    mp = MyPlot()
    mp.plot_close_value(data, 20090105, 20191104)
