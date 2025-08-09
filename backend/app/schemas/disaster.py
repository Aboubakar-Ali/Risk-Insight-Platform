from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.natural_disaster import DisasterType

class NaturalDisasterResponse(BaseModel):
    id: int
    latitude: float = Field(..., description="Latitude")
    longitude: float = Field(..., description="Longitude")
    region: Optional[str] = Field(None, description="Région")
    country: str = Field(default="France", description="Pays")
    disaster_type: DisasterType = Field(..., description="Type de catastrophe")
    magnitude: Optional[float] = Field(None, description="Magnitude/intensité")
    description: Optional[str] = Field(None, description="Description")
    start_date: datetime = Field(..., description="Date de début")
    end_date: Optional[datetime] = Field(None, description="Date de fin")
    damage_estimate: Optional[float] = Field(None, description="Estimation des dégâts en euros")
    affected_area: Optional[float] = Field(None, description="Zone affectée en km²")
    casualties: Optional[int] = Field(None, description="Nombre de victimes")
    data_source: Optional[str] = Field(None, description="Source des données")
    external_id: Optional[str] = Field(None, description="ID externe")
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True 