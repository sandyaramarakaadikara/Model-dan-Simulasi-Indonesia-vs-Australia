"""Summarize cross-country distributions and direction concordance.

Uses the two existing five-year comparison tables. These are descriptive
summaries only; no significance tests or causal estimates are produced.
"""
from pathlib import Path
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

def resolve_input(filename: str) -> Path:
    for candidate in [DATA_PROCESSED_DIR / filename, PROJECT_ROOT / filename, SCRIPT_DIR / filename]:
        if candidate.exists():
            return candidate
    return DATA_PROCESSED_DIR / filename

MAIN = pd.read_csv(resolve_input("panel_perbandingan_dua_periode_14negara.csv"))
SENS = pd.read_csv(resolve_input("sensitivity_panel_2015_2024.csv"))

specs = [
    ("2016-2020 vs 2021-2025", MAIN, {
        "expenditure_change_pct": "exp_change_pct",
        "burden_change_percentage_points": "burden_change_pp",
        "WDI_arms_imports_change_pct": "arms_imports_change_pct_only_if_5yr_complete",
    }),
    ("2015-2019 vs 2020-2024 (overlapping sensitivity)", SENS, {
        "expenditure_change_pct": "exp_change_pct",
        "burden_change_percentage_points": "burden_change_pp",
        "WDI_arms_imports_change_pct": "arms_imports_change_pct_only_if_5yr_complete",
    }),
]

dist = []
directions = []
for window, data, cols in specs:
    for indicator, col in cols.items():
        values = data[col].dropna()
        dist.append({
            "window": window, "indicator": indicator, "n_countries": len(values),
            "median": values.median(), "q1": values.quantile(.25),
            "q3": values.quantile(.75), "minimum": values.min(), "maximum": values.max(),
            "n_increase": int((values > 0).sum()), "n_decrease": int((values < 0).sum()),
            "n_no_change": int((values == 0).sum()),
        })
    exp_col = cols["expenditure_change_pct"]
    arms_col = cols["WDI_arms_imports_change_pct"]
    paired = data[data[arms_col].notna()].copy()
    def direction(x):
        return "increase" if x > 0 else ("decrease" if x < 0 else "no_change")
    paired["expenditure_direction"] = paired[exp_col].map(direction)
    paired["arms_imports_direction"] = paired[arms_col].map(direction)
    counts = paired.groupby(["expenditure_direction", "arms_imports_direction"]).size()
    all_pairs = [(a, b) for a in ["increase", "decrease", "no_change"]
                 for b in ["increase", "decrease", "no_change"]]
    for exp_dir, arms_dir in all_pairs:
        directions.append({
            "window": window, "paired_countries_n": len(paired),
            "expenditure_direction": exp_dir, "arms_imports_direction": arms_dir,
            "country_count": int(counts.get((exp_dir, arms_dir), 0)),
        })

DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
pd.DataFrame(dist).to_csv(DATA_PROCESSED_DIR / "ringkasan_distribusi_perubahan_negara_2026-10-24.csv",
                          index=False, encoding="utf-8-sig")
pd.DataFrame(directions).to_csv(DATA_PROCESSED_DIR / "tabulasi_kesesuaian_arah_belanja_impor_2026-10-24.csv",
                                index=False, encoding="utf-8-sig")
print(pd.DataFrame(dist).round(3).to_string(index=False))
print("Direction tables written for both windows.")
