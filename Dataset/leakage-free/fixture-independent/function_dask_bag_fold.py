from dask import bag

def cumulative_sum(input_list):
    
    try:
        dask_bag = bag.from_sequence(input_list)

        result = dask_bag.fold(lambda x, y: x + y).compute()
        return result
    except Exception as e:
        raise ValueError(f"Error in computing cumulative sum: {e}")
