from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.site import BuildingType

class SiteBase(BaseModel):
    name: str = Field(..., description="Nom du site")
    address: str = Field(..., description="Adresse complète")
    city: str = Field(..., description="Ville")
    postal_code: str = Field(..., description="Code postal")
    country: str = Field(default="France", description="Pays")
    latitude: float = Field(..., description="Latitude")
    longitude: float = Field(..., description="Longitude")
    building_type: BuildingType = Field(..., description="Type de bâtiment")
    building_value: float = Field(..., description="Valeur du bâtiment en euros")
    surface_area: Optional[float] = Field(None, description="Surface en m²")
    construction_year: Optional[int] = Field(None, description="Année de construction")
    notes: Optional[str] = Field(None, description="Notes additionnelles")

class SiteCreate(SiteBase):
    pass

class SiteUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    building_type: Optional[BuildingType] = None
    building_value: Optional[float] = None
    surface_area: Optional[float] = None
    construction_year: Optional[int] = None
    notes: Optional[str] = None

class SiteResponse(SiteBase):
    id: int
    risk_score: float = Field(..., description="Score de risque (0-100)")
    last_risk_update: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True 