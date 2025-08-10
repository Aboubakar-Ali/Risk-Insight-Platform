Write-Host " Ajout de données de test à Risk Insight Platform" -ForegroundColor Green

# Données de test
$testSites = @(
    @{
        name = "Siège Social Paris"
        address = "123 Avenue des Champs-Élysées"
        city = "Paris"
        postal_code = "75008"
        country = "France"
        latitude = 48.8566
        longitude = 2.3522
        building_type = "office"
        building_value = 5000000
        surface_area = 2000
        construction_year = 2010
    },
    @{
        name = "Entrepôt Lyon"
        address = "456 Rue de la Soie"
        city = "Lyon"
        postal_code = "69001"
        country = "France"
        latitude = 45.7578
        longitude = 4.8320
        building_type = "warehouse"
        building_value = 2000000
        surface_area = 5000
        construction_year = 2015
    },
    @{
        name = "Usine Marseille"
        address = "789 Boulevard de la Mer"
        city = "Marseille"
        postal_code = "13001"
        country = "France"
        latitude = 43.2965
        longitude = 5.3698
        building_type = "factory"
        building_value = 8000000
        surface_area = 10000
        construction_year = 2008
    },
    @{
        name = "Centre Commercial Nice"
        address = "321 Promenade des Anglais"
        city = "Nice"
        postal_code = "06000"
        country = "France"
        latitude = 43.7102
        longitude = 7.2620
        building_type = "retail"
        building_value = 3500000
        surface_area = 8000
        construction_year = 2012
    }
)

Write-Host "`n Création de $($testSites.Count) sites de test..." -ForegroundColor Yellow

$createdSites = @()

foreach ($site in $testSites) {
    try {
        $jsonData = $site | ConvertTo-Json
        $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/sites" -Method POST -ContentType "application/json" -Body $jsonData
        $createdSites += $response
        Write-Host " Site créé: $($site.name) (ID: $($response.id))" -ForegroundColor Green
    } catch {
        Write-Host " Erreur lors de la création de $($site.name): $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n Résumé des sites créés:" -ForegroundColor Cyan
foreach ($site in $createdSites) {
    Write-Host "   - $($site.name) ($($site.city)) - Score de risque: $($site.risk_score)" -ForegroundColor White
}

Write-Host "`n Données de test ajoutées avec succès !" -ForegroundColor Green
Write-Host " Accès à l'application: http://localhost:3000" -ForegroundColor Cyan
Write-Host " Documentation API: http://localhost:8000/docs" -ForegroundColor Cyan 