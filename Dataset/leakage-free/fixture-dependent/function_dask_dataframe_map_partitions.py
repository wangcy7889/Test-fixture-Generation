import dask.dataframe as dd


def compute_partition_means(data, column):
    if not isinstance(data, dd.DataFrame):
        raise ValueError("Error: Input data must be a Dask DataFrame.")

    if column not in data.columns:
        raise ValueError(f"Error: Column '{column}' not found in the DataFrame.")

    try:
        partition_means = data.map_partitions(lambda df: df[column].mean()).compute()
        return partition_means.tolist()
    except Exception as e:
        raise ValueError(f"Error in computing partition means: {e}")
