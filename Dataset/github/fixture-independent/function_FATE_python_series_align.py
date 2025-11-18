import pandas as pd
from typing import List

def series_to_ndarray(series_obj: 'pd.Series', fields_to_align: List[str]=None):
    if isinstance(series_obj.index, pd.RangeIndex) or not fields_to_align:
        return series_obj.values
    else:
        if len(series_obj) != len(fields_to_align):
            raise ValueError(f"Can't not align fields, src={fields_to_align}, dst={series_obj}")
        indexer = series_obj.index.get_indexer(fields_to_align)
        return series_obj[indexer].values