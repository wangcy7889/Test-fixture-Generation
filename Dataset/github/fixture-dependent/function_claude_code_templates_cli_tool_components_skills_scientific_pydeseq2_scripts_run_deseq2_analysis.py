import pandas as pd
def load_and_validate_data(counts_path, metadata_path, transpose_counts=True):
    print(f"Loading count data from {counts_path}...")
    counts_df = pd.read_csv(counts_path, index_col=0)
    if transpose_counts:
        print("Transposing count matrix to samples × genes format...")
        counts_df = counts_df.T

    print(f"Loading metadata from {metadata_path}...")
    metadata = pd.read_csv(metadata_path, index_col=0)
    print(f"\nData loaded:")
    print(f"  Counts shape: {counts_df.shape} (samples × genes)")
    print(f"  Metadata shape: {metadata.shape} (samples × variables)")
    if not all(counts_df.index == metadata.index):
        print("\nWarning: Sample indices don't match perfectly. Taking intersection...")
        common_samples = counts_df.index.intersection(metadata.index)
        counts_df = counts_df.loc[common_samples]
        metadata = metadata.loc[common_samples]
        print(f"  Using {len(common_samples)} common samples")
    if (counts_df < 0).any().any():
        raise ValueError("Count matrix contains negative values")

    return counts_df, metadata
