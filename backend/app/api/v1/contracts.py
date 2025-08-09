from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.contract import ContractCreate, ContractUpdate, ContractResponse
from app.models.insurance_contract import InsuranceContract

router = APIRouter()

@router.get("/", response_model=List[ContractResponse])
async def get_contracts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Récupérer tous les contrats"""
    contracts = db.query(InsuranceContract).offset(skip).limit(limit).all()
    return contracts

@router.get("/{contract_id}", response_model=ContractResponse)
async def get_contract(contract_id: int, db: Session = Depends(get_db)):
    """Récupérer un contrat par son ID"""
    contract = db.query(InsuranceContract).filter(InsuranceContract.id == contract_id).first()
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrat non trouvé"
        )
    return contract

@router.post("/", response_model=ContractResponse)
async def create_contract(contract: ContractCreate, db: Session = Depends(get_db)):
    """Créer un nouveau contrat"""
    db_contract = InsuranceContract(**contract.dict())
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract 