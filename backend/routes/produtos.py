# routes/produtos.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.engine import get_db
from repositories import produto_repo, plano_repo
from schemas import ProdutoOut, PlanoOut, ProdutoComPlanosOut
from services.plano_service import enriquecer_plano

router = APIRouter(prefix="/api/produtos", tags=["produtos"])


@router.get("/", response_model=list[ProdutoOut])
async def listar(db: AsyncSession = Depends(get_db)):
    return await produto_repo.listar(db)


@router.get("/{produto_id}", response_model=ProdutoComPlanosOut)
async def detalhe(produto_id: int, db: AsyncSession = Depends(get_db)):
    p = await produto_repo.buscar(db, produto_id)
    if not p:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    planos = await plano_repo.listar_por_produto(db, produto_id)
    return {
        "id": p.id,
        "nome": p.nome,
        "descricao": p.descricao,
        "ativo": p.ativo,
        "planos": [enriquecer_plano(pl) for pl in planos],
    }


@router.get("/{produto_id}/planos", response_model=list[PlanoOut])
async def planos_do_produto(produto_id: int, db: AsyncSession = Depends(get_db)):
    p = await produto_repo.buscar(db, produto_id)
    if not p:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    planos = await plano_repo.listar_por_produto(db, produto_id)
    return [enriquecer_plano(pl) for pl in planos]