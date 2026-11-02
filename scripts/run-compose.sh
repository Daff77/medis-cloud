#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$SCRIPT_DIR/.."
cd "$ROOT_DIR"

echo "=========================================================="
echo "  MENJALANKAN ORKESTRASI DOCKER COMPOSE MEDIS-CLOUD (WSL) "
echo "=========================================================="

echo -e "\n>>> [1/4] Membersihkan kontainer lama..."
docker rm -f app-monolit service-pasien service-apotek service-jadwal nginx-gateway 2>/dev/null || true
docker compose down --remove-orphans 2>/dev/null || true

echo -e "\n>>> [2/4] Membangun images via Docker Compose..."
docker compose build

echo -e "\n>>> [3/4] Menjalankan layanan di background..."
docker compose up -d

echo -e "\nMenunggu inisialisasi healthcheck (6 detik)..."
sleep 6

echo -e "\n>>> [4/4] Status Layanan Docker Compose:"
docker compose ps

echo -e "\n>>> Pengujian Akses Nginx API Gateway (Port 8080):"
curl -s http://localhost:8080/ | python3 -m json.tool || curl -s http://localhost:8080/
echo -e "\n[SUKSES] Nginx API Gateway aktif di http://localhost:8080"

