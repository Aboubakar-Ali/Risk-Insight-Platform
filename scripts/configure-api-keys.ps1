Write-Host "🔑 Configuration des clés API" -ForegroundColor Cyan

# Vérifier si le fichier .env existe
if (Test-Path ".env") {
    Write-Host " Fichier .env trouvé" -ForegroundColor Green
} else {
    Write-Host " Création du fichier .env..." -ForegroundColor Yellow
    
    # Créer le fichier .env avec la configuration de base
    $envContent = @"
# Configuration de la base de données
DATABASE_URL=postgresql://risk_user:risk_password@localhost:5432/risk_insight

# APIs externes
OPENAI_API_KEY=your_openai_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here

# Configuration du backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DEBUG=true

# Configuration du frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Risk Insight Platform

# Configuration ML
ML_MODEL_PATH=./ml-engine/models
ML_CACHE_DIR=./ml-engine/cache

# Sécurité
SECRET_KEY=your_secret_key_here
JWT_SECRET=your_jwt_secret_here

# Logs
LOG_LEVEL=INFO
"@
    
    $envContent | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host " Fichier .env créé" -ForegroundColor Green
}

# Demander la clé OpenWeatherMap
Write-Host "`n Configuration OpenWeatherMap API" -ForegroundColor Yellow
Write-Host "1. Allez sur https://openweathermap.org/api" -ForegroundColor White
Write-Host "2. Créez un compte gratuit" -ForegroundColor White
Write-Host "3. Récupérez votre clé API" -ForegroundColor White
Write-Host "4. Collez-la ci-dessous" -ForegroundColor White

$openweatherKey = Read-Host "`nEntrez votre clé API OpenWeatherMap"

if ($openweatherKey -and $openweatherKey -ne "your_openweather_api_key_here") {
    # Mettre à jour le fichier .env
    $envContent = Get-Content ".env" -Raw
    $envContent = $envContent -replace "OPENWEATHER_API_KEY=.*", "OPENWEATHER_API_KEY=$openweatherKey"
    $envContent | Out-File -FilePath ".env" -Encoding UTF8
    
    Write-Host " Clé OpenWeatherMap configurée !" -ForegroundColor Green
    
    # Redémarrer le backend pour appliquer les changements
    Write-Host "`n Redémarrage du backend..." -ForegroundColor Yellow
    docker-compose restart backend
    
    Write-Host "`n Test de la configuration..." -ForegroundColor Yellow
    Start-Sleep -Seconds 3
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/weather/site/1" -Method GET
        Write-Host " API météo fonctionne !" -ForegroundColor Green
        Write-Host "   Score de risque météo: $($response.weather_risk.risk_score)%" -ForegroundColor White
        Write-Host "   Conditions: $($response.weather_risk.risk_factors.conditions)" -ForegroundColor White
    } catch {
        Write-Host " Erreur lors du test: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "   Vérifiez que votre clé API est correcte" -ForegroundColor Yellow
    }
} else {
    Write-Host " Clé API non fournie ou invalide" -ForegroundColor Red
    Write-Host "   Les données météo utiliseront des valeurs par défaut" -ForegroundColor Yellow
}

Write-Host "`n Accès à l'application: http://localhost:3000" -ForegroundColor Cyan 