# ========================================================
# Script: setup-network.ps1
# Praktikum Cloud Pertemuan 2 - Kelompok 4
# Kasus: Sistem Informasi Medis Rumah Sakit
# ========================================================

Write-Host ">>> Memeriksa Docker Network 'medis-net'..." -ForegroundColor Cyan

$networkExist = docker network ls --filter "name=^medis-net$" --format "{{.Name}}"

if ($networkExist -eq "medis-net") {
    Write-Host "Docker network 'medis-net' sudah ada." -ForegroundColor Yellow
} else {
    Write-Host "Membuat custom bridge network 'medis-net'..." -ForegroundColor Green
    docker network create --driver bridge medis-net
}

Write-Host ">>> Detail Jaringan 'medis-net':" -ForegroundColor Cyan
docker network inspect medis-net --format "Subnet: {{range .IPAM.Config}}{{.Subnet}}{{end}}"
