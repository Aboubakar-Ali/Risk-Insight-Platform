Write-Host "🌤️ Test de l'API météo OpenWeatherMap" -ForegroundColor Cyan

# Test 1: Vérifier la météo pour un site existant
Write-Host "`n📡 Test 1: Récupération météo pour un site existant" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/weather/site/1" -Method GET
    Write-Host "✅ Météo récupérée avec succès pour le site 1" -ForegroundColor Green
    Write-Host "   Site: $($response.site_name)" -ForegroundColor White
    Write-Host "   Localisation: $($response.location)" -ForegroundColor White
    Write-Host "   Score de risque météo: $($response.weather_risk.risk_score)%" -ForegroundColor White
    Write-Host "   Conditions: $($response.weather_risk.risk_factors.conditions)" -ForegroundColor White
} catch {
    Write-Host "❌ Erreur lors de la récupération météo: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Mettre à jour tous les scores de risque
Write-Host "`n🔄 Test 2: Mise à jour des scores de risque pour tous les sites" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/weather/update-risk-scores" -Method POST
    Write-Host "✅ Scores de risque mis à jour avec succès" -ForegroundColor Green
    Write-Host "   Sites mis à jour: $($response.updated_sites.Count)" -ForegroundColor White
    Write-Host "   Message: $($response.message)" -ForegroundColor White
    
    foreach ($site in $response.updated_sites) {
        Write-Host "   - $($site.name): $($site.new_risk_score)% ($($site.weather_conditions))" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ Erreur lors de la mise à jour des scores: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Vérifier les sites après mise à jour
Write-Host "`n📊 Test 3: Vérification des sites après mise à jour" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/sites" -Method GET
    Write-Host "✅ Sites récupérés avec succès" -ForegroundColor Green
    Write-Host "   Nombre de sites: $($response.Count)" -ForegroundColor White
    
    $totalRisk = 0
    foreach ($site in $response) {
        $totalRisk += $site.risk_score
        Write-Host "   - $($site.name): $([math]::Round($site.risk_score, 1))%" -ForegroundColor Gray
    }
    
    $averageRisk = $totalRisk / $response.Count
    Write-Host "   Risque moyen: $([math]::Round($averageRisk, 1))%" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Erreur lors de la récupération des sites: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🎯 Test de l'API météo terminé !" -ForegroundColor Green
Write-Host "📱 Accès à l'application: http://localhost:3000" -ForegroundColor Cyan 