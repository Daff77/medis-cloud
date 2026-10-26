#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICES_DIR="$SCRIPT_DIR/../services"

# 1. Setup Network
bash "$SCRIPT_DIR/setup-network.sh"

echo -e "\n>>> Membersihkan container lama..."
docker rm -f service-pasien service-apotek service-jadwal 2>/dev/null || true

echo -e "\n>>> 1. Membangun Image Service Pasien..."
cd "$SERVICES_DIR/pasien"
docker build -t medis-pasien:1.0 .

echo -e "\n>>> 2. Membangun Image Service Apotek..."
cd "$SERVICES_DIR/apotek"
docker build -t medis-apotek:1.0 .

echo -e "\n>>> 3. Membangun Image Service Jadwal Dokter..."
cd "$SERVICES_DIR/jadwal-dokter"
docker build -t medis-jadwal:1.0 .

echo -e "\n>>> Menjalankan Service Pasien di port 5001..."
docker run -d --name service-pasien \
    --network medis-net \
    -p 5001:5001 \
    medis-pasien:1.0

echo ">>> Menjalankan Service Apotek di port 5002..."
docker run -d --name service-apotek \
    --network medis-net \
    -p 5002:5002 \
    -e PASIEN_SERVICE_URL="http://service-pasien:5001" \
    medis-apotek:1.0

echo ">>> Menjalankan Service Jadwal Dokter di port 5003..."
docker run -d --name service-jadwal \
    --network medis-net \
    -p 5003:5003 \
    -e PASIEN_SERVICE_URL="http://service-pasien:5001" \
    medis-jadwal:1.0

sleep 4
echo -e "\n>>> Status Semua Container Microservices:"
docker ps --filter "name=service-"
