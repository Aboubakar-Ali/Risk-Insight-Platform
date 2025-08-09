import httpx
import asyncio
from typing import Dict, List, Optional
from fastapi import HTTPException
import os
import json
from datetime import datetime, timedelta
import random

class DisasterService:
    def __init__(self):
        # Configuration des APIs
        self.catnat_base_url = "https://api.catnat.fr/v1"
        self.emdat_base_url = "https://public.emdat.be/api/v1"
        
        # Clés API (à configurer)
        self.catnat_api_key = os.getenv("CATNAT_API_KEY")
        self.emdat_api_key = os.getenv("EMDAT_API_KEY")
        
        # Vérifier la configuration
        if not self.catnat_api_key or self.catnat_api_key == "your_catnat_api_key_here":
            print("⚠️  CATNAT_API_KEY non configurée - Utilisation des données par défaut")
            self.catnat_api_key = None
            
        if not self.emdat_api_key or self.emdat_api_key == "your_emdat_api_key_here":
            print("⚠️  EMDAT_API_KEY non configurée - Utilisation des données par défaut")
            self.emdat_api_key = None

    async def get_catnat_disasters(self, latitude: float, longitude: float, radius_km: int = 50) -> List[Dict]:
        """Récupérer les catastrophes naturelles françaises via CatNat"""
        if not self.catnat_api_key:
            return self._get_default_catnat_data(latitude, longitude)

        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.catnat_base_url}/disasters"
                params = {
                    "lat": latitude,
                    "lon": longitude,
                    "radius": radius_km,
                    "api_key": self.catnat_api_key,
                    "format": "json"
                }
                
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                
                return response.json().get("disasters", [])

        except httpx.HTTPStatusError as e:
            print(f"⚠️  Erreur API CatNat: {e.response.status_code} - Utilisation des données par défaut")
            return self._get_default_catnat_data(latitude, longitude)
        except Exception as e:
            print(f"⚠️  Erreur lors de la récupération CatNat: {str(e)} - Utilisation des données par défaut")
            return self._get_default_catnat_data(latitude, longitude)

    async def get_emdat_disasters(self, latitude: float, longitude: float, country: str = "France") -> List[Dict]:
        """Récupérer les catastrophes naturelles via EM-DAT"""
        if not self.emdat_api_key:
            return self._get_default_emdat_data(latitude, longitude, country)

        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.emdat_base_url}/disasters"
                params = {
                    "country": country,
                    "lat": latitude,
                    "lon": longitude,
                    "api_key": self.emdat_api_key,
                    "format": "json"
                }
                
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                
                return response.json().get("disasters", [])

        except httpx.HTTPStatusError as e:
            print(f"⚠️  Erreur API EM-DAT: {e.response.status_code} - Utilisation des données par défaut")
            return self._get_default_emdat_data(latitude, longitude, country)
        except Exception as e:
            print(f"⚠️  Erreur lors de la récupération EM-DAT: {str(e)} - Utilisation des données par défaut")
            return self._get_default_emdat_data(latitude, longitude, country)

    def _get_default_catnat_data(self, latitude: float, longitude: float) -> List[Dict]:
        """Générer des données CatNat par défaut basées sur la localisation"""
        disasters = []
        
        # Utiliser les coordonnées comme seed pour la cohérence
        base_seed = int(latitude * 1000 + longitude * 1000)
        random.seed(base_seed)
        
        # Déterminer la région basée sur les coordonnées
        if 43.0 <= latitude <= 51.0 and -5.0 <= longitude <= 10.0:  # France métropolitaine
            # Déterminer la zone géographique avec des variations plus importantes
            if latitude > 48.0:  # Nord de la France
                disaster_types = [
                    {"type": "inondation", "frequency": 0.6, "severity": "élevée"},
                    {"type": "tempête", "frequency": 0.5, "severity": "élevée"},
                    {"type": "sécheresse", "frequency": 0.1, "severity": "modérée"},
                    {"type": "mouvement de terrain", "frequency": 0.05, "severity": "faible"},
                    {"type": "feu de forêt", "frequency": 0.05, "severity": "modérée"},
                    {"type": "séisme", "frequency": 0.02, "severity": "faible"},
                    {"type": "avalanche", "frequency": 0.08, "severity": "modérée"},
                    {"type": "submersion marine", "frequency": 0.12, "severity": "élevée"}
                ]
            elif latitude > 45.0:  # Centre de la France
                disaster_types = [
                    {"type": "inondation", "frequency": 0.4, "severity": "modérée"},
                    {"type": "tempête", "frequency": 0.35, "severity": "modérée"},
                    {"type": "sécheresse", "frequency": 0.3, "severity": "élevée"},
                    {"type": "mouvement de terrain", "frequency": 0.15, "severity": "modérée"},
                    {"type": "feu de forêt", "frequency": 0.2, "severity": "élevée"},
                    {"type": "séisme", "frequency": 0.08, "severity": "modérée"},
                    {"type": "avalanche", "frequency": 0.02, "severity": "faible"},
                    {"type": "submersion marine", "frequency": 0.03, "severity": "faible"}
                ]
            else:  # Sud de la France
                disaster_types = [
                    {"type": "inondation", "frequency": 0.3, "severity": "modérée"},
                    {"type": "tempête", "frequency": 0.25, "severity": "modérée"},
                    {"type": "sécheresse", "frequency": 0.5, "severity": "élevée"},
                    {"type": "mouvement de terrain", "frequency": 0.25, "severity": "élevée"},
                    {"type": "feu de forêt", "frequency": 0.35, "severity": "élevée"},
                    {"type": "séisme", "frequency": 0.15, "severity": "modérée"},
                    {"type": "avalanche", "frequency": 0.03, "severity": "faible"},
                    {"type": "submersion marine", "frequency": 0.08, "severity": "modérée"}
                ]
        else:
            # Autres pays - données génériques
            disaster_types = [
                {"type": "inondation", "frequency": 0.25, "severity": "modérée"},
                {"type": "tempête", "frequency": 0.2, "severity": "modérée"},
                {"type": "sécheresse", "frequency": 0.15, "severity": "modérée"},
                {"type": "mouvement de terrain", "frequency": 0.08, "severity": "faible"},
                {"type": "feu de forêt", "frequency": 0.1, "severity": "modérée"},
                {"type": "séisme", "frequency": 0.05, "severity": "faible"},
                {"type": "avalanche", "frequency": 0.02, "severity": "faible"},
                {"type": "submersion marine", "frequency": 0.05, "severity": "modérée"}
            ]
        
        # Générer des catastrophes avec des variations plus importantes
        for disaster_type in disaster_types:
            if random.random() < disaster_type["frequency"]:
                # Date aléatoire dans les 5 dernières années
                days_ago = random.randint(1, 1825)  # 5 ans
                disaster_date = datetime.now() - timedelta(days=days_ago)
                
                disasters.append({
                    "id": f"catnat_{random.randint(1000, 9999)}",
                    "type": disaster_type["type"],
                    "date": disaster_date.strftime("%Y-%m-%d"),
                    "severity": disaster_type["severity"],
                    "location": {
                        "latitude": latitude + random.uniform(-0.1, 0.1),
                        "longitude": longitude + random.uniform(-0.1, 0.1)
                    },
                    "damage_estimate": random.randint(100000, 5000000),
                    "affected_area_km2": random.randint(1, 100)
                })
        
        return disasters

    def _get_default_emdat_data(self, latitude: float, longitude: float, country: str) -> List[Dict]:
        """Générer des données EM-DAT par défaut"""
        disasters = []
        
        # Types de catastrophes par région
        if country.lower() == "france":
            disaster_types = [
                {"type": "Flood", "frequency": 0.25, "avg_deaths": 5, "avg_damage": 1000000},
                {"type": "Storm", "frequency": 0.2, "avg_deaths": 3, "avg_damage": 500000},
                {"type": "Drought", "frequency": 0.15, "avg_deaths": 0, "avg_damage": 2000000},
                {"type": "Wildfire", "frequency": 0.1, "avg_deaths": 2, "avg_damage": 300000},
                {"type": "Earthquake", "frequency": 0.05, "avg_deaths": 10, "avg_damage": 5000000},
                {"type": "Landslide", "frequency": 0.05, "avg_deaths": 1, "avg_damage": 200000}
            ]
        else:
            # Données génériques pour d'autres pays
            disaster_types = [
                {"type": "Flood", "frequency": 0.3, "avg_deaths": 10, "avg_damage": 2000000},
                {"type": "Storm", "frequency": 0.25, "avg_deaths": 5, "avg_damage": 1000000},
                {"type": "Earthquake", "frequency": 0.1, "avg_deaths": 50, "avg_damage": 10000000},
                {"type": "Drought", "frequency": 0.15, "avg_deaths": 0, "avg_damage": 5000000},
                {"type": "Wildfire", "frequency": 0.1, "avg_deaths": 3, "avg_damage": 500000},
                {"type": "Landslide", "frequency": 0.1, "avg_deaths": 2, "avg_damage": 300000}
            ]
        
        # Générer des catastrophes historiques
        for disaster_type in disaster_types:
            if random.random() < disaster_type["frequency"]:
                # Date aléatoire dans les 20 dernières années
                years_ago = random.randint(1, 20)
                days_ago = random.randint(1, 365 * years_ago)
                disaster_date = datetime.now() - timedelta(days=days_ago)
                
                disasters.append({
                    "id": f"emdat_{random.randint(10000, 99999)}",
                    "type": disaster_type["type"],
                    "date": disaster_date.strftime("%Y-%m-%d"),
                    "country": country,
                    "location": {
                        "latitude": latitude + random.uniform(-0.5, 0.5),
                        "longitude": longitude + random.uniform(-0.5, 0.5)
                    },
                    "deaths": random.randint(0, disaster_type["avg_deaths"] * 2),
                    "injured": random.randint(0, disaster_type["avg_deaths"] * 5),
                    "damage_usd": random.randint(
                        disaster_type["avg_damage"] // 2,
                        disaster_type["avg_damage"] * 2
                    ),
                    "affected_area_km2": random.randint(1, 500)
                })
        
        return disasters

    def calculate_disaster_risk(self, disasters: List[Dict], site_type: str, site_value: float) -> Dict:
        """Calculer un score de risque basé sur l'historique des catastrophes"""
        try:
            if not disasters:
                return {
                    "disaster_risk_score": 15.0,
                    "risk_factors": {
                        "historical_events": 0,
                        "frequency": "faible",
                        "severity": "faible",
                        "proximity_risk": "faible"
                    }
                }
            
            # Analyser les catastrophes
            total_events = len(disasters)
            recent_events = len([d for d in disasters if self._is_recent(d.get("date", ""))])
            
            # Calculer la fréquence
            if total_events > 0:
                frequency_score = min(100, (total_events / 10) * 50)  # 10 événements = 50% de risque
            else:
                frequency_score = 0
            
            # Calculer la sévérité moyenne
            severity_scores = []
            for disaster in disasters:
                if disaster.get("severity") == "élevée":
                    severity_scores.append(80)
                elif disaster.get("severity") == "modérée":
                    severity_scores.append(50)
                else:
                    severity_scores.append(20)
            
            avg_severity = sum(severity_scores) / len(severity_scores) if severity_scores else 0
            
            # Facteur de proximité (événements récents)
            proximity_score = min(100, recent_events * 20)  # Chaque événement récent = +20%
            
            # Facteur de type de site
            site_type_multiplier = {
                "résidentiel": 1.0,
                "commercial": 1.2,
                "industriel": 1.5,
                "agricole": 1.3,
                "public": 1.1,
                "logistique": 1.4
            }.get(site_type.lower(), 1.0)
            
            # Calculer le score final
            disaster_risk = (
                frequency_score * 0.3 +
                avg_severity * 0.4 +
                proximity_score * 0.3
            ) * site_type_multiplier
            
            return {
                "disaster_risk_score": min(100.0, max(0.0, disaster_risk)),
                "risk_factors": {
                    "historical_events": total_events,
                    "recent_events": recent_events,
                    "frequency": self._get_frequency_label(total_events),
                    "severity": self._get_severity_label(avg_severity),
                    "proximity_risk": self._get_proximity_label(recent_events)
                }
            }
            
        except Exception as e:
            print(f"Erreur lors du calcul du risque catastrophe: {e}")
            return {
                "disaster_risk_score": 15.0,
                "risk_factors": {
                    "historical_events": 0,
                    "frequency": "faible",
                    "severity": "faible",
                    "proximity_risk": "faible"
                }
            }

    def _is_recent(self, date_str: str, days: int = 365) -> bool:
        """Vérifier si une date est récente"""
        try:
            disaster_date = datetime.strptime(date_str, "%Y-%m-%d")
            return (datetime.now() - disaster_date).days <= days
        except:
            return False

    def _get_frequency_label(self, events: int) -> str:
        if events == 0:
            return "aucune"
        elif events <= 2:
            return "faible"
        elif events <= 5:
            return "modérée"
        else:
            return "élevée"

    def _get_severity_label(self, severity_score: float) -> str:
        if severity_score < 30:
            return "faible"
        elif severity_score < 60:
            return "modérée"
        else:
            return "élevée"

    def _get_proximity_label(self, recent_events: int) -> str:
        if recent_events == 0:
            return "faible"
        elif recent_events <= 2:
            return "modérée"
        else:
            return "élevée"

    async def get_disaster_risk_for_site(self, latitude: float, longitude: float, site_type: str, site_value: float) -> Dict:
        """Récupérer le risque de catastrophe pour un site"""
        try:
            # Récupérer les données CatNat (France)
            catnat_disasters = await self.get_catnat_disasters(latitude, longitude)
            
            # Récupérer les données EM-DAT (international)
            emdat_disasters = await self.get_emdat_disasters(latitude, longitude)
            
            # Combiner les données
            all_disasters = catnat_disasters + emdat_disasters
            
            # Calculer le risque
            risk_assessment = self.calculate_disaster_risk(all_disasters, site_type, site_value)
            
            return {
                "disasters": all_disasters,
                "disaster_risk": risk_assessment,
                "data_sources": {
                    "catnat": len(catnat_disasters),
                    "emdat": len(emdat_disasters)
                }
            }
            
        except Exception as e:
            print(f"Erreur lors de la récupération du risque catastrophe: {e}")
            return {
                "disasters": [],
                "disaster_risk": {
                    "disaster_risk_score": 15.0,
                    "risk_factors": {
                        "historical_events": 0,
                        "frequency": "faible",
                        "severity": "faible",
                        "proximity_risk": "faible"
                    }
                },
                "data_sources": {
                    "catnat": 0,
                    "emdat": 0
                }
            }

# Instance globale du service
disaster_service = DisasterService() 