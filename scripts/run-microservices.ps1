# ========================================================
# Script: run-microservices.ps1
# Build & Jalankan 3 Microservices dalam Docker Network 'medis-net'
# ========================================================

$RootPath = Resolve-Path (Join-Path $PSScriptRoot "..")
$ServicesDir = Join-Path $RootPath "services"

# 1. Pastikan Network ada
& (Join-Path $PSScriptRoot "setup-network.ps1")

# 2. Hentikan container lama jika ada
Write-Host "`n>>> Membersihkan container lama..." -ForegroundColor Yellow
docker rm -f service-pasien service-apotek service-jadwal 2>$null

# 3. Build Images
Write-Host "`n>>> 1. Membangun Image Service Pasien..." -ForegroundColor Cyan
Set-Location (Join-Path $ServicesDir "pasien")
docker build -t medis-pasien:1.0 .

Write-Host "`n>>> 2. Membangun Image Service Apotek..." -ForegroundColor Cyan
Set-Location (Join-Path $ServicesDir "apotek")
docker build -t medis-apotek:1.0 .

Write-Host "`n>>> 3. Membangun Image Service Jadwal Dokter..." -ForegroundColor Cyan
Set-Location (Join-Path $ServicesDir "jadwal-dokter")
docker build -t medis-jadwal:1.0 .

# 4. Jalankan Containers di dalam network medis-net
Write-Host "`n>>> Menjalankan Service Pasien di port 5001..." -ForegroundColor Green
docker run -d --name service-pasien `
    --network medis-net `
    -p 5001:5001 `
    medis-pasien:1.0

Write-Host ">>> Menjalankan Service Apotek di port 5002..." -ForegroundColor Green
docker run -d --name service-apotek `
    --network medis-net `
    -p 5002:5002 `
    -e PASIEN_SERVICE_URL="http://service-pasien:5001" `
    medis-apotek:1.0

Write-Host ">>> Menjalankan Service Jadwal Dokter di port 5003..." -ForegroundColor Green
docker run -d --name service-jadwal `
    --network medis-net `
    -p 5003:5003 `
    -e PASIEN_SERVICE_URL="http://service-pasien:5001" `
    medis-jadwal:1.0

Start-Sleep -Seconds 4

Write-Host "`n>>> Status Semua Container Microservices:" -ForegroundColor Cyan
docker ps --filter "name=service-"
