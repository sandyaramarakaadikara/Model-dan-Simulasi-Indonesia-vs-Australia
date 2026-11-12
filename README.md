# Model dan Simulasi: Analisis Pertahanan Indo-Pasifik (Tugas ke-5)

Repositori ini memuat proyek pemodelan, simulasi, analisis data panel empiris (SIPRI & World Bank WDI 2010–2025), aplikasi interaktif wargame C4ISR, serta draf manuskrip publikasi untuk *Jurnal Pertahanan*.

---

## 📁 Struktur Direktori Proyek

```text
├── dashboard_pertahanan.py          # Antarmuka Dashboard Interaktif Utama (Streamlit)
├── wargame_3d_engine.py             # Mesin Taktis WebGL/Three.js C4ISR Battlespace
├── README.md                        # Dokumentasi struktur & panduan eksekusi
├── .streamlit/                      # Konfigurasi Streamlit theme & server
│
├── data/                            # Manajemen data mentah dan data terproses
│   ├── raw/                         # Berkas data mentah resmi (ekspor SIPRI & JSON API WDI)
│   │   ├── SIPRI-Milex-data-1949-2025_v1.2.xlsx
│   │   ├── WDI_14countries_GDP_constant_2015_USD.json
│   │   ├── WDI_14countries_armed_forces_personnel.json
│   │   ├── WDI_Arms_imports_SIPRI_all.json
│   │   ├── WDI_AUS_GDP_constant_2015_USD.json
│   │   └── WDI_IDN_GDP_constant_2015_USD.json
│   └── processed/                   # Panel data gabungan & tabel statistik keluaran
│       ├── panel_regional_WDI_SIPRI_14negara_2010_2025.csv
│       ├── panel_perbandingan_dua_periode_14negara.csv
│       ├── perbandingan_indonesia_australia_2016_2025.csv
│       ├── sensitivity_panel_2015_2024.csv
│       ├── ringkasan_distribusi_perubahan_negara_2026-10-24.csv
│       ├── tabulasi_kesesuaian_arah_belanja_impor_2026-10-24.csv
│       ├── tabel_hasil_simulasi_monte_carlo_idn_aus.csv
│       └── tabel_feature_importance_ml_idn_aus.csv
│
├── docs/                            # Dokumen naskah publikasi dan audit ilmiah
│   ├── manuscript/                  # Naskah artikel ilmiah (Markdown & DOCX)
│   │   ├── Naskah_Revisi_Exploratory_Indonesia_Australia_EN.md
│   │   ├── Manuscript_Blind_Review_Jurnal_Pertahanan_EN.docx
│   │   └── Title_Page_Jurnal_Pertahanan_EN.docx
│   └── audit/                       # Catatan audit metodologi, kebaruan, dan provenans
│       ├── Audit_Kebaruan_dan_Pivot_Artikel.md
│       ├── Audit_Kesesuaian_Jurnal_Target_SINTA2.md
│       ├── Cakupan_Panel_Regional_WDI_SIPRI.md
│       ├── Matriks_Provenans_Data.md
│       └── Temuan_Audit_Awal.md
│
├── figures/                         # Gambar grafik dan visualisasi resolusi tinggi (300 DPI)
│   ├── grafik_tren_fiskal_pertahanan_2010_2025.png
│   ├── grafik_klaster_pca_pertahanan_kawasan.png
│   ├── grafik_radar_20_variabel_idn_aus.png
│   ├── grafik_distribusi_monte_carlo_3skenario.png
│   ├── grafik_feature_importance_random_forest.png
│   └── perubahan_belanja_dan_impor_WDI_12negara_lengkap.png
│
├── notebooks/                       # Alur komputasi interaktif Jupyter Notebook
│   ├── Analisis_Simulasi_Pertahanan_Indonesia_Australia.ipynb
│   └── Analisis_Artikel_Panel_SIPRI_WDI.ipynb
│
├── references/                      # Modul perkuliahan dan literatur standar
│   ├── Pertemuan 5.pdf
│   ├── NIST.IR.7875.pdf
│   └── Analisis variabel penentu keunggulan negara dalam peperangan.pdf
│
└── scripts/                         # Skrip otomasi pipeline komputasi & build
    ├── extract_regional_panel.py    # Ekstraksi data mentah SIPRI/WDI -> CSV panel
    ├── summarize_cross_country_changes.py # Tabulasi perbandingan antar-periode & sensitivitas
    ├── plot_perbandingan_dua_periode.py   # Regenerasi plot scatter perbandingan dua periode
    └── build_submission_draft.py    # Kompilasi otomatis DOCX naskah & title page
```

---

## 🚀 Panduan Eksekusi

### 1. Menjalankan Dashboard Streamlit
Untuk membuka antarmuka simulasi dan visualisasi interaktif:
```bash
streamlit run dashboard_pertahanan.py
```

### 2. Menjalankan Pipeline Analisis Data
Seluruh skrip di dalam direktori `scripts/` telah dikonfigurasi dengan path resolver otomatis yang mendukung eksekusi dari root direktori maupun dari subdirektori:
- **Mengekstrak dataset panel regional**:
  ```bash
  python scripts/extract_regional_panel.py
  ```
- **Menghitung ringkasan distribusi dan arah perubahan belanja/impor**:
  ```bash
  python scripts/summarize_cross_country_changes.py
  ```
- **Membuat grafik perbandingan dua periode**:
  ```bash
  python scripts/plot_perbandingan_dua_periode.py
  ```
- **Mengompilasi DOCX Naskah Buta Review & Halaman Judul**:
  ```bash
  python scripts/build_submission_draft.py
  ```

### 3. Membuka Notebook Analisis
Buka Jupyter Notebook melalui terminal:
```bash
jupyter notebook notebooks/
```
Kedua notebook (`Analisis_Simulasi_Pertahanan_Indonesia_Australia.ipynb` dan `Analisis_Artikel_Panel_SIPRI_WDI.ipynb`) secara dinamis mendeteksi struktur folder proyek baik saat dijalankan dari folder `notebooks/` maupun dari root direktori proyek.
