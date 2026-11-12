# Temuan Audit Awal Naskah Ketahanan Pertahanan RI–Australia

Dokumen ini mencatat pemeriksaan awal terhadap naskah, notebook, skrip pembangkit data, dan engine simulasi pada 24 Oktober 2026. Ini belum merupakan validasi independen sumber eksternal.

## Status ringkas

Naskah belum aman direvisi sebagai artikel empiris dengan hasil yang saat ini diklaim. Hambatan utama ada pada asal-usul data dan ketidakcocokan antara uraian metode, kode, serta hasil. Angka abstrak, hasil, dan kesimpulan sebaiknya ditahan sampai keputusan data dan perhitungan dibuat.

## Temuan kritis

1. **Data yang diberi label historis dibangkitkan oleh kode.** `init_database.py` menetapkan nilai awal dan laju pertumbuhan per negara, menerapkan rumus tren dan perturbasi sinus, lalu memberi status “Audited Historical” untuk 2010–2024. Kode itu tidak mengimpor deret observasi dari sumber yang disebutkan. Label historis/audited karena itu tidak didukung proses pembentukan data yang tersedia. Klaim empiris, komparasi negara, dan generalisasi berbasis data ini perlu dihentikan sampai diganti data yang dapat dilacak atau penelitian secara eksplisit diubah menjadi studi simulasi berbasis data sintetis.

2. **Metode MCDA yang diklaim tidak sama dengan implementasi.** `init_database.py` menghitung normalisasi Min–Max tahunan per indikator. Notebook menghitung bobot Entropy pada data mentah 2024–2026, tetapi membentuk target ML sebagai rata-rata sederhana 20 fitur; engine `.py` menggunakan bobot indikator manual yang berbeda. Tidak ditemukan implementasi AHP maupun TOPSIS, sedangkan naskah mengklaim keduanya serta melaporkan CR AHP. Klaim dan hasil AHP/TOPSIS perlu dihapus atau dihitung ulang dengan prosedur yang benar-benar dijalankan dan terdokumentasi. Ketidaksamaan pipeline notebook dan `.py` juga harus dibereskan.

3. **Deskripsi Monte Carlo tidak cocok dengan kode.** Notebook dan `simulasi_ketahanan.py` memakai gangguan Normal dan Uniform, bukan Beta/PERT. Notebook memakai bobot Entropy untuk indikator lalu bobot strategis/taktis skenario; engine `.py` memakai bobot manual indikator. Tidak ditemukan AHP, TOPSIS, maupun perhitungan VaR pada kedua implementasi tersebut. Tabel 3 perlu dihitung ulang dari keluaran asli menggunakan statistik yang didefinisikan secara tepat; nilai yang ada belum bisa dipertahankan.

4. **Model ML/DNN merekonstruksi skor dari komponennya.** Notebook membentuk target `skor_ketahanan_komposit` sebagai rata-rata dari 20 indikator, lalu memakai indikator yang sama sebagai fitur untuk memprediksi target. Skor (R^2) dan feature importance mengukur kemampuan merekonstruksi rumus target tersebut, bukan validasi empiris terhadap ketahanan atau keberhasilan pertahanan. Bagian “validasi/prediksi” dan interpretasi kausal harus ditulis ulang atau dikeluarkan.

5. **Proyeksi 2027–2035 menggunakan asumsi tren buatan.** Kode mengekstrapolasi perubahan indikator 2018–2026 dan menambahkan kenaikan manual pada fitur tertentu, lalu memberi hasilnya kepada model rekonstruksi skor. Ini bukan validasi prediksi masa depan; angka proyeksi 2035 perlu dihapus atau diposisikan jelas sebagai skenario bersyarat dengan asumsi yang dinyatakan.

6. **Statistik inferensial dalam naskah tidak konsisten dengan ringkasan yang dilaporkan.** Dengan mean 14,98 dan 67,84, SD 0,89 dan 1,08, serta 5.000 simulasi per negara, Welch (t) dari asumsi sampel independen kira-kira (-2.670), bukan (-267,42). Cohen’s (d) kira-kira 53, bukan 5,34. Ini hitung pemeriksaan dari ringkasan terbitan, bukan pengganti hitung ulang data simulasi asli. Interval di skrip juga memakai μ ± 1,96 SD, yang merupakan rentang sebaran normal aproksimatif, bukan interval kepercayaan mean.

