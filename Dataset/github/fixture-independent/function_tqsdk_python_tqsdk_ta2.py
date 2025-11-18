import pandas as pd
import numpy as np

def ASI(df):
    lc = df['close'].shift(1)
    aa = np.absolute(df['high'] - lc)
    bb = np.absolute(df['low'] - lc)
    cc = np.absolute(df['high'] - df['low'].shift(1))
    dd = np.absolute(lc - df['open'].shift(1))
    r = np.where((aa > bb) & (aa > cc), aa + bb / 2 + dd / 4, np.where((bb > cc) & (bb > aa), bb + aa / 2 + dd / 4, cc + dd / 4))
    x = df['close'] - lc + (df['close'] - df['open']) / 2 + lc - df['open'].shift(1)
    si = np.where(r == 0, 0, 16 * x / r * np.where(aa > bb, aa, bb))
    new_df = pd.DataFrame(data=list(pd.Series(si).cumsum()), columns=['asi'])
    return new_df