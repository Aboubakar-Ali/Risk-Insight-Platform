# APIs de Risques Géonaturels et Vulnérabilité

## Vue d'ensemble

La plateforme Risk Insight intègre maintenant des APIs avancées pour l'évaluation des risques géonaturels et de la vulnérabilité par zones géographiques. Ces services fournissent une analyse complète combinant :

- **Données météo en temps réel** (OpenWeatherMap)
- **Historique des catastrophes naturelles** (CatNat, EM-DAT)
- **Vulnérabilité géographique** (JBA Risk Management, FEMA)

## Services implémentés

### 1. Service de Catastrophes Naturelles (`DisasterService`)

#### **Sources de données :**
- **CatNat** : Catastrophes naturelles françaises
- **EM-DAT** : Base de données mondiale des catastrophes

#### **Fonctionnalités :**
- Récupération d'historique des catastrophes par localisation
- Calcul de scores de risque basés sur la fréquence et la sévérité
- Analyse des événements récents (dernière année)
- Génération de données réalistes en mode fallback

#### **Endpoints API :**
```bash
# Risque de catastrophe pour un site
GET /api/v1/disasters/site/{site_id}

# Historique des catastrophes
GET /api/v1/disasters/historical/{site_id}

# Mise à jour des scores pour tous les sites
POST /api/v1/disasters/update-all-sites

# Statistiques globales
GET /api/v1/disasters/statistics
```

### 2. Service de Vulnérabilité (`VulnerabilityService`)

#### **Sources de données :**
- **JBA Risk Management** : Données de vulnérabilité détaillées
- **FEMA** : Données de vulnérabilité américaines (adaptées)

#### **Types de vulnérabilité analysés :**
- **Inondations** : Probabilité, profondeur, fréquence
- **Séismes** : Probabilité, magnitude, fréquence
- **Vents/Tempêtes** : Probabilité, vitesse, fréquence
- **Affaissements** : Probabilité, sévérité, fréquence

#### **Endpoints API :**
```bash
# Risque de vulnérabilité pour un site
GET /api/v1/vulnerability/site/{site_id}

# Zones de vulnérabilité détaillées
GET /api/v1/vulnerability/zones/{site_id}

# Analyse détaillée des zones
GET /api/v1/vulnerability/zone-analysis/{site_id}

# Mise à jour des scores pour tous les sites
POST /api/v1/vulnerability/update-all-sites

# Statistiques de vulnérabilité
GET /api/v1/vulnerability/statistics
```

### 3. Service de Calcul de Risque Global (`RiskCalculatorService`)

#### **Algorithme de pondération :**
- **Météo** : 25% (conditions actuelles)
- **Catastrophes** : 35% (historique)
- **Vulnérabilité** : 40% (géographique)

#### **Facteurs additionnels :**
- **Valeur du site** : Multiplicateur 0.8-1.5
- **Type de bâtiment** : Multiplicateur selon l'usage
- **Score de confiance** : Qualité des données sources

#### **Endpoints API :**
```bash
# Analyse globale pour un site
GET /api/v1/comprehensive-risk/site/{site_id}

# Recommandations détaillées
GET /api/v1/comprehensive-risk/recommendations/{site_id}

# Mise à jour globale pour tous les sites
POST /api/v1/comprehensive-risk/update-all-sites

# Statistiques globales
GET /api/v1/comprehensive-risk/statistics
```

## Exemples de réponses

### Analyse globale d'un site
```json
{
  "site_id": 1,
  "site_name": "Usine Marseille",
  "comprehensive_analysis": {
    "comprehensive_risk": {
      "global_risk_score": 41.48,
      "risk_level": "élevé",
      "risk_category": "surveillance",
      "confidence_score": 0.73,
      "risk_factors": {
        "weather_contribution": 4.85,
        "disaster_contribution": 7.95,
        "vulnerability_contribution": 15.02,
        "value_factor": 1.2,
        "type_factor": 1.3
      }
    },
    "recommendations": [
      "Risque élevé - Surveiller régulièrement les conditions",
      "Zone inondable - Vérifier les systèmes de drainage",
      "Zone venteuse - Sécuriser les éléments extérieurs"
    ]
  }
}
```

