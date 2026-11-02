Berikut adalah revisi rencana praktikum dengan penyesuaian **hanya menggunakan Docker** (Docker Engine, Docker Compose, atau Docker Swarm) sebagai *environment* implementasi dan simulasi cloud.

## Rencana Silabus Praktikum Cloud - Berbasis Docker (5 Pertemuan)

| Pertemuan | Fokus Utama | Aktivitas & Praktikum |
| --- | --- | --- |
| **1** | **Arsitektur Cloud & Dasar Docker** | Konsep dasar arsitektur cloud. Praktik dasar Docker: membuat *Container*, *Image*, dan *Docker Volumes*. Simulasi konsep *Availability* dan *Disaster Recovery* dengan *backup volume* antar container. Pembagian kelompok. |
| **2** | **Microservices & Implementasi AI** | Transformasi dari *Aplikasi Awal* (Monolitik) ke *Aplikasi Akhir* (Microservices). **Penggunaan AI:** Praktikan mem-prompt AI (ChatGPT/Copilot) untuk memecah rancangan monolit menjadi microservices dan meng-generate file `Dockerfile` serta konfigurasi dasar jaringan. |
| **3** | **Orkestrasi Docker Compose & Jaringan** | Menggabungkan seluruh layanan (Microservices, Database, Cache) menggunakan `docker-compose.yml`. Praktik *Elasticity* dengan men-setup Nginx/HAProxy di dalam Docker sebagai *Load Balancer* untuk merutekan trafik ke beberapa replika container (`docker-compose up --scale`). |
| **4** | **Plan & Simulation (Load Testing)** | Pengenalan *tools* uji beban (JMeter, K6, atau Locust). Setiap kelompok menyusun skrip skenario pengujian bertahap dari 1 hingga 500 *virtual users* yang diarahkan langsung ke *Load Balancer* Docker mereka. |
| **5** | **Extreme Test & Evaluasi Arsitektur** | Eksekusi *Stress Test* hingga 1000 *virtual users*. Praktikan memantau metrik performa menggunakan `docker stats` (CPU, Memory, latensi), mengevaluasi batas maksimal container sebelum *crash*, dan mempresentasikan laporannya. |

---

## Pembagian Kelompok & Studi Kasus Spesifik (Berbasis Docker)

Setiap kelompok akan menjalankan sistem mereka secara lokal atau pada satu server VM menggunakan **Docker Compose**, mempraktikkan arsitektur *microservices* dengan kasus berikut:

* **Kelompok 1 (Nidzom, Azzam, Fahmud, Jabbar, Faisal)**
* **Kasus:** Platform *Ticketing* Konser Online.
* **Fokus Docker:** Simulasi *Elasticity* ekstrem. Kelompok ini harus men-scale container sistem antrean (Queue) menjadi jumlah yang sangat banyak saat dites beban ribuan *virtual users* untuk simulasi "War Tiket".


* **Kelompok 2 (Zani, Resti, Faizah, *[Nama 4]*, *[Nama 5]*)**
* **Kasus:** Sistem E-Learning Berbasis Ujian Serentak.
* **Fokus Docker:** Kestabilan sesi (*Session management*). Menerapkan Redis di dalam container terpisah agar jika container aplikasi ujian mati/di-restart, jawaban siswa yang sedang ujian tidak hilang.


* **Kelompok 3 (Alvira, Titha, Ella, Elvira)**
* **Kasus:** Aplikasi E-Commerce *Flash Sale*.
* **Fokus Docker:** Komunikasi antar-container yang aman dan cepat (*Docker Networks*). Memisahkan *network* antara container Katalog Produk (publik) dan container Manajemen Inventaris/Database (privat) agar tidak terjadi *overselling*.


* **Kelompok 4 (Yudis, Agra, Qosi, Diaz, Daffa)**
* **Kasus:** Sistem Informasi Medis Rumah Sakit.
* **Fokus Docker:** *Disaster Recovery* dan persistensi data. Praktik manajemen *Docker Volumes* secara ketat untuk database Rekam Medis pasien, memastikan data tidak hilang meskipun container dihapus atau hancur.


* **Kelompok 5 (Anisa, Frisillia, Riyana, Salsa, Ima)**
* **Kasus:** Platform *Ride-Hailing* (Ojek Online).
* **Fokus Docker:** Penggunaan AI untuk men-generate kode *mock-up* GPS Tracking dan *matching* algoritma. Sistem Docker dibagi menjadi container Lokasi, *Matching*, dan Dompet Digital dengan load balancing Nginx untuk menahan *request* lokasi yang terus-menerus.


* **Kelompok 6 (Faiq, Hakim, Faisol, Darma)**
* **Kasus:** Aplikasi *Trading* Saham/Kripto.
* **Fokus Docker:** *High Availability*. Mempraktikkan skenario *failover* manual atau menggunakan Docker Swarm dasar, di mana jika satu container *Order Engine* dimatikan paksa (simulasi mati listrik), transaksi pengguna dialihkan ke replika container lainnya tanpa *error*.

