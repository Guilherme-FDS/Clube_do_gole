from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.engine import get_db
from repositories import produto_repo
from schemas import ProdutoOut

router = APIRouter(prefix="/api/produtos", tags=["produtos"])

@router.get("/", response_model=list[ProdutoOut])
async def listar(db: AsyncSession = Depends(get_db)):
    return await produto_repo.listar(db)

@router.get("/gold", response_model=list[ProdutoOut])
async def gold(db: AsyncSession = Depends(get_db)):
    return await produto_repo.listar(db, tipo="gold")

@router.get("/premium", response_model=list[ProdutoOut])
async def premium(db: AsyncSession = Depends(get_db)):
    return await produto_repo.listar(db, tipo="premium")

@router.get("/{produto_id}", response_model=ProdutoOut)
async def detalhe(produto_id: int, db: AsyncSession = Depends(get_db)):
    p = await produto_repo.buscar(db, produto_id)
    if not p:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return p