from pathlib import Path
import pandas as pd
def read_gene_list(file_path):
    file_path = Path(file_path)
    if file_path.suffix == ".csv":
        df = pd.read_csv(file_path)
        genes = df.iloc[:, 0].tolist()
    else:
        with open(file_path, "r") as f:
            genes = [line.strip() for line in f if line.strip()]
    return genes
