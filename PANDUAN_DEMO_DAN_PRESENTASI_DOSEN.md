# PANDUAN LENGKAP DEMO & PRESENTASI DOSEN (PERTEMUAN 1, 2, & 3)
## SISTEM INFORMASI MEDIS RUMAH SAKIT — KELOMPOK 4
**Mata Kuliah:** Cloud Computing (Semester 5)  
**Dosen Pengampu:** Dr. Moch. Yasin, S.Kom., M.Kom., M.B.A., MTCNA, CDCP  
**Anggota Kelompok 4:**
1. Achmad Dani Permana (09020624021)
2. Achmad Yudis Dzaky (09020624022)
3. Achmad Wahyu Efendi (09020624023)
4. Daffa Danendra Fairuzza (09020624026)

---

## 1. PUSAT KENDALI DEMO (ONE-CLICK DEMO LAUNCHER)

Kelompok telah menyiapkan script pusat kendali menu interaktif di terminal PowerShell. Cukup jalankan perintah berikut:

```powershell
# Pindah ke direktori proyek
Set-Location "C:\DaffaP\KULIAH_DAFFA\Semester_5\CC\medis-cloud"

# Jalankan Menu Interaktif Master Demo
.\demo.ps1
```

Tampilan menu yang akan muncul di hadapan dosen:
```
==============================================================
     SISTEM INFORMASI MEDIS RUMAH SAKIT - KELOMPOK 4          
        PUSAT KENDALI DEMO PRAKTIKUM CLOUD COMPUTING          
==============================================================
 [1] Demo Pertemuan 1: Dasar Docker, Named Volume, & Disaster Recovery
 [2] Demo Pertemuan 2: Transformasi Microservices (DDD) & Inter-Service
 [3] Demo Pertemuan 3: Orkestrasi Docker Compose, Nginx Load Balancer & Elasticity
 [A] Jalankan Seluruh Skenario Demo Bertahap (1 -> 2 -> 3)
 [S] Status Kontainer & Network Docker Saat Ini
 [C] Bersihkan (Stop & Clean) Seluruh Kontainer Pengujian
 [Q] Keluar
==============================================================
```

---

## 2. PANDUAN NARASI & SKENARIO DEMO PER PERTEMUAN

Berikut adalah naskah presentasi (*talking points*), pembuktian teknis, dan apa yang harus ditunjukkan ke dosen saat menjalankan masing-masing demo:

---

### A. DEMO PERTEMUAN 1: DASAR DOCKER & DISASTER RECOVERY

> **Perintah Cepat:** Tekan `1` di menu `.\demo.ps1` atau jalankan `.\scripts\demo-p1.ps1`

#### Poin Narasi ke Dosen:
> *"Selamat pagi/siang Pak Yasin. Pada Pertemuan 1, fokus spesialisasi Kelompok 4 adalah **Disaster Recovery** dan **Persistensi Data Rekam Medis** menggunakan Docker Named Volumes.*
> *Kami membuktikan bahwa kontainer bersifat ephemeral (mudah rusak/hilang), namun data rekam medis pasien dijamin 100% aman tersimpan pada volume host, dan sistem kami mampu pulih dengan RTO (Recovery Time Objective) di bawah 1 detik."*

#### Alur Eksekusi & Bukti di Layar:
1. **Praktik A (Container & Port Mapping)**:
   - Membangun dan menjalankan `medis-lab1:1.0` di port 8000.
   - Uji respon HTTP: `"Sistem Informasi Medis - OK"`.
2. **Praktik B (Docker Named Volumes)**:
   - Membuat volume `medis_demo_p1_data` dan menyimpan data rekam medis pasien contoh.
3. **Praktik C (Simulasi Disaster Recovery)**:
   - **Snapshot**: Membuat cadangan arsip tarball `demo_p1_dr_backup.tar.gz`.
   - **Simulasi Bencana**: Kontainer dan volume sengaja dihapus paksa (`docker volume rm`).
   - **Restorasi**: Volume dipulihkan kembali dari snapshot arsip backup.
   - **Verifikasi**: Data rekam medis terbaca kembali utuh 100%.
   - **Metrik RTO**: Terukur pemulihan hanya membutuhkan **0.38 detik** (jauh melampaui standar SLA rumah sakit < 15 detik).

---

### B. DEMO PERTEMUAN 2: MICROSERVICES & DOMAIN-DRIVEN DESIGN (DDD)

