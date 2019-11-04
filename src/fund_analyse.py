import pandas as pd





# 全部买卖指数基金，追求10%的收益
def all_buy_all_sold():
    pass




if __name__ == '__main__':
    # 把我要分析的基金涉及到的指数拿出来
    path_jj_buy = '../data/data_jijin/jijin_analyse_sort_p5_buy_20191029.xlsx'
    df_fund_basic = pd.read_excel(path_jj_buy)
    l_market = df_fund_basic['benchmark_format'].unique()
    print(l_market)
    path_market_all = '../data/data_market/market_index.xlsx'
    df_market_all = pd.read_excel(path_market_all)



