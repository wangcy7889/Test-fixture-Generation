import pandas as pd
from pandas.tseries.frequencies import to_offset

def QA_data_min_resample(min_data, type_='5min'):
    CONVERSION = {'code': 'first', 'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'vol': 'sum', 'amount': 'sum'} if 'vol' in min_data.columns else {'code': 'first', 'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum', 'amount': 'sum'}
    min_data = min_data.loc[:, list(CONVERSION.keys())]
    idx = min_data.index
    part_1 = min_data.iloc[idx.indexer_between_time('9:30', '11:30')]
    part_1_res = part_1.resample(type_, offset='30min', closed='right').apply(CONVERSION)
    part_1_res.index = part_1_res.index + to_offset(type_)
    part_2 = min_data.iloc[idx.indexer_between_time('13:00', '15:00')]
    part_2_res = part_2.resample(type_, offset='0min', closed='right').agg(CONVERSION)
    part_2_res.index = part_2_res.index + to_offset(type_)
    part_1_res['type'] = part_2_res['type'] = type_ if type_ != '1D' else 'day'
    return pd.concat([part_1_res, part_2_res]).dropna().sort_index().reset_index().set_index(['datetime', 'code'])