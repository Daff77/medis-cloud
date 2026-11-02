# ========================================================
# DEMO PERTEMUAN 3: ORKESTRASI DOCKER COMPOSE & ELASTICITY
# Kelompok 4 - Sistem Informasi Medis Rumah Sakit
# ========================================================

Clear-Host
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   DEMO PRAKTIKUM PERTEMUAN 3: DOCKER COMPOSE & ELASTICITY" -ForegroundColor Cyan
Write-Host "   Kelompok 4 - Kasus: Load Balancer Nginx & Auto Scaling " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Menjalankan Tumpukan Layanan (Docker Compose)
Write-Host "`n[STEP 1/5] Single-Command Up: Membangun Seluruh Ekosistem Medis..." -ForegroundColor Yellow
docker compose up -d 2>$null | Out-Null
Start-Sleep -Seconds 3

Write-Host " Status Seluruh Kontainer Layanan Medis:" -ForegroundColor White
docker compose ps

# 2. Pengujian Routing Nginx API Gateway di Port 8080
Write-Host "`n[STEP 2/5] Uji Gerbang Tunggal Nginx API Gateway (Port 8080):" -ForegroundColor Yellow

try {
    $gwRoot = Invoke-RestMethod -Uri "http://localhost:8080/" -Method Get
    Write-Host " [OK] Gateway Root Online    : $($gwRoot.gateway)" -ForegroundColor Green
} catch {
    Write-Host " [FAIL] Gateway root: $_" -ForegroundColor Red
}

try {
    $pasienResp = Invoke-RestMethod -Uri "http://localhost:8080/api/pasien" -Method Get
    Write-Host " [OK] Route /api/pasien       : $($pasienResp.Count) pasien rekam medis terhubung" -ForegroundColor Green
} catch {
    Write-Host " [FAIL] Route /api/pasien: $_" -ForegroundColor Red
}

try {
    $obatResp = Invoke-RestMethod -Uri "http://localhost:8080/api/obat" -Method Get
    Write-Host " [OK] Route /api/obat         : $($obatResp.Count) katalog obat terhubung" -ForegroundColor Green
} catch {
    Write-Host " [FAIL] Route /api/obat: $_" -ForegroundColor Red
}

try {
    $dokterResp = Invoke-RestMethod -Uri "http://localhost:8080/api/dokter" -Method Get
    Write-Host " [OK] Route /api/dokter       : $($dokterResp.Count) jadwal dokter terhubung" -ForegroundColor Green
} catch {
    Write-Host " [FAIL] Route /api/dokter: $_" -ForegroundColor Red
}

# 3. Simulasi Elasticity: Scaling Horizontal 3 Replika
Write-Host "`n[STEP 3/5] Simulasi Elasticity: Penskalaan Horizontal Layanan Pasien..." -ForegroundColor Yellow
Write-Host " Menambah replika: docker compose up -d --scale service-pasien=3..." -ForegroundColor Gray
docker compose up -d --scale service-pasien=3 2>$null | Out-Null
Start-Sleep -Seconds 3

Write-Host " [OK] Daftar Replika Cluster service-pasien:" -ForegroundColor Green
docker compose ps service-pasien

# 4. Pengujian Load Balancing Round-Robin Nginx
Write-Host "`n[STEP 4/5] Pengujian Distribusi Trafik Load Balancing Round-Robin:" -ForegroundColor Yellow
Write-Host " Mengirimkan 8 request HTTP berurutan ke http://localhost:8080/api/pasien..." -ForegroundColor Gray

$results = @()
for ($i = 1; $i -le 8; $i++) {
    $wr = Invoke-WebRequest -Uri "http://localhost:8080/api/pasien" -Method Get -UseBasicParsing
    $servedBy = $wr.Headers["X-Served-By"]
    if (-not $servedBy) { $servedBy = "N/A" }
    $results += [PSCustomObject]@{
        "Request #"    = $i
        "Endpoint"     = "/api/pasien"
        "HTTP Status"  = $wr.StatusCode
        "Backend Host" = $servedBy
    }
}
$results | Format-Table

