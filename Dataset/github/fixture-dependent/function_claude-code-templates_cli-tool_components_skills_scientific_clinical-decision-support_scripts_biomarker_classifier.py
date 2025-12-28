import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
def stratify_cohort_report(data, stratification_var, output_dir='stratification_report'):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"\nCOHORT STRATIFICATION REPORT")
    print("="*60)
    print(f"Stratification Variable: {stratification_var}")
    print(f"Total Patients: {len(data)}")
    distribution = data[stratification_var].value_counts()
    print(f"\nGroup Distribution:")
    for group, count in distribution.items():
        pct = count / len(data) * 100
        print(f"  {group}: {count} ({pct:.1f}%)")
    distribution.to_csv(output_dir / 'group_distribution.csv')
    print(f"\nBaseline Characteristics by {stratification_var}:")
    results = []
    continuous_vars = data.select_dtypes(include=[np.number]).columns.tolist()
    continuous_vars = [v for v in continuous_vars if v != stratification_var]
    for var in continuous_vars[:5]:
        print(f"\n{var}:")
        for group in distribution.index:
            group_data = data[data[stratification_var] == group][var].dropna()
            print(f"  {group}: median {group_data.median():.1f} [IQR {group_data.quantile(0.25):.1f}-{group_data.quantile(0.75):.1f}]")
        if len(distribution) == 2:
            groups_list = distribution.index.tolist()
            g1 = data[data[stratification_var] == groups_list[0]][var].dropna()
            g2 = data[data[stratification_var] == groups_list[1]][var].dropna()
            _, p_value = stats.mannwhitneyu(g1, g2, alternative='two-sided')
            print(f"  p-value: {p_value:.4f}")
            results.append({
                'Variable': var,
                'Test': 'Mann-Whitney U',
                'p_value': p_value,
                'Significant': 'Yes' if p_value < 0.05 else 'No'
            })
    if results:
        df_results = pd.DataFrame(results)
        df_results.to_csv(output_dir / 'statistical_comparisons.csv', index=False)
        print(f"\nStatistical comparison results saved to: {output_dir}/statistical_comparisons.csv")
    print(f"\nStratification report complete! Files saved to {output_dir}/")
