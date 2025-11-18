import datetime
import time
import pandas as pd
import numpy as np
Bitmex2QA_FREQUENCY_DICT = {'1m': '1min', '5m': '5min', '15m': '15min', '30m': '30min', '60m': '60min', '1h': '60min', '1d': 'day'}

def format_btimex_data_fields(datas, frequency):
    frame = pd.DataFrame(datas)
    frame['symbol'] = frame['symbol'].apply(lambda x: 'BITMEX.{}'.format(x))
    frame['datetime'] = pd.to_datetime(frame['timestamp'], utc=False)
    frame['date'] = frame['datetime'].dt.strftime('%Y-%m-%d')
    frame['datetime'] = frame['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    frame['time_stamp'] = pd.to_datetime(frame['timestamp']).astype(np.int64) // 10 ** 9
    frame['date_stamp'] = pd.to_datetime(frame['date']).astype(np.int64) // 10 ** 9
    frame['created_at'] = int(time.mktime(datetime.datetime.now().utctimetuple()))
    frame['updated_at'] = int(time.mktime(datetime.datetime.now().utctimetuple()))
    frame.rename({'trades': 'trade'}, axis=1, inplace=True)
    frame['amount'] = frame['volume'] * (frame['open'] + frame['close']) / 2
    frame.drop(['foreignNotional', 'homeNotional', 'lastSize', 'timestamp', 'turnover', 'vwap'], axis=1, inplace=True)
    if frequency not in ['1day', Bitmex2QA_FREQUENCY_DICT['1d'], '1d']:
        frame['type'] = Bitmex2QA_FREQUENCY_DICT[frequency]
    return frame