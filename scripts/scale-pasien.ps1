# ========================================================
# Script: scale-pasien.ps1
# Praktikum Cloud Pertemuan 3 - Kelompok 4
# Simulasi Elasticity: Scaling Service Pasien menjadi 3 Replika
# ========================================================

$RootPath = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RootPath

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  SIMULASI ELASTICITY: SCALE SERVICE-PASIEN = 3 REPLIKA   " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

Write-Host "`n>>> [1/3] Menjalankan penskalaan horizontal (3 container)..." -ForegroundColor Yellow
docker compose up -d --scale service-pasien=3

Write-Host "`n>>> [2/3] Menunggu sinkronisasi DNS Docker (4 detik)..." -ForegroundColor Yellow
Start-Sleep -Seconds 4

Write-Host "`n>>> [3/3] Daftar Replika Kontainer Aktif:" -ForegroundColor Green
docker compose ps service-pasien

Write-Host "`n[INFO] Service Pasien kini memiliki 3 replika aktif di backend." -ForegroundColor Green
Write-Host "Jalankan .\test-loadbalance.ps1 untuk menguji distribusi beban Round-Robin Nginx." -ForegroundColor Cyan

