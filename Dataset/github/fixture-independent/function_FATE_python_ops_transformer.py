import pandas as pd
import numpy as np

def transform_block_to_list(blocks, fields_loc):
    if blocks[0].shape[0] == 0:
        return []
    i = 0
    dst_list = None
    lines = 0
    while i < len(fields_loc):
        bid = fields_loc[i][0]
        if isinstance(blocks[bid], pd.Index):
            if not dst_list:
                lines = len(blocks[bid])
                dst_list = [[] for i in range(lines)]
            for j in range(lines):
                dst_list[j].append(blocks[bid][j])
            i += 1
        else:
            indexes = [fields_loc[i][1]]
            j = i + 1
            while j < len(fields_loc) and fields_loc[j] == fields_loc[j - 1]:
                indexes.append(fields_loc[j][1])
                j += 1
            if isinstance(blocks[bid], np.ndarray):
                for line_id, row_value in enumerate(blocks[bid][:, indexes]):
                    dst_list[line_id].extend(row_value.tolist())
            else:
                try:
                    for line_id, row_value in enumerate(blocks[bid][:, indexes].tolist()):
                        dst_list[line_id].extend(row_value)
                except Exception as e:
                    assert 1 == 2, (e, type(blocks[bid]), indexes)
            i = j
    return dst_list