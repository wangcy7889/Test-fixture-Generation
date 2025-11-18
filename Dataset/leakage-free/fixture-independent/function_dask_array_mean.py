import dask.array as da

def calculate_blockwise_mean(data, chunks):

    try:
        dask_array = da.from_array(data, chunks=chunks)
        # Compute the mean blockwise
        block_mean = dask_array.mean().compute()
        return block_mean
    except Exception as e:
        raise ValueError(f"Error computing blockwise mean: {e}")
