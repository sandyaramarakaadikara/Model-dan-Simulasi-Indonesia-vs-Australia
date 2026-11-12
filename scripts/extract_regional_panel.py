"""Build a provenance-preserving 14-country WDI/SIPRI panel (2010-2025).

The military personnel series is sourced from WDI and is not extrapolated;
its latest year in the downloaded vintage is 2020. Output includes missing
values and source metadata so analysts can select a defensible study window.
"""

import csv
import json
from pathlib import Path

from openpyxl import load_workbook

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DOCS_AUDIT_DIR = PROJECT_ROOT / "docs" / "audit"

def find_input(filename: str) -> Path:
    for candidate in [DATA_RAW_DIR / filename, PROJECT_ROOT / filename, SCRIPT_DIR / filename]:
        if candidate.exists():
            return candidate
    return DATA_RAW_DIR / filename
YEARS = range(2010, 2026)
GDP_FILE = "WDI_14countries_GDP_constant_2015_USD.json"
PERSONNEL_FILE = "WDI_14countries_armed_forces_personnel.json"
ARMS_IMPORTS_FILE = "WDI_Arms_imports_SIPRI_all.json"
SIPRI_FILE = "SIPRI-Milex-data-1949-2025_v1.2.xlsx"
WDI_GDP_URL = "https://api.worldbank.org/v2/country/{iso3}/indicator/NY.GDP.MKTP.KD?format=json&per_page=100"
WDI_PERSONNEL_URL = "https://api.worldbank.org/v2/country/{iso3}/indicator/MS.MIL.TOTL.P1?format=json&per_page=100"
WDI_ARMS_IMPORTS_URL = "https://api.worldbank.org/v2/country/{iso3}/indicator/MS.MIL.MPRT.KD?format=json&per_page=100"
SIPRI_DOI = "https://doi.org/10.55163/CQGC9685"
COUNTRIES = {
    "AUS": ("Australia", "Australia"),
    "CHN": ("China", "China"),
    "IDN": ("Indonesia", "Indonesia"),
    "IND": ("India", "India"),
    "JPN": ("Japan", "Japan"),
    "KOR": ("Korea, South", "Korea, Rep."),
    "MYS": ("Malaysia", "Malaysia"),
    "NZL": ("New Zealand", "New Zealand"),
    "PAK": ("Pakistan", "Pakistan"),
    "PHL": ("Philippines", "Philippines"),
    "SGP": ("Singapore", "Singapore"),
    "THA": ("Thailand", "Thailand"),
    "USA": ("United States of America", "United States"),
    "VNM": ("Viet Nam", "Vietnam"),
}


def read_wdi(filename):
    rows = json.loads(find_input(filename).read_text(encoding="utf-8"))[1]
    return {
        (r["countryiso3code"], int(r["date"])): (r["value"] if r["value"] is not None else "")
        for r in rows if r.get("countryiso3code") and r.get("date")
    }


