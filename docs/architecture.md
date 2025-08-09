# Architecture Technique

## Vue d'ensemble

La plateforme Risk Insight est construite avec une architecture modulaire et évolutive, séparant clairement les responsabilités entre les différentes couches.

## Architecture générale

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   ML Engine     │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (LangChain)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │   APIs Externes │    │   Cache Redis   │
│   (Base de      │    │   (Météo,       │    │   (Optionnel)   │
│    données)     │    │    CatNat...)   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Composants détaillés

### 1. Frontend (Next.js 14)

**Technologies :**
- Next.js 14 avec App Router
- TypeScript pour la sécurité des types
- Tailwind CSS pour le styling
- Shadcn/ui pour les composants
- Recharts pour les graphiques
- React Hook Form + Zod pour la validation

**Structure :**
```
frontend/
├── app/                    # App Router Next.js
│   ├── (dashboard)/       # Routes du dashboard
│   ├── api/               # API routes Next.js
│   └── globals.css        # Styles globaux
├── components/            # Composants réutilisables
│   ├── ui/               # Composants UI de base
│   ├── forms/            # Formulaires
│   └── charts/           # Graphiques
├── lib/                  # Utilitaires
├── hooks/                # Hooks personnalisés
└── types/                # Types TypeScript
```

### 2. Backend (FastAPI)

**Technologies :**
- FastAPI pour l'API REST
- Pydantic pour la validation
- SQLAlchemy pour l'ORM
- PostgreSQL comme base de données
- Alembic pour les migrations

**Structure :**
```
backend/
├── app/
│   ├── api/              # Routes API
│   │   └── v1/          # Version 1 de l'API
│   ├── core/            # Configuration
│   ├── models/          # Modèles SQLAlchemy
│   ├── schemas/         # Schémas Pydantic
│   ├── services/        # Logique métier
│   └── utils/           # Utilitaires
├── alembic/             # Migrations
└── tests/               # Tests
```

### 3. Moteur ML (LangChain + OpenAI)

**Technologies :**
- LangChain pour l'orchestration IA
- OpenAI pour les modèles de langage
- Scikit-learn pour les modèles de scoring
- Pandas pour le traitement des données

**Fonctionnalités :**
- Scoring de risque automatisé
- Agent IA spécialisé
- Prédictions de rentabilité
- Analyse de données historiques

## Modèles de données

### Sites
- Informations géographiques
- Caractéristiques du bâtiment
- Score de risque calculé

### Contrats d'assurance
- Détails du contrat
- Prédictions de rentabilité
- Évaluation des risques

### Données externes
- Météo (OpenWeatherMap)
- Catastrophes naturelles (CatNat, EM-DAT)
- Données de vulnérabilité

## APIs externes intégrées

### 1. OpenWeatherMap
- Données météo actuelles
- Prévisions météorologiques
- Historique météo

### 2. CatNat (France)
- Déclarations de catastrophes naturelles
- Zones sinistrées
- Montants des dommages

### 3. EM-DAT (International)
- Base de données des catastrophes
- Données historiques globales
- Statistiques d'impact

## Sécurité

### Authentification
- JWT pour l'authentification
- Sessions sécurisées
- Gestion des rôles

### Validation
- Validation côté client (Zod)
- Validation côté serveur (Pydantic)
- Sanitisation des données

### CORS
- Configuration stricte des origines
- Headers de sécurité
- Protection CSRF

## Performance

### Caching
- Cache Redis pour les données externes
- Cache des scores de risque
- Mise en cache des réponses API

### Optimisation
- Pagination des résultats
- Requêtes optimisées
- Lazy loading des composants

## Monitoring

### Logs
- Logs structurés
- Niveaux de log configurables
- Rotation des logs

### Métriques
- Métriques de performance
- Métriques métier
- Alertes automatisées

## Déploiement

### Docker
- Images optimisées
- Multi-stage builds
- Configuration via variables d'environnement

### Orchestration
- Docker Compose pour le développement
- Kubernetes pour la production
- CI/CD automatisé

## Évolutivité

### Architecture modulaire
- Services indépendants
- APIs versionnées
- Évolution sans breaking changes

### Scalabilité
- Base de données scalable
- Load balancing
- Auto-scaling

## Roadmap technique

### Phase 1 - MVP
- [x] Architecture de base
- [x] Modèles de données
- [ ] API REST complète
- [ ] Interface utilisateur basique

### Phase 2 - IA
- [ ] Intégration LangChain
- [ ] Agent IA spécialisé
- [ ] Modèles de prédiction

### Phase 3 - Automatisation
- [ ] Intégration n8n
- [ ] Workflows automatisés
- [ ] Alertes en temps réel 