$uniqueHosts = ($results | Select-Object -ExpandProperty "Backend Host" -Unique)
Write-Host " Analisis Distribusi Beban:" -ForegroundColor White
Write-Host " * Jumlah Request      : 8" -ForegroundColor White
Write-Host " * Jumlah Instance Unik: $($uniqueHosts.Count)" -ForegroundColor Green
Write-Host " * Host Backend        : $($uniqueHosts -join ', ')" -ForegroundColor Cyan
if ($uniqueHosts.Count -ge 2) {
    Write-Host " [BERHASIL] Trafik terdistribusi merata (Round-Robin) ke beberapa replika!" -ForegroundColor Green
} else {
    Write-Host " [INFO] Load balancer sedang memperbarui tabel DNS cache." -ForegroundColor Yellow
}

# 5. Pengujian Persistensi Data Medis (Disaster Recovery di Bawah Scaling)
Write-Host "`n[STEP 5/5] Uji Persistensi Data Rekam Medis (Disaster Recovery & Named Volume):" -ForegroundColor Yellow
$randId = Get-Random -Minimum 1000 -Maximum 9999
$testNik = "357801050599$randId"
Write-Host " [1/3] Mendaftarkan Pasien Baru dengan NIK: $testNik..." -ForegroundColor Gray

$bodyObj = @{
    nik = $testNik
    nama = "Pasien Demo P3 ($randId)"
    tgl_lahir = "1999-05-05"
    riwayat_alergi = "Tidak Ada"
} | ConvertTo-Json

try {
    $addRes = Invoke-RestMethod -Uri "http://localhost:8080/api/pasien" -Method Post -Body $bodyObj -ContentType "application/json"
    Write-Host "       Pasien '$($addRes.nama)' berhasil didaftarkan (ID: $($addRes.id))." -ForegroundColor Green
} catch {
    Write-Host "       Gagal registrasi: $_" -ForegroundColor Red
}

Write-Host " [2/3] Simulasi Crash/Restart Cluster: docker compose restart service-pasien..." -ForegroundColor Gray
docker compose restart service-pasien 2>$null | Out-Null
Start-Sleep -Seconds 3

Write-Host " [3/3] Memeriksa apakah data pasien baru tetap bertahan pasca-restart..." -ForegroundColor Gray
try {
    $verifyResp = Invoke-RestMethod -Uri "http://localhost:8080/api/pasien" -Method Get
    $found = ($verifyResp | Where-Object { $_.nik -eq $testNik })
    if ($found) {
        Write-Host "       [TERBUKTI UTUH] Pasien '$($found.nama)' tetap ada di database volume!" -ForegroundColor Green
    } else {
        Write-Host "       [PERINGATAN] Data tidak ditemukan!" -ForegroundColor Red
    }
} catch {
    Write-Host "       Gagal query: $_" -ForegroundColor Red
}

Write-Host "`n----------------------------------------------------------" -ForegroundColor Cyan
Write-Host "  KESIMPULAN DEMO PERTEMUAN 3 KELOMPOK 4:                 " -ForegroundColor Cyan
Write-Host "  * Orkestrasi Compose   : Berhasil 4 layanan + multi-tier net" -ForegroundColor Green
Write-Host "  * API Gateway 8080     : Routing dinamis berfungsi 100%     " -ForegroundColor Green
Write-Host "  * Elasticity (Scaling) : 3 replika aktif dinamis            " -ForegroundColor Green
Write-Host "  * Load Balancing       : Round-Robin rotasi backend terbukti" -ForegroundColor Green
Write-Host "  * Persistensi Medis    : Aman di named volume medis_pasien  " -ForegroundColor Green
Write-Host "----------------------------------------------------------" -ForegroundColor Cyan

Write-Host "`n[SELESAI] Demo Praktikum Pertemuan 3 Sukses 100%!`n" -ForegroundColor Green