7. **Unit data disebut tidak konsisten.** Dataset yang dimaksud berisi (15 \times 17 \times 20 = 5.100) nilai negara–indikator–tahun, atau 255 kombinasi negara–tahun. Naskah berganti menyebut 255 “rekaman” dan 5.100 “baris”. Istilah unit observasi harus dibetulkan di seluruh naskah.

8. **Kredensial ditanam langsung dalam kode.** Konfigurasi koneksi database berisi kata sandi di beberapa berkas proyek. Hapus kredensial dari skrip dan gunakan konfigurasi lokal/environment variable sebelum berbagi atau mengunggah berkas.

## Urutan pekerjaan yang disarankan

1. Putuskan basis penelitian: (a) kumpulkan dan dokumentasikan data observasi asli, atau (b) nyatakan secara terbuka sebagai simulasi sintetis dan batasi klaim pada konsekuensi asumsi model.
2. Kunci ulang definisi indikator, unit analisis, formula indeks, bobot, dan skenario; cocokkan semuanya dengan kode yang dapat dijalankan.
3. Hitung ulang tabel, statistik, dan grafik dari satu sumber hasil yang sama; hapus angka yang belum dapat direproduksi.
4. Baru susun ulang metode, hasil, pembahasan, abstrak, kesimpulan, dan rekomendasi sesuai bukti yang tersisa.
5. Setelah memilih jurnal tujuan, terapkan pedoman dan template jurnal tersebut.

## Batas pemeriksaan

Pemeriksaan ini bersumber pada berkas lokal proyek dan tidak mengonfirmasi satu per satu rujukan data, fakta geopolitik, DOI, atau kelayakan jurnal. Bagian itu memerlukan sumber primer/tautan spesifik dan pilihan jurnal target.

## Rekomendasi setelah audit lanjutan

**Jalur yang paling kuat untuk mengejar artikel jurnal adalah membangun ulang penelitian berbasis data observasi yang bisa diverifikasi, dengan cakupan indikator yang dipersempit.** Jangan mempertahankan 20 indikator saat ini sebagai data empiris: beberapa—misalnya readiness, hari cadangan amunisi, stok BBM militer, interoperability, dan perlindungan medis tempur—tidak memiliki sumber observasi yang ditunjukkan dan sebagian besar saat ini dibuat dari profil serta tren buatan.

Rancangan yang lebih dapat dipertanggungjawabkan:

1. Rumuskan ulang objek sebagai **perbandingan indikator kapasitas pertahanan terukur**, bukan pengukuran menyeluruh atas “ketahanan nasional” atau prediksi hasil konflik.
2. Batasi variabel pada data tahunan yang benar-benar dapat ditelusuri ke sumber primer, dokumentasikan definisi, satuan, transformasi, periode, dan tanggal akses. Pilih negara/periode berdasarkan kelengkapan data, bukan sebaliknya.
3. Pertahankan MCDA hanya jika bobot dan normalisasi ditetapkan eksplisit. Gunakan AHP hanya jika ada penilaian pakar terdokumentasi; gunakan Entropy hanya sebagai analisis alternatif/robustness dan implementasikan TOPSIS jika memang menjadi metode inti.
4. Jadikan Monte Carlo analisis **sensitivitas terhadap ketidakpastian bobot atau pengukuran**, dengan rentang dan distribusi yang punya dasar. Jangan menafsirkannya sebagai probabilitas hasil perang atau VaR kerugian tanpa data kerugian dan kalibrasi.
5. Keluarkan DNN, proyeksi 2035, feature importance, serta model Lanchester dari klaim inti dalam bentuk saat ini. Target AI adalah fungsi langsung fitur yang sama, proyeksinya mengandung perubahan fitur yang ditentukan manual, sedangkan kode “Lanchester” memakai pembaruan aditif dengan parameter tanpa kalibrasi.
6. Bangun ulang seluruh tabel dan grafik dari pipeline yang sama setelah data lolos audit. Tulis abstrak dan kesimpulan paling akhir.

