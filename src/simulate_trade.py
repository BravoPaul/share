import pandas as pd
import warnings
from datetime import datetime
import os
import math

warnings.simplefilter(action='ignore', category=FutureWarning)


# 基金的属性并不是仅仅由fund_code决定的，fund_code仅仅决定了他的一部分属性，他是一个每天都变的产品，
# 他由fund_code，时间，开盘价，当天变化价和收盘价 共同决定


class SimulateTrade(object):
    def __init__(self, data_o, e_roi=0.15, value_buy=6250, total_argent=300000):
        self.e_roi = e_roi
        self.total_argent = total_argent
        self.data = data_o.sort_values(by=['ts_code', 'trade_date'])
        self.df_buy = pd.DataFrame.from_dict(
            {'ts_code': [], 'date': [], 'argent': [], 'open_value': [], 'close_value': []})
        self.df_sold = pd.DataFrame.from_dict(
            {'ts_code': [], 'date': [], 'argent': [], 'open_value': [], 'close_value': []})
        self.df_bill = pd.DataFrame.from_dict(
            {'fund_code': [], 'date_init': [], 'init_open_value': [], 'init_close_value': [], 'date_op': [],
             'value_op': [],
             'custodian': [], 'custodian_op': []})
        self.df_profit = pd.DataFrame.from_dict(
            {'date': [], 'close_value': [], 'fund_code': [], 'profit': [], 'invertissment': [], 'roi': [],
             'argent_left': [], 'argent_use_rate': []})
        self.left_argent = total_argent
        self.police_buy = ''
        self.police_sold = ''
        self.value_buy = value_buy

    def buy(self, fund_code, open_value, close_value, dt, week_day):
        if self.left_argent < 0:
            raise ValueError
        if len(self.df_buy) == 0:
            index_add = 0
            index_bill = 0
        else:
            index_add = self.df_buy.index.max() + 1
            index_bill = self.df_bill.index.max() + 1
        # 最傻瓜式的买法
        # argent, self.suffix_buy = Policy.buy('_buy_basic', week_day=week_day, week_day_buy=4, value_buy=2000)
        argent = Policy.buy(self, week_day=week_day, value_buy=self.value_buy, bill=self.df_bill,
                            open_value=open_value, dt=dt, close_value=close_value)
        if argent == 0:
            return
        else:
            argent = min(argent, self.left_argent)
            self.df_buy.loc[index_add] = [fund_code, dt, argent, open_value, close_value]
            self.df_bill.loc[index_bill] = [fund_code, dt, open_value, close_value, dt, close_value,
                                            argent / close_value,
                                            argent / close_value]
            self.left_argent = self.left_argent - argent

    # 这个函数决定卖不卖，卖多少钱
    def sold(self, fund_code, open_value, close_value, dt):
        if len(self.df_bill) == 0:
            return
        else:
            if len(self.df_sold) == 0:
                index_add = 0
            else:
                index_add = self.df_sold.index.max() + 1
            index_bill = self.df_bill.index.max() + 1
            sold_tmp = Policy.sold(self, e_roi=self.e_roi, open_value=open_value)
            if len(sold_tmp) > 0:
                # 策略是全部卖出，能不能根据之前买的股票的涨幅平滑卖出
                for index, row in sold_tmp.iterrows():
                    self.df_bill.loc[index_bill] = [row['fund_code'], row['date_init'], row['init_open_value'],
                                                    row['init_close_value'], dt, close_value,
                                                    0, -row['custodian']]
                    index_bill += 1
                argent = sold_tmp['custodian'].sum() * close_value
                self.df_sold.loc[index_add] = [fund_code, dt, argent, open_value, close_value]
                if argent < 0:
                    raise ValueError
                self.left_argent = self.left_argent + argent
            return

    # 这个函数决定卖不卖，卖多少钱
    def profit_calculate(self, fund_code, close_value, dt):
        bill_tmp = self.df_bill.sort_values(['date_op']).drop_duplicates(['fund_code', 'date_init'], keep='last')
        bill_profiter = bill_tmp[(bill_tmp['custodian'] != 0)]
        # 目前基金的持有价值
        position_fund = bill_profiter['custodian'].sum() * close_value
        invertissement = self.df_buy['argent'].sum()
        profit = self.left_argent + position_fund - self.total_argent
        if len(self.df_profit) == 0:
            index_add = 0
        else:
            index_add = self.df_profit.index.max() + 1
        self.df_profit.loc[index_add] = [dt, close_value, fund_code, profit, invertissement,
                                         profit / (invertissement + 0.0000000001),
                                         self.left_argent, 1 - self.left_argent / self.total_argent]

    def simulate(self, police_buy, police_sold, path_dir, start_date=-1, end_date=9999999999):
        self.police_buy = police_buy
        self.police_sold = police_sold
        data_tmp = self.data[(self.data['trade_date'] >= start_date) & (self.data['trade_date'] <= end_date)]
        data_tmp = data_tmp.sort_values(by=['ts_code', 'trade_date'])
        for index, row in data_tmp.iterrows():
            ts_code, open_value, close_value, dt, week_day = row['ts_code'], row['open'], row['close'], row[
                'trade_date'], row['week_day']
            self.sold(ts_code, open_value, close_value, dt)
            self.buy(ts_code, open_value, close_value, dt, week_day)
            self.profit_calculate(ts_code, close_value, dt)
        self.df_buy.to_excel(path_dir + 'buy$$' + self.police_buy + '_' + self.police_sold + '$$.xlsx')
        self.df_sold.to_excel(path_dir + 'sold$$' + self.police_buy + '_' + self.police_sold + '$$.xlsx')
        self.df_bill.to_excel(path_dir + 'bill$$' + self.police_buy + '_' + self.police_sold + '$$.xlsx')
        self.df_profit.to_excel(path_dir + 'profit$$' + self.police_buy + '_' + self.police_sold + '$$.xlsx')
        self.df_buy.drop(self.df_buy.index, inplace=True)
        self.df_sold.drop(self.df_sold.index, inplace=True)
        self.df_bill.drop(self.df_bill.index, inplace=True)
        self.df_profit.drop(self.df_profit.index, inplace=True)
        self.left_argent = self.total_argent

    def simulate_all(self, police_buy, police_sold, path_dir, start_date=-1, end_date=9999999999):
        data_tmp = self.data[(self.data['trade_date'] >= start_date) & (self.data['trade_date'] <= end_date)]
        now_close_value = data_tmp.iloc[-1]['close']
        max_close_value = data_tmp['close'].max()
        min_close_value = data_tmp['close'].min()
        # mean_close_value = data_tmp['close'].mean()
        data_tmp['trade_date_d'] = data_tmp['trade_date'].map(lambda x: datetime.strptime(str(x), '%Y%m%d').date())
        data_tmp = data_tmp[data_tmp['trade_date_d'].map(lambda x: (data_tmp.iloc[-1]['trade_date_d'] - x).days > 90)]
        date_max = data_tmp[data_tmp['close'] == max_close_value].iloc[0]['trade_date']
        date_min = data_tmp[data_tmp['close'] == min_close_value].iloc[0]['trade_date']
        # date_mean = data_tmp[data_tmp['close'] == mean_close_value]['trade_date'].values.tolist()
        date_now = data_tmp[data_tmp['close'].map(lambda x: math.fabs(x / now_close_value - 1) < 0.05)].iloc[0][
            'trade_date']
        suffix = 'max' + '$$'
        self.simulate(police_buy, police_sold, path_dir + suffix,
                      start_date=date_max, end_date=end_date)

        suffix = 'min' + '$$'
        self.simulate(police_buy, police_sold, path_dir + suffix,
                      start_date=date_min, end_date=end_date)

        suffix = 'now' + '$$'
        self.simulate(police_buy, police_sold, path_dir + suffix,
                      start_date=date_now, end_date=end_date)


