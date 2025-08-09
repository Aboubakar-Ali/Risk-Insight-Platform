from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime

class ContractAnalysisRequest(BaseModel):
    """Requête pour l'analyse de contrat"""
    site_id: int
    contract_id: int

class StrategicRecommendationsRequest(BaseModel):
    """Requête pour les recommandations stratégiques"""
    include_risk_analysis: bool = True
    include_cost_optimization: bool = True
    include_growth_opportunities: bool = True

class RiskMitigationRequest(BaseModel):
    """Requête pour l'analyse de mitigation des risques"""
    site_id: int
    include_cost_estimation: bool = True
    include_priority_ranking: bool = True

class AIAnalysis(BaseModel):
    """Analyse IA"""
    recommendation: str
    score: int
    confidence: float

class ContractAnalysis(BaseModel):
    """Analyse de contrat"""
    ai_analysis: Dict[str, Any]

class ContractAnalysisResponse(BaseModel):
    """Réponse d'analyse de contrat"""
    success: bool
    analysis: Dict[str, Any]
    site_data: Dict[str, Any]
    contract_data: Dict[str, Any]
    risk_data: Dict[str, Any]

class StrategicRecommendations(BaseModel):
    """Recommandations stratégiques"""
    analysis_type: str
    ai_analysis: AIAnalysis
    strategic_positioning: Dict[str, Any]

class StrategicRecommendationsResponse(BaseModel):
    """Réponse de recommandations stratégiques"""
    success: bool
    recommendations: Dict[str, Any]
    portfolio_data: Dict[str, Any]

class RiskMitigation(BaseModel):
    """Mitigation des risques"""
    mitigation_analysis: Dict[str, Any]

class RiskMitigationResponse(BaseModel):
    """Réponse de mitigation des risques"""
    success: bool
    mitigation: Dict[str, Any]
    site_data: Dict[str, Any]
    risk_data: Dict[str, Any]

class AIAgentHealth(BaseModel):
    """État de santé de l'agent IA"""
    status: str
    ai_available: bool
    message: str
