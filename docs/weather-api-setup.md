# Configuration de l'API Météo OpenWeatherMap

## Prérequis

Pour avoir des données météo réelles dans la plateforme, vous devez configurer une clé API OpenWeatherMap.

## Étape 1 : Obtenir une clé API gratuite

1. **Allez sur** https://openweathermap.org/api
2. **Cliquez sur "Sign Up"** pour créer un compte gratuit
3. **Confirmez votre email** (vérifiez vos spams)
4. **Connectez-vous** à votre compte
5. **Allez dans "My API Keys"**
6. **Copiez votre clé API** (gratuite pour 1000 appels/jour)

## ⚙️ Étape 2 : Configurer la clé dans le projet

### Option A : Script automatique (recommandé)

```powershell
.\scripts\configure-api-keys.ps1
```

Le script vous guidera pour :
- Créer le fichier `.env` s'il n'existe pas
- Entrer votre clé API OpenWeatherMap
- Tester la configuration
- Redémarrer automatiquement le backend

### Option B : Configuration manuelle

1. **Créez un fichier `.env`** à la racine du projet
2. **Ajoutez votre clé API** :

```env
# Configuration de la base de données
DATABASE_URL=postgresql://risk_user:risk_password@localhost:5432/risk_insight

# APIs externes
OPENAI_API_KEY=your_openai_api_key_here
OPENWEATHER_API_KEY=VOTRE_CLE_API_ICI

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
```

3. **Redémarrez le backend** :

```powershell
docker-compose restart backend
```

## Étape 3 : Tester la configuration

### Test via PowerShell

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/weather/site/1" -Method GET
```

### Test via l'interface web

1. **Allez sur** http://localhost:3000
2. **Cliquez sur un site** dans la liste
3. **Vérifiez la section "Conditions Météo Actuelles"**

## Résultats attendus

### Avec clé API configurée :
- **Données météo réelles** en temps réel
- **Scores de risque précis** basés sur les conditions actuelles
- **Température, humidité, vent** affichés
- **Conditions météo détaillées**

### Sans clé API :
- **Données météo simulées** (réalistes mais aléatoires)
- **Scores de risque basés** sur des données par défaut
- **Message d'avertissement** dans les logs

## Dépannage

### Erreur "API key not valid"
- Vérifiez que votre clé API est correcte
- Attendez quelques minutes après la création de la clé (activation différée)
- Vérifiez que vous avez bien copié toute la clé

### Erreur "API key not found"
- Vérifiez que le fichier `.env` existe
- Vérifiez que la variable `OPENWEATHER_API_KEY` est définie
- Redémarrez le backend après modification

### Pas de données météo
- Vérifiez les logs du backend : `docker-compose logs backend`
- Testez l'API directement : `Invoke-RestMethod -Uri "http://localhost:8000/api/v1/weather/site/1"`

## Limites de l'API gratuite

- **1000 appels/jour** (suffisant pour les tests)
- **Données actuelles** uniquement (pas d'historique)
- **Mise à jour toutes les 10 minutes**

## Améliorations possibles

- **Cache des données** pour réduire les appels API
- **Données historiques** avec un plan payant
- **Prévisions météo** pour l'évaluation des risques futurs
- **Alertes météo** pour les conditions extrêmes 