import pandas as pd

def _QA_data_stock_to_fq(bfq_data, xdxr_data, fqtype):
    info = xdxr_data.query('category==1')
    bfq_data = bfq_data.assign(if_trade=1)
    if len(info) > 0:
        data = pd.concat([bfq_data, info.loc[bfq_data.index[0]:bfq_data.index[-1], ['category']]], axis=1)
        data['if_trade'].fillna(value=0, inplace=True)
        data = data.fillna(method='ffill')
        data = pd.concat([data, info.loc[bfq_data.index[0]:bfq_data.index[-1], ['fenhong', 'peigu', 'peigujia', 'songzhuangu']]], axis=1)
    else:
        data = pd.concat([bfq_data, info.loc[:, ['category', 'fenhong', 'peigu', 'peigujia', 'songzhuangu']]], axis=1)
    data = data.fillna(0)
    data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] + data['peigu'] * data['peigujia']) / (10 + data['peigu'] + data['songzhuangu'])
    if fqtype in ['01', 'qfq']:
        data['adj'] = (data['preclose'].shift(-1) / data['close']).fillna(1)[::-1].cumprod()
    else:
        data['adj'] = (data['close'] / data['preclose'].shift(-1)).cumprod().shift(1).fillna(1)
    for col in ['open', 'high', 'low', 'close', 'preclose']:
        data[col] = data[col] * data['adj']
    data['volume'] = data['volume'] if 'volume' in data.columns else data['vol']
    try:
        data['high_limit'] = data['high_limit'] * data['adj']
        data['low_limit'] = data['low_limit'] * data['adj']
    except:
        pass
    return data.query('if_trade==1 and open != 0').drop(['fenhong', 'peigu', 'peigujia', 'songzhuangu', 'if_trade', 'category'], axis=1, errors='ignore')