# routes/estoque.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from database.engine import get_db
from services import estoque_service
from utils.auth import admin_required

router = APIRouter(prefix="/api/estoque", tags=["estoque"])


class MovimentacaoIn(BaseModel):
    id_produto: int
    quantidade: int
    motivo: str = ""


@router.get("/admin", dependencies=[Depends(admin_required)])
async def listar(db: AsyncSession = Depends(get_db)):
    return await estoque_service.listar_movimentacoes(db)


@router.get("/admin/produto/{id_produto}", dependencies=[Depends(admin_required)])
async def por_produto(id_produto: int, db: AsyncSession = Depends(get_db)):
    return await estoque_service.listar_por_produto(db, id_produto)


@router.post("/admin/entrada", dependencies=[Depends(admin_required)])
async def entrada(body: MovimentacaoIn, db: AsyncSession = Depends(get_db)):
    try:
        return await estoque_service.entrada(db, body.id_produto, body.quantidade, body.motivo or "entrada manual")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/admin/saida", dependencies=[Depends(admin_required)])
async def saida(body: MovimentacaoIn, db: AsyncSession = Depends(get_db)):
    try:
        return await estoque_service.saida(db, body.id_produto, body.quantidade, body.motivo or "saida manual")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/admin/ajuste", dependencies=[Depends(admin_required)])
async def ajuste(body: MovimentacaoIn, db: AsyncSession = Depends(get_db)):
    try:
        return await estoque_service.ajuste(db, body.id_produto, body.quantidade, body.motivo or "ajuste manual")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
