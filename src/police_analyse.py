import pandas as pd

E_ROI = 0.1


# 这个类负责分析策略的好坏，有以下几个方面：
# 策略平均盈利能力,抗风险能力
# 策略牛市盈利能力,抗风险能力
# 策略熊市盈利能力,抗风险能力
# 策略投资大小以及手头可流动资金
# 投资到截止日期的盈利
class FundEvaluator(object):
    def __init__(self, ts_code,data_o,e_roi=0.1):
        self.e_roi = e_roi
        self.ts_code = ts_code
        self.data = data_o
        self.__basic_value_cal()

    def __basic_value_cal(self):
        self.data['roi_basic'] = (self.data['close_value'] - self.data.iloc[0]['close_value']) / self.data.iloc[0]['close_value']
        self.basic_roi = self.data['roi_basic'].mean()
        self.final_roi = self.data.iloc[-1]['roi_basic']
        self.std_roi = self.data['roi_basic'].std()

    def alpha_beta_cal(self):
        x = self.data
        return x['roi'].mean() - self.basic_roi, x['roi'].std() / self.std_roi

    def show_details(self):
        x = self.data
        # 利润
        final_profit = x.iloc[-1]['profit']
        # ROI
        final_roi = x.iloc[-1]['roi']
        # 投资金额
        mean_invertissment = x.iloc[-1]['invertissment']
        mean_roi = x['roi'].mean()
        # 符合预期的投入产出比占总的天数
        num_roi_police = len(x[x['roi'] > self.e_roi]) / len(x)
        num_roi_basic = len(x[x['roi_basic'] > self.e_roi]) / len(x)
        # 投入产出比的标准差
        std_roi = x['roi'].std()
        # 最多亏损数
        max_loss = x['profit'].min()
        print('final_profit:  ', final_profit)
        print('final_roi:  ', final_roi)
        print('mean_invertissment:  ', mean_invertissment)
        print('mean_roi_police:  ', mean_roi,',mean_roi_basic:  ',self.basic_roi)
        print('num_roi_police:  ', num_roi_police,',num_roi_basic:  ',num_roi_basic)
        print('std_roi_police:  ', std_roi,',std_roi_basic:  ',self.std_roi)
        print('max_loss:  ', max_loss)

    def bull_market(self, x):
        pass

    def bear_market(self, x):
        pass

    def final_profit(self, x):
        pass


# 这个函数负责分析每次买多少的策略进行评估：
# 收益率平均值：mean_profit
# 投资总计收入: final_profit
# ROI稳定在10%以上的天数：num_roi
# ROI是多少: mean_roi
# 手中流动资金平均值: mean_argent_main
# roi波动: std_roi
# 最大赔钱: max_loss
# 手中流动资金最小值: min_argent_main




if __name__ == '__main__':


    path_input = '../data/data_ananlyse/profit_history_2000_015_ban.xlsx'
    data = pd.read_excel(path_input)
    fe = FundEvaluator('000300.SH',  data)
    alpha, beta = fe.alpha_beta_cal()
    print('alpha: ',alpha)
    print('beta: ',beta)
    fe.show_details()

    # buy_value_analyse(data_police,0.1)



