# Guide d'Installation

## Prérequis

### Système
- **OS** : Windows 10/11, macOS 10.15+, ou Linux
- **RAM** : Minimum 8GB (recommandé 16GB)
- **Espace disque** : 5GB minimum
- **Docker** : Version 20.10+
- **Docker Compose** : Version 2.0+

### APIs externes (optionnel pour le MVP)
- **OpenWeatherMap** : Clé API gratuite
- **OpenAI** : Clé API pour les fonctionnalités IA

## Installation rapide

### 1. Cloner le projet
```bash
git clone <repository-url>
cd risk-insight-platform
```

### 2. Configuration automatique
```bash
# Sur Linux/macOS
chmod +x scripts/setup.sh
./scripts/setup.sh

# Sur Windows (PowerShell)
.\scripts\setup.ps1
```

### 3. Configuration manuelle (si nécessaire)

#### Étape 1 : Variables d'environnement
```bash
cp env.example .env
```

Éditer le fichier `.env` :
```env
# Configuration de la base de données
DATABASE_URL=postgresql://risk_user:risk_password@localhost:5432/risk_insight

# APIs externes (optionnel)
OPENAI_API_KEY=your_openai_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here

# Configuration du backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DEBUG=true
```

#### Étape 2 : Démarrage des services
```bash
# Construire les images
docker-compose build

# Démarrer les services
docker-compose up -d
```

#### Étape 3 : Vérification
```bash
# Vérifier que les services sont démarrés
docker-compose ps

# Voir les logs
docker-compose logs -f
```

## Installation détaillée

### Option 1 : Installation avec Docker (Recommandée)

#### Prérequis Docker
1. **Installer Docker Desktop**
   - [Windows](https://docs.docker.com/desktop/install/windows/)
   - [macOS](https://docs.docker.com/desktop/install/mac/)
   - [Linux](https://docs.docker.com/desktop/install/linux/)

2. **Vérifier l'installation**
   ```bash
   docker --version
   docker-compose --version
   ```

#### Démarrage
```bash
# Cloner le projet
git clone <repository-url>
cd risk-insight-platform

# Configuration
cp env.example .env
# Éditer .env avec vos clés API

# Démarrage
docker-compose up -d

# Vérification
docker-compose ps
```

### Option 2 : Installation locale

#### Prérequis
- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL 15+**

#### Backend
```bash
cd backend

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configuration de la base de données
# Créer une base PostgreSQL et mettre à jour DATABASE_URL dans .env

# Démarrer le serveur
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend

# Installer les dépendances
npm install

# Démarrer le serveur de développement
npm run dev
```

## Configuration des APIs externes

### OpenWeatherMap
1. Créer un compte sur [OpenWeatherMap](https://openweathermap.org/)
2. Obtenir une clé API gratuite
3. Ajouter la clé dans `.env` :
   ```env
   OPENWEATHER_API_KEY=your_api_key_here
   ```

### OpenAI
1. Créer un compte sur [OpenAI](https://platform.openai.com/)
2. Obtenir une clé API
3. Ajouter la clé dans `.env` :
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

## Vérification de l'installation

### Services accessibles
- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs
- **Base de données** : localhost:5432

### Tests de base
```bash
# Test du backend
curl http://localhost:8000/health

# Test du frontend
curl http://localhost:3000

# Test de la base de données
docker-compose exec postgres psql -U risk_user -d risk_insight -c "SELECT version();"
```

## Dépannage

### Problèmes courants

#### 1. Ports déjà utilisés
```bash
# Vérifier les ports utilisés
netstat -an | grep :3000
netstat -an | grep :8000
netstat -an | grep :5432

# Changer les ports dans docker-compose.yml si nécessaire
```

#### 2. Problèmes de permissions Docker
```bash
# Sur Linux, ajouter l'utilisateur au groupe docker
sudo usermod -aG docker $USER
# Redémarrer la session
```

#### 3. Erreurs de base de données
```bash
# Redémarrer la base de données
docker-compose restart postgres

# Vérifier les logs
docker-compose logs postgres
```

#### 4. Problèmes de mémoire
```bash
# Augmenter la mémoire Docker (Docker Desktop)
# Settings > Resources > Memory: 8GB minimum
```

### Logs et debugging
```bash
# Voir tous les logs
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres

# Accéder à un conteneur
docker-compose exec backend bash
docker-compose exec postgres psql -U risk_user -d risk_insight
```

## Mise à jour

### Mise à jour du code
```bash
# Récupérer les dernières modifications
git pull origin main

# Reconstruire les images
docker-compose build

# Redémarrer les services
docker-compose up -d
```

### Mise à jour des dépendances
```bash
# Backend
cd backend
pip install --upgrade -r requirements.txt

# Frontend
cd frontend
npm update
```

## Désinstallation

### Arrêter les services
```bash
docker-compose down
```

### Supprimer les données
```bash
# Supprimer les volumes (attention : perte de données)
docker-compose down -v

# Supprimer les images
docker-compose down --rmi all
```

## Support

### Documentation
- [Architecture](./architecture.md)
- [API Reference](./api.md)
- [Guide utilisateur](./user-guide.md)

### Problèmes connus
- Vérifier que Docker Desktop a suffisamment de mémoire (8GB minimum)
- Sur Windows, s'assurer que WSL2 est activé
- Sur macOS, vérifier que les ports ne sont pas bloqués par le firewall

### Contact
- Issues GitHub : [Lien vers le repository]
- Documentation : [Lien vers la documentation] 