# PANDUAN PRAKTIKUM PERTEMUAN 2
## SISTEM INFORMASI MEDIS RUMAH SAKIT (KELOMPOK 4)
**Topik:** Transformasi Monolitik ke Microservices, Implementasi AI, Dockerfile, & Docker Network

---

### A. Prasyarat Sebelum Memulai
1. **Buka Docker Desktop**: Pastikan ikon paus di system tray berstatus **"Engine running"**.
2. **Buka PowerShell**: Buka terminal Windows PowerShell (rekomendasi: *Run as Administrator*).
3. **Pindah ke Direktori Proyek**:
   ```powershell
   Set-Location "C:\DaffaP\KULIAH_DAFFA\Semester_5\CC\Pertemuan 8\medis-cloud"
   ```

---

### B. Alur Eksekusi Praktikum (Step-by-Step)

#### TAHAP 1: Menjalankan Aplikasi Awal (Monolitik)
*Tujuan: Memahami baseline aplikasi rumah sakit sebelum dipisah.*
1. **Pindah ke folder monolit & bangun image**:
   ```powershell
   Set-Location "C:\DaffaP\KULIAH_DAFFA\Semester_5\CC\Pertemuan 8\medis-cloud\monolit"
   docker build -t medis-monolit:1.0 .
   ```
2. **Jalankan container monolitik di port 5000**:
   ```powershell
   docker run -d --name app-monolit -p 5000:5000 medis-monolit:1.0
   ```
3. **Uji endpoint monolitik**:
   ```powershell
   # Healthcheck
   (Invoke-WebRequest -Uri "http://localhost:5000/health" -UseBasicParsing).Content

   # Data Pasien
   (Invoke-WebRequest -Uri "http://localhost:5000/api/pasien" -UseBasicParsing).Content

   # Dashboard Terpusat
   (Invoke-WebRequest -Uri "http://localhost:5000/api/dashboard" -UseBasicParsing).Content
   ```
4. **Hentikan container monolitik** (agar port dan resource bebas):
   ```powershell
   docker rm -f app-monolit
   ```

---

#### TAHAP 2: Membuat Docker Custom Bridge Network
*Tujuan: Mengaktifkan Automatic DNS Service Discovery antar-kontainer.*
```powershell
docker network create --driver bridge medis-net
docker network ls --filter "name=medis-net"
```

---

#### TAHAP 3: Membangun Image Ketiga Microservices
*Tujuan: Membungkus kode layanan Pasien, Apotek, dan Jadwal Dokter ke image Docker masing-masing.*
```powershell
$Base = "C:\DaffaP\KULIAH_DAFFA\Semester_5\CC\Pertemuan 8\medis-cloud\services"

# 1. Service Pasien (Port 5001)
Set-Location (Join-Path $Base "pasien")
docker build -t medis-pasien:1.0 .

# 2. Service Apotek (Port 5002)
Set-Location (Join-Path $Base "apotek")
docker build -t medis-apotek:1.0 .

# 3. Service Jadwal Dokter (Port 5003)
Set-Location (Join-Path $Base "jadwal-dokter")
docker build -t medis-jadwal:1.0 .

# Verifikasi image
docker images | Select-String "medis-"
```

---

#### TAHAP 4: Menjalankan Ketiga Kontainer ke dalam Network `medis-net`
*Catatan: Environment variable `PASIEN_SERVICE_URL` diarahkan ke hostname DNS kontainer `http://service-pasien:5001`.*
```powershell
# 1. Jalankan Service Pasien
docker run -d --name service-pasien `
    --network medis-net `
    -p 5001:5001 `
    medis-pasien:1.0

# 2. Jalankan Service Apotek
docker run -d --name service-apotek `
    --network medis-net `
    -p 5002:5002 `
    -e PASIEN_SERVICE_URL="http://service-pasien:5001" `
    medis-apotek:1.0

# 3. Jalankan Service Jadwal Dokter
docker run -d --name service-jadwal `
    --network medis-net `
    -p 5003:5003 `
    -e PASIEN_SERVICE_URL="http://service-pasien:5001" `
    medis-jadwal:1.0

