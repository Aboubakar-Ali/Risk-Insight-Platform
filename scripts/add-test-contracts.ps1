Write-Host "📋 Ajout de contrats d'assurance pour les sites existants" -ForegroundColor Green

# Récupérer d'abord la liste des sites
Write-Host "`n🏢 Récupération des sites existants..." -ForegroundColor Yellow
try {
    $sitesResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/sites" -Method GET
    Write-Host "✅ Sites trouvés: $($sitesResponse.Count)" -ForegroundColor Green
} catch {
    Write-Host "❌ Erreur lors de la récupération des sites: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Créer des contrats pour chaque site
$createdContracts = @()

foreach ($site in $sitesResponse) {
    $contractData = @{
        contract_number = "CONTRACT-$(Get-Random -Minimum 1000 -Maximum 9999)"
        site_id = $site.id
        premium_amount = [math]::Round($site.building_value * 0.02, 2)
        coverage_amount = $site.building_value
        deductible = [math]::Round($site.building_value * 0.01, 2)
        start_date = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss")
        end_date = (Get-Date).AddYears(1).ToString("yyyy-MM-ddTHH:mm:ss")
    }

    try {
        $jsonData = $contractData | ConvertTo-Json
        $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/contracts" -Method POST -ContentType "application/json" -Body $jsonData
        $createdContracts += $response
        Write-Host "✅ Contrat créé pour $($site.name): $($contractData.contract_number)" -ForegroundColor Green
    } catch {
        Write-Host "❌ Erreur lors de la création du contrat pour $($site.name): $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n📋 Résumé des contrats créés:" -ForegroundColor Cyan
foreach ($contract in $createdContracts) {
    Write-Host "   - $($contract.contract_number) - Prime: $($contract.premium_amount)€" -ForegroundColor White
}

Write-Host "`n🎯 Contrats d'assurance ajoutés avec succès !" -ForegroundColor Green
Write-Host "📱 Accès à l'application: http://localhost:3000" -ForegroundColor Cyan 