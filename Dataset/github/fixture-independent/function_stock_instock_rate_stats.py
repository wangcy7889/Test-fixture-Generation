import logging
import numpy as np
import pandas as pd
__author__ = 'myh '
__date__ = '2023/3/10 '

def get_rates(code_name, data, stock_column, threshold=101):
    try:
        if data is None:
            return None
        start_date = code_name[0]
        code = code_name[1]
        stock_data_list = [start_date, code]
        mask = data['date'] >= start_date
        data = data.loc[mask].copy()
        data = data.head(n=threshold)
        if len(data.index) <= 1:
            return None
        close1 = data.iloc[0]['close']
        data.loc[:, 'sum_pct_change'] = np.around(100 * (data['close'].values - close1) / close1, decimals=2)
        first = True
        col_len = len(data.columns)
        for row in data.values:
            if first:
                first = False
            else:
                stock_data_list.append(row[col_len - 1])
        _l = len(stock_column) - len(stock_data_list)
        for i in range(0, _l):
            stock_data_list.append(None)
    except Exception as e:
        logging.error(f'rate_stats.get_rates处理异常：{code}代码{e}')
    return pd.Series(stock_data_list, index=stock_column)