from fastapi import APIRouter
from .sites import router as sites_router
from .contracts import router as contracts_router
from .weather import router as weather_router
from .risk import router as risk_router
from .disasters import router as disasters_router
from .vulnerability import router as vulnerability_router
from .comprehensive_risk import router as comprehensive_risk_router
from .ai_agent import router as ai_agent_router

api_router = APIRouter()

# Inclure les sous-routers
api_router.include_router(sites_router, prefix="/sites", tags=["sites"])
api_router.include_router(contracts_router, prefix="/contracts", tags=["contracts"])
api_router.include_router(weather_router, prefix="/weather", tags=["weather"])
api_router.include_router(risk_router, prefix="/risk", tags=["risk"])
api_router.include_router(disasters_router, prefix="/disasters", tags=["disasters"])
api_router.include_router(vulnerability_router, prefix="/vulnerability", tags=["vulnerability"])
api_router.include_router(comprehensive_risk_router, prefix="/comprehensive-risk", tags=["comprehensive-risk"])
api_router.include_router(ai_agent_router, prefix="/ai-agent", tags=["ai-agent"]) 