## Rencana Silabus Praktikum Cloud (5 Pertemuan)

| Pertemuan | Fokus Utama | Aktivitas & Praktikum |
| --- | --- | --- |
| **1** | **Cloud Architecture Fundamentals** | Pengenalan topologi cloud. Praktik konfigurasi dasar untuk *Availability* (Multi-AZ), *Elasticity* (Auto-scaling groups), dan *Disaster Recovery* (Strategi backup & replikasi). Pembagian studi kasus kelompok. |
| **2** | **Migrasi & Microservices (dengan AI)** | Transformasi dari *Aplikasi Awal* (Monolitik) ke *Aplikasi Akhir* (Microservices). **Penggunaan AI:** Praktikan menggunakan AI (seperti ChatGPT/Copilot) untuk men-generate rancangan *Domain-Driven Design*, memecah kode monolit menjadi servis terpisah, dan membuat *boilerplate* konfigurasi Docker/Kubernetes. |
| **3** | **Deployment Cloud & Integrasi** | Mengunggah arsitektur microservices ke environment cloud (AWS/GCP/Azure). Mengonfigurasi Load Balancer, API Gateway, dan memastikan komunikasi antar-microservices berjalan stabil. |
| **4** | **Plan & Simulation (Load Testing)** | Pengenalan *tools* uji beban (JMeter, K6, atau Locust). Setiap kelompok menyusun skrip skenario pengujian bertahap dari 1 hingga 500 *virtual users* sesuai *endpoints* pada kasus masing-masing. |
| **5** | **Extreme Test & Evaluasi Arsitektur** | Eksekusi *Stress Test* hingga 1000 *virtual users*. Praktikan memantau metrik performa (CPU, latensi, *error rate*), mengevaluasi apakah sistem berhasil melakukan *auto-scaling* secara elastis, dan mempresentasikan laporannya. |

---

## Pembagian Kelompok & Studi Kasus Spesifik

Setiap kelompok memulai praktikum dari "Aplikasi Awal" (sistem tradisional/monolitik) dan harus membangun "Aplikasi Akhir" berupa arsitektur microservices modern di cloud dengan kasus berikut:

* **Kelompok 1 (Nidzom, Azzam, Fahmud, Jabbar, Faisal)**
* **Kasus:** Platform *Ticketing* Konser Online.
* **Fokus Arsitektur:** *Elasticity* ekstrem untuk menangani lonjakan ribuan *virtual users* secara mendadak saat sesi "War Tiket" dibuka. Microservice terpisah untuk sistem antrean (Queue) dan pembayaran.


* **Kelompok 2 (Zani, Resti, Faizah, *[Nama 4]*, *[Nama 5]*)**
* **Kasus:** Sistem E-Learning Berbasis Ujian Serentak.
* **Fokus Arsitektur:** Kestabilan sesi (Session management) dan ketersediaan data soal saat diakses ratusan siswa bersamaan. Microservice terpisah untuk *Streaming* video materi dan *Scoring* ujian.


* **Kelompok 3 (Alvira, Titha, Ella, Elvira)**
* **Kasus:** Aplikasi E-Commerce *Flash Sale*.
* **Fokus Arsitektur:** Sinkronisasi *database* dan *caching* (misal Redis) untuk mencegah *overselling* barang. Microservice terpisah untuk manajemen Inventaris, Keranjang Belanja, dan Katalog Produk.


* **Kelompok 4 (Yudis, Agra, Qosi, Diaz, Daffa)**
* **Kasus:** Sistem Informasi Medis Rumah Sakit.
* **Fokus Arsitektur:** *Disaster Recovery* dengan metrik RTO (Recovery Time Objective) ketat untuk rekam medis pasien. Pengamanan data dan pemisahan microservice antara Data Pasien, Apotek, dan Jadwal Dokter.


* **Kelompok 5 (Anisa, Frisillia, Riyana, Salsa, Ima)**
* **Kasus:** Platform *Ride-Hailing* (Ojek Online).
* **Fokus Arsitektur:** Latensi rendah untuk *tracking* GPS. Penggunaan AI untuk men-generate algoritma *matching* penumpang-driver di *Aplikasi Akhir*. Microservice terpisah untuk Lokasi, *Matching*, dan Dompet Digital.


* **Kelompok 6 (Faiq, Hakim, Faisol, Darma)**
* **Kasus:** Aplikasi *Trading* Saham/Kripto.
* **Fokus Arsitektur:** *High Availability* 99.99%. Jika server utama mati, *failover* harus berjalan tanpa transaksi yang hilang. Microservice terpisah untuk *Order Engine*, *Live Price Feed*, dan Portofolio Pengguna.