**Jalur simulasi sintetis** tetap cocok jika prioritasnya menyelesaikan tugas mata kuliah dan mendemonstrasikan coding. Dalam jalur itu, ubah label artikel menjadi *model simulasi eksploratif berbasis skenario*, tandai semua masukan sintetis/assumption-driven, hilangkan klaim empiris dan inferensial, dan simpulkan hanya tentang respons model terhadap asumsi. Jalur ini lebih cepat, tetapi kontribusi dan daya dukungnya untuk artikel SINTA 2 lebih lemah tanpa kebaruan metodologis yang jelas dan validasi eksternal.

Dengan tujuan publikasi SINTA 2 yang disebut di audit, saya merekomendasikan **jalur data observasi yang dipersempit**. Jika data mentah yang dapat ditelusuri tidak tersedia, pilihan ilmiah yang jujur adalah mempersempit klaim ke studi simulasi, bukan mempertahankan label historis pada data sintetis. Status SINTA 2 sendiri tidak menjamin artikel diterima; jurnal tujuan dan pedoman penulisnya masih perlu dipilih serta diperiksa.

## Kandidat jurnal dan implikasi format

Kandidat awal yang cocok dengan topik adalah **Jurnal Pertahanan** Universitas Pertahanan RI. Halaman jurnal menyatakan fokus pada strategi, manajemen, teknologi pertahanan, dan isu keamanan; halaman SINTA yang diperiksa menandainya SINTA 2. Pedoman penulis saat ini meminta naskah berbahasa Inggris, 3.000–7.000 kata, maksimum 25 halaman, gaya APA, serta format Cambria. Artinya naskah yang sekarang berbahasa Indonesia/berformat IEEE belum siap dikirim ke jurnal ini meskipun topiknya sesuai. Ini kandidat untuk ditelaah, belum keputusan target final.

Sumber pedoman: [Jurnal Pertahanan – About](https://jurnal.idu.ac.id/index.php/DefenseJournal/), [Author Guidelines / Submissions](https://jurnal.idu.ac.id/index.php/DefenseJournal/about/submissions), dan [profil Jurnal Pertahanan pada SINTA](https://sinta.kemdiktisaintek.go.id/journals/profile/2063). Kesesuaian ruang lingkup tidak menjamin penerimaan; mutu bukti, metode, kebaruan, dan hasil telaah sejawat tetap menentukan.

### Pemeriksaan kesiapan format awal

Naskah saat ini berisi sekitar 3.822 kata dari pendahuluan sampai kesimpulan dan 22 entri pustaka; seluruh nomor pustaka 1–22 muncul dalam sitasi teks. Panjang tersebut berada dalam rentang umum pedoman jurnal kandidat (3.000–7.000 kata), tetapi naskah belum memenuhi ketentuan bahasa Inggris dan gaya APA. Hitungan ini berasal dari berkas Markdown lokal; jumlah halaman Word perlu dicek setelah pemformatan.

### Dataset sumber resmi tahap pertama

Berhasil diekstrak berkas data baru untuk 2 negara × 16 tahun (2010–2025), 32 baris, berisi PDB konstan 2015 dari WDI dan belanja militer dari SIPRI (dolar konstan 2024 serta persentase PDB). Tidak ada nilai hilang pada ketiga seri yang diekstrak. Dataset dan skrip ekstraksinya dicatat pada `data_sumber_resmi_IDN_AUS_2010_2025.csv` dan `extract_official_data.py`; catatan provenans lengkap ada di `Matriks_Provenans_Data.md`.

Dataset 2 negara dan 3 seri ini belum cukup untuk mempertahankan konstruk komposit “ketahanan pertahanan”. Tahap desain berikutnya perlu memilih antara perluasan panel regional memakai indikator sebanding yang benar-benar tersedia, atau perubahan fokus artikel menjadi analisis sumber daya pertahanan. Jangan menghitung ulang skor lama sebagai indeks ketahanan dari tiga angka ini tanpa dasar konstruk dan pembobotan yang dapat dibela.