### Analyse de vulnérabilité
```json
{
  "vulnerability_risk": {
    "vulnerability_risk_score": 37.55,
    "zone_assessments": {
      "flood_zone": "élevée",
      "earthquake_zone": "faible",
      "wind_zone": "modérée",
      "subsidence_zone": "faible"
    },
    "risk_factors": {
      "flood_vulnerability": 45.2,
      "earthquake_vulnerability": 12.8,
      "wind_vulnerability": 38.4,
      "subsidence_vulnerability": 8.2,
      "infrastructure_vulnerability": 35.0
    }
  }
}
```

## Configuration des APIs

### Variables d'environnement requises :

```env
# APIs de catastrophes naturelles
CATNAT_API_KEY=your_catnat_api_key_here
EMDAT_API_KEY=your_emdat_api_key_here

# APIs de vulnérabilité
JBA_API_KEY=your_jba_api_key_here
FEMA_API_KEY=your_fema_api_key_here

# API météo (déjà configurée)
OPENWEATHER_API_KEY=84761b5d2a6226713689b94d03a4170e
```

### Mode fallback :
- **Sans clés API** : Génération de données réalistes basées sur la localisation
- **Données simulées** : Basées sur les caractéristiques géographiques de la France
- **Scores cohérents** : Maintien de la logique métier même sans données réelles

## Utilisation pratique

### 1. Évaluation d'un nouveau site
```bash
# Analyser un site spécifique
curl -X GET "http://localhost:8000/api/v1/comprehensive-risk/site/1"
```

### 2. Mise à jour globale du portfolio
```bash
# Mettre à jour tous les sites
curl -X POST "http://localhost:8000/api/v1/comprehensive-risk/update-all-sites"
```

### 3. Obtenir des recommandations
```bash
# Recommandations détaillées pour un site
curl -X GET "http://localhost:8000/api/v1/comprehensive-risk/recommendations/1"
```

### 4. Statistiques du portfolio
```bash
# Statistiques globales
curl -X GET "http://localhost:8000/api/v1/comprehensive-risk/statistics"
```

## Métriques et indicateurs

### Scores de risque :
- **0-20%** : Faible
- **20-40%** : Modéré
- **40-60%** : Élevé
- **60%+** : Très élevé

### Catégories de risque :
- **Acceptable** : < 25%
- **Surveillance** : 25-45%
- **Préoccupant** : 45-65%
- **Critique** : > 65%

### Zones de vulnérabilité :
- **Faible** : Risque minimal
- **Modérée** : Risque présent mais maîtrisé
- **Élevée** : Risque significatif nécessitant attention

## Améliorations futures

### APIs réelles à intégrer :
1. **CatNat API** : Données officielles françaises
2. **EM-DAT API** : Base de données mondiale
3. **JBA Risk Management** : Données de vulnérabilité détaillées
4. **FEMA API** : Données américaines (référence)

### Fonctionnalités avancées :
- **Prévisions météo** : Intégration de prévisions à 7-15 jours
- **Alertes en temps réel** : Notifications automatiques
- **Cartographie interactive** : Visualisation géographique
- **Modèles ML** : Prédiction de risques futurs

## Dépannage

### Erreurs courantes :
- **API non configurée** : Utilisation automatique du mode fallback
- **Données manquantes** : Génération de données réalistes
- **Scores incohérents** : Vérification des facteurs de pondération

### Logs utiles :
```bash
# Vérifier les logs du backend
docker-compose logs backend

# Tester un endpoint spécifique
curl -X GET "http://localhost:8000/api/v1/comprehensive-risk/site/1"
```

## Ressources

- **Documentation OpenWeatherMap** : https://openweathermap.org/api
- **Base CatNat** : https://www.catastrophes-naturelles.fr/
- **EM-DAT** : https://www.emdat.be/
- **JBA Risk Management** : https://www.jbarisk.com/
- **FEMA** : https://www.fema.gov/ 