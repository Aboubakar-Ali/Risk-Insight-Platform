# Risk Insight Platform

Plateforme d'aide à la décision pour les assurances corporate

## Objectifs

- **Gestion de portefeuille** : Visualiser et analyser les sites assurés
- **Évaluation des risques** : Scorer dynamiquement les nouveaux sites
- **Prédiction de rentabilité** : Analyser la viabilité des contrats
- **Agent IA spécialisé** : Recommandations intelligentes en langage naturel

## Architecture

```
risk-insight-platform/
├── frontend/                 # Next.js 14 + TypeScript + Tailwind
├── backend/                  # FastAPI + Pydantic
├── ml-engine/               # Moteur de scoring + LangChain
├── database/                # PostgreSQL + Prisma
├── docker/                  # Configuration Docker
├── docs/                    # Documentation
└── scripts/                 # Scripts utilitaires
```

## Technologies

- **Frontend** : Next.js 14, TypeScript, Tailwind CSS, Shadcn/ui
- **Backend** : FastAPI, Pydantic, PostgreSQL
- **IA/ML** : LangChain, OpenAI, Scikit-learn
- **APIs** : OpenWeatherMap, CatNat, EM-DAT
- **Infrastructure** : Docker, Docker Compose

## Prérequis

- **Docker Desktop** : Version 4.0+ 
- **Git** : Pour cloner le repository
- **8GB RAM minimum** (16GB recommandé)
- **5GB d'espace disque libre**

## Démarrage Rapide

### Avec Docker (Recommandé)

```bash
# 1. Cloner le projet
git clone <votre-repository-url>
cd risk-insight-platform

# 2. Configuration (optionnel)
cp env.example .env
# Éditer .env avec vos clés API si vous en avez

# 3. Démarrer la plateforme
docker-compose up --build

# 4. Accéder à l'application
# Frontend : http://localhost:3000
# Backend API : http://localhost:8000
# Documentation API : http://localhost:8000/docs
```

### Commandes Docker utiles

```bash
# Démarrer en arrière-plan
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter la plateforme
docker-compose down

# Reconstruire après modifications
docker-compose up --build
```

### Installation locale (Pour développement)

```bash
# 1. Prérequis
# - Python 3.11+
# - Node.js 18+
# - PostgreSQL 15+

# 2. Configuration
cp env.example .env

# 3. Backend (Terminal 1)
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 4. Frontend (Terminal 2)
cd frontend
npm install
npm run dev

# 5. Base de données (Terminal 3)
# Démarrer PostgreSQL ou utiliser Docker :
docker run --name postgres-risk -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15
```

## Configuration

### Variables d'environnement (.env)

```env
# Configuration de la base de données
DATABASE_URL=postgresql://risk_user:risk_password@localhost:5432/risk_insight

# APIs externes (optionnel pour le MVP)
OPENAI_API_KEY=your_openai_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here

# Configuration du backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DEBUG=true

# Configuration du frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Risk Insight Platform
```

### APIs externes (optionnel)

1. **OpenWeatherMap** : Clé API gratuite pour les données météo
2. **OpenAI** : Clé API pour les fonctionnalités IA

## Documentation

- [Guide d'installation](./docs/installation.md)
- [Architecture technique](./docs/architecture.md)
- [API Reference](./docs/api.md)
- [Guide utilisateur](./docs/user-guide.md)

## Fonctionnalités

### Phase 1 - MVP (Implémenté)
- [x] Architecture de base
- [x] Modèles de données
- [x] API REST complète
- [x] Interface utilisateur basique
- [x] Dashboard de sites
- [x] Gestion des risques

### Phase 2 - IA (En cours)
- [ ] Intégration LangChain
- [ ] Agent IA spécialisé
- [ ] Prédictions de rentabilité
- [ ] Recommandations intelligentes

### Phase 3 - Automatisation (Planifié)
- [ ] Intégration n8n
- [ ] Workflows automatisés
- [ ] Alertes en temps réel

## Développement

### Structure du projet

```
├── frontend/                 # Application Next.js
│   ├── app/                 # Pages et composants
│   ├── components/          # Composants réutilisables
│   └── lib/                # Utilitaires
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/            # Routes API
│   │   ├── models/         # Modèles SQLAlchemy
│   │   ├── schemas/        # Schémas Pydantic
│   │   └── services/       # Logique métier
│   └── main.py             # Point d'entrée
├── ml-engine/              # Moteur ML (optionnel)
├── database/               # Scripts DB
└── docs/                   # Documentation
```

### Commandes utiles

```bash
# Docker (Production)
docker-compose up --build          # Démarrer avec construction
docker-compose up -d               # Démarrer en arrière-plan
docker-compose logs -f             # Voir les logs en temps réel
docker-compose down                # Arrêter tous les services

# Développement local
cd backend && uvicorn main:app --reload  # Backend avec auto-reload
cd frontend && npm run dev         # Frontend avec hot-reload

# Tests
cd backend && python -m pytest    # Tests backend
cd frontend && npm test           # Tests frontend

# Build de production
cd frontend && npm run build      # Build optimisé du frontend
```

## Dépannage

### Problèmes courants

1. **Ports déjà utilisés** : Changer les ports dans docker-compose.yml
2. **Docker non démarré** : Démarrer Docker Desktop
3. **Erreurs de dépendances** : Supprimer node_modules et réinstaller

### Logs

```bash
# Docker
docker-compose logs -f

# Backend
cd backend && python -m uvicorn main:app --reload --log-level debug

# Frontend
cd frontend && npm run dev
```

## Roadmap

### Version 1.0 (MVP)
- Dashboard de base
- Gestion des sites
- API REST
- Interface utilisateur

### Version 1.1 (IA)
- Agent IA spécialisé
- Prédictions avancées
- Analyse de risques

### Version 2.0 (Production)
- Déploiement cloud
- Authentification
- Application mobile
- Automatisation complète

## Contribution

1. Fork le projet
2. Créer une branche feature
3. Commit les changements
4. Push vers la branche
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## Support

- Issues GitHub : [Lien vers le repository]
- Documentation : [Lien vers la documentation]
- Email : support@risk-insight.com 