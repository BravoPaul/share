import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


# 基金的属性并不是仅仅由fund_code决定的，fund_code仅仅决定了他的一部分属性，他是一个每天都变的产品，
# 他由fund_code，时间，开盘价，当天变化价和收盘价 共同决定


class SimulateTrade(object):
    def __init__(self, data_o, start_date=20150112, end_date=20191104, e_roi=0.15, total_argent=600000):
        self.e_roi = e_roi
        self.total_argent = total_argent
        self.data = data_o[(data['trade_date'] >= start_date) & (data['trade_date'] <= end_date)]
        self.data = self.data.sort_values(by=['trade_date'])
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
             'argent_left': []})
        self.left_argent = total_argent

    def buy(self, fund_code, open_value, close_value, dt, week_day):
        if self.left_argent < 0:
            raise ValueError
        if len(self.df_buy) == 0:
            index_add = 0
            index_bill = 0
        else:

            index_add = self.df_buy.index.max() + 1
            index_bill = self.df_bill.index.max() + 1
        argent = Policy.buy('_buy_basic', week_day=week_day, week_day_buy=4, value_buy=2000)
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
            earn_throld = Policy.sold('_sold_basic', e_roi=self.e_roi, open_value=open_value)
            bill_tmp = self.df_bill.sort_values(['date_op']).drop_duplicates(['fund_code', 'date_init'], keep='last')
            bill_tmp = bill_tmp[bill_tmp['custodian'] != 0]
            sold_tmp = bill_tmp[(bill_tmp['init_close_value'] <= earn_throld) & (bill_tmp['fund_code'] == fund_code)]
            if len(sold_tmp) > 0:
                argent = sold_tmp['custodian'].sum() * (close_value)
                # 策略是全部卖出，能不能根据之前买的股票的涨幅平滑卖出
                for index, row in sold_tmp.iterrows():
                    self.df_bill.loc[index_bill] = [row['fund_code'], row['date_init'], row['init_open_value'],
                                                    row['init_close_value'], dt, close_value,
                                                    0, -row['custodian']]
                    index_bill += 1
                self.df_sold.loc[index_add] = [fund_code, dt, argent, open_value, close_value]
                if argent < 0:
                    raise ValueError
                self.left_argent = self.left_argent + argent
            return

    # 这个函数决定卖不卖，卖多少钱
    def profit_calculate(self, fund_code, close_value, dt):
        bill_tmp = self.df_bill.sort_values(['date_op']).drop_duplicates(['fund_code', 'date_init'], keep='last')
        bill_profiter = bill_tmp[(bill_tmp['custodian'] != 0) & (bill_tmp['fund_code'] == fund_code)]
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
                                         self.left_argent]

    def simulate(self, path_buy, path_sold, path_bill, path_profit):
        for index, row in self.data.iterrows():
            ts_code, open_value, close_value, dt, week_day = row['ts_code'], row['open'], row['close'], row[
                'trade_date'], row['week_day']
            self.sold(ts_code, open_value, close_value, dt)
            self.buy(ts_code, open_value, close_value, dt, week_day)
            self.profit_calculate(ts_code, close_value, dt)
        self.df_buy.to_excel(path_buy)
        self.df_sold.to_excel(path_sold)
        self.df_bill.to_excel(path_bill)
        self.df_profit.to_excel(path_profit)


class Policy(object):

    @classmethod
    def buy(cls, policy_name, **param):
        method_call = getattr(globals()['Policy'], policy_name)
        return method_call(**param)

    # 每次等额买，每周都买
    @classmethod
    def _buy_basic(cls, **param):
        if param['week_day'] == param['week_day_buy']:
            return param['value_buy']
        else:
            return 0

    # 对当前购买的基金价值进行预估
    @classmethod
    def _buy_fv(cls, **param):
        if param['week_day'] == param['week_day_buy']:
            return param['value_buy']
        else:
            return 0

    @classmethod
    def sold(cls, policy_name, **param):
        method_call = getattr(globals()['Policy'], policy_name)
        return method_call(**param)

    # 每次达到收益率就卖掉
    @classmethod
    def _sold_basic(cls, **param):
        e_roi = param['e_roi']
        open_value = param['open_value']
        earn_throld = open_value / (e_roi + 1)
        return earn_throld


if __name__ == '__main__':
    # 策略分析 #
    path_data = '../data/data_market/market_value.csv'
    data = pd.read_csv(path_data)
    data = data[data['ts_code'] == '000300.SH']
    st = SimulateTrade(data)
    path_data_buy = '../data/data_ananlyse/buy_history_.xlsx'
    path_data_sold = '../data/data_ananlyse/sold_history_.xlsx'
    path_data_bill = '../data/data_ananlyse/bill_history_.xlsx'
    path_data_profit = '../data/data_ananlyse/profit_history_2000_015_ban_xin.xlsx'
    st.simulate(path_data_buy, path_data_sold, path_data_bill, path_data_profit)
