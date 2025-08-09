# Test simple de l'agent IA
Write-Host "TEST SIMPLE DE L'AGENT IA" -ForegroundColor Green

# Test de santé
Write-Host "Test de santé..." -ForegroundColor Cyan
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/ai-agent/health" -Method GET
    Write-Host "✅ Agent IA opérationnel" -ForegroundColor Green
    Write-Host "Status: $($health.status)" -ForegroundColor White
    Write-Host "IA disponible: $($health.ai_available)" -ForegroundColor White
}
catch {
    Write-Host "❌ Erreur: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nTest terminé" -ForegroundColor Green
