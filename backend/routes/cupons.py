from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.engine import get_db
from services import cupom_service
from schemas import ValidarCupomIn, ValidarCupomOut

router = APIRouter(prefix="/api/cupons", tags=["cupons"])

@router.post("/validar", response_model=ValidarCupomOut)
async def validar(body: ValidarCupomIn, db: AsyncSession = Depends(get_db)):
    valido, mensagem, desconto = await cupom_service.validar(db, body.codigo.strip().upper())
    return ValidarCupomOut(valido=valido, mensagem=mensagem, desconto=desconto)