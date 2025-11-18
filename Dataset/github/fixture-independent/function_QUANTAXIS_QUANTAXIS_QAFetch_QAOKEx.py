import datetime
import time
import pandas as pd
import numpy as np
column_names = ['time', 'open', 'high', 'low', 'close', 'volume']
OKEx2QA_FREQUENCY_DICT = {'60': '1min', '300': '5min', '900': '15min', '1800': '30min', '3600': '60min', '86400': 'day'}

def format_okex_data_fields(datas, symbol, frequency):
    frame = pd.DataFrame(datas, columns=column_names)
    frame['symbol'] = 'OKEX.{}'.format(symbol)
    frame['time_stamp'] = pd.to_datetime(frame['time']).astype(np.int64) // 10 ** 9
    frame['datetime'] = pd.to_datetime(frame['time_stamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')
    frame['date'] = frame['datetime'].dt.strftime('%Y-%m-%d')
    frame['date_stamp'] = pd.to_datetime(frame['date']).dt.tz_localize('Asia/Shanghai').astype(np.int64) // 10 ** 9
    frame['datetime'] = frame['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    frame['created_at'] = int(time.mktime(datetime.datetime.now().utctimetuple()))
    frame['updated_at'] = int(time.mktime(datetime.datetime.now().utctimetuple()))
    frame.drop(['time'], axis=1, inplace=True)
    frame['trade'] = 1
    frame['amount'] = frame.apply(lambda x: float(x['volume']) * (float(x['open']) + float(x['close'])) / 2, axis=1)
    if frequency not in ['1day', 'day', '86400', '1d']:
        frame['type'] = OKEx2QA_FREQUENCY_DICT[frequency]
    return frame