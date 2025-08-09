from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.insurance_contract import ContractStatus

class ContractBase(BaseModel):
    contract_number: str = Field(..., description="Numéro du contrat")
    site_id: int = Field(..., description="ID du site")
    premium_amount: float = Field(..., description="Montant de la prime en euros")
    coverage_amount: float = Field(..., description="Montant de couverture en euros")
    deductible: float = Field(default=0.0, description="Franchise en euros")
    start_date: datetime = Field(..., description="Date de début du contrat")
    end_date: datetime = Field(..., description="Date de fin du contrat")

class ContractCreate(ContractBase):
    pass

class ContractUpdate(BaseModel):
    contract_number: Optional[str] = None
    premium_amount: Optional[float] = None
    coverage_amount: Optional[float] = None
    deductible: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[ContractStatus] = None

class ContractResponse(ContractBase):
    id: int
    status: ContractStatus
    predicted_profitability: Optional[float] = None
    risk_assessment: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True 