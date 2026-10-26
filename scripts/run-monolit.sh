#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MONOLIT_DIR="$SCRIPT_DIR/../monolit"

echo ">>> Membangun Docker Image Monolitik..."
cd "$MONOLIT_DIR"
docker build -t medis-monolit:1.0 .

echo ">>> Menghentikan container monolit lama (jika ada)..."
docker rm -f app-monolit 2>/dev/null || true

echo ">>> Menjalankan container monolitik di port 5000..."
docker run -d --name app-monolit -p 5000:5000 medis-monolit:1.0

sleep 3
echo ">>> Status Container Monolit:"
docker ps --filter "name=app-monolit"

echo -e "\n>>> Pengujian Endpoint Healthcheck Monolitik:"
curl -s http://localhost:5000/health | python3 -m json.tool || curl -s http://localhost:5000/health
