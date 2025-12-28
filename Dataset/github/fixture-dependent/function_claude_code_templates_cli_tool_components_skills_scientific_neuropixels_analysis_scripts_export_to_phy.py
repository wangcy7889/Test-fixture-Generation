from pathlib import Path
import spikeinterface.full as si
from spikeinterface.exporters import export_to_phy
def export_phy(
    analyzer_path: str,
    output_dir: str,
    copy_binary: bool = True,
    compute_amplitudes: bool = True,
    compute_pc_features: bool = True,
    n_jobs: int = -1,
):
    print(f"Loading analyzer from: {analyzer_path}")
    analyzer = si.load_sorting_analyzer(analyzer_path)
    print(f"Units: {len(analyzer.sorting.unit_ids)}")
    output_path = Path(output_dir)
    if compute_amplitudes and analyzer.get_extension('spike_amplitudes') is None:
        print("Computing spike amplitudes...")
        analyzer.compute('spike_amplitudes')

    if compute_pc_features and analyzer.get_extension('principal_components') is None:
        print("Computing principal components...")
        analyzer.compute('principal_components', n_components=5, mode='by_channel_local')

    print(f"Exporting to Phy: {output_path}")
    export_to_phy(
        analyzer,
        output_folder=output_path,
        copy_binary=copy_binary,
        compute_amplitudes=compute_amplitudes,
        compute_pc_features=compute_pc_features,
        n_jobs=n_jobs,
    )

    print("\nExport complete!")
    print(f"To open in Phy, run:")
    print(f"  phy template-gui {output_path / 'params.py'}")
