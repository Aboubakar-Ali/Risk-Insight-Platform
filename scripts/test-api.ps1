Write-Host "🧪 Test de l'API Risk Insight Platform" -ForegroundColor Green

# Test 1: Health check
Write-Host "`n1. Test du health check..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET
    Write-Host "✅ Health check OK: $($response.status)" -ForegroundColor Green
} catch {
    Write-Host "❌ Health check échoué: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Liste des sites
Write-Host "`n2. Test de la liste des sites..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/sites" -Method GET
    Write-Host "✅ Liste des sites OK: $($response.Count) sites trouvés" -ForegroundColor Green
} catch {
    Write-Host "❌ Liste des sites échoué: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Création d'un site
Write-Host "`n3. Test de création d'un site..." -ForegroundColor Yellow
$siteData = @{
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
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/sites" -Method POST -ContentType "application/json" -Body $siteData
    Write-Host "✅ Création de site OK: Site créé avec ID $($response.id)" -ForegroundColor Green
} catch {
    Write-Host "❌ Création de site échoué: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Vérification du site créé
Write-Host "`n4. Vérification du site créé..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/sites" -Method GET
    Write-Host "✅ Sites trouvés: $($response.Count)" -ForegroundColor Green
    if ($response.Count -gt 0) {
        $site = $response[0]
        Write-Host "   - Nom: $($site.name)" -ForegroundColor Cyan
        Write-Host "   - Ville: $($site.city)" -ForegroundColor Cyan
        Write-Host "   - Score de risque: $($site.risk_score)" -ForegroundColor Cyan
    }
} catch {
    Write-Host "❌ Vérification échouée: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🎯 Tests terminés !" -ForegroundColor Green
Write-Host "📱 Accès à la documentation API: http://localhost:8000/docs" -ForegroundColor Cyan 