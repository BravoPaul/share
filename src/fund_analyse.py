import pandas as pd
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# 基金的属性并不是仅仅由fund_code决定的，fund_code仅仅决定了他的一部分属性，他是一个每天都变的产品，
# 他由fund_code，时间，开盘价，当天变化价和收盘价 共同决定


EARNING_RATE = 0.3

DF_BUY = pd.DataFrame.from_dict({'date': [], 'argent': [], 'open_value': [], 'close_value': []})

DF_SOLD = pd.DataFrame.from_dict({'date': [], 'argent': [], 'open_value': [], 'close_value': []})

# 记录的是每天以各种价格买的基金的份额变化，站在基金的角度看问题
# meta:基金号，基金初始化日期，基金初始化日期当天开盘价，基金初始化日期当天收盘价，对基金操作日期，对基金操作当天收盘价，当前持有的基金，具体操作
DF_BILL = pd.DataFrame.from_dict(
    {'fund_code': [], 'date_init': [], 'init_open_value': [], 'init_close_value': [], 'date_op': [], 'value_op': [],
     'custodian': [], 'custodian_op': []})

# profit分为俩个部分：1，已经卖出的份额得到的利润；2，还没有卖出的份额对应的利润
DF_PROFIT = pd.DataFrame.from_dict(
    {'date': [], 'fund_code': [], 'profit': [], 'invertissment': [], 'roi': [], 'argent_left': []})

TOTAL_ARGENT = 6000000000

BUY_FIRST_ARGENT = 4000

LEFT_ARGENT = 6000000000


# 这个函数决定买不买，买多少钱
def condition_buy(fund_code, open_value, close_value, dt, week_day):
    global LEFT_ARGENT, DF_BILL, DF_BUY
    if week_day == 1:
        if LEFT_ARGENT <= 0:
            index_add = DF_BUY.index.max() + 1
            argent = 0
            index_bill = DF_BILL.index.max() + 1
        else:
            # 购买系数
            if len(DF_BUY) == 0:
                index_add = 0
                index_bill = 0
                argent = BUY_FIRST_ARGENT
            else:
                a = (open_value - DF_BUY.iloc[-1]['close_value']) / DF_BUY.iloc[-1]['close_value']
                # @TOTO：这里有问题，假如我没钱买了，购买为0，但是卖出一些后又有钱了，根据上次的购买记录直接买，又等于0了。所有有问题
                argent = min(DF_BUY.iloc[-1]['argent'] * (1 - a), LEFT_ARGENT)
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
        earn_throld = open_value / (EARNING_RATE + 1)
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
    DF_PROFIT.loc[index_add] = [dt, fund_code, profit, invertissement, profit/invertissement,LEFT_ARGENT]


# 返回每年的收益率以及到目前为止的总收益率
# 返回我的操作记录
# 卖达到我收益的部分
# 每周选择一天定投
def pk_police(ts_code, open_value, close_value, dt, week_day):
    condition_buy(ts_code, open_value, close_value, dt, week_day)
    condition_sold(ts_code, open_value, close_value, dt)
    profit_calculate(ts_code, close_value, dt)


def market_value_analyse(x, y):
    plt.plot(x, y, color="r", linestyle="--", marker="s", linewidth=1.0)
    plt.show()


if __name__ == '__main__':
    # # 把我要分析的基金涉及到的指数拿出来,这些指数对应的真实tscode已经人工存到了 common_fund_index ，
    # # 这些指数10年对应的value值已经放到了 market_value.csv
    # path_jj_buy = '../data/data_jijin/jijin_analyse_sort_p5_buy_20191029.xlsx'
    # df_fund_basic = pd.read_excel(path_jj_buy)
    # l_market = df_fund_basic['benchmark_format'].unique()
    # print(l_market)
    # path_market_all = '../data/data_market/market_index.xlsx'
    # df_market_all = pd.read_excel(path_market_all)
    # # 为了方便观测，我把星期几也加上
    # path_input_file = '../data/data_market/market_value.csv'
    # df_origin = pd.read_csv(path_input_file)
    # df_origin['week_day'] = df_origin['trade_date'].map(lambda x: dt.dt.strptime(str(x), '%Y%m%d').weekday()+1)
    # path_input_file = '../data/data_market/market_value.csv'
    # df_origin.to_csv(path_input_file)

    # 数据分析 #
    # path_data = '../data/data_market/market_value.csv'
    # data = pd.read_csv(path_data)
    # date = data['trade_date'].values.tolist()
    # close_value = data['close'].values.tolist()
    # print(date)
    # market_value_analyse(date, close_value)

    # 策略分析 #
    path_data = '../data/data_market/market_value.csv'
    data = pd.read_csv(path_data)
    data = data[data['ts_code'] == '000300.SH']
    data = data.sort_values(by=['trade_date'])
    for index, row in data.iterrows():
        pk_police(row['ts_code'], row['open'], row['close'], row['trade_date'], row['week_day'])
    path_data_buy = '../data/data_result/buy_history.xlsx'
    path_data_sold = '../data/data_result/sold_history.xlsx'
    path_data_bill = '../data/data_result/bill_history.xlsx'
    path_data_profit = '../data/data_result/profit_history.xlsx'
    path_data_origin = '../data/data_result/data_origin.xlsx'
    DF_BUY.to_excel(path_data_buy)
    DF_SOLD.to_excel(path_data_sold)
    DF_BILL.to_excel(path_data_bill)
    DF_PROFIT.to_excel(path_data_profit)
    data.to_excel(path_data_origin)
