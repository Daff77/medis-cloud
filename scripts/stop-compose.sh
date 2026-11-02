#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$SCRIPT_DIR/.."
cd "$ROOT_DIR"

echo ">>> Menghentikan seluruh container Docker Compose..."
docker compose down

echo -e "\n>>> Status container saat ini:"
docker compose ps

echo -e "\n[INFO] Layanan berhasil dihentikan. Data pada Docker Volume tetap tersimpan aman."

