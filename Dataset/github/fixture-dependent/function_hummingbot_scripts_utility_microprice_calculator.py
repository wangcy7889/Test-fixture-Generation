import datetime
import os
import pandas as pd

def get_csv_path(self):
    files = os.listdir(self.path_to_data)
    for i in files:
        if i.startswith(f'microprice_{self.trading_pair}_{self.exchange}'):
            len_data = len(pd.read_csv(f'{self.path_to_data}/{i}', index_col=[0]))
            if len_data > self.data_size_min:
                return f'{self.path_to_data}/{i}'
    return f"{self.path_to_data}/microprice_{self.trading_pair}_{self.exchange}_{datetime.datetime.now().strftime('%Y-%m-%d')}.csv"