class Policy(object):

    @classmethod
    def buy(cls, simu_stat, **param):
        method_call = getattr(globals()['Policy'], simu_stat.police_buy)
        return method_call(simu_stat, **param)

    # 每次等额买，每周都买
    @classmethod
    def _buy_basic(cls, simu_stat, **param):
        if param['week_day'] == 4:
            return param['value_buy']
        else:
            return 0

    # 对当前购买的基金价值进行预估,你此时对基金的预估都是和你持有的基金在10%以内的
    # 在预估基金价值的情况下，我选择每天预估一下买，还是只在周四预估去买
    # 为了简单，我先按照周四去预估一次去买
    @classmethod
    def _buy_fv_func(cls, simu_stat, fois, **param):
        if len(simu_stat.df_bill) == 0:
            return param['value_buy']
        mean_hd_value = simu_stat.df_bill['init_close_value'].mean()
        open_value = param['open_value']
        if param['week_day'] == 4:
            return param['value_buy'] * (mean_hd_value / open_value) ** 2
        else:
            return 0

    @classmethod
    def _buy_fv(cls, simu_stat, **param):
        cls._buy_fv_func(simu_stat, 2, **param)

    @classmethod
    def _buy_fv_3(cls, simu_stat, **param):
        cls._buy_fv_func(simu_stat, 3, **param)

    @classmethod
    def _buy_fv_4(cls, simu_stat, **param):
        cls._buy_fv_func(simu_stat, 4, **param)

    @classmethod
    def _buy_fv_10(cls, simu_stat, **param):
        cls._buy_fv_func(simu_stat, 10, **param)

    @classmethod
    def _buy_fv_4_min(cls, simu_stat, **param):
        if len(simu_stat.df_bill) == 0:
            return param['value_buy']
        mean_hd_value = simu_stat.df_bill['init_close_value'].min()
        open_value = param['open_value']
        if param['week_day'] == 4:
            return param['value_buy'] * (mean_hd_value / open_value) ** 4
        else:
            return 0

    @classmethod
    def sold(cls, simu_stat, **param):
        method_call = getattr(globals()['Policy'], simu_stat.police_sold)
        return method_call(simu_stat, **param)

    # 每次达到收益率就卖掉
    @classmethod
    def _sold_basic(cls, simu_stat, **param):
        e_roi = param['e_roi']
        open_value = param['open_value']
        earn_throld = open_value / (e_roi + 1)
        bill_tmp = simu_stat.df_bill.sort_values(['date_op']).drop_duplicates(['fund_code', 'date_init'], keep='last')
        bill_tmp = bill_tmp[bill_tmp['custodian'] != 0]
        sold_tmp = bill_tmp[bill_tmp['init_close_value'] <= earn_throld]
        return sold_tmp

    @classmethod
    def _sold_fv_new(cls, simu_stat, **param):
        if len(simu_stat.df_bill) == 0:
            return param['value_buy']
        mean_sd_value = simu_stat.df_sold['close_value'].mean()
        max_sd_value = simu_stat.df_sold['close_value'].max()
        open_value = param['open_value']
        if open_value < mean_sd_value:
            e_roi = param['e_roi'] + 0.05
        elif open_value > max_sd_value:
            e_roi = param['e_roi'] - 0.05
        else:
            e_roi = param['e_roi']
        open_value = param['open_value']
        earn_throld = open_value / (e_roi + 1)
        bill_tmp = simu_stat.df_bill.sort_values(['date_op']).drop_duplicates(['fund_code', 'date_init'], keep='last')
        bill_tmp = bill_tmp[bill_tmp['custodian'] != 0]
        sold_tmp = bill_tmp[bill_tmp['init_close_value'] <= earn_throld]
        return sold_tmp

    @classmethod
    def _sold_fv(cls, simu_stat, **param):
        if len(simu_stat.df_bill) == 0:
            return param['value_buy']
        mean_sd_value = simu_stat.df_sold['close_value'].mean()
        open_value = param['open_value']
        if open_value < mean_sd_value:
            e_roi = param['e_roi'] + 0.05
        else:
            e_roi = param['e_roi']
        open_value = param['open_value']
        earn_throld = open_value / (e_roi + 1)
        bill_tmp = simu_stat.df_bill.sort_values(['date_op']).drop_duplicates(['fund_code', 'date_init'], keep='last')
        bill_tmp = bill_tmp[bill_tmp['custodian'] != 0]
        sold_tmp = bill_tmp[bill_tmp['init_close_value'] <= earn_throld]
        return sold_tmp


if __name__ == '__main__':
    # 策略分析 #
    path_data = '../data/data_market/market_value.csv'
    data = pd.read_csv(path_data)
    data = data[data['ts_code'] == '000300.SH']
    st = SimulateTrade(data)
    police_buy_name = '_buy_basic'
    police_sold_name = '_sold_basic'
    path_data = '../data/data_ananlyse_6250/' + police_buy_name + police_sold_name
    mkdir = lambda x: os.makedirs(x) if not os.path.exists(x) else True  # 目录是否存在,不存在则创建
    mkdir(path_data)
    st.simulate_all(police_buy_name, police_sold_name, path_data + '/')
