import pandas as pd
import tushare as ts



data = pd.read_excel('/Users/kunyue/project_personal/share/data/data_market/market_index.xlsx')


data.to_csv('/Users/kunyue/project_personal/share/data/data_market/dd.csv')