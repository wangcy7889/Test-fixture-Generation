from dask import delayed, compute

def filter_even_numbers_dask(data):
    
    try:
        delayed_task = delayed(lambda x: [num for num in x if num % 2 == 0])(data)
        # Compute the result
        return compute(delayed_task)[0]
    except Exception as e:
        raise ValueError(f"Error in filtering even numbers: {e}")
