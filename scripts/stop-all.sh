#!/usr/bin/env bash
echo ">>> Menghentikan dan menghapus semua container praktikum..."
docker rm -f app-monolit service-pasien service-apotek service-jadwal 2>/dev/null || true

echo ">>> Menghapus docker network 'medis-net'..."
docker network rm medis-net 2>/dev/null || true

echo ">>> Pembersihan selesai."
docker ps -a --filter "name=service-" --filter "name=app-monolit"
