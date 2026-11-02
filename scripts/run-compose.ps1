# ========================================================
# Script: run-compose.ps1
# Praktikum Cloud Pertemuan 3 - Kelompok 4
# Menjalankan Seluruh Stack Microservices via Docker Compose
# ========================================================

$RootPath = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RootPath

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  MENJALANKAN ORKESTRASI DOCKER COMPOSE MEDIS-CLOUD       " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Bersihkan sisa kontainer lama jika ada
Write-Host "`n>>> [1/4] Membersihkan kontainer lama..." -ForegroundColor Yellow
docker rm -f app-monolit service-pasien service-apotek service-jadwal nginx-gateway 2>$null
docker compose down --remove-orphans 2>$null

# 2. Build images
Write-Host "`n>>> [2/4] Membangun images via Docker Compose..." -ForegroundColor Cyan
docker compose build

# 3. Jalankan stack di background
Write-Host "`n>>> [3/4] Menjalankan layanan (Gateway & 3 Microservices)..." -ForegroundColor Green
docker compose up -d

Write-Host "`nMenunggu inisialisasi healthcheck (6 detik)..." -ForegroundColor Yellow
Start-Sleep -Seconds 6

# 4. Tampilkan status container
Write-Host "`n>>> [4/4] Status Layanan Docker Compose:" -ForegroundColor Cyan
docker compose ps

Write-Host "`n>>> Pengujian Akses Nginx API Gateway (Port 8080):" -ForegroundColor Green
try {
    $gw = Invoke-RestMethod -Uri "http://localhost:8080/" -Method Get
    $gw | ConvertTo-Json
    Write-Host "`n[SUKSES] Nginx API Gateway aktif di http://localhost:8080" -ForegroundColor Green
} catch {
    Write-Warning "Gagal menghubungi Gateway: $_"
}

