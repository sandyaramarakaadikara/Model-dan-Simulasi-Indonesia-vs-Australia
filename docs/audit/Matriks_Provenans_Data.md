# Matriks Pemeriksaan Provenans Data

Pemeriksaan lokal atas `init_database.py`, `db_hankam_indopasifik.sql`, `Artikel_Jurnal_Ketahanan_Nasional_RI_AUS.md`, dan `referensi_mendeley.bib` (24 Oktober 2026).

## Kesimpulan utama

Database mencantumkan label sumber untuk setiap indikator dan daftar pustaka mencantumkan beberapa publikasi/dataset relevan. Namun, di berkas proyek yang diperiksa, `init_database.py` **tidak mengunduh atau membaca nilai dari sumber-sumber tersebut**. Skrip menetapkan profil dasar per negara, memakai tren/rumus untuk menghasilkan nilai tahun berikutnya, lalu menyimpan label sumber dan status “Audited Historical”. Karena itu, status saat ini dalam berkas lokal adalah **nilai hasil pembangkitan skrip dengan label sumber**, belum observasi yang terlacak ke halaman/tabel sumber.

Ini tidak membuktikan bahwa penulis tidak pernah mengambil data di luar skrip. Jika ada file ekstraksi, lembar kerja, catatan angka, atau dokumen sumber yang digunakan, artefak tersebut perlu dicocokkan sebelum nilai dibuang atau diganti.

## Inventaris indikator

| Kode | Indikator dalam naskah | Label sumber dalam generator | Cara nilai saat ini dibentuk | Tindakan untuk menjadikannya dapat diverifikasi |
|---|---|---|---|---|
| S1 | PDB riil | World Bank WDI (NY.GDP.MKTP.CD) | Nilai dasar per negara × CAGR tetap dan pola sinus | Ambil seri WDI per negara/tahun; dokumentasikan unit dan konversi ke USD/miliar |
| S2 | Belanja pertahanan | SIPRI Military Expenditure Database 2024 | Nilai dasar per negara × CAGR tetap, pola kosinus, dan faktor kenaikan manual akhir periode | Cocokkan seri SIPRI dengan unit, mata uang/harga konstan, tahun, dan tanggal unduh |
| S3 | Kemandirian industri pertahanan | SIPRI Arms Industry / Ministry of Defence Reports | Nilai awal dan kenaikan tetap per tahun | Tetapkan definisi operasional dan rubrik; sitasi laporan/tabel tiap nilai, atau keluarkan |
| S4 | Personel militer aktif | IISS The Military Balance | Nilai awal ditambah/ dikurangi tren tetap tahunan | Catat edisi, negara, halaman/tabel, dan definisi personel; rekonsiliasi perubahan tahunan |
| S5 | Cadangan logistik BBM | IEA Energy Review & Defense Logistics | Nilai awal dan kenaikan 0,5 hari per tahun | Perlu sumber spesifik untuk stok militer; data energi nasional umum tidak langsung mengukur hari pasok militer |
| S6 | Keamanan/ketahanan siber | ITU Global Cybersecurity Index & NCSI | Nilai awal dan kenaikan 1,2 poin per tahun | Gunakan skor/tahun terbit yang benar-benar tersedia; jangan interpolasi seolah observasi tanpa label |
| S7 | Integrasi pakta/aliansi | International Treaties & SIPRI Arms Transfers | Nilai awal; kenaikan tertentu dikondisikan tahun 2021 | Definisikan skala skor, aturan pengkodean, sumber per perjanjian, dan validasi pengodean |
| S8 | Tata kelola | World Bank Worldwide Governance Indicators | Nilai awal ditambah tren 0,3 per tahun | Gunakan indikator WGI yang spesifik; terangkan transformasi skala asli ke 0–100 |
| S9 | Geografi | CIA World Factbook & geospatial data | Nilai dasar tetap per negara | Geografi fisik bukan seri tahunan; jelaskan justifikasi skor dan apakah indikator layak masuk indeks tahunan |
| S10 | Kohesi sosial/modal pertahanan sipil | National Bureau of Statistics / Lemhannas | Nilai awal ditambah 0,2 per tahun | Tentukan survei/indeks dan variabel terukur; bila tidak ada, keluarkan atau tandai sebagai skenario |
| T1 | Pelatihan personel/jam terbang | IISS Training Hours & Exercise Records | Nilai awal dan kenaikan tetap 0,3 per tahun | Butuh catatan jam terbang/latihan per negara-tahun dan aturan pembentukan skor |
| T2 | Kesiapan operasional | Official Fleet Readiness & Maintenance Audits | Nilai awal dengan gelombang sinus tahunan | Cantumkan dokumen audit resmi dan cakupan armada/tahun; jika tidak tersedia, jangan klaim data aktual |
| T3 | Keandalan C2 | C4ISR Operational Doctrine & Data-Link Reports | Nilai awal dan kenaikan 0,6 per tahun | Definisikan ukuran dan sumber laporan yang dapat ditelusuri; jika skor pakar, catat panel/rubrik |
| T4 | Pengawasan maritim/ISR | Early Warning Radar & Satellite Coverage Maps | Nilai awal dan kenaikan 0,7 per tahun | Tetapkan ukuran cakupan dan tahun; tautkan peta/laporan serta metode menghitung skor |
| T5 | Interoperabilitas tri-matra | Joint Staff Exercise & Interoperability Assessments | Nilai awal dan kenaikan 0,5 per tahun | Sumber latihan dan rubrik skor harus spesifik per negara/tahun |
| T6 | Mobilitas strategis | Airlift / Sealift Fleet Tonnage Capacity (IISS) | Nilai awal dan kenaikan 0,4 per tahun | Ekstrak jumlah/kapasitas platform per edisi; tentukan rumus agregasi dan unit |
| T7 | Cadangan amunisi | War Reserve Munitions Stockpile Estimates | Nilai awal dan kenaikan 0,8 hari per tahun | Data stok umumnya tidak transparan; perlu sumber terbuka spesifik atau keluarkan dari data empiris |
| T8 | Peperangan elektronika | Electronic Warfare & Cyber Resistance Assessments | Nilai awal dan kenaikan 0,8 per tahun | Definisikan rubric/benchmark dan sumber spesifik; jangan gunakan skor tanpa proses pengukuran |
| T9 | Adaptasi taktis/drone | Military Lessons Learned & Doctrine Revision Velocity | Nilai awal dan kenaikan 0,4 per tahun | Definisikan hitungan/ukuran operasional yang dapat diulang; dokumentasikan sumber dan aturan skor |
| T10 | Proteksi medis tempur | Combat Casualty Care & Medevac Reach Times | Nilai awal dan kenaikan 0,3 per tahun | Gunakan indikator terukur dan data per negara/tahun; jika tidak tersedia, keluarkan atau jadikan asumsi |

