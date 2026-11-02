# ========================================================
# MASTER DEMO LAUNCHER: PERTEMUAN 1, 2, & 3
# Kelompok 4 - Sistem Informasi Medis Rumah Sakit
# ========================================================

$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $baseDir

function Show-Header {
    Clear-Host
    Write-Host "==============================================================" -ForegroundColor Cyan
    Write-Host "     SISTEM INFORMASI MEDIS RUMAH SAKIT - KELOMPOK 4          " -ForegroundColor Cyan
    Write-Host "        PUSAT KENDALI DEMO PRAKTIKUM CLOUD COMPUTING          " -ForegroundColor White
    Write-Host "==============================================================" -ForegroundColor Cyan
    Write-Host " Dosen Pengampu : Dr. Moch. Yasin, S.Kom., M.Kom., M.B.A." -ForegroundColor Gray
    Write-Host " Kasus Khusus   : Disaster Recovery, DDD, & Auto-Scaling Medis" -ForegroundColor Gray
    Write-Host " Anggota        : Yudis, Agra, Qosi, Diaz, Daffa (Kelompok 4)" -ForegroundColor Gray
    Write-Host "==============================================================" -ForegroundColor Cyan
}

do {
    Show-Header
    Write-Host "`nSilakan pilih demonstrasi praktikum yang ingin dijalankan:" -ForegroundColor Yellow
    Write-Host " [1] Demo Pertemuan 1: Dasar Docker, Named Volume, & Disaster Recovery" -ForegroundColor White
    Write-Host " [2] Demo Pertemuan 2: Transformasi Microservices (DDD) & Inter-Service" -ForegroundColor White
    Write-Host " [3] Demo Pertemuan 3: Orkestrasi Docker Compose, Nginx Load Balancer & Elasticity" -ForegroundColor White
    Write-Host " [A] Jalankan Seluruh Skenario Demo Bertahap (1 -> 2 -> 3)" -ForegroundColor Green
    Write-Host " [S] Status Kontainer & Network Docker Saat Ini" -ForegroundColor Cyan
    Write-Host " [C] Bersihkan (Stop & Clean) Seluruh Kontainer Pengujian" -ForegroundColor Magenta
    Write-Host " [Q] Keluar" -ForegroundColor Gray
    Write-Host "--------------------------------------------------------------" -ForegroundColor Cyan
    
    $choice = (Read-Host "Masukkan pilihan Anda [1, 2, 3, A, S, C, Q]").Trim().ToUpper()

    switch ($choice) {
        "1" {
            & ".\scripts\demo-p1.ps1"
            Read-Host "`nTekan [ENTER] untuk kembali ke menu..."
        }
        "2" {
            & ".\scripts\demo-p2.ps1"
            Read-Host "`nTekan [ENTER] untuk kembali ke menu..."
        }
        "3" {
            & ".\scripts\demo-p3.ps1"
            Read-Host "`nTekan [ENTER] untuk kembali ke menu..."
        }
        "A" {
            Write-Host "`n>>> MENJALANKAN DEMO LENGKAP PERTEMUAN 1, 2, DAN 3 <<<" -ForegroundColor Green
            & ".\scripts\demo-p1.ps1"
            Start-Sleep -Seconds 2
            & ".\scripts\demo-p2.ps1"
            Start-Sleep -Seconds 2
            & ".\scripts\demo-p3.ps1"
            Write-Host "`n>>> SELURUH DEMO PERTEMUAN 1, 2, DAN 3 BERHASIL DILAKSANAKAN! <<<" -ForegroundColor Green
            Read-Host "`nTekan [ENTER] untuk kembali ke menu..."
        }
        "S" {
            Clear-Host
            Write-Host "=== STATUS DOCKER AKTIF ===" -ForegroundColor Cyan
            docker ps -a
            Write-Host "`n=== DAFTAR NETWORK DOCKER ===" -ForegroundColor Cyan
            docker network ls --filter "name=medis"
            Write-Host "`n=== DAFTAR NAMED VOLUME DOCKER ===" -ForegroundColor Cyan
            docker volume ls --filter "name=medis"
            Read-Host "`nTekan [ENTER] untuk kembali ke menu..."
        }
        "C" {
            Clear-Host
            Write-Host "Menghentikan dan membersihkan seluruh kontainer uji..." -ForegroundColor Yellow
            docker compose down 2>$null | Out-Null
            docker rm -f app-monolit app-lab1 service-pasien service-apotek service-jadwal 2>$null | Out-Null
            Write-Host "Pembersihan selesai!" -ForegroundColor Green
            Start-Sleep -Seconds 1
        }
        "Q" {
            Write-Host "`nKeluar dari Master Demo. Terima kasih!`n" -ForegroundColor Green
            break
        }
        default {
            Write-Host "Pilihan tidak valid, silakan coba lagi." -ForegroundColor Red
            Start-Sleep -Seconds 1
        }
    }
} while ($choice -ne "Q")
