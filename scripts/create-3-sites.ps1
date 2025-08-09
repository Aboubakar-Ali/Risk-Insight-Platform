# Script pour créer 3 sites de test dans des régions différentes
Write-Host "CREATION DE 3 SITES DE TEST" -ForegroundColor Green

# Site 1: Nord de la France (Lille)
$site1 = @{
    name = "Usine Lille"
    address = "123 Rue de la Barre"
    city = "Lille"
    postal_code = "59000"
    country = "France"
    latitude = 50.6292
    longitude = 3.0573
    building_type = "factory"
    building_value = 5000000.0
    surface_area = 8000.0
    construction_year = 2010
    notes = "Site de test - Nord de la France"
}

# Site 2: Centre de la France (Lyon)
$site2 = @{
    name = "Bureau Lyon"
    address = "456 Rue de la Part-Dieu"
    city = "Lyon"
    postal_code = "69003"
    country = "France"
    latitude = 45.7578
    longitude = 4.832
    building_type = "office"
    building_value = 3000000.0
    surface_area = 2500.0
    construction_year = 2015
    notes = "Site de test - Centre de la France"
}

# Site 3: Sud de la France (Marseille)
$site3 = @{
    name = "Entrepot Marseille"
    address = "789 Boulevard Michelet"
    city = "Marseille"
    postal_code = "13008"
    country = "France"
    latitude = 43.2965
    longitude = 5.3698
    building_type = "warehouse"
    building_value = 4000000.0
    surface_area = 10000.0
    construction_year = 2012
    notes = "Site de test - Sud de la France"
}

$sites = @($site1, $site2, $site3)

foreach ($site in $sites) {
    Write-Host "Creation de: $($site.name)" -ForegroundColor Cyan
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/sites" -Method POST -Body ($site | ConvertTo-Json) -ContentType "application/json"
        Write-Host "Site cree avec succes: $($response.name)" -ForegroundColor Green
    }
    catch {
        Write-Host "Erreur lors de la creation: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "3 sites de test ont ete crees" -ForegroundColor Green
