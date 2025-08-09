from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WeatherDataResponse(BaseModel):
    id: int
    site_id: int
    temperature: Optional[float] = Field(None, description="Température en °C")
    humidity: Optional[float] = Field(None, description="Humidité en %")
    pressure: Optional[float] = Field(None, description="Pression en hPa")
    wind_speed: Optional[float] = Field(None, description="Vitesse du vent en m/s")
    wind_direction: Optional[float] = Field(None, description="Direction du vent en degrés")
    precipitation: Optional[float] = Field(None, description="Précipitations en mm")
    weather_condition: Optional[str] = Field(None, description="Condition météo")
    weather_description: Optional[str] = Field(None, description="Description météo")
    recorded_at: datetime
    data_source: str = Field(default="openweathermap", description="Source des données")
    
    class Config:
        from_attributes = True 