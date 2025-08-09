# Script pour supprimer tous les sites existants
Write-Host "SUPPRESSION DE TOUS LES SITES" -ForegroundColor Red

# Récupérer tous les sites
$sites = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/sites" -Method GET

Write-Host "Sites trouves: $($sites.Count)" -ForegroundColor Yellow

# Supprimer chaque site
foreach ($site in $sites) {
    $siteId = $site.id
    $siteName = $site.name
    
    Write-Host "Suppression de: $siteName (ID: $siteId)" -ForegroundColor Cyan
    
    try {
        Invoke-RestMethod -Uri "http://localhost:8000/api/v1/sites/$siteId" -Method DELETE
        Write-Host "Supprime avec succes" -ForegroundColor Green
    }
    catch {
        Write-Host "Erreur lors de la suppression: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "Tous les sites ont ete supprimes" -ForegroundColor Green
