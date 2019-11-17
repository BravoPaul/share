import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

e_roi = 0.15
TOTAL_ARGENT = 600000
BUY_FIRST_ARGENT = 2000
LEFT_ARGENT = 600000

DF_BUY = pd.DataFrame.from_dict({'date': [], 'argent': [], 'open_value': [], 'close_value': []})
DF_SOLD = pd.DataFrame.from_dict({'date': [], 'argent': [], 'open_value': [], 'close_value': []})
# 记录的是每天以各种价格买的基金的份额变化，站在基金的角度看问题
# meta:基金号，基金初始化日期，基金初始化日期当天开盘价，基金初始化日期当天收盘价，对基金操作日期，对基金操作当天收盘价，当前持有的基金，具体操作
DF_BILL = pd.DataFrame.from_dict(
    {'fund_code': [], 'date_init': [], 'init_open_value': [], 'init_close_value': [], 'date_op': [], 'value_op': [],
     'custodian': [], 'custodian_op': []})
# profit分为俩个部分：1，已经卖出的份额得到的利润；2，还没有卖出的份额对应的利润
DF_PROFIT = pd.DataFrame.from_dict(
    {'date': [], 'close_value': [], 'fund_code': [], 'profit': [], 'invertissment': [], 'roi': [], 'argent_left': []})


# 这个函数决定买不买，买多少钱
def condition_buy(fund_code, open_value, close_value, dt, week_day):
    global LEFT_ARGENT, DF_BILL, DF_BUY
    if week_day == 4:
        if LEFT_ARGENT < 0:
            raise ValueError
        if len(DF_BUY) == 0:
            index_add = 0
            index_bill = 0
            argent = min(BUY_FIRST_ARGENT, LEFT_ARGENT)
        else:
            argent = min(BUY_FIRST_ARGENT, LEFT_ARGENT)
            index_add = DF_BUY.index.max() + 1
            index_bill = DF_BILL.index.max() + 1
        DF_BUY.loc[index_add] = [dt, argent, open_value, close_value]
        DF_BILL.loc[index_bill] = [fund_code, dt, open_value, close_value, dt, close_value, argent / close_value,
                                   argent / close_value]
        LEFT_ARGENT = LEFT_ARGENT - argent
    return


# 这个函数决定卖不卖，卖多少钱
def condition_sold(fund_code, open_value, close_value, dt):
    global LEFT_ARGENT, DF_BILL, DF_SOLD
    if len(DF_BILL) == 0:
        return
    else:
        if len(DF_SOLD) == 0:
            index_add = 0
        else:
            index_add = DF_SOLD.index.max() + 1
        index_bill = DF_BILL.index.max() + 1
        earn_throld = open_value / (e_roi + 1)
        bill_tmp = DF_BILL.sort_values(['date_op']).drop_duplicates(['fund_code', 'date_init'], keep='last')
        bill_tmp = bill_tmp[bill_tmp['custodian'] != 0]
        sold_tmp = bill_tmp[(bill_tmp['init_close_value'] <= earn_throld) & (bill_tmp['fund_code'] == fund_code)]
        if len(sold_tmp) > 0:
            argent = sold_tmp['custodian'].sum() * (close_value)
            # 策略是全部卖出，能不能根据之前买的股票的涨幅平滑卖出
            for index, row in sold_tmp.iterrows():
                DF_BILL.loc[index_bill] = [row['fund_code'], row['date_init'], row['init_open_value'],
                                           row['init_close_value'], dt, close_value,
                                           0, -row['custodian']]
                index_bill += 1
            DF_SOLD.loc[index_add] = [dt, argent, open_value, close_value]
            if argent < 0:
                raise ValueError
            LEFT_ARGENT = LEFT_ARGENT + argent
    return


# 天级别的profit,自己的每笔投资分别让自己赚了多少钱
# 目前持有的基金的盈亏 = 持有份额*目前的净值 - 当时购买这些份额花的钱
# 已经卖出的基金的盈亏 = 卖出的份额*卖出当天的基金的净值 - 当时购买这些份额花的钱
# 天级别的基金盈亏 = 目前持有的基金的盈亏 + 已经卖出的基金的盈亏
def profit_calculate(fund_code, close_value, dt):
    global DF_PROFIT
    bill_tmp = DF_BILL.sort_values(['date_op']).drop_duplicates(['fund_code', 'date_init'], keep='last')
    bill_profiter = bill_tmp[(bill_tmp['custodian'] != 0) & (bill_tmp['fund_code'] == fund_code)]
    # 目前基金的持有价值
    position_fund = bill_profiter['custodian'].sum() * close_value
    invertissement = DF_BUY['argent'].sum()
    profit = LEFT_ARGENT + position_fund - TOTAL_ARGENT
    if len(DF_PROFIT) == 0:
        index_add = 0
    else:
        index_add = DF_PROFIT.index.max() + 1
    DF_PROFIT.loc[index_add] = [dt, close_value, fund_code, profit, invertissement, profit / (invertissement+0.000000001),
                                LEFT_ARGENT]


# 返回每年的收益率以及到目前为止的总收益率
# 返回我的操作记录
# 卖达到我收益的部分
# 每周选择一天定投
def pk_police(ts_code, open_value, close_value, dt, week_day):
    condition_sold(ts_code, open_value, close_value, dt)
    condition_buy(ts_code, open_value, close_value, dt, week_day)
    profit_calculate(ts_code, close_value, dt)


if __name__ == '__main__':
    # 策略分析 #
    path_data = '../data/data_market/market_value.csv'
    data = pd.read_csv(path_data)
    data = data[data['ts_code'] == '000300.SH']
    data = data[(data['trade_date'] <= 2019110897894) & (data['trade_date'] >= 20090113)]
    data = data.sort_values(by=['trade_date'])
    for index, row in data.iterrows():
        pk_police(row['ts_code'], row['open'], row['close'], row['trade_date'], row['week_day'])
    path_data_buy = '../data/data_ananlyse/buy_history.xlsx'
    path_data_sold = '../data/data_ananlyse/sold_history.xlsx'
    path_data_bill = '../data/data_ananlyse/bill_history.xlsx'
    path_data_profit = '../data/data_ananlyse/profit_history_2000_015_ban.xlsx'
    path_data_origin = '../data/data_ananlyse/data_origin.xlsx'
    DF_BUY.to_excel(path_data_buy)
    DF_SOLD.to_excel(path_data_sold)
    DF_BILL.to_excel(path_data_bill)
    DF_PROFIT.to_excel(path_data_profit)
    data.to_excel(path_data_origin)
