# Script de test pour l'agent IA
Write-Host "TEST DE L'AGENT IA" -ForegroundColor Green

# Test de santé de l'agent IA
Write-Host "1. Test de santé de l'agent IA..." -ForegroundColor Cyan
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/ai-agent/health" -Method GET
    Write-Host "Status: $($health.status)" -ForegroundColor Green
    Write-Host "IA disponible: $($health.ai_available)" -ForegroundColor Green
    Write-Host "Message: $($health.message)" -ForegroundColor Green
}
catch {
    Write-Host "Erreur lors du test de santé: $($_.Exception.Message)" -ForegroundColor Red
}

# Test des recommandations stratégiques
Write-Host "`n2. Test des recommandations stratégiques..." -ForegroundColor Cyan
try {
    $recommendations = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/ai-agent/strategic-recommendations" -Method POST -Body (@{
        include_risk_analysis = $true
        include_cost_optimization = $true
        include_growth_opportunities = $true
    } | ConvertTo-Json) -ContentType "application/json"
    
    Write-Host "Recommandations obtenues avec succès!" -ForegroundColor Green
    Write-Host "Type d'analyse: $($recommendations.recommendations.analysis_type)" -ForegroundColor Yellow
    Write-Host "Recommandation: $($recommendations.recommendations.ai_analysis.recommendation)" -ForegroundColor Yellow
    Write-Host "Score: $($recommendations.recommendations.ai_analysis.score)/100" -ForegroundColor Yellow
    Write-Host "Confiance: $([math]::Round($recommendations.recommendations.ai_analysis.confidence * 100))%" -ForegroundColor Yellow
    
    Write-Host "`nPortefeuille:" -ForegroundColor Cyan
    Write-Host "- Sites: $($recommendations.portfolio_data.total_sites)" -ForegroundColor White
    Write-Host "- Valeur totale: $($recommendations.portfolio_data.total_value)€" -ForegroundColor White
    Write-Host "- Primes: $($recommendations.portfolio_data.total_premiums)€" -ForegroundColor White
    Write-Host "- Risque moyen: $($recommendations.portfolio_data.average_risk)%" -ForegroundColor White
}
catch {
    Write-Host "Erreur lors des recommandations: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nTest de l'agent IA termine" -ForegroundColor Green
