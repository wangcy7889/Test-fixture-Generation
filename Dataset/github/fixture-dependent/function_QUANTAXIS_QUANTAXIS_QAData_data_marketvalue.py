import pandas as pd

def QA_data_calc_marketvalue(data, xdxr):
    mv = xdxr.query('category!=6').loc[:, ['shares_after', 'liquidity_after']].dropna()
    res = pd.concat([data, mv], axis=1)
    res = res.assign(shares=res.shares_after.groupby(level=1).fillna(method='ffill'), lshares=res.liquidity_after.groupby(level=1).fillna(method='ffill')).sort_index()
    return res.assign(mv=res.close * res.shares * 10000, liquidity_mv=res.close * res.lshares * 10000).drop(['shares_after', 'liquidity_after'], axis=1).loc[(slice(data.index.remove_unused_levels().levels[0][0], data.index.remove_unused_levels().levels[0][-1]), slice(None)), :]