#!/usr/bin/env bash

echo "=========================================================="
echo "  PENGUJIAN LOAD BALANCING NGINX & ELASTICITY (WSL)       "
echo "=========================================================="

echo -e "\n[A] Verifikasi Routing Endpoint Melalui Nginx (Port 8080):"
for ep in "pasien" "obat" "dokter"; do
    echo -n " - /api/$ep -> "
    curl -s -i "http://localhost:8080/api/$ep" | grep -iE "(HTTP/|x-served-by:)" || echo "Gagal"
done

echo -e "\n[B] Pengujian Distribusi Trafik Round-Robin (8 Request Berurutan ke /api/pasien):"
printf "%-12s | %-12s | %-25s | %-20s\n" "Request #" "Status" "Backend Host (X-Served-By)" "Upstream Address"
echo "----------------------------------------------------------------------------------"

declare -A host_count

for i in {1..8}; do
    resp=$(curl -s -i "http://localhost:8080/api/pasien")
    status=$(echo "$resp" | grep -i "HTTP/" | head -n1 | awk '{print $2}')
    backend=$(echo "$resp" | grep -i "^x-served-by:" | head -n1 | awk '{print $2}' | tr -d '\r')
    upstream=$(echo "$resp" | grep -i "^x-upstream-addr:" | head -n1 | awk '{print $2}' | tr -d '\r')
    
    [ -z "$backend" ] && backend="Unknown"
    [ -z "$upstream" ] && upstream="N/A"
    
    host_count["$backend"]=$(( ${host_count["$backend"]:-0} + 1 ))
    printf "%-12s | %-12s | %-25s | %-20s\n" "Request #$i" "$status" "$backend" "$upstream"
    sleep 0.25
done

echo -e "\n>>> Analisis Hasil Load Balancing:"
unique_count=${#host_count[@]}
echo " Jumlah Replika Terdeteksi: $unique_count"
for h in "${!host_count[@]}"; do
    echo " - Host '$h' melayani: ${host_count[$h]} request"
done

if [ "$unique_count" -gt 1 ]; then
    echo -e "\n\033[0;32m[BERHASIL] Trafik berhasil didistribusikan secara elastis ke $unique_count replika container!\033[0m"
else
    echo -e "\n\033[0;33m[CATATAN] Trafik hanya dilayani 1 kontainer. Pastikan Anda telah menjalankan ./scripts/scale-pasien.sh terlebih dahulu.\033[0m"
fi

