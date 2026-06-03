# routes/assinaturas.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.engine import get_db
from services import assinatura_service
from utils.auth import login_required, admin_required

router = APIRouter(prefix="/api/assinaturas", tags=["assinaturas"])


@router.get("/minhas")
async def minhas_assinaturas(
    payload: dict = Depends(login_required),
    db: AsyncSession = Depends(get_db),
):
    return await assinatura_service.listar_por_cliente(db, payload["id"])


@router.get("/admin", dependencies=[Depends(admin_required)])
async def listar_todas(db: AsyncSession = Depends(get_db)):
    return await assinatura_service.listar_todas(db)


@router.patch("/admin/{id_assinatura}/cancelar", dependencies=[Depends(admin_required)])
async def cancelar(id_assinatura: int, db: AsyncSession = Depends(get_db)):
    await assinatura_service.cancelar_assinatura(db, id_assinatura)
    return {"message": "Assinatura cancelada."}