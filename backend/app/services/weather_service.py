import httpx
import asyncio
from typing import Dict, Optional
from fastapi import HTTPException
import os

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
        # Vérifier si la clé API est configurée
        if not self.api_key or self.api_key == "your_openweather_api_key_here":
            print("⚠️  OPENWEATHER_API_KEY non configurée - Utilisation des données par défaut")
            self.api_key = None
    
    async def get_current_weather(self, latitude: float, longitude: float) -> Dict:
        """Récupérer les conditions météo actuelles"""
        # Si pas de clé API, retourner des données par défaut
        if not self.api_key:
            return self._get_default_weather_data(latitude, longitude)
        
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/weather"
                params = {
                    "lat": latitude,
                    "lon": longitude,
                    "appid": self.api_key,
                    "units": "metric",  # Température en Celsius
                    "lang": "fr"
                }
                
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                return response.json()
                
        except httpx.HTTPStatusError as e:
            print(f"⚠️  Erreur API OpenWeatherMap: {e.response.status_code} - Utilisation des données par défaut")
            return self._get_default_weather_data(latitude, longitude)
        except Exception as e:
            print(f"⚠️  Erreur lors de la récupération météo: {str(e)} - Utilisation des données par défaut")
            return self._get_default_weather_data(latitude, longitude)
    
    def _get_default_weather_data(self, latitude: float, longitude: float) -> Dict:
        """Générer des données météo par défaut"""
        import random
        
        # Données météo réalistes basées sur la saison et la localisation
        temp = random.uniform(10, 25)  # Température entre 10-25°C
        humidity = random.uniform(40, 80)  # Humidité entre 40-80%
        wind_speed = random.uniform(0, 15)  # Vent entre 0-15 m/s
        
        conditions = random.choice([
            "ciel dégagé", "nuageux", "pluie légère", "brouillard", "partiellement nuageux"
        ])
        
        return {
            "main": {
                "temp": round(temp, 1),
                "humidity": round(humidity)
            },
            "wind": {
                "speed": round(wind_speed, 1)
            },
            "weather": [{
                "main": "Clouds",
                "description": conditions
            }],
            "rain": {"1h": 0},
            "snow": {"1h": 0}
        }
    
    def calculate_weather_risk(self, weather_data: Dict) -> float:
        """Calculer un score de risque basé sur les conditions météo"""
        try:
            # Extraire les données météo
            temp = weather_data.get("main", {}).get("temp", 20)
            humidity = weather_data.get("main", {}).get("humidity", 50)
            wind_speed = weather_data.get("wind", {}).get("speed", 0)
            rain_1h = weather_data.get("rain", {}).get("1h", 0)
            snow_1h = weather_data.get("snow", {}).get("1h", 0)
            
            # Identifier le type de temps principal
            weather_main = weather_data.get("weather", [{}])[0].get("main", "").lower()
            weather_description = weather_data.get("weather", [{}])[0].get("description", "").lower()
            
            risk_score = 0.0
            
            # Facteurs de risque météo
            risk_factors = {
                # Température extrême
                "temp_extreme": abs(temp - 20) / 30,  # Écart par rapport à 20°C
                
                # Humidité élevée (risque d'inondation)
                "humidity_risk": max(0, (humidity - 70) / 30),
                
                # Vent fort (risque de tempête)
                "wind_risk": min(1.0, wind_speed / 20),  # 20 m/s = 100% risque
                
                # Précipitations (risque d'inondation)
                "rain_risk": min(1.0, rain_1h / 10),  # 10mm/h = 100% risque
                
                # Neige (risque structurel)
                "snow_risk": min(1.0, snow_1h / 5),  # 5mm/h = 100% risque
                
                # Conditions météo spécifiques
                "weather_conditions": 0.0
            }
            
            # Évaluer les conditions météo spécifiques
            if any(keyword in weather_description for keyword in ["orage", "thunderstorm", "storm"]):
                risk_factors["weather_conditions"] = 0.8
            elif any(keyword in weather_description for keyword in ["pluie", "rain", "drizzle"]):
                risk_factors["weather_conditions"] = 0.4
            elif any(keyword in weather_description for keyword in ["neige", "snow"]):
                risk_factors["weather_conditions"] = 0.6
            elif any(keyword in weather_description for keyword in ["brouillard", "fog", "mist"]):
                risk_factors["weather_conditions"] = 0.2
            
            # Calculer le score de risque global (0-100)
            weather_risk = (
                risk_factors["temp_extreme"] * 10 +
                risk_factors["humidity_risk"] * 15 +
                risk_factors["wind_risk"] * 25 +
                risk_factors["rain_risk"] * 20 +
                risk_factors["snow_risk"] * 15 +
                risk_factors["weather_conditions"] * 15
            )
            
            return min(100.0, max(0.0, weather_risk))
            
        except Exception as e:
            print(f"Erreur lors du calcul du risque météo: {e}")
            return 25.0  # Risque par défaut modéré
    
    async def get_weather_risk_for_site(self, latitude: float, longitude: float) -> Dict:
        """Récupérer le risque météo pour un site"""
        try:
            weather_data = await self.get_current_weather(latitude, longitude)
            risk_score = self.calculate_weather_risk(weather_data)
            
            return {
                "weather_data": weather_data,
                "risk_score": risk_score,
                "risk_factors": {
                    "temperature": weather_data.get("main", {}).get("temp"),
                    "humidity": weather_data.get("main", {}).get("humidity"),
                    "wind_speed": weather_data.get("wind", {}).get("speed"),
                    "conditions": weather_data.get("weather", [{}])[0].get("description")
                }
            }
            
        except Exception as e:
            print(f"Erreur lors de la récupération du risque météo: {e}")
            return {
                "weather_data": None,
                "risk_score": 25.0,
                "risk_factors": {
                    "temperature": None,
                    "humidity": None,
                    "wind_speed": None,
                    "conditions": "Données non disponibles"
                }
            }

# Instance globale du service
weather_service = WeatherService() 