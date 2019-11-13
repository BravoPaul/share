import pandas as pd

E_ROI = 0.1


# 这个函数负责分析每次买多少的策略进行评估：
# 收益率平均值：mean_profit
# 投资总计收入: final_profit
# ROI稳定在10%以上的天数：num_roi
# ROI是多少: mean_roi
# 手中流动资金平均值: mean_argent_main
# roi波动: std_roi
# 最大赔钱: max_loss
# 手中流动资金最小值: min_argent_main
def buy_value_analyse(x, e_roi):
    mean_profit = x['profit'].mean()
    num_roi = len(x[x['roi'] > e_roi])
    mean_roi = x['roi'].mean()
    final_profit = x.iloc[-1]['profit']
    mean_argent_main = x['argent_left'].mean()
    std_roi = x['roi'].std()
    max_loss = x['profit'].min()
    min_argent_main = x['argent_left'].min()
    print('mean_profit:  ', mean_profit)
    print('final_profit:  ', final_profit)
    print('num_roi:  ', num_roi)
    print('mean_roi:  ', mean_roi)
    print('mean_argent_main:  ', mean_argent_main)
    print('max_loss:  ', max_loss)
    print('std_roi:  ', std_roi)
    print('min_argent_main:  ', min_argent_main)


if __name__ == '__main__':
    print('每次按照基础面额投注')
    # 策略代码
    # alpha = (open_value - DF_BUY.iloc[-1]['close_value']) / DF_BUY.iloc[-1]['close_value']
    # argent = min(DF_BUY.iloc[-1]['argent'] * (1 - alpha), LEFT_ARGENT)
    path_profit = '../data/data_ananlyse/profit_history.xlsx'
    data = pd.read_excel(path_profit)
    buy_value_analyse(data, E_ROI)

    print('基础面额固定，每次根据基础面额上涨和下跌的半分比，选择少买多买多少')
    # 策略代码
    # alpha = (open_value - DF_BUY.iloc[-1]['close_value']) / DF_BUY.iloc[-1]['close_value']
    # argent = min(BUY_FIRST_ARGENT * (1 - alpha), LEFT_ARGENT)
    path_profit = '../data/data_ananlyse/profit_history_die_duo.xlsx'
    data = pd.read_excel(path_profit)
    buy_value_analyse(data, E_ROI)

    print('基础面额固定，每次根据基础面额上涨和下跌的半分比，选择多买少买多少')
    # 策略代码
    # alpha = (open_value - DF_BUY.iloc[-1]['close_value']) / DF_BUY.iloc[-1]['close_value']
    # argent = min(BUY_FIRST_ARGENT * (1 - alpha), LEFT_ARGENT)
    path_profit = '../data/data_ananlyse/profit_history_die_shao.xlsx'
    data = pd.read_excel(path_profit)
    buy_value_analyse(data, E_ROI)

    print('基础面额固定，每次根据上次投注面额上涨和下跌的半分比，选择少买多买多少')
    # 策略代码
    # alpha = (open_value - DF_BUY.iloc[-1]['close_value']) / DF_BUY.iloc[-1]['close_value']
    # argent = min(DF_BUY.iloc[-1]['argent'] * (1 - alpha), LEFT_ARGENT)
    path_profit = '../data/data_ananlyse/profit_history_die_duo_last.xlsx'
    data = pd.read_excel(path_profit)
    buy_value_analyse(data, E_ROI)
