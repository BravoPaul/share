import pandas as pd
import tushare as ts
import time


def fund_basic_download(path_output):
    pro = ts.pro_api()
    df_changnei = pro.fund_basic(market='E')
    df_changwai = pro.fund_basic(market='O')
    df_jj = pd.concat([df_changnei, df_changwai])
    df_jj.to_excel(path_output)


def fund_value_download(fund_code):
    pro = ts.pro_api()
    while(True):
        try:
            df = pro.fund_nav(ts_code=fund_code)
            return df
        except:
            time.sleep(60)


def market_basic_download(market_code):
    pro = ts.pro_api()
    df = pro.index_basic(market=market_code)
    return df



if __name__ == '__main__':
    # 下载基金的基本数据
    # path_jj = '../data/data_jijin/jijin_20191029.xlsx'
    # fund_basic_download(path_jj)

    # 下载已经选出来的基金的每天的净值数据
    # path_jj_basic = '../data/data_jijin/jijin_analyse_sort_p5_buy_20191029.xlsx'
    # data_jj = pd.read_excel(path_jj_basic)
    # jj_codes = data_jj['ts_code'].values
    # list_jj_value = []
    # for one_code in jj_codes:
    #     df = fund_value_download(one_code)
    #     list_jj_value.append(df)
    # data_jj_value = pd.concat(list_jj_value)
    # path_jj_value = '../data/data_jijin/jijin_analyse_sort_p5_buy_value_20191029.xlsx'
    # data_jj_value.to_excel(path_jj_value)

    # 下载常见的指数，比较各个指数间的不同的差异
    market_list = ['MSCI','CSI','SSE','SZSE','CICC','SW']
    df_list = []
    for one_m in market_list:
        df_list.append(market_basic_download(one_m))
    result = pd.concat(df_list)
    path_output = '../data/data_market/market_index.xlsx'
    result.to_excel(path_output)


