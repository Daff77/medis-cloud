# PANDUAN PRAKTIKUM PERTEMUAN 2 (VERSI WSL / LINUX)
## SISTEM INFORMASI MEDIS RUMAH SAKIT — KELOMPOK 4
**Topik:** Transformasi Monolitik ke Microservices, Implementasi AI, Dockerfile, & Docker Network

Panduan ini dikhususkan bagi Anda yang menjalankan Docker melalui **WSL (Windows Subsystem for Linux / Ubuntu)**.

---

### A. Persiapan Lingkungan WSL

#### 1. Masuk ke Terminal WSL
Buka terminal PowerShell atau Windows Terminal, lalu ketik:
```bash
wsl
```
*(Atau langsung buka aplikasi **Ubuntu** dari Start Menu Windows)*.

#### 2. Pindah ke Folder Proyek di WSL
Di dalam terminal WSL/Ubuntu, jalankan:
```bash
cd "/mnt/c/DaffaP/KULIAH_DAFFA/Semester_5/CC/Pertemuan 8/medis-cloud"
pwd
ls -la
```

#### 3. Verifikasi Docker Aktif di WSL
Pastikan Docker Engine terhubung:
```bash
docker version
```
*Jika bagian **Server: Docker Desktop Engine** muncul, berarti integrasi Docker WSL sudah siap 100%!*

---

### B. Opsi 1: Eksekusi Cepat (Skrip Otomatis Bash)

Kelompok telah menyediakan skrip bash executable di dalam folder `scripts/`:

```bash
# 1. Jalankan & uji baseline Monolitik (Praktik A)
./scripts/run-monolit.sh

# 2. Setup Network 'medis-net' & jalankan 3 Microservices (Praktik B & C)
./scripts/run-microservices.sh

# 3. Jalankan seluruh skenario pengujian REST API & Komunikasi Inter-Service (Praktik D)
./scripts/test-services.sh

# 4. Hentikan dan bersihkan kontainer setelah praktikum
./scripts/stop-all.sh
```

---

### C. Opsi 2: Eksekusi Manual Bertahap (Step-by-Step Bash & Curl)

Gunakan langkah manual ini untuk memahami setiap tahapan dan mengambil screenshot bukti pengujian untuk laporan.

---

#### TAHAP 1: Praktik A — Menjalankan Aplikasi Awal (Monolitik)
*Tujuan: Memahami baseline aplikasi rumah sakit sebelum dipisah.*

1. **Pindah ke folder monolit dan build image**:
   ```bash
   cd "/mnt/c/DaffaP/KULIAH_DAFFA/Semester_5/CC/Pertemuan 8/medis-cloud/monolit"
   docker build -t medis-monolit:1.0 .
   ```
2. **Jalankan container monolitik di port 5000**:
   ```bash
   docker run -d --name app-monolit -p 5000:5000 medis-monolit:1.0
   docker ps --filter "name=app-monolit"
   ```
3. **Uji endpoint monolitik dengan `curl`**:
   ```bash
   # Healthcheck
   curl -s http://localhost:5000/health | python3 -m json.tool

   # Kueri data pasien
   curl -s http://localhost:5000/api/pasien | python3 -m json.tool

   # Dashboard terpusat
   curl -s http://localhost:5000/api/dashboard | python3 -m json.tool
   ```
   *(📸 **Ambil Screenshot 1**: Hasil status container dan respon dashboard monolitik -> simpan sebagai `screenshots/A1-monolit-running.png`)*

4. **Hentikan container monolitik** agar port 5000 bebas:
   ```bash
   docker rm -f app-monolit
   ```

---

#### TAHAP 2: Praktik B1 — Membuat Docker Custom Bridge Network
*Tujuan: Mengaktifkan DNS Service Discovery internal antar-kontainer.*

```bash
docker network create --driver bridge medis-net
docker network ls --filter "name=medis-net"
docker network inspect medis-net --format "Subnet: {{range .IPAM.Config}}{{.Subnet}}{{end}}"
```
*(📸 **Ambil Screenshot 2**: Hasil output `docker network inspect medis-net` -> simpan sebagai `screenshots/B1-docker-network.png`)*

---

#### TAHAP 3: Praktik B2 — Membangun 3 Image Microservices
*Tujuan: Membungkus kode masing-masing Bounded Context DDD (Pasien, Apotek, Jadwal).*

```bash
BASE="/mnt/c/DaffaP/KULIAH_DAFFA/Semester_5/CC/Pertemuan 8/medis-cloud/services"

# 1. Build Service Pasien (Port 5001)
cd "$BASE/pasien"
docker build -t medis-pasien:1.0 .

# 2. Build Service Apotek (Port 5002)
cd "$BASE/apotek"
docker build -t medis-apotek:1.0 .

# 3. Build Service Jadwal Dokter (Port 5003)
cd "$BASE/jadwal-dokter"
docker build -t medis-jadwal:1.0 .

# Verifikasi image
docker images | grep "medis-"
```
*(📸 **Ambil Screenshot 3**: Daftar 3 image Docker `medis-*` -> simpan sebagai `screenshots/B2-docker-images.png`)*

---

#### TAHAP 4: Praktik C — Menjalankan Ketiga Kontainer Microservices
*Catatan: Environment variable `PASIEN_SERVICE_URL` diarahkan ke hostname DNS kontainer `http://service-pasien:5001`.*

