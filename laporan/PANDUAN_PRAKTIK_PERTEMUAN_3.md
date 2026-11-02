# PANDUAN PRAKTIKUM PERTEMUAN 3
## SISTEM INFORMASI MEDIS RUMAH SAKIT — KELOMPOK 4
**Topik:** Orkestrasi Docker Compose, Nginx Load Balancer, & Simulasi Elasticity

Panduan ini dapat dijalankan menggunakan **Windows PowerShell** maupun **WSL (Ubuntu Linux)**.

---

### A. Prasyarat Praktikum
1. **Docker Desktop**: Pastikan berstatus hijau (**"Engine running"**).
2. **Direktori Kerja**:
   * **PowerShell**:
     ```powershell
     cd "C:\DaffaP\KULIAH_DAFFA\Semester_5\CC\medis-cloud"
     ```
   * **WSL / Ubuntu**:
     ```bash
     cd "/mnt/c/DaffaP/KULIAH_DAFFA/Semester_5/CC/medis-cloud"
     ```

---

### B. Opsi 1: Eksekusi Cepat (Skrip Otomatis)

#### Menggunakan PowerShell:
```powershell
# 1. Jalankan seluruh layanan (Gateway & 3 Microservices)
& ".\scripts\run-compose.ps1"

# 2. Lakukan penskalaan horizontal (3 replika service-pasien)
& ".\scripts\scale-pasien.ps1"

# 3. Uji Load Balancing Round-Robin & Routing Gateway
& ".\scripts\test-loadbalance.ps1"

# 4. Hentikan stack compose jika sudah selesai
& ".\scripts\stop-compose.ps1"
```

#### Menggunakan WSL / Ubuntu:
```bash
# 1. Jalankan seluruh layanan
./scripts/run-compose.sh

# 2. Skalakan service-pasien menjadi 3 replika
./scripts/scale-pasien.sh

# 3. Uji Load Balancing Round-Robin
./scripts/test-loadbalance.sh

# 4. Hentikan layanan
./scripts/stop-compose.sh
```

---

### C. Opsi 2: Eksekusi Manual Bertahap (Step-by-Step)

Gunakan langkah manual ini untuk memahami setiap konsep dan mengambil screenshot untuk laporan praktikum.

---

#### TAHAP 1: Praktik A — Memeriksa Konfigurasi & Membangun Image
1. Periksa berkas `docker-compose.yml` dan `infra/nginx/nginx.conf`:
   ```bash
   cat docker-compose.yml
   ```
2. Build image seluruh layanan secara serentak:
   ```bash
   docker compose build
   ```

---

#### TAHAP 2: Praktik B — Menjalankan Stack Orkestrasi (`docker compose up`)
1. Jalankan seluruh layanan di background:
   ```bash
   docker compose up -d
   ```
2. Periksa status kontainer:
   ```bash
   docker compose ps
   ```
   *Hasil yang diharapkan: 4 kontainer aktif (`nginx-gateway`, `service-pasien-1`, `service-apotek-1`, `service-jadwal-1`) dengan status `Up (healthy)`.*
   *(📸 **Ambil Screenshot 1**: Output `docker compose ps` -> simpan sebagai `screenshots/A1-compose-up.png`)*

---

#### TAHAP 3: Praktik C — Pengujian Routing Nginx API Gateway (Port 8080)
*Buktikan seluruh layanan dapat diakses melalui satu gerbang tunggal di port 8080 tanpa mengakses port internal microservice.*

1. **Uji Gateway Root & Health**:
   ```bash
   curl -s http://localhost:8080/ | python3 -m json.tool
   curl -s http://localhost:8080/health | python3 -m json.tool
   ```

2. **Uji Routing ke Layanan Pasien**:
   ```bash
   curl -s http://localhost:8080/api/pasien | python3 -m json.tool
   ```

3. **Uji Routing ke Layanan Obat / Apotek**:
   ```bash
   curl -s http://localhost:8080/api/obat | python3 -m json.tool
   ```

4. **Uji Routing ke Layanan Dokter**:
   ```bash
   curl -s http://localhost:8080/api/dokter | python3 -m json.tool
   ```
   *(📸 **Ambil Screenshot 2**: Respon endpoint melalui port 8080 -> simpan sebagai `screenshots/B1-gateway-routing.png`)*

---

#### TAHAP 4: Praktik D — Simulasi Elasticity & Load Balancing (`--scale`)
*Tujuan: Mensimulasikan lonjakan pasien rumah sakit dengan menambah kapasitas replika secara horizontal.*

1. **Skalakan Layanan Pasien menjadi 3 Replika**:
   ```bash
   docker compose up -d --scale service-pasien=3
   ```
2. **Periksa Kontainer Pasien yang Bertambah**:
   ```bash
   docker compose ps service-pasien
   ```
   *Hasil yang diharapkan: Terdapat 3 kontainer `service-pasien` yang aktif (`service-pasien-1`, `service-pasien-2`, `service-pasien-3`).*
   *(📸 **Ambil Screenshot 3**: Daftar 3 kontainer `service-pasien` -> simpan sebagai `screenshots/C1-scale-pasien.png`)*

3. **Uji Distribusi Beban Round-Robin**:
   Kirimkan 6–8 request berturut-turut ke `/api/pasien` dan amati header `X-Served-By` atau `hostname`:
   * **Di PowerShell**:
     ```powershell
     & ".\scripts\test-loadbalance.ps1"
     ```
   * **Di WSL**:
     ```bash
     ./scripts/test-loadbalance.sh
     ```
   *Hasil yang diperoleh: Request didistribusikan bergantian ke ID kontainer yang berbeda (Round-Robin)!*
   *(📸 **Ambil Screenshot 4**: Tabel distribusi load balancing -> simpan sebagai `screenshots/C2-loadbalance-evidence.png`)*

---

#### TAHAP 5: Praktik E — Verifikasi Persistensi Data (Docker Named Volumes)
*Tujuan: Membuktikan data rekam medis pasien tidak hilang saat kontainer di-restart atau di-scale down.*

1. **Tambahkan Pasien Baru Melalui Gateway (Port 8080)**:
   ```bash
   curl -s -X POST http://localhost:8080/api/pasien \
       -H "Content-Type: application/json" \
       -d '{
           "nik": "3578010505990005",
           "nama": "Pasien Uji Elasticity",
           "tgl_lahir": "1999-05-05",
           "riwayat_alergi": "Tidak Ada"
       }' | python3 -m json.tool
   ```
2. **Restart Layanan Pasien**:
   ```bash
   docker compose restart service-pasien
   ```
3. **Cek Kembali Data Pasien**:
   ```bash
   curl -s http://localhost:8080/api/pasien | python3 -m json.tool
   ```
   *Hasil: Data "Pasien Uji Elasticity" tetap ada utuh di database volume `medis_pasien_data`!*
   *(📸 **Ambil Screenshot 5**: Kueri data pasien setelah restart -> simpan sebagai `screenshots/D1-persistence-check.png`)*

---

### D. Menghentikan Layanan
Setelah selesai praktikum dan mengambil screenshot:
```bash
docker compose down
```
*(Catatan: Perintah `docker compose down` hanya mematikan kontainer dan network; data rekam medis pada named volumes tetap tersimpan aman).*

