import pandas as pd
import traceback

def PPSR(df, p):
    try:
        PP = pd.Series((df['high'] + df['low'] + df['close']) / 3)
        R1 = pd.Series(2 * PP - df['low'])
        S1 = pd.Series(2 * PP - df['high'])
        R2 = pd.Series(PP + df['high'] - df['low'])
        S2 = pd.Series(PP - df['high'] + df['low'])
        R3 = pd.Series(df['high'] + 2 * (PP - df['low']))
        S3 = pd.Series(df['low'] - 2 * (df['high'] - PP))
        psr = {'PP': PP, 'R1': R1, 'S1': S1, 'R2': R2, 'S2': S2, 'R3': R3, 'S3': S3}
        PSR = pd.DataFrame(psr)
        if PSR.empty:
            return df
        overlap_cols = df.columns.intersection(PSR.columns)
        df = df.drop(columns=overlap_cols)
        df = df.join(PSR)
        df['PPSR'] = df.PP
        df['PPR1'] = df.R1
        df['PPS1'] = df.S1
        df['PPR2'] = df.R2
        df['PPS2'] = df.S2
        df['PPR3'] = df.R3
        df['PPS3'] = df.S3
        return df
    except Exception as e:
        print(df)
        print(df.columns)
        print(PSR)
        traceback.print_exc()
        return df