```bash
# 1. Jalankan Service Pasien
docker run -d --name service-pasien \
    --network medis-net \
    -p 5001:5001 \
    medis-pasien:1.0

# 2. Jalankan Service Apotek
docker run -d --name service-apotek \
    --network medis-net \
    -p 5002:5002 \
    -e PASIEN_SERVICE_URL="http://service-pasien:5001" \
    medis-apotek:1.0

# 3. Jalankan Service Jadwal Dokter
docker run -d --name service-jadwal \
    --network medis-net \
    -p 5003:5003 \
    -e PASIEN_SERVICE_URL="http://service-pasien:5001" \
    medis-jadwal:1.0

# Verifikasi ketiga container berstatus Up
docker ps --filter "name=service-"
```
*(📸 **Ambil Screenshot 4**: Output `docker ps` menampilkan 3 kontainer aktif -> simpan sebagai `screenshots/C1-services-running.png`)*

---

#### TAHAP 5: Praktik D — Pengujian Integrasi REST API & Komunikasi Inter-Service

##### 1. Healthcheck Semua Service:
```bash
curl -s http://localhost:5001/health | python3 -m json.tool
curl -s http://localhost:5002/health | python3 -m json.tool
curl -s http://localhost:5003/health | python3 -m json.tool
```

##### 2. Registrasi Pasien Baru di Service Pasien:
```bash
curl -s -X POST http://localhost:5001/api/pasien \
    -H "Content-Type: application/json" \
    -d '{
        "nik": "3578010404950004",
        "nama": "Pasien Baru Kelompok 4",
        "tgl_lahir": "1995-04-04",
        "riwayat_alergi": "Penisilin"
    }' | python3 -m json.tool
```

##### 3. Penebusan Resep di Service Apotek (Cross-Service Call & Deteksi Alergi):
*Pasien 1 alergi **Penisilin**. Dokter meresepkan antibiotik **Amoxicillin**.*
```bash
curl -s -X POST http://localhost:5002/api/resep \
    -H "Content-Type: application/json" \
    -d '{
        "pasien_id": 1,
        "obat_id": 2,
        "jumlah": 10,
        "aturan_pakai": "3x1 tablet sesudah makan"
    }' | python3 -m json.tool
```
*Hasil: Service Apotek memanggil `http://service-pasien:5001` via internal DNS, memverifikasi riwayat alergi, dan mengeluarkan peringatan bahaya alergi!*
*(📸 **Ambil Screenshot 5**: Respon JSON memuat peringatan alergi -> simpan sebagai `screenshots/D1-resep-cross-service.png`)*

##### 4. Pendaftaran Janji Temu di Service Jadwal Dokter:
```bash
curl -s -X POST http://localhost:5003/api/janji-temu \
    -H "Content-Type: application/json" \
    -d '{
        "pasien_id": 2,
        "dokter_id": 1,
        "tgl_periksa": "2026-11-10",
        "keluhan": "Pemeriksaan kesehatan rutin"
    }' | python3 -m json.tool
```
*Hasil: Service Jadwal memvalidasi pasien dan menerbitkan no antrean otomatis `POLI-01-001`.*
*(📸 **Ambil Screenshot 6**: Respon JSON booking janji temu -> simpan sebagai `screenshots/D2-janji-temu.png`)*

##### 5. Uji Isolasi Jaringan (Security Boundary):
*Buktikan kontainer dari luar `medis-net` tidak bisa mengakses rekam medis pasien:*
```bash
docker run --rm alpine ping -c 2 service-pasien
```
*Hasil yang diharapkan: `ping: bad address 'service-pasien'` (resolusi DNS internal ditolak).*
*(📸 **Ambil Screenshot 7**: Bukti kegagalan ping dari luar jaringan -> simpan sebagai `screenshots/D3-network-isolation.png`)*

##### 6. Uji Fault Tolerance (Saat Service Pasien Dihentikan):
```bash
# Matikan kontainer Service Pasien sementara
docker stop service-pasien

# Uji apakah Service Apotek dan Jadwal Dokter tetap melayani kueri lokal:
curl -s http://localhost:5002/api/obat | python3 -m json.tool
curl -s http://localhost:5003/api/dokter | python3 -m json.tool

# Nyalakan kembali
docker start service-pasien
```
*Hasil: Apotek dan Jadwal tetap melayani data katalog lokal tanpa mengalami crash!*
*(📸 **Ambil Screenshot 8**: Output kueri obat & dokter saat service-pasien dihentikan -> simpan sebagai `screenshots/D4-fault-isolation.png`)*

---

### D. Pembersihan Kontainer Setelah Selesai
Untuk menghentikan dan membersihkan semua kontainer serta network praktikum:
```bash
cd "/mnt/c/DaffaP/KULIAH_DAFFA/Semester_5/CC/Pertemuan 8/medis-cloud"
./scripts/stop-all.sh
```

---

### E. Ringkasan File Screenshot untuk Laporan Word
File screenshot yang Anda ambil dapat ditaruh di folder `screenshots/` untuk melengkapi dokumen:
📄 **[Laporan_Praktikum_Pertemuan_2_Kelompok_4.docx](file:///c:/DaffaP/KULIAH_DAFFA/Semester_5/CC/Pertemuan%208/Laporan_Praktikum_Pertemuan_2_Kelompok_4.docx)**

1. `A1-monolit-running.png` : Status kontainer monolitik port 5000 & respon dashboard.
2. `B1-docker-network.png`   : Subnet hasil inspect custom bridge network `medis-net`.
3. `B2-docker-images.png`    : Output daftar image `medis-pasien`, `medis-apotek`, `medis-jadwal`.
4. `C1-services-running.png` : Output `docker ps` ketiga microservices berstatus Up.
5. `D1-resep-cross-service.png` : Respon resep memuat peringatan kontraindikasi alergi.
6. `D2-janji-temu.png`       : Respon booking janji temu dengan nomor antrean `POLI-01-001`.
7. `D3-network-isolation.png`: Pesan `ping: bad address` saat diakses kontainer luar.
8. `D4-fault-isolation.png`  : Kueri obat & dokter tetap berhasil saat `service-pasien` down.
