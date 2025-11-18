import os
import dask.dataframe as dd


def csv_directory_to_parquet_csvinput(input_dir_obj, output_dir_obj, storage_options=None):

    if (isinstance(input_dir_obj, str) or isinstance(output_dir_obj, str) or
            not isinstance(input_dir_obj, os.PathLike) or not isinstance(output_dir_obj, os.PathLike)):
        raise TypeError("Error: The parameters must be implemented os.PathLike The custom object cannot be of string type.")


    input_dir = os.fspath(input_dir_obj)
    output_dir = os.fspath(output_dir_obj)


    if not os.path.isdir(input_dir):
        raise FileNotFoundError(f"Error: The input directory does not exist: {input_dir}")


    csv_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir)
                 if isinstance(f, str) and f.lower().endswith('.csv') and os.path.isfile(os.path.join(input_dir, f))]
    if not csv_files:
        raise ValueError("Error: The input directory does not find CSV file")


    try:
        df = dd.read_csv(csv_files, assume_missing=True, storage_options=storage_options)
    except Exception as e:
        raise ValueError(f"Error: read CSV file failed: {e}")


    try:
        dd.to_parquet(df, output_dir, write_index=False, storage_options=storage_options)
    except Exception as e:
        raise ValueError(f"Error: write Parquet failed: {e}")


    try:
        files = [os.path.join(output_dir, f) for f in os.listdir(output_dir)
                 if f.endswith('.parquet')]
        return files
    except Exception:
        return []


