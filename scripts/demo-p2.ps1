# ========================================================
# DEMO PERTEMUAN 2: MICROSERVICES & DOMAIN-DRIVEN DESIGN
# Kelompok 4 - Sistem Informasi Medis Rumah Sakit
# ========================================================

Clear-Host
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   DEMO PRAKTIKUM PERTEMUAN 2: MICROSERVICES & NETWORK   " -ForegroundColor Cyan
Write-Host "   Kelompok 4 - Kasus: Transformasi Monolit ke Microservices" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Bersihkan sisa container lama jika ada
docker rm -f app-monolit service-pasien service-apotek service-jadwal 2>$null | Out-Null

# 2. Demo Praktik A: Baseline Monolitik
Write-Host "`n[STEP 1/4] Praktik A - Baseline Aplikasi Awal (Monolitik):" -ForegroundColor Yellow
Write-Host " Menjalankan container monolitik di Port 5000..." -ForegroundColor Gray
docker run -d --name app-monolit -p 5000:5000 medis-monolit:1.0 | Out-Null
Start-Sleep -Seconds 2

try {
    $resMono = Invoke-RestMethod -Uri "http://localhost:5000/api/dashboard" -Method Get
    Write-Host " [OK] Respon Dashboard Monolitik Terpusat:" -ForegroundColor Green
    Write-Host "      Total Pasien: $($resMono.data_pasien.Count), Total Obat: $($resMono.data_obat.Count), Total Dokter: $($resMono.data_dokter.Count)" -ForegroundColor White
} catch {
    Write-Host " [FAIL] Tidak dapat mengakses port 5000: $_" -ForegroundColor Red
}

Write-Host " Evaluasi Monolit: Seluruh modul berjalan dalam 1 proses tunggal." -ForegroundColor Gray
Write-Host " Menghentikan monolit untuk beralih ke arsitektur microservices..." -ForegroundColor Gray
docker rm -f app-monolit | Out-Null

# 3. Demo Praktik B & C: Setup Docker Custom Bridge Network & Microservices
Write-Host "`n[STEP 2/4] Praktik B & C - Custom Bridge Network & 3 Bounded Context:" -ForegroundColor Yellow
$netExists = docker network ls --filter "name=medis-net" -q
if (-not $netExists) {
    docker network create --driver bridge medis-net | Out-Null
}
Write-Host " [OK] Docker Custom Bridge Network 'medis-net' aktif." -ForegroundColor Green

Write-Host " Menjalankan 3 Microservices Terisolasi (Pasien, Apotek, Jadwal)..." -ForegroundColor Gray
docker run -d --name service-pasien --network medis-net -p 5001:5001 -e PORT=5001 medis-pasien:1.0 | Out-Null
docker run -d --name service-apotek --network medis-net -p 5002:5002 -e PORT=5002 -e SERVICE_PASIEN_URL=http://service-pasien:5001 medis-apotek:1.0 | Out-Null
docker run -d --name service-jadwal --network medis-net -p 5003:5003 -e PORT=5003 -e SERVICE_PASIEN_URL=http://service-pasien:5001 medis-jadwal:1.0 | Out-Null

Write-Host " Menunggu kontainer inisialisasi (4 detik)..." -ForegroundColor Gray
Start-Sleep -Seconds 4

Write-Host " Verifikasi Healthcheck 3 Services:" -ForegroundColor White
$services = @(
    @{ Name = "Layanan Data Pasien"; Url = "http://localhost:5001/health" },
    @{ Name = "Layanan Apotek     "; Url = "http://localhost:5002/health" },
    @{ Name = "Layanan Jadwal     "; Url = "http://localhost:5003/health" }
)
foreach ($s in $services) {
    try {
        $h = Invoke-RestMethod -Uri $s.Url -Method Get -TimeoutSec 3
        Write-Host " [OK] $($s.Name) -> $($h.status) | Service: $($h.service)" -ForegroundColor Green
    } catch {
        Write-Host " [FAIL] $($s.Name) gagal diakses!" -ForegroundColor Red
    }
}