## Langkah rekonsiliasi yang akan dipakai

Untuk setiap nilai yang ingin dipertahankan, lengkapi satu baris dengan:

`kode negara | kode indikator | tahun | nilai di database | nilai sumber | unit sumber | judul dokumen/dataset | URL/DOI | halaman/tabel | tanggal akses | transformasi | status`

Nilai kemudian diklasifikasikan sebagai:

- **Terverifikasi:** nilai cocok dengan sumber spesifik dan transformasinya dapat diulang.
- **Turunan:** dihitung dari observasi sumber dengan rumus yang dinyatakan.
- **Estimasi/proyeksi:** bukan observasi; asumsi dan metode estimasinya dicatat.
- **Skor pakar:** ada rubrik, panel/ahli, prosedur, dan reliabilitas yang dijelaskan.
- **Sintetis/asumsi:** dibangkitkan untuk eksperimen; tidak disebut data historis empiris.
- **Tidak terverifikasi:** belum ada bukti yang cukup; jangan dipakai untuk klaim empiris.

## Prioritas rekonsiliasi

Mulai dari S1 (PDB), S2 (belanja militer), S4 (personel), dan S8 (WGI), karena label sumbernya merujuk ke dataset yang lebih jelas dan nilai tahunan berpotensi dicocokkan. Setelah itu putuskan nasib S3, S5–S7, S9–S10, dan T1–T10 berdasarkan ketersediaan bukti/rubrik. Jangan menjalankan ulang generator untuk membuat ulang dataset dan menganggapnya sebagai pengganti verifikasi sumber.

Belum dilakukan pengunduhan atau penggantian data. Dokumen sumber asli/lembar ekstraksi dari penulis akan memungkinkan rekonsiliasi angka; tanpa itu, nilai yang dihasilkan generator harus tetap ditandai sebagai belum terverifikasi.

## Pemeriksaan sumber terbuka yang sudah dimulai

World Bank WDI dapat diakses melalui API resmi untuk GDP Indonesia dan Australia, dengan observasi terbaru 2025 pada rilis yang dibaca. Untuk seri yang diklaim **PDB riil**, gunakan kode `NY.GDP.MKTP.KD` (GDP constant 2015 US$), bukan `NY.GDP.MKTP.CD` (GDP current US$) yang tercantum dalam komentar kode proyek.

