Write-Host " Configuration de Risk Insight Platform..." -ForegroundColor Green

# Vérifier que Docker est installé
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Docker n'est pas installé. Veuillez installer Docker Desktop d'abord." -ForegroundColor Red
    exit 1
}

if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host " Docker Compose n'est pas installé. Veuillez installer Docker Compose d'abord." -ForegroundColor Red
    exit 1
}

# Copier le fichier d'environnement
if (-not (Test-Path ".env")) {
    Write-Host " Création du fichier .env..." -ForegroundColor Yellow
    Copy-Item "env.example" ".env"
    Write-Host " Fichier .env créé. Veuillez configurer vos variables d'environnement." -ForegroundColor Green
}

# Construire et démarrer les services
Write-Host " Construction des images Docker..." -ForegroundColor Yellow
docker-compose build

Write-Host " Démarrage des services..." -ForegroundColor Yellow
docker-compose up -d

Write-Host " Attente du démarrage des services..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Vérifier que les services sont démarrés
Write-Host " Vérification des services..." -ForegroundColor Yellow

try {
    $backendResponse = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 10
    if ($backendResponse.StatusCode -eq 200) {
        Write-Host " Backend démarré avec succès" -ForegroundColor Green
    } else {
        Write-Host " Erreur lors du démarrage du backend" -ForegroundColor Red
    }
} catch {
    Write-Host " Erreur lors du démarrage du backend" -ForegroundColor Red
}

try {
    $frontendResponse = Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing -TimeoutSec 10
    if ($frontendResponse.StatusCode -eq 200) {
        Write-Host " Frontend démarré avec succès" -ForegroundColor Green
    } else {
        Write-Host " Erreur lors du démarrage du frontend" -ForegroundColor Red
    }
} catch {
    Write-Host " Erreur lors du démarrage du frontend" -ForegroundColor Red
}

Write-Host ""
Write-Host " Risk Insight Platform est prêt !" -ForegroundColor Green
Write-Host ""
Write-Host " Accès aux services :" -ForegroundColor Cyan
Write-Host "   - Frontend : http://localhost:3000" -ForegroundColor White
Write-Host "   - Backend API : http://localhost:8000" -ForegroundColor White
Write-Host "   - Documentation API : http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host " Documentation :" -ForegroundColor Cyan
Write-Host "   - Architecture : ./docs/architecture.md" -ForegroundColor White
Write-Host "   - Guide d'installation : ./docs/installation.md" -ForegroundColor White
Write-Host ""
Write-Host " Commandes utiles :" -ForegroundColor Cyan
Write-Host "   - Arrêter les services : docker-compose down" -ForegroundColor White
Write-Host "   - Voir les logs : docker-compose logs -f" -ForegroundColor White
Write-Host "   - Redémarrer : docker-compose restart" -ForegroundColor White 