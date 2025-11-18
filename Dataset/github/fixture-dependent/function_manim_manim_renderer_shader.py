from __future__ import annotations
import numpy as np

def filter_attributes(unfiltered_attributes, attributes):
    filtered_attributes_dtype = []
    for i, dtype_name in enumerate(unfiltered_attributes.dtype.names):
        if dtype_name in attributes:
            filtered_attributes_dtype.append((dtype_name, unfiltered_attributes.dtype[i].subdtype[0].str, unfiltered_attributes.dtype[i].shape))
    filtered_attributes = np.zeros(unfiltered_attributes[unfiltered_attributes.dtype.names[0]].shape[0], dtype=filtered_attributes_dtype)
    for dtype_name in unfiltered_attributes.dtype.names:
        if dtype_name in attributes:
            filtered_attributes[dtype_name] = unfiltered_attributes[dtype_name]
    return filtered_attributes