# Periksa status kontainer
docker ps --filter "name=service-"
```

---

#### TAHAP 5: Pengujian Integrasi REST API & Komunikasi Lintas Kontainer

##### 1. Healthcheck Semua Service:
```powershell
(Invoke-WebRequest -Uri "http://localhost:5001/health" -UseBasicParsing).Content
(Invoke-WebRequest -Uri "http://localhost:5002/health" -UseBasicParsing).Content
(Invoke-WebRequest -Uri "http://localhost:5003/health" -UseBasicParsing).Content
```

##### 2. Registrasi Pasien Baru di Service Pasien:
```powershell
$pasienBaru = @{
    nik = "3578010404950004"
    nama = "Pasien Baru Kelompok 4"
    tgl_lahir = "1995-04-04"
    riwayat_alergi = "Penisilin"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5001/api/pasien" -Method Post -Body $pasienBaru -ContentType "application/json"
```

##### 3. Penebusan Resep di Service Apotek (Cross-Service Call & Deteksi Alergi):
*Meminta obat Amoxicillin untuk Pasien ID 1 (yang memiliki riwayat alergi Penisilin).*
```powershell
$resepBody = @{
    pasien_id = 1
    obat_id = 2
    jumlah = 10
    aturan_pakai = "3x1 sehari sesudah makan"
} | ConvertTo-Json

$resResep = Invoke-RestMethod -Uri "http://localhost:5002/api/resep" -Method Post -Body $resepBody -ContentType "application/json"
$resResep | ConvertTo-Json -Depth 4
```
*Hasil: Service Apotek memanggil Service Pasien via DNS Docker, mendeteksi alergi, dan mengeluarkan peringatan kontraindikasi!*

##### 4. Pendaftaran Janji Temu di Service Jadwal Dokter:
```powershell
$janjiBody = @{
    pasien_id = 2
    dokter_id = 1
    tgl_periksa = "2026-11-10"
    keluhan = "Pemeriksaan kesehatan rutin"
} | ConvertTo-Json

$resJanji = Invoke-RestMethod -Uri "http://localhost:5003/api/janji-temu" -Method Post -Body $janjiBody -ContentType "application/json"
$resJanji | ConvertTo-Json -Depth 4
```

##### 5. Uji Isolasi Jaringan (Security Boundary):
*Buktikan kontainer di luar jaringan tidak dapat menghubungi internal service:*
```powershell
docker run --rm alpine ping -c 2 service-pasien
# Hasil yang diharapkan: ping: bad address 'service-pasien'
```

##### 6. Uji Fault Tolerance (Saat Service Pasien Dihentikan):
```powershell
docker stop service-pasien

# Layanan Apotek & Jadwal tetap bisa melayani katalog & jadwal lokal:
(Invoke-WebRequest -Uri "http://localhost:5002/api/obat" -UseBasicParsing).Content
(Invoke-WebRequest -Uri "http://localhost:5003/api/dokter" -UseBasicParsing).Content

# Nyalakan kembali
docker start service-pasien
```

---

### C. Eksekusi Cepat Menggunakan Skrip Otomatis (.ps1)
Kelompok sudah menyediakan script siap pakai di folder `scripts/`:

1. **Jalankan Monolit**:
   ```powershell
   & "C:\DaffaP\KULIAH_DAFFA\Semester_5\CC\Pertemuan 8\medis-cloud\scripts\run-monolit.ps1"
   ```
2. **Jalankan Seluruh Microservices & Network**:
   ```powershell
   & "C:\DaffaP\KULIAH_DAFFA\Semester_5\CC\Pertemuan 8\medis-cloud\scripts\run-microservices.ps1"
   ```
3. **Jalankan Semua Skenario Uji Otomatis**:
   ```powershell
   & "C:\DaffaP\KULIAH_DAFFA\Semester_5\CC\Pertemuan 8\medis-cloud\scripts\test-services.ps1"
   ```
4. **Hentikan & Bersihkan Kontainer**:
   ```powershell
   & "C:\DaffaP\KULIAH_DAFFA\Semester_5\CC\Pertemuan 8\medis-cloud\scripts\stop-all.ps1"
   ```

---

### D. Daftar Screenshot untuk Laporan Word
Ambil screenshot terminal saat menjalankan perintah di atas dan simpan ke folder `screenshots/` untuk melengkapi dokumen:
1. `A1-monolit-running.png`: Output `docker ps` dan curl/Invoke-WebRequest port 5000.
2. `B1-docker-images.png`: Output `docker images` yang memuat ketiga image `medis-*.`
3. `C1-docker-network.png`: Output `docker network inspect medis-net`.
4. `C2-network-isolation.png`: Output `docker run --rm alpine ping service-pasien` yang menghasilkan *bad address*.
5. `D1-resep-cross-service.png`: Output JSON respon resep dengan peringatan alergi.
6. `D2-janji-temu.png`: Output JSON respon booking antrean dokter.
7. `D3-fault-isolation.png`: Output kueri obat/dokter saat container pasien di-stop.