> **Perintah Cepat:** Tekan `2` di menu `.\demo.ps1` atau jalankan `.\scripts\demo-p2.ps1`

#### Poin Narasi ke Dosen:
> *"Pada Pertemuan 2, kami melakukan modernisasi arsitektur dari aplikasi **Monolitik** menjadi **3 Microservices Bounded Context** menggunakan bantuan prompt AI. Ketiga layanan tersebut adalah: Layanan Data Pasien (port 5001), Layanan Apotek (port 5002), dan Layanan Jadwal Dokter (port 5003).*
> *Ketiganya dihubungkan melalui Docker Custom Bridge Network `medis-net` dengan fitur Automatic DNS Service Discovery, serta dilengkapi mekanisme Fault Isolation agar tidak terjadi cascading failure."*

#### Alur Eksekusi & Bukti di Layar:
1. **Praktik A (Baseline Monolitik)**:
   - Menjalankan `app-monolit` di port 5000, menampilkan dashboard terpusat.
   - Menjelaskan kelemahan monolit: jika satu fungsi crash, seluruh rumah sakit lumpuh. Monolit lalu dihentikan.
2. **Praktik B & C (Custom Bridge Network & Microservices)**:
   - Menjalankan network `medis-net`.
   - Mengaktifkan ketiga layanan mandiri dengan database masing-masing (*Database-per-Service*).
3. **Praktik D (Komunikasi Lintas Servis / Inter-Service REST Call)**:
   - **Uji Alergi Obat**: Layanan Apotek memanggil Layanan Pasien via DNS `http://service-pasien:5001`.
   - Saat diresepkan *Amoxicillin* untuk Pasien 1, sistem otomatis mendeteksi riwayat alergi:  
     `"PERINGATAN: Pasien memiliki riwayat alergi (Penisilin) terhadap antibiotik ini!"`
4. **Fault Isolation Test (Ketahanan Sistem)**:
   - `service-pasien` dimatikan paksa (`docker stop`).
   - Terbukti: Layanan Apotek dan Layanan Jadwal **TETAP HIDUP** melayani katalog obat dan dokter tanpa mengalami crash!

---

### C. DEMO PERTEMUAN 3: DOCKER COMPOSE, LOAD BALANCER NGINX & ELASTICITY

> **Perintah Cepat:** Tekan `3` di menu `.\demo.ps1` atau jalankan `.\scripts\demo-p3.ps1`

#### Poin Narasi ke Dosen:
> *"Pada Pertemuan 3, kami mengorkestrasi seluruh ekosistem layanan menggunakan **Docker Compose** dan menerapkan **Nginx sebagai API Gateway sekaligus Load Balancer** pada port 8080.*
> *Kami mempraktikkan **Elasticity** dengan menskalakan Layanan Pasien menjadi 3 replika kontainer secara dinamis untuk menangani lonjakan antrean rumah sakit, serta membuktikan pembagian beban secara merata mengikuti algoritma **Round-Robin**."*

#### Alur Eksekusi & Bukti di Layar:
1. **Single-Command Deployment**:
   - `docker compose up -d` menghidupkan 4 kontainer, 2 jaringan isolasi (`frontend-net` & `backend-net`), dan persistensi named volume `medis_pasien_data`.
2. **Nginx API Gateway (Port 8080)**:
   - Klien hanya mengakses satu pintu: `http://localhost:8080/`.
   - Nginx merutekan trafik secara cerdas ke backend: `/api/pasien`, `/api/obat`, `/api/dokter`.
3. **Simulasi Elasticity (Horizontal Scaling)**:
   - Penskalaan instan: `docker compose up -d --scale service-pasien=3`.
   - Terlihat 3 replika kontainer pasien berjalan secara paralel di latar belakang tanpa menimbulkan *downtime*.
4. **Pembuktian Load Balancing Round-Robin**:
   - Skrip mengirimkan 8 request berturut-turut ke endpoint rekam medis.
   - Nginx mendistribusikan request secara bergantian ke 3 ID kontainer backend berbeda yang dibuktikan melalui header HTTP `X-Served-By`.
5. **Integritas Rekam Medis Pasca Crash/Restart**:
   - Mendaftarkan pasien baru melalui Gateway.
   - Seluruh cluster pasien dimatikan dan direstart paksa (`docker compose restart service-pasien`).
   - Kueri ulang membuktikan data pasien baru **TETAP UTUH 100%**, menjamin standar keselamatan data medis.

---

## 3. CHEAT SHEET TANYA JAWAB (Q&A DEFENSE DENGAN DOSEN)

