# ========================================================
# Script: test-loadbalance.ps1
# Praktikum Cloud Pertemuan 3 - Kelompok 4
# Pengujian Load Balancing Round-Robin & Integrasi Gateway
# ========================================================

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  PENGUJIAN LOAD BALANCING NGINX & ELASTICITY             " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Uji Routing Gateway ke 3 Layanan
Write-Host "`n[A] Verifikasi Routing Endpoint Melalui Nginx (Port 8080):" -ForegroundColor Yellow
$endpoints = @(
    @{ Name = "Layanan Pasien"; Url = "http://localhost:8080/api/pasien" },
    @{ Name = "Layanan Obat  "; Url = "http://localhost:8080/api/obat" },
    @{ Name = "Layanan Dokter"; Url = "http://localhost:8080/api/dokter" }
)

foreach ($ep in $endpoints) {
    try {
        $resp = Invoke-WebRequest -Uri $ep.Url -UseBasicParsing -TimeoutSec 4
        $servedBy = $resp.Headers["X-Served-By"]
        Write-Host " [OK] $($ep.Name) -> HTTP $($resp.StatusCode) (Dilayani oleh Host: $servedBy)" -ForegroundColor Green
    } catch {
        Write-Host " [FAIL] $($ep.Name) -> $_" -ForegroundColor Red
    }
}

# 2. Uji Distribusi Beban (Round-Robin) ke Service Pasien
Write-Host "`n[B] Pengujian Distribusi Trafik Round-Robin (8 Request Berurutan ke /api/pasien):" -ForegroundColor Yellow
$results = @()

for ($i = 1; $i -le 8; $i++) {
    try {
        $req = Invoke-WebRequest -Uri "http://localhost:8080/api/pasien" -UseBasicParsing -TimeoutSec 3
        $backendHost = $req.Headers["X-Served-By"]
        $upstreamAddr = $req.Headers["X-Upstream-Addr"]
        
        $results += [PSCustomObject]@{
            "Request #"    = $i
            "Target Path"  = "/api/pasien"
            "Status"       = $req.StatusCode
            "Backend Host" = $backendHost
            "Upstream IP"  = $upstreamAddr
        }
        Start-Sleep -Milliseconds 250
    } catch {
        Write-Warning "Request #$i gagal: $_"
    }
}

$results | Format-Table -AutoSize

# Analisis statistik host unik
$uniqueHosts = ($results | Select-Object -ExpandProperty "Backend Host" -Unique)
Write-Host "`n>>> Analisis Hasil Load Balancing:" -ForegroundColor Cyan
Write-Host " Jumlah Request      : $($results.Count)"
Write-Host " Jumlah Replika Unik : $($uniqueHosts.Count)"
Write-Host " ID Kontainer Replika: $($uniqueHosts -join ', ')"

if ($uniqueHosts.Count -gt 1) {
    Write-Host "[BERHASIL] Trafik berhasil didistribusikan secara elastis ke $($uniqueHosts.Count) replika container!" -ForegroundColor Green
} else {
    Write-Host "[CATATAN] Trafik hanya dilayani 1 kontainer. Pastikan Anda telah menjalankan .\scale-pasien.ps1 terlebih dahulu." -ForegroundColor Yellow
}

