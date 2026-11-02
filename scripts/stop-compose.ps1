# ========================================================
# Script: stop-compose.ps1
# Praktikum Cloud Pertemuan 3 - Kelompok 4
# Menghentikan Layanan Docker Compose
# ========================================================

$RootPath = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RootPath

Write-Host ">>> Menghentikan seluruh container Docker Compose..." -ForegroundColor Yellow
docker compose down

Write-Host "`n>>> Status container saat ini:" -ForegroundColor Cyan
docker compose ps

Write-Host "`n[INFO] Layanan berhasil dihentikan. Data pada Docker Volume tetap tersimpan aman." -ForegroundColor Green