def main():
    gdp = read_wdi(GDP_FILE)
    personnel = read_wdi(PERSONNEL_FILE)
    arms_imports = read_wdi(ARMS_IMPORTS_FILE)
    wb = load_workbook(find_input(SIPRI_FILE), read_only=True, data_only=True)
    exp_sheet = wb["Constant (2024) US$"]
    share_sheet = wb["Share of GDP"]

    def read_sipri(sheet):
        header = next(sheet.iter_rows(min_row=6, max_row=6, values_only=True))
        year_col = {v: i for i, v in enumerate(header) if isinstance(v, int)}
        output = {}
        for row in sheet.iter_rows(min_row=7, values_only=True):
            if row and row[0] is not None:
                output[row[0]] = (row, year_col)
        return output

    exp_rows, share_rows = read_sipri(exp_sheet), read_sipri(share_sheet)
    records = []
    for iso3, (sipri_name, wdi_name) in COUNTRIES.items():
        erow, ecols = exp_rows[sipri_name]
        srow, scols = share_rows[sipri_name]
        for year in YEARS:
            e = erow[ecols[year]]
            share = srow[scols[year]]
            personnel_value = personnel.get((iso3, year))
            records.append({
                "iso3": iso3,
                "country": sipri_name,
                "year": year,
                "gdp_constant_2015_usd": gdp.get((iso3, year), ""),
                "military_expenditure_constant_2024_usd_millions": e if isinstance(e, (int, float)) else "",
                "military_expenditure_share_gdp_percent": 100 * share if isinstance(share, (int, float)) else "",
                "active_military_personnel_number": personnel_value if personnel_value is not None else "",
                "arms_imports_wdi_constant_1990_usd": arms_imports.get((iso3, year), ""),
                "gdp_indicator": "NY.GDP.MKTP.KD",
                "gdp_api": WDI_GDP_URL.format(iso3=iso3),
                "personnel_indicator": "MS.MIL.TOTL.P1",
                "personnel_api": WDI_PERSONNEL_URL.format(iso3=iso3),
                "arms_imports_indicator": "MS.MIL.MPRT.KD",
                "arms_imports_api": WDI_ARMS_IMPORTS_URL.format(iso3=iso3),
                "sipri_sheet_expenditure": exp_sheet.title,
                "sipri_sheet_share_gdp": share_sheet.title,
                "sipri_row_note": erow[2] or "",
                "sipri_doi": SIPRI_DOI,
                "sipri_release": "SIPRI Military Expenditure Database 1949-2025, revised 2026-04-27",
            })

    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    out = DATA_PROCESSED_DIR / "panel_regional_WDI_SIPRI_14negara_2010_2025.csv"
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    # Report simple coverage metrics for each variable and strict complete cases.
    fields = ["gdp_constant_2015_usd", "military_expenditure_constant_2024_usd_millions",
              "military_expenditure_share_gdp_percent", "active_military_personnel_number",
              "arms_imports_wdi_constant_1990_usd"]
    summary = [f"# Cakupan Panel Regional WDI–SIPRI", "",
               "Dibangun dari ekspor SIPRI dan respons API World Bank yang tersimpan lokal.",
               "Tidak ada interpolasi atau ekstrapolasi. Panel seimbang pada level baris (14 negara × 16 tahun);",
               "empat indikator dan satu seri impor senjata WDI; kelengkapan diperiksa sebelum memilih spesifikasi analisis.", "",
               f"CSV: `{out.name}` (224 baris negara–tahun).", "",
               "## Kelengkapan per indikator", ""]
    for field in fields:
        valid = [r for r in records if r[field] != ""]
        ys = sorted({r["year"] for r in valid})
        summary.append(f"- `{field}`: {len(valid)}/224 nilai; rentang observasi {min(ys)}–{max(ys)}.")
    complete = [r for r in records if all(r[k] != "" for k in fields)]
    summary += ["", f"Baris lengkap untuk seluruh lima seri (empat input + impor senjata WDI): {len(complete)}/224.",
                "Nilai impor senjata WDI kosong: Malaysia 2025 dan Selandia Baru 2016, 2017, serta 2025; nilai kosong tidak dianggap nol.", "",
                "## Implikasi rancangan", "",
                "- PDB konstan 2015, belanja militer konstan 2024, dan belanja militer/PDB SIPRI tersedia pada semua 224 baris untuk 2010–2025.",
                "- Personel militer aktif WDI (sumber asal IISS Military Balance) hanya sampai 2020 pada ekstrak ini. Jangan mengisi 2021–2025 dengan tren atau menyebut panel 2010–2025 lengkap.",
                "- Jendela 2010–2020 terverifikasi seimbang untuk tiga indikator makro (14 × 11 = 154 baris); personel juga lengkap hanya pada rentang ini. Seri impor senjata WDI tidak lengkap untuk seluruh negara-tahun; nilai kosong tidak boleh diisi nol.",
                "- SIPRI mencatat Indonesia memiliki penerimaan off-budget militer yang tidak seluruhnya tercakup dan ukurannya tidak diketahui; pertahankan catatan ini sebagai keterbatasan.",
                "- Empat indikator makro/personel mengukur input sumber daya, bukan kesiapan tempur, efektivitas operasional, atau ketahanan saat perang. Seri WDI `MS.MIL.MPRT.KD` berlabel arms imports (constant 1990 US$) dan bersumber dari SIPRI; jangan menyebut angka seri ini TIV mentah atau harga kontrak. TIV SIPRI mengukur volume transfer dan bukan nilai finansial. Beri label unit WDI yang benar dan jangan membandingkannya secara nominal dengan belanja militer SIPRI yang berbasis harga konstan 2024.",
                "- Nilai personel dari WDI bukan pengamatan independen yang pasti setiap tahun; jelaskan sumber asal dan keterbatasan pengukuran. Periksa penandaan estimasi SIPRI sel demi sel sebelum menguji statistik.", ""]
    (DOCS_AUDIT_DIR / "Cakupan_Panel_Regional_WDI_SIPRI.md").write_text("\n".join(summary), encoding="utf-8")
    print(f"Wrote {len(records)} rows to {out.name}")
    for field in fields:
        print(field, sum(r[field] != "" for r in records), "/", len(records))
    print("complete cases", len(complete), "/", len(records))


if __name__ == "__main__":
    main()
