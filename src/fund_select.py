import pandas as pd
import re


def fund_cate(one_data):
    if one_data['invest_type'] == '被动指数型' and one_data['fund_type'] == '股票型':
        matchObj = re.findall(r'(.*?)\*([0-9]+)%', one_data['benchmark'])
        if len(matchObj) >= 2:
            sort_match = sorted(matchObj, key=lambda item: int(item[1]), reverse=True)
            if int(sort_match[0][1]) >= 80:
                return sort_match[0][0]
            else:
                return one_data['benchmark']
        else:
            return one_data['benchmark']
    else:
        return False


if __name__ == '__main__':
    ###------------因为我只看被动型指数基金，所以这里只分析指数基金就可以了----------------###
    ###-------- 只有指数股票型基金的表为：jijin_analyse_20191029.xlsx

    # path_jj = '../data/data_jijin/jijin_20191029.xlsx'
    # data = pd.read_excel(path_jj)
    # data['benchmark_format'] = data.apply(fund_cate, axis=1)
    # path_output = '../data/data_jijin/jijin_format_20191029.xlsx'
    # data.to_excel(path_output)
    # data_analyse = data[data['benchmark_format']!=False]
    # data_analyse['benchmark_format'] = data_analyse['benchmark_format'].map(lambda x: x if x[-3:]!='收益率' else x[0:-3])
    # path_output = '../data/data_jijin/jijin_analyse_20191029.xlsx'
    # data_analyse.to_excel(path_output,index=False)

    ##--------------------对指数股票型基金进行分析1,目的是通过指数的被跟踪数再过滤一批---------------------------
    # 目前有1255只股票型被动指数型基金
    # 一共跟踪425种指数
    # path_input = '../data/data_jijin/jijin_analyse_20191029.xlsx'
    # data = pd.read_excel(path_input)
    # print(len(data['benchmark_format'].unique()))
    # # 我们只分析跟踪的相对多的指数，太小众的指数就不分析了。
    # bench_count = data.groupby(['benchmark_format'])['benchmark_format'].count().rename('c_benchmark')
    # data_org = pd.merge(data,bench_count,how='inner',on=['benchmark_format'])
    # data_org = data_org.sort_values(by=['c_benchmark','benchmark_format'],ascending=False)
    # path_output = '../data/data_jijin/jijin_analyse_sort_20191029.xlsx'
    # # 根据追踪指数被追踪的多少进行排序
    # data_org.to_excel(path_output)
    # data_select = data_org[data_org['c_benchmark'] > 5]
    # path_output = '../data/data_jijin/jijin_analyse_sort_p5_20191029.xlsx'
    # # 只选出被跟踪的多的指数，和跟踪他们的基金
    # data_select.to_excel(path_output)

    ##--------------------对指数股票型基金进行分析2,目的是分析被跟踪的多的指数，大于5的跟踪数的基金--------------------
    # 目前有41种指数是被5个基金以上跟踪的
    # 跟踪这41中指数的基金有529只,而可以用于分析的，也就是说从17年9月到现在还上市的仅仅361只
    path_input = '../data/data_jijin/jijin_analyse_sort_p5_20191029.xlsx'
    data = pd.read_excel(path_input)
    data = data.fillna(-1)
    # 我要分析募集自己大，而且现在仍然在上市中的基金
    data_select = data[(data['issue_amount']>1) & (data['delist_date']==-1) & (data['min_amount']<=0.1)]
    path_output = '../data/data_jijin/jijin_analyse_sort_p5_buy_20191029.xlsx'
    data_select.to_excel(path_output)


