#!/usr/bin/env bash
echo "=========================================================="
echo "  PENGUJIAN REST API DAN KOMUNIKASI LINTAS CONTAINER (WSL) "
echo "=========================================================="

echo -e "\n[1/5] Health Check Setiap Service:"
for svc in "5001:Pasien" "5002:Apotek" "5003:Jadwal"; do
    port="${svc%%:*}"
    name="${svc##*:}"
    echo -n " - $name (port $port): "
    curl -s -f "http://localhost:$port/health" | python3 -m json.tool 2>/dev/null || curl -s "http://localhost:$port/health" || echo "Gagal"
done

echo -e "\n[2/5] Uji Endpoint Pasien (GET /api/pasien):"
curl -s http://localhost:5001/api/pasien | python3 -m json.tool 2>/dev/null || curl -s http://localhost:5001/api/pasien

echo -e "\n[3/5] Uji Service Apotek menerbitkan resep (Cross-Service Call & Deteksi Alergi):"
curl -s -X POST http://localhost:5002/api/resep \
    -H "Content-Type: application/json" \
    -d '{"pasien_id": 1, "obat_id": 2, "jumlah": 10, "aturan_pakai": "3x1 sehari sesudah makan"}' \
    | python3 -m json.tool 2>/dev/null || true

echo -e "\n[4/5] Uji Service Jadwal membuat antrean janji temu (Komunikasi ke Service Pasien):"
curl -s -X POST http://localhost:5003/api/janji-temu \
    -H "Content-Type: application/json" \
    -d '{"pasien_id": 2, "dokter_id": 1, "tgl_periksa": "2026-11-05", "keluhan": "Demam dan flu sejak 2 hari"}' \
    | python3 -m json.tool 2>/dev/null || true

echo -e "\n[5/5] Uji Isolasi Jaringan (Security Boundary):"
echo "Mencoba ping service-pasien dari container di luar network medis-net..."
docker run --rm alpine ping -c 2 service-pasien 2>&1 || true

echo -e "\n=========================================================="
echo "  PENGUJIAN SELESAI                                       "
echo "=========================================================="
