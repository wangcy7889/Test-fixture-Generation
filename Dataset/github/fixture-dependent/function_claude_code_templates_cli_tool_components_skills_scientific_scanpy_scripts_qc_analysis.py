import scanpy as sc
def calculate_qc_metrics(adata, mt_threshold=5, min_genes=200, min_cells=3):
    adata.var['mt'] = adata.var_names.str.startswith(('MT-', 'mt-', 'Mt-'))
    sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], percent_top=None,
                                log1p=False, inplace=True)
    print("\n=== QC Metrics Summary ===")
    print(f"Total cells: {adata.n_obs}")
    print(f"Total genes: {adata.n_vars}")
    print(f"Mean genes per cell: {adata.obs['n_genes_by_counts'].mean():.2f}")
    print(f"Mean counts per cell: {adata.obs['total_counts'].mean():.2f}")
    print(f"Mean mitochondrial %: {adata.obs['pct_counts_mt'].mean():.2f}")

    return adata
