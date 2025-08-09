Write-Host "🚀 Démarrage local de Risk Insight Platform..." -ForegroundColor Green

# Vérifier que Python est installé
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python n'est pas installé. Veuillez installer Python 3.11+ d'abord." -ForegroundColor Red
    exit 1
}

# Vérifier que Node.js est installé
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Node.js n'est pas installé. Veuillez installer Node.js 18+ d'abord." -ForegroundColor Red
    exit 1
}

Write-Host "📦 Installation des dépendances..." -ForegroundColor Yellow

# Installer les dépendances du backend
Write-Host "Installing backend dependencies..." -ForegroundColor Cyan
Set-Location backend
python -m pip install -r requirements.txt
Set-Location ..

# Installer les dépendances du frontend
Write-Host "Installing frontend dependencies..." -ForegroundColor Cyan
Set-Location frontend
npm install
Set-Location ..

Write-Host "✅ Dépendances installées avec succès!" -ForegroundColor Green

Write-Host ""
Write-Host "🎯 Pour démarrer l'application :" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Démarrer le backend (dans un terminal) :" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Démarrer le frontend (dans un autre terminal) :" -ForegroundColor White
Write-Host "   cd frontend" -ForegroundColor Gray
Write-Host "   npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "📱 Accès aux services :" -ForegroundColor Cyan
Write-Host "   - Frontend : http://localhost:3000" -ForegroundColor White
Write-Host "   - Backend API : http://localhost:8000" -ForegroundColor White
Write-Host "   - Documentation API : http://localhost:8000/docs" -ForegroundColor White 