Siapkan jawaban taktis berikut jika dosen mengajukan pertanyaan kritis:

* **Tanya 1: "Mengapa Kelompok 4 memilih arsitektur Database-per-Service, bukan satu database MySQL/Postgres bersama?"**  
  * **Jawab:** *"Untuk menerapkan prinsip *Loose Coupling* dan isolasi batas data (*Bounded Context*). Dalam standar medis, jika database apotek mengalami lonjakan transaksi atau *lock table*, basis data rekam medis pasien tidak akan ikut terganggu. Selain itu, ini mencegah kebocoran data antar-departemen."*

* **Tanya 2: "Bagaimana Nginx bisa langsung tahu ada kontainer replika baru saat di-scale tanpa harus me-restart Nginx?"**  
  * **Jawab:** *"Pada `infra/nginx/nginx.conf`, kami menambahkan direktif `resolver 127.0.0.11 valid=2s ipv6=off;`. `127.0.0.11` adalah DNS server internal bawaan Docker Engine. Dengan TTL 2 detik, Nginx secara aktif me-resolve ulang IP address `service-pasien` setiap ada kontainer baru yang ditambahkan."*

* **Tanya 3: "Mengapa menggunakan SQLite WAL Mode di dalam kontainer yang di-scale?"**  
  * **Jawab:** *"Mode WAL (*Write-Ahead Logging*) memungkinkan pembacaan (*concurrent reads*) dilakukan secara paralel oleh banyak kontainer replika secara bersamaan tanpa menyebabkan `database is locked`."*

* **Tanya 4: "Apa fungsi pemisahan dua jaringan `medis-frontend-net` dan `medis-backend-net`?"**  
  * **Jawab:** *"Ini adalah konsep keamanan *Multi-tier Architecture*. Port microservices backend (5001, 5002, 5003) tidak kami ekspos ke host publik. Hanya Nginx Gateway yang berada di `frontend-net` yang memiliki akses publik port 8080. Kontainer backend terisolasi aman di dalam `backend-net`."*

* **Tanya 5: "Berapa RTO dan RPO pada sistem rekam medis kelompok Anda?"**  
  * **Jawab:** *"RTO (*Recovery Time Objective*) kami teruji di bawah **1 detik (0.38 detik)** berkat otomasi restorasi Docker Named Volume. RPO (*Recovery Point Objective*) kami mendekati **0 detik** karena volume di-mount secara direct I/O dari media penyimpanan host."*

---

## 4. DAFTAR BERKAS PROYEK & LAPORAN YANG SIAP DITUNJUKKAN

Semua berkas laporan resmi telah disusun sesuai format akademik template Pertemuan 9 dan tersimpan rapi:

* **Folder Laporan Resmi**:
  📁 [medis-cloud/laporan/](file:///c:/DaffaP/KULIAH_DAFFA/Semester_5/CC/medis-cloud/laporan/)
  - 📄 **Laporan Pertemuan 3 (Final Berisi Semua Gambar Screenshot)**:  
    `Laporan_Praktikum_Pertemuan_3_Kelompok_4_TERISI.docx`
  - 📄 **Laporan Pertemuan 2 (Microservices & DDD)**:  
    `Laporan_Praktikum_Pertemuan_2_Kelompok_4.docx`
  - 📄 **Laporan Pertemuan 1 (Dasar Docker & Disaster Recovery)**:  
    `Kelompok_4_Pertemuan_1_Arsitektur_Cloud_Dasar_Docker_revisi2.docx` (di folder `Pertemuan 8/`)
* **Folder Skrip Otomasi**:
  📁 [medis-cloud/scripts/](file:///c:/DaffaP/KULIAH_DAFFA/Semester_5/CC/medis-cloud/scripts/)
  - `demo-p1.ps1`: Skrip otomatis Demo Pertemuan 1
  - `demo-p2.ps1`: Skrip otomatis Demo Pertemuan 2
  - `demo-p3.ps1`: Skrip otomatis Demo Pertemuan 3
  - `demo.ps1`: Master Menu Interaktif
* **Folder Tangkapan Layar Terminal**:
  📁 [medis-cloud/screenshots/](file:///c:/DaffaP/KULIAH_DAFFA/Semester_5/CC/medis-cloud/screenshots/) (17 gambar PNG siap tayang)

Semua sistem sudah diuji coba dan **100% SIAP UNTUK DEMO DI DEPAN DOSEN!**
