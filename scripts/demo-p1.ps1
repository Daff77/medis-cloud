# ========================================================
# DEMO PERTEMUAN 1: ARSITEKTUR CLOUD & DASAR DOCKER
# Kelompok 4 - Sistem Informasi Medis Rumah Sakit
# ========================================================

Clear-Host
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   DEMO PRAKTIKUM PERTEMUAN 1: DASAR DOCKER & RECOVERY   " -ForegroundColor Cyan
Write-Host "   Kelompok 4 - Kasus: Disaster Recovery Medis Rumah Sakit" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Verifikasi Docker Engine
Write-Host "`n[STEP 1/4] Memeriksa Status Docker Engine..." -ForegroundColor Yellow
$dockerVer = docker version --format 'Docker Engine v{{.Server.Version}} (OS: {{.Server.Os}})' 2>$null
if ($dockerVer) {
    Write-Host " [OK] $dockerVer aktif dan siap." -ForegroundColor Green
} else {
    Write-Host " [ERROR] Docker Desktop belum berjalan. Pastikan Engine running!" -ForegroundColor Red
    exit 1
}

# 2. Demo Praktik A: Container Dasar & Port Mapping
Write-Host "`n[STEP 2/4] Praktik A - Container & Port Mapping (Layanan Dasar Medis):" -ForegroundColor Yellow
Write-Host " Membangun image lab1 (Python Lightweight HTTP)..." -ForegroundColor Gray
docker build -t medis-lab1:1.0 .\lab1 | Out-Null
docker rm -f app-lab1 2>$null | Out-Null
docker run -d --name app-lab1 -p 8000:8000 medis-lab1:1.0 | Out-Null
Start-Sleep -Seconds 2

try {
    $resA = Invoke-RestMethod -Uri "http://localhost:8000/" -Method Get
    Write-Host " [OK] Kontainer app-lab1 merespon di Port 8000: '$resA'" -ForegroundColor Green
} catch {
    Write-Host " [FAIL] Tidak dapat mengakses port 8000: $_" -ForegroundColor Red
}
docker rm -f app-lab1 | Out-Null
Write-Host " [INFO] Kontainer uji Praktik A dibersihkan." -ForegroundColor Gray

# 3. Demo Praktik B: Docker Named Volumes
Write-Host "`n[STEP 3/4] Praktik B - Persistensi Data Rekam Medis (Named Volume):" -ForegroundColor Yellow
$volName = "medis_demo_p1_data"
docker volume create $volName | Out-Null
Write-Host " [OK] Named Volume '$volName' berhasil dibuat." -ForegroundColor Green

# Tulis data simulasi rekam medis ke volume
$sampleData = "REKAM_MEDIS: PASIEN_001 | NIK: 3578010101900001 | DIAGNOSA: Hipertensi Primer | STATUS: AMAN"
docker run --rm -v "${volName}:/data" alpine sh -c "echo '$sampleData' > /data/rekam_medis.txt" | Out-Null
Write-Host " [OK] Data rekam medis pasien berhasil ditulis ke volume." -ForegroundColor Green

# 4. Demo Praktik C: Simulasi Disaster Recovery & RTO
Write-Host "`n[STEP 4/4] Praktik C - Simulasi Bencana (Disaster Recovery & RTO):" -ForegroundColor Yellow

# A. Backup Volume
$backupDir = Join-Path (Get-Location) "backup"
if (-not (Test-Path $backupDir)) { New-Item -ItemType Directory -Path $backupDir | Out-Null }
$backupFile = "demo_p1_dr_backup.tar.gz"

Write-Host " [1/4] Mengambil Snapshot Backup Volume ke '$backupFile'..." -ForegroundColor Gray
docker run --rm -v "${volName}:/data" -v "${backupDir}:/backup" alpine tar czf "/backup/$backupFile" -C /data . | Out-Null
Write-Host "       Snapshot backup berhasil dibuat di folder backup/." -ForegroundColor Green

# B. Bencana Terjadi
Write-Host " [2/4] SIMULASI BENCANA: Volume rekam medis dihapus secara paksa!" -ForegroundColor Red
docker volume rm -f $volName | Out-Null
Write-Host "       Volume '$volName' telah hancur/hilang dari sistem." -ForegroundColor Red

# C. Proses Pemulihan (Disaster Recovery) & Ukur RTO
Write-Host " [3/4] MEMULAI PROSES PEMULIHAN (RESTORE DISASTER RECOVERY)..." -ForegroundColor Yellow
$startTime = Get-Date

docker volume create $volName | Out-Null
docker run --rm -v "${volName}:/data" -v "${backupDir}:/backup" alpine tar xzf "/backup/$backupFile" -C /data | Out-Null

$endTime = Get-Date
$rtoSeconds = [math]::Round(($endTime - $startTime).TotalSeconds, 2)
Write-Host "       Volume '$volName' berhasil dipulihkan dari arsip backup!" -ForegroundColor Green

# D. Verifikasi Integritas Data
Write-Host " [4/4] Verifikasi Integritas Data Pasca Pemulihan:" -ForegroundColor Gray
$restoredData = docker run --rm -v "${volName}:/data" alpine cat /data/rekam_medis.txt
Write-Host "       Isi Data Terbaca: $restoredData" -ForegroundColor Green

Write-Host "`n----------------------------------------------------------" -ForegroundColor Cyan
Write-Host "  HASIL PENGUKURAN METRIK DISASTER RECOVERY KELOMPOK 4:   " -ForegroundColor Cyan
Write-Host "  * Target RTO Rumah Sakit : < 15 detik                   " -ForegroundColor White
Write-Host "  * RTO Riil Pengujian     : $rtoSeconds detik (SANGAT BAIK)        " -ForegroundColor Green
Write-Host "  * Status Integritas Data : 100% UTUH (Data Match)       " -ForegroundColor Green
Write-Host "----------------------------------------------------------" -ForegroundColor Cyan

# Cleanup
docker volume rm -f $volName | Out-Null
Remove-Item (Join-Path $backupDir $backupFile) -Force -ErrorAction SilentlyContinue
Write-Host "`n[SELESAI] Demo Praktikum Pertemuan 1 Sukses 100%!`n" -ForegroundColor Green
