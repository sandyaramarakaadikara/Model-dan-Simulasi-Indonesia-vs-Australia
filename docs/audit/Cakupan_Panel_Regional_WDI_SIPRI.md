# Cakupan Panel Regional WDI–SIPRI

Dibangun dari ekspor SIPRI dan respons API World Bank yang tersimpan lokal.
Tidak ada interpolasi atau ekstrapolasi. Panel seimbang pada level baris (14 negara × 16 tahun);
empat indikator dan satu seri impor senjata WDI; kelengkapan diperiksa sebelum memilih spesifikasi analisis.

CSV: `panel_regional_WDI_SIPRI_14negara_2010_2025.csv` (224 baris negara–tahun).

## Kelengkapan per indikator

- `gdp_constant_2015_usd`: 224/224 nilai; rentang observasi 2010–2025.
- `military_expenditure_constant_2024_usd_millions`: 224/224 nilai; rentang observasi 2010–2025.
- `military_expenditure_share_gdp_percent`: 224/224 nilai; rentang observasi 2010–2025.
- `active_military_personnel_number`: 154/224 nilai; rentang observasi 2010–2020.
- `arms_imports_wdi_constant_1990_usd`: 220/224 nilai; rentang observasi 2010–2025.

Baris lengkap untuk seluruh lima seri (empat input + impor senjata WDI): 152/224.
Nilai impor senjata WDI kosong: Malaysia 2025 dan Selandia Baru 2016, 2017, serta 2025; nilai kosong tidak dianggap nol.

## Implikasi rancangan

- PDB konstan 2015, belanja militer konstan 2024, dan belanja militer/PDB SIPRI tersedia pada semua 224 baris untuk 2010–2025.
- Personel militer aktif WDI (sumber asal IISS Military Balance) hanya sampai 2020 pada ekstrak ini. Jangan mengisi 2021–2025 dengan tren atau menyebut panel 2010–2025 lengkap.
- Jendela 2010–2020 terverifikasi seimbang untuk tiga indikator makro (14 × 11 = 154 baris); personel juga lengkap hanya pada rentang ini. Seri impor senjata WDI tidak lengkap untuk seluruh negara-tahun; nilai kosong tidak boleh diisi nol.
- SIPRI mencatat Indonesia memiliki penerimaan off-budget militer yang tidak seluruhnya tercakup dan ukurannya tidak diketahui; pertahankan catatan ini sebagai keterbatasan.
- Empat indikator makro/personel mengukur input sumber daya, bukan kesiapan tempur, efektivitas operasional, atau ketahanan saat perang. Seri WDI `MS.MIL.MPRT.KD` berlabel arms imports (constant 1990 US$) dan bersumber dari SIPRI; jangan menyebut angka seri ini TIV mentah atau harga kontrak. TIV SIPRI mengukur volume transfer dan bukan nilai finansial. Beri label unit WDI yang benar dan jangan membandingkannya secara nominal dengan belanja militer SIPRI yang berbasis harga konstan 2024.
- Nilai personel dari WDI bukan pengamatan independen yang pasti setiap tahun; jelaskan sumber asal dan keterbatasan pengukuran. Periksa penandaan estimasi SIPRI sel demi sel sebelum menguji statistik.
