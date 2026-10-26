# ========================================================
# Script: run-monolit.ps1
# Build & Run Aplikasi Awal (Monolitik)
# ========================================================

$RootPath = Resolve-Path (Join-Path $PSScriptRoot "..")
$MonolitDir = Join-Path $RootPath "monolit"

Write-Host ">>> Membangun Docker Image Monolitik..." -ForegroundColor Cyan
Set-Location $MonolitDir
docker build -t medis-monolit:1.0 .

Write-Host ">>> Menghentikan container monolit lama (jika ada)..." -ForegroundColor Yellow
docker rm -f app-monolit 2>$null

Write-Host ">>> Menjalankan container monolitik di port 5000..." -ForegroundColor Green
docker run -d --name app-monolit -p 5000:5000 medis-monolit:1.0

Start-Sleep -Seconds 3

Write-Host ">>> Status Container Monolit:" -ForegroundColor Cyan
docker ps --filter "name=app-monolit"

Write-Host "`n>>> Pengujian Endpoint Healthcheck Monolitik:" -ForegroundColor Cyan
try {
    $res = Invoke-RestMethod -Uri "http://localhost:5000/health" -Method Get
    $res | ConvertTo-Json
} catch {
    Write-Warning "Gagal menghubungi container monolitik: $_"
}
