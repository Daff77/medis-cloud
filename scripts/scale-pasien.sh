#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$SCRIPT_DIR/.."
cd "$ROOT_DIR"

echo "=========================================================="
echo "  SIMULASI ELASTICITY: SCALE SERVICE-PASIEN = 3 REPLIKA   "
echo "=========================================================="

echo -e "\n>>> [1/3] Menjalankan penskalaan horizontal (3 container)..."
docker compose up -d --scale service-pasien=3

echo -e "\n>>> [2/3] Menunggu sinkronisasi DNS Docker (4 detik)..."
sleep 4

echo -e "\n>>> [3/3] Daftar Replika Kontainer Aktif:"
docker compose ps service-pasien

echo -e "\n[INFO] Service Pasien kini memiliki 3 replika aktif di backend."
echo "Jalankan ./scripts/test-loadbalance.sh untuk menguji distribusi beban Round-Robin Nginx."

