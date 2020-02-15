import pandas as pd
import os
import re
import platform
from datetime import datetime

E_ROI = 0.1


# 这个类负责分析策略的好坏，有以下几个方面：
# 策略平均盈利能力,抗风险能力
# 策略牛市盈利能力,抗风险能力
# 策略熊市盈利能力,抗风险能力
# 策略投资大小以及手头可流动资金
# 投资到截止日期的盈利
class FundEvaluator(object):
    def __init__(self, ts_code=None, data_o=None, e_roi=0.1):
        self.e_roi = e_roi
        self.ts_code = ts_code
        self.data = data_o.sort_values(by=['ts_code', 'trade_date'])

    def __basic_value_cal(self, start_date, end_date):
        self.data = self.data[(self.data['trade_date'] >= start_date) & (self.data['trade_date'] <= end_date)]
        self.data['roi_basic'] = (self.data['close'] - self.data.iloc[0]['close']) / self.data.iloc[0]['close']
        self.basic_roi = self.data['roi_basic'].mean()
        self.final_roi = self.data.iloc[-1]['roi_basic']
        self.std_roi = self.data['roi_basic'].std()

    def alpha_beta_cal(self, x):
        self.__basic_value_cal(x.iloc[0]['date'], x.iloc[-1]['date'])
        return x['roi'].mean() - self.basic_roi, x['roi'].std() / self.std_roi

    @staticmethod
    def get_evaluate(x, e_roi):
        final_profit = x.iloc[-1]['profit']
        final_roi = x.iloc[-1]['roi']
        final_invertissment = x.iloc[-1]['invertissment']
        mean_invertissment = x.iloc[-1]['invertissment']/len(x)
        mean_roi = x['roi'].mean()
        std_roi = x['roi'].std()
        num_roi_police = len(x[x['roi'] > e_roi]) / len(x)
        max_loss = x['profit'].min()
        mean_argent_use = x['argent_use_rate'].mean()
        from_to = str(x.iloc[0]['date']) + '_' + str(x.iloc[-1]['date'])
        duree = (datetime.strptime(str(x.iloc[-1]['date']), "%Y%m%d") - datetime.strptime(str(x.iloc[0]['date']), "%Y%m%d")).days
        return pd.DataFrame.from_dict({
            'final_profit': [final_profit],
            'final_roi': [final_roi],
            'final_invertissment': [final_invertissment],
            'mean_invertissment': [mean_invertissment],
            'mean_roi': [mean_roi],
            'std_roi': [std_roi],
            'num_roi_police': [num_roi_police],
            'max_loss': [max_loss],
            'mean_argent_use': [mean_argent_use],
            'from_to': [from_to],
            'duree': [duree]
        })

    def show_details(self, x):
        self.__basic_value_cal(x.iloc[0]['date'], x.iloc[-1]['date'])
        # 利润
        final_profit = x.iloc[-1]['profit']
        # ROI
        final_roi = x.iloc[-1]['roi']
        # 投资金额
        mean_invertissment = x.iloc[-1]['invertissment']
        mean_roi = x['roi'].mean()
        # 符合预期的投入产出比占总的天数
        std_roi = x['roi'].std()
        num_roi_police = len(x[x['roi'] > self.e_roi]) / len(x)
        num_roi_basic = len(self.data['roi_basic'][self.data['roi_basic'] > self.e_roi]) / len(x)
        # 投入产出比的标准差
        # 最多亏损数
        max_loss = x['profit'].min()
        print('final_profit:  ', final_profit)
        print('final_roi:  ', final_roi)
        print('mean_invertissment:  ', mean_invertissment)
        print('mean_roi_police:  ', mean_roi, ',mean_roi_basic:  ', self.basic_roi)
        print('num_roi_police:  ', num_roi_police, ',num_roi_basic:  ', num_roi_basic)
        print('std_roi_police:  ', std_roi, ',std_roi_basic:  ', self.std_roi)
        print('max_loss:  ', max_loss)

    @staticmethod
    def compare(x1, x2):
        return x1['roi'].mean() - x2['roi'].mean(), x1['roi'].std() / x2['roi'].std()

    def bear_market(self, x):
        pass

    def final_profit(self, x):
        pass


def evaluate_all(dir_result):
    result_ev = []
    result_file = []
    for subdir, dirs, files in os.walk(dir_result):
        for file in files:
            open_file = os.path.join(subdir, file)
            if platform.system() == 'Windows':
                file_detail = re.split('\$\$', open_file.split('\\')[-1])
            else:
                file_detail = re.split('\$\$', open_file.split('/')[-1])
            if file_detail[1] == 'profit':
                data = pd.read_excel(open_file)
                one_evaluate = FundEvaluator.get_evaluate(data, 0.1)
                result_ev.append(one_evaluate)
                starting_point = file_detail[0]
                policy = file_detail[2]
                result_file.append(pd.DataFrame.from_dict({'policy': [policy], 'starting_point': [starting_point]}))
    if (len(result_ev) > 0) & (len(result_ev) == len(result_file)):
        df_ev = pd.concat(result_ev)
        df_file = pd.concat(result_file)
        df_result = pd.concat([df_file, df_ev], axis=1)
        return df_result
    return None


if __name__ == '__main__':
    data_output = '../data/data_analyse_result/result.xlsx'
    result = evaluate_all('../data/data_ananlyse/')
    print(result)
    result.to_excel(data_output)
    #
    # path_data = '../data/data_market/market_value.csv'
    # data_o = pd.read_csv(path_data)
    # data_o = data_o[data_o['ts_code'] == '000300.SH']
    # fe = FundEvaluator('000300.SH', data_o)
    # path_input = '../data/data_ananlyse/_buy_fv_3_sold_fv_new/max_0$$profit$$_buy_fv_3__sold_fv_new$$.xlsx'
    # data = pd.read_excel(path_input)
    # alpha, beta = fe.alpha_beta_cal(data)
    # print('alpha: ', alpha)
    # print('beta: ', beta)
    # fe.show_details(data)
    #
    # path_input = '../data/data_ananlyse/_buy_fv_3_sold_fv/max_0$$profit$$_buy_fv_3__sold_fv$$.xlsx'
    # data2 = pd.read_excel(path_input)
    #
    # alpha, beta = fe.compare(data, data2)
    # print('alpha: ', alpha)
    # print('beta: ', beta)

    # buy_value_analyse(data_police,0.1)
