import argparse
import gzip
from pathlib import Path

import correctionlib.convert
import correctionlib.schemav2
import uproot


def _choose_histogram(root_file: Path, preferred_hist: str) -> str:
    with uproot.open(root_file) as f:
        keys = [k.split(";")[0] for k in f.keys()]
    if preferred_hist in keys:
        return preferred_hist
    candidates = [k for k in keys if k.endswith("_efficiencyData")]
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        raise ValueError(
            f"Found multiple *_efficiencyData histograms in {root_file}: {candidates}. "
            "Please pass --hist-name explicitly."
        )
    raise ValueError(
        f"Histogram '{preferred_hist}' not found and no unique *_efficiencyData candidate in {root_file}."
    )


def convert_root_hist_to_correction(
    root_file: Path,
    hist_name: str,
    output_name: str,
    correction_name: str,
    description: str,
) -> Path:
    hist_name = _choose_histogram(root_file, hist_name)
    correction = correctionlib.convert.from_uproot_THx(
        path=f"{root_file}:{hist_name}",
        axis_names=["eta", "pt"],
    )
    correction.name = correction_name
    correction.description = description
    correction.data.flow = "clamp"

    cset = correctionlib.schemav2.CorrectionSet(
        schema_version=2,
        description=f"HLT efficiency from {root_file.name}",
        corrections=[correction],
    )

    out_json = root_file.parent / output_name
    payload = cset.json(exclude_unset=True)

    with out_json.open("w") as fout:
        fout.write(payload)

    with gzip.open(f"{out_json}.gz", "wt") as fout:
        fout.write(payload)

    return out_json


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a ROOT TH2 trigger efficiency histogram to correctionlib JSON."
    )
    parser.add_argument(
        "--root-file",
        default="data/hlt_eff/2024/NUM_IsoMu24_DEN_TightID_and_PFIsoTight_eta_pt.root",
        help="Path to input ROOT file.",
    )
    parser.add_argument(
        "--hist-name",
        default="NUM_IsoMu24_DEN_TightID_and_PFIsoTight_eta_pt_efficiencyMC",
        help="Histogram name inside ROOT file.",
    )
    parser.add_argument(
        "--output-name",
        default="trigger_eff_2024.json",
        help="Output JSON file name (placed in the same folder as the ROOT file).",
    )
    parser.add_argument(
        "--correction-name",
        default="NUM_IsoMu24_DEN_TightID_and_PFIsoTight_eta_pt_efficiencyMC",
        help="Name used inside correctionlib JSON.",
    )
    parser.add_argument(
        "--description",
        default="Single-muon trigger efficiency for fsim trigger emulation",
        help="Correction description field.",
    )

    args = parser.parse_args()
    root_file = Path(args.root_file)
    if not root_file.exists():
        raise FileNotFoundError(f"ROOT file not found: {root_file}")

    out_json = convert_root_hist_to_correction(
        root_file=root_file,
        hist_name=args.hist_name,
        output_name=args.output_name,
        correction_name=args.correction_name,
        description=args.description,
    )

    print(f"Converted ROOT histogram to JSON: {out_json}")
    print(f"Compressed copy: {out_json}.gz")


if __name__ == "__main__":
    main()
