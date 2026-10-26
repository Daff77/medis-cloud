# ========================================================
# Script: stop-all.ps1
# Menghentikan dan membersihkan container & network praktikum
# ========================================================

Write-Host ">>> Menghentikan dan menghapus semua container praktikum..." -ForegroundColor Yellow
docker rm -f app-monolit service-pasien service-apotek service-jadwal 2>$null

Write-Host ">>> Menghapus docker network 'medis-net'..." -ForegroundColor Yellow
docker network rm medis-net 2>$null

Write-Host ">>> Pembersihan selesai." -ForegroundColor Green
docker ps -a --filter "name=service-" --filter "name=app-monolit"
