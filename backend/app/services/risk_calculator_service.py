import asyncio
from typing import Dict, List, Optional
from fastapi import HTTPException
import random

from .weather_service import weather_service
from .disaster_service import disaster_service
from .vulnerability_service import vulnerability_service

class RiskCalculatorService:
    def __init__(self):
        self.weather_service = weather_service
        self.disaster_service = disaster_service
        self.vulnerability_service = vulnerability_service

    async def calculate_comprehensive_risk(self, latitude: float, longitude: float, site_type: str, site_value: float) -> Dict:
        """Calculer un score de risque global combinant tous les facteurs"""
        try:
            # Récupérer les données de tous les services
            weather_risk = await self.weather_service.get_weather_risk_for_site(latitude, longitude)
            disaster_risk = await self.disaster_service.get_disaster_risk_for_site(latitude, longitude, site_type, site_value)
            vulnerability_risk = await self.vulnerability_service.get_vulnerability_risk_for_site(latitude, longitude, site_type, site_value)
            
            # Calculer le score de risque global
            comprehensive_risk = self._calculate_global_risk_score(
                weather_risk, disaster_risk, vulnerability_risk, site_type, site_value
            )
            
            return {
                "comprehensive_risk": comprehensive_risk,
                "weather_risk": weather_risk,
                "disaster_risk": disaster_risk,
                "vulnerability_risk": vulnerability_risk,
                "risk_breakdown": self._get_risk_breakdown(weather_risk, disaster_risk, vulnerability_risk),
                "recommendations": self._generate_recommendations(comprehensive_risk, weather_risk, disaster_risk, vulnerability_risk)
            }
            
        except Exception as e:
            print(f"Erreur lors du calcul du risque global: {e}")
            return self._get_default_comprehensive_risk()

    def _calculate_global_risk_score(self, weather_risk: Dict, disaster_risk: Dict, vulnerability_risk: Dict, site_type: str, site_value: float) -> Dict:
        """Calculer le score de risque global"""
        try:
            # Extraire les scores de risque
            weather_score = weather_risk.get("risk_score", 25.0)
            disaster_score = disaster_risk.get("disaster_risk", {}).get("disaster_risk_score", 15.0)
            vulnerability_score = vulnerability_risk.get("vulnerability_risk", {}).get("vulnerability_risk_score", 25.0)
            
            # Pondération des facteurs de risque
            weather_weight = 0.25      # 25% - Conditions météo actuelles
            disaster_weight = 0.35     # 35% - Historique des catastrophes
            vulnerability_weight = 0.40 # 40% - Vulnérabilité géographique
            
            # Calculer le score pondéré
            weighted_score = (
                weather_score * weather_weight +
                disaster_score * disaster_weight +
                vulnerability_score * vulnerability_weight
            )
            
            # Facteur de valeur du site (plus la valeur est élevée, plus le risque est important)
            value_factor = min(1.5, max(0.8, site_value / 1000000))  # Entre 0.8 et 1.5
            
            # Facteur de type de site
            type_factor = {
                "résidentiel": 1.0,
                "commercial": 1.1,
                "industriel": 1.3,
                "agricole": 1.2,
                "public": 1.0,
                "logistique": 1.2
            }.get(site_type.lower(), 1.0)
            
            # Score final
            final_score = weighted_score * value_factor * type_factor
            
            return {
                "global_risk_score": min(100.0, max(0.0, final_score)),
                "risk_level": self._get_risk_level(final_score),
                "risk_category": self._get_risk_category(final_score),
                "confidence_score": self._calculate_confidence_score(weather_risk, disaster_risk, vulnerability_risk),
                "risk_factors": {
                    "weather_contribution": weather_score * weather_weight,
                    "disaster_contribution": disaster_score * disaster_weight,
                    "vulnerability_contribution": vulnerability_score * vulnerability_weight,
                    "value_factor": value_factor,
                    "type_factor": type_factor
                }
            }
            
        except Exception as e:
            print(f"Erreur lors du calcul du score global: {e}")
            return {
                "global_risk_score": 30.0,
                "risk_level": "modéré",
                "risk_category": "acceptable",
                "confidence_score": 0.7,
                "risk_factors": {
                    "weather_contribution": 6.25,
                    "disaster_contribution": 5.25,
                    "vulnerability_contribution": 10.0,
                    "value_factor": 1.0,
                    "type_factor": 1.0
                }
            }

    def _get_risk_level(self, score: float) -> str:
        """Déterminer le niveau de risque"""
        if score < 20:
            return "faible"
        elif score < 40:
            return "modéré"
        elif score < 60:
            return "élevé"
        else:
            return "très élevé"

    def _get_risk_category(self, score: float) -> str:
        """Déterminer la catégorie de risque"""
        if score < 25:
            return "acceptable"
        elif score < 45:
            return "surveillance"
        elif score < 65:
            return "préoccupant"
        else:
            return "critique"

    def _calculate_confidence_score(self, weather_risk: Dict, disaster_risk: Dict, vulnerability_risk: Dict) -> float:
        """Calculer un score de confiance basé sur la qualité des données"""
        confidence_factors = []
        
        # Qualité des données météo
        if weather_risk.get("weather_data"):
            confidence_factors.append(0.9)  # Données réelles
        else:
            confidence_factors.append(0.6)  # Données simulées
        
        # Qualité des données de catastrophes
        disaster_data_sources = disaster_risk.get("data_sources", {})
        if disaster_data_sources.get("catnat", 0) > 0 or disaster_data_sources.get("emdat", 0) > 0:
            confidence_factors.append(0.8)  # Données historiques disponibles
        else:
            confidence_factors.append(0.5)  # Données simulées
        
        # Qualité des données de vulnérabilité
        jba_data = vulnerability_risk.get("jba_data", {})
        fema_data = vulnerability_risk.get("fema_data", {})
        if jba_data or fema_data:
            confidence_factors.append(0.8)  # Données de vulnérabilité disponibles
        else:
            confidence_factors.append(0.5)  # Données simulées
        
        return sum(confidence_factors) / len(confidence_factors)

    def _get_risk_breakdown(self, weather_risk: Dict, disaster_risk: Dict, vulnerability_risk: Dict) -> Dict:
        """Obtenir la répartition détaillée des risques"""
        return {
            "weather": {
                "score": weather_risk.get("risk_score", 25.0),
                "factors": weather_risk.get("risk_factors", {}),
                "conditions": weather_risk.get("risk_factors", {}).get("conditions", "inconnues")
            },
            "disasters": {
                "score": disaster_risk.get("disaster_risk", {}).get("disaster_risk_score", 15.0),
                "historical_events": disaster_risk.get("disaster_risk", {}).get("risk_factors", {}).get("historical_events", 0),
                "recent_events": disaster_risk.get("disaster_risk", {}).get("risk_factors", {}).get("recent_events", 0),
                "frequency": disaster_risk.get("disaster_risk", {}).get("risk_factors", {}).get("frequency", "faible")
            },
            "vulnerability": {
                "score": vulnerability_risk.get("vulnerability_risk", {}).get("vulnerability_risk_score", 25.0),
                "zones": vulnerability_risk.get("vulnerability_risk", {}).get("zone_assessments", {}),
                "factors": vulnerability_risk.get("vulnerability_risk", {}).get("risk_factors", {})
            }
        }

    def _generate_recommendations(self, comprehensive_risk: Dict, weather_risk: Dict, disaster_risk: Dict, vulnerability_risk: Dict) -> List[str]:
        """Générer des recommandations basées sur l'analyse des risques"""
        recommendations = []
        
        global_score = comprehensive_risk.get("global_risk_score", 30.0)
        risk_level = comprehensive_risk.get("risk_level", "modéré")
        
        # Recommandations générales basées sur le niveau de risque
        if global_score > 60:
            recommendations.append("🚨 Risque critique - Considérer des mesures de protection renforcées")
            recommendations.append("📋 Réaliser une évaluation détaillée des vulnérabilités")
            recommendations.append("🛡️ Mettre en place des systèmes de surveillance en temps réel")
        elif global_score > 40:
            recommendations.append("⚠️ Risque élevé - Surveiller régulièrement les conditions")
            recommendations.append("🔧 Renforcer les mesures de protection existantes")
            recommendations.append("📊 Maintenir un suivi des indicateurs de risque")
        elif global_score > 20:
            recommendations.append("📈 Risque modéré - Maintenir la vigilance")
            recommendations.append("📋 Réviser périodiquement les plans de prévention")
        else:
            recommendations.append("✅ Risque faible - Maintenir les bonnes pratiques")
        
        # Recommandations spécifiques basées sur les facteurs de risque
        weather_score = weather_risk.get("risk_score", 25.0)
        if weather_score > 50:
            recommendations.append("🌤️ Conditions météo défavorables - Surveiller les prévisions")
        
        disaster_score = disaster_risk.get("disaster_risk", {}).get("disaster_risk_score", 15.0)
        if disaster_score > 40:
            recommendations.append("🌊 Historique de catastrophes - Renforcer la préparation")
        
        vulnerability_score = vulnerability_risk.get("vulnerability_risk", {}).get("vulnerability_risk_score", 25.0)
        if vulnerability_score > 50:
            recommendations.append("🏗️ Vulnérabilité géographique élevée - Considérer des renforcements structurels")
        
        # Recommandations basées sur les zones
        zones = vulnerability_risk.get("vulnerability_risk", {}).get("zone_assessments", {})
        if zones.get("flood_zone") == "élevée":
            recommendations.append("🌊 Zone inondable - Vérifier les systèmes de drainage")
        if zones.get("earthquake_zone") == "élevée":
            recommendations.append("🌋 Zone sismique - Renforcer la structure du bâtiment")
        if zones.get("wind_zone") == "élevée":
            recommendations.append("💨 Zone venteuse - Sécuriser les éléments extérieurs")
        
        return recommendations

    def _get_default_comprehensive_risk(self) -> Dict:
        """Retourner un risque par défaut en cas d'erreur"""
        return {
            "comprehensive_risk": {
                "global_risk_score": 30.0,
                "risk_level": "modéré",
                "risk_category": "acceptable",
                "confidence_score": 0.7,
                "risk_factors": {
                    "weather_contribution": 6.25,
                    "disaster_contribution": 5.25,
                    "vulnerability_contribution": 10.0,
                    "value_factor": 1.0,
                    "type_factor": 1.0
                }
            },
            "weather_risk": {
                "risk_score": 25.0,
                "risk_factors": {
                    "temperature": 20.0,
                    "humidity": 60.0,
                    "wind_speed": 10.0,
                    "conditions": "données par défaut"
                }
            },
            "disaster_risk": {
                "disaster_risk": {
                    "disaster_risk_score": 15.0,
                    "risk_factors": {
                        "historical_events": 0,
                        "frequency": "faible",
                        "severity": "faible",
                        "proximity_risk": "faible"
                    }
                },
                "disasters": [],
                "data_sources": {"catnat": 0, "emdat": 0}
            },
            "vulnerability_risk": {
                "vulnerability_risk": {
                    "vulnerability_risk_score": 25.0,
                    "risk_factors": {
                        "flood_vulnerability": 20.0,
                        "earthquake_vulnerability": 15.0,
                        "wind_vulnerability": 20.0,
                        "subsidence_vulnerability": 10.0,
                        "infrastructure_vulnerability": 25.0,
                        "site_type_multiplier": 1.0
                    },
                    "zone_assessments": {
                        "flood_zone": "inconnue",
                        "earthquake_zone": "inconnue",
                        "wind_zone": "inconnue",
                        "subsidence_zone": "inconnue"
                    }
                },
                "jba_data": {},
                "fema_data": {}
            },
            "risk_breakdown": {
                "weather": {"score": 25.0, "factors": {}, "conditions": "inconnues"},
                "disasters": {"score": 15.0, "historical_events": 0, "recent_events": 0, "frequency": "faible"},
                "vulnerability": {"score": 25.0, "zones": {}, "factors": {}}
            },
            "recommendations": [
                "✅ Risque modéré - Maintenir la vigilance",
                "📋 Réviser périodiquement les plans de prévention"
            ]
        }

# Instance globale du service
risk_calculator_service = RiskCalculatorService() 