# Script pour supprimer les anciens sites 1 et 2
Write-Host "SUPPRESSION DES ANCIENS SITES" -ForegroundColor Red

# Supprimer le site 1
Write-Host "Suppression du site ID 1..." -ForegroundColor Cyan
try {
    Invoke-RestMethod -Uri "http://localhost:8000/api/v1/sites/1" -Method DELETE
    Write-Host "Site 1 supprime avec succes" -ForegroundColor Green
}
catch {
    Write-Host "Erreur lors de la suppression du site 1: $($_.Exception.Message)" -ForegroundColor Red
}

# Supprimer le site 2
Write-Host "Suppression du site ID 2..." -ForegroundColor Cyan
try {
    Invoke-RestMethod -Uri "http://localhost:8000/api/v1/sites/2" -Method DELETE
    Write-Host "Site 2 supprime avec succes" -ForegroundColor Green
}
catch {
    Write-Host "Erreur lors de la suppression du site 2: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "Suppression terminee" -ForegroundColor Green
