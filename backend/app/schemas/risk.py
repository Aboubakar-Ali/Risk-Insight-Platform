from pydantic import BaseModel, Field
from typing import Optional, List

class RiskScore(BaseModel):
    overall_score: float = Field(..., description="Score de risque global (0-100)")
    flood_risk: float = Field(..., description="Risque d'inondation (0-100)")
    earthquake_risk: float = Field(..., description="Risque sismique (0-100)")
    storm_risk: float = Field(..., description="Risque de tempête (0-100)")
    wildfire_risk: float = Field(..., description="Risque d'incendie (0-100)")

class RiskAssessment(RiskScore):
    site_id: int = Field(..., description="ID du site")
    factors: List[str] = Field(default=[], description="Facteurs de risque identifiés")
    last_calculated: Optional[str] = None 