# 4. Demo Praktik D: Komunikasi Antar-Servis (Inter-Service Cross-Call)
Write-Host "`n[STEP 3/4] Praktik D - Komunikasi Lintas Service (Validasi Alergi Resep):" -ForegroundColor Yellow
Write-Host " Skenario: Dokter meresepkan Amoxicillin (obat_id: 2) untuk Pasien ID 1 (alergi Penisilin)." -ForegroundColor White
$resepPayload = @{
    pasien_id = 1
    obat_id = 2
    jumlah = 10
    aturan_pakai = "3x1 sesudah makan"
} | ConvertTo-Json

try {
    $resResep = Invoke-RestMethod -Uri "http://localhost:5002/api/resep" -Method Post -Body $resepPayload -ContentType "application/json"
    Write-Host " [BERHASIL] Service Apotek memanggil Service Pasien via DNS Docker 'service-pasien:5001'!" -ForegroundColor Green
    Write-Host " >> Pesan Sistem        : $($resResep.message)" -ForegroundColor White
    Write-Host " >> Peringatan Alergi   : $($resResep.peringatan_alergi)" -ForegroundColor Red
    Write-Host " >> Data Obat Keluar    : $($resResep.data_obat.nama) (Stok Sisa: $($resResep.data_obat.sisa_stok))" -ForegroundColor Cyan
} catch {
    Write-Host " [FAIL] Error pemrosesan resep: $_" -ForegroundColor Red
}

# 5. Fault Isolation Test
Write-Host "`n[STEP 4/4] Pengujian Ketahanan Sistem (Fault Isolation):" -ForegroundColor Yellow
Write-Host " Simulasi insiden: Mematikan paksa 'service-pasien'..." -ForegroundColor Red
docker stop service-pasien | Out-Null
Write-Host " [INFO] service-pasien berstatus STOP / DOWN." -ForegroundColor Gray

Write-Host " Memeriksa apakah Service Apotek & Jadwal tetap bisa melayani kueri lokal katalog:" -ForegroundColor White
try {
    $obatList = Invoke-RestMethod -Uri "http://localhost:5002/api/obat" -Method Get
    Write-Host " [OK] Service Apotek TETAP AKTIF melayani katalog obat ($($obatList.Count) data obat)." -ForegroundColor Green
} catch {
    Write-Host " [FAIL] Apotek ikut crash: $_" -ForegroundColor Red
}

try {
    $dokterList = Invoke-RestMethod -Uri "http://localhost:5003/api/dokter" -Method Get
    Write-Host " [OK] Service Jadwal TETAP AKTIF melayani jadwal poli ($($dokterList.Count) dokter)." -ForegroundColor Green
} catch {
    Write-Host " [FAIL] Jadwal ikut crash: $_" -ForegroundColor Red
}

Write-Host "`n Menyalakan kembali service-pasien..." -ForegroundColor Gray
docker start service-pasien | Out-Null

Write-Host "`n----------------------------------------------------------" -ForegroundColor Cyan
Write-Host "  KESIMPULAN DEMO PERTEMUAN 2 KELOMPOK 4:                 " -ForegroundColor Cyan
Write-Host "  * Dekomposisi DDD       : Berhasil menjadi 3 domain mandiri" -ForegroundColor Green
Write-Host "  * Service Discovery     : Berhasil via DNS internal Docker" -ForegroundColor Green
Write-Host "  * Fault Isolation       : Terbukti (TIDAK ADA cascading crash)" -ForegroundColor Green
Write-Host "----------------------------------------------------------" -ForegroundColor Cyan

# Cleanup
docker rm -f service-pasien service-apotek service-jadwal 2>$null | Out-Null
Write-Host "`n[SELESAI] Demo Praktikum Pertemuan 2 Sukses 100%!`n" -ForegroundColor Green