Pemeriksaan silang awal pada seri current-US$ menunjukkan mengapa angka lama perlu diganti, bukan hanya diberi sitasi:

| Negara/tahun | Database proyek | WDI current US$ | Catatan |
|---|---:|---:|---|
| Indonesia 2010 | 755,000 miliar | 755,094 miliar | Baseline awal sangat dekat |
| Indonesia 2011 | 802,043 miliar | 892,969 miliar | Nilai proyek mengikuti rumus tren, tidak cocok dengan observasi WDI |
| Australia 2010 | 1.145,000 miliar | 1.152,567 miliar | Baseline awal dekat |
| Australia 2011 | Nilai proyek berbasis formula pertumbuhan | 1.402,940 miliar | Seri WDI aktual memperlihatkan perbedaan besar dari tren sederhana |

Nilai WDI di atas adalah **current US$ untuk pemeriksaan silang**, bukan seri riil yang sebaiknya dipakai dalam model utama. API mencatat Indonesia 2025 = US$1.445,643 miliar dan Australia 2025 = US$1.798,519 miliar. Dataset GDP constant 2015 US$ tersedia untuk periode 1960–2025. Sebelum membangun data final, pilih satu seri dan satuan yang konsisten untuk semua negara/tahun.

Sumber primer yang diperiksa: [World Bank API – Indonesia, GDP current US$](https://api.worldbank.org/v2/country/IDN/indicator/NY.GDP.MKTP.CD?format=json), [World Bank API – Australia, GDP current US$](https://api.worldbank.org/v2/country/AUS/indicator/NY.GDP.MKTP.CD?format=json), dan [World Bank – GDP constant 2015 US$ metadata/data](https://data.worldbank.org/indicator/NY.GDP.MKTP.KD). Pemeriksaan cakupan SIPRI juga mengonfirmasi database belanja militer mencakup seri negara hingga 2025; perlu dicatat tahun terakhir yang tersedia per negara ketika diambil.

### Ekstraksi awal yang sudah dibuat

File resmi sudah diunduh: SIPRI Military Expenditure Database rilis 1949–2025 versi direvisi 27 April 2026, serta respons API WDI untuk PDB konstan 2015 AS. Skrip [extract_official_data.py](extract_official_data.py) menggabungkan hanya data Indonesia dan Australia untuk 2010–2025 ke [data_sumber_resmi_IDN_AUS_2010_2025.csv](data_sumber_resmi_IDN_AUS_2010_2025.csv). Ekstraksi menghasilkan 32 baris negara–tahun, tanpa nilai hilang untuk PDB, belanja militer konstan, dan belanja militer sebagai persentase PDB.

Contoh nilai yang diekstrak (angka dibulatkan untuk ringkasan):

| Negara | Tahun | PDB konstan 2015 (US$ miliar) | Belanja militer konstan 2024 (US$ miliar) | Belanja militer (% PDB, SIPRI) |
|---|---:|---:|---:|---:|
| Indonesia | 2010 | 657,835 | 4,619 | 0,618 |
| Indonesia | 2025 | 1.301,512 | 15,330 | 1,045 |
| Australia | 2010 | 1.184,611 | 24,103 | 1,847 |
| Australia | 2025 | 1.694,658 | 35,264 | 1,918 |

Ini baru **dataset inti awal**, belum indeks ketahanan dan belum cukup untuk mendukung klaim kemenangan tempur. Untuk artikel empiris, indikator makro ini harus diberi nama dan interpretasi yang tepat. WDI GDP berada dalam dolar konstan 2015; nilai SIPRI di sheet belanja militer berada dalam juta dolar konstan 2024; karena basis harga berbeda, keduanya dianalisis sebagai seri terpisah. Sheet persentase PDB dari SIPRI merupakan rasio tersendiri.

Ekstraksi membawa catatan kaki sumber: SIPRI menyatakan angka Indonesia tidak mencakup sejumlah penerimaan off-budget militer yang ukurannya tidak diketahui; catatan ini harus masuk keterbatasan bila seri dipakai. Australia tidak memiliki catatan negara pada kolom tersebut. SIPRI mengizinkan penggunaan statistik dalam artikel jurnal dengan atribusi yang jelas, tetapi reproduksi lebih dari 10% dataset memerlukan izin. Karena itu, sumber data mentah disimpan lokal untuk analisis; jangan melampirkan ulang seluruh dataset mentah ke materi publikasi. [Ketentuan penggunaan SIPRI](https://www.sipri.org/about/terms-and-conditions).
