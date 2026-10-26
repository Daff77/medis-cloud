# ========================================================
# Script: test-services.ps1
# Uji Integrasi & Komunikasi Antar-Microservice
# ========================================================

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  PENGUJIAN REST API DAN KOMUNIKASI LINTAS CONTAINER       " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Healthcheck 3 Services
Write-Host "`n[1/5] Health Check Setiap Service:" -ForegroundColor Yellow
$services = @(
    @{ Name = "Pasien "; Url = "http://localhost:5001/health" },
    @{ Name = "Apotek "; Url = "http://localhost:5002/health" },
    @{ Name = "Jadwal "; Url = "http://localhost:5003/health" }
)

foreach ($s in $services) {
    try {
        $resp = Invoke-RestMethod -Uri $s.Url -Method Get -TimeoutSec 3
        Write-Host " [OK] $($s.Name) -> $($resp.service) | Status: $($resp.status) | Host: $($resp.hostname)" -ForegroundColor Green
    } catch {
        Write-Host " [FAIL] $($s.Name) -> $($_.Exception.Message)" -ForegroundColor Red
    }
}

# 2. Test Get Pasien
Write-Host "`n[2/5] Uji Endpoint Pasien (GET /api/pasien):" -ForegroundColor Yellow
try {
    $pasienList = Invoke-RestMethod -Uri "http://localhost:5001/api/pasien" -Method Get
    Write-Host " Berhasil mendapatkan $($pasienList.Count) data pasien." -ForegroundColor Green
    $pasienList | Format-Table id, nama, nik, riwayat_alergi
} catch {
    Write-Host " Gagal: $_" -ForegroundColor Red
}

# 3. Test Apotek mengeluarkan resep (Cross-service call ke Pasien)
Write-Host "`n[3/5] Uji Service Apotek menerbitkan resep (Komunikasi ke Service Pasien):" -ForegroundColor Yellow
$resepBody = @{
    pasien_id = 1
    obat_id = 2  # Amoxicillin (Pasien 1 alergi Penisilin!)
    jumlah = 10
    aturan_pakai = "3x1 sehari sesudah makan"
} | ConvertTo-Json

try {
    $resepResp = Invoke-RestMethod -Uri "http://localhost:5002/api/resep" -Method Post -Body $resepBody -ContentType "application/json"
    Write-Host " Resep Berhasil Dibuat!" -ForegroundColor Green
    $resepResp | ConvertTo-Json -Depth 4
} catch {
    Write-Host " Gagal: $_" -ForegroundColor Red
}

# 4. Test Jadwal Dokter mendaftarkan janji temu (Cross-service call ke Pasien)
Write-Host "`n[4/5] Uji Service Jadwal membuat antrean janji temu (Komunikasi ke Service Pasien):" -ForegroundColor Yellow
$janjiBody = @{
    pasien_id = 2
    dokter_id = 1
    tgl_periksa = "2026-11-05"
    keluhan = "Demam dan flu sejak 2 hari"
} | ConvertTo-Json

try {
    $janjiResp = Invoke-RestMethod -Uri "http://localhost:5003/api/janji-temu" -Method Post -Body $janjiBody -ContentType "application/json"
    Write-Host " Janji Temu Berhasil Didaftarkan!" -ForegroundColor Green
    $janjiResp | ConvertTo-Json -Depth 4
} catch {
    Write-Host " Gagal: $_" -ForegroundColor Red
}

# 5. Uji Validasi Error (Pasien ID tidak ditemukan)
Write-Host "`n[5/5] Uji Error Handling Komunikasi Antar-Servis (Pasien ID 999):" -ForegroundColor Yellow
$invalidResep = @{
    pasien_id = 999
    obat_id = 1
    jumlah = 5
    aturan_pakai = "1x1"
} | ConvertTo-Json

try {
    $errResp = Invoke-RestMethod -Uri "http://localhost:5002/api/resep" -Method Post -Body $invalidResep -ContentType "application/json"
    Write-Host " Unexpected Success: $($errResp | ConvertTo-Json)" -ForegroundColor Red
} catch {
    Write-Host " [Diharapkan] Layanan Apotek mendeteksi pasien tidak valid dari Service Pasien:" -ForegroundColor Green
    Write-Host " Detail Response: $($_.ErrorDetails.Message)" -ForegroundColor Gray
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host "  PENGUJIAN SELESAI                                       " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
