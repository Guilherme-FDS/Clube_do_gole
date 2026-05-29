from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.engine import get_db
from repositories import auth_repo, produto_repo, endereco_repo, venda_repo, cupom_repo
from schemas import ProdutoIn, ProdutoOut, CupomIn, CupomOut, ClienteAdminOut, EnderecoOut
from utils.auth import admin_required

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/dashboard")
async def dashboard(_: dict = Depends(admin_required), db: AsyncSession = Depends(get_db)):
    return await venda_repo.dashboard(db)

@router.get("/clientes", response_model=list[ClienteAdminOut])
async def listar_clientes(_: dict = Depends(admin_required), db: AsyncSession = Depends(get_db)):
    return await auth_repo.listar_clientes(db)

@router.get("/clientes/{cliente_id}")
async def detalhe_cliente(cliente_id: int, _: dict = Depends(admin_required), db: AsyncSession = Depends(get_db)):
    cliente = await auth_repo.buscar_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    enderecos = await endereco_repo.listar(db, cliente_id)
    pedidos = await venda_repo.pedidos_do_cliente_admin(db, cliente_id)
    return {"cliente": ClienteAdminOut.model_validate(cliente), "enderecos": [EnderecoOut.model_validate(e) for e in enderecos], "pedidos": pedidos}

@router.get("/produtos", response_model=list[ProdutoOut])
async def listar_produtos(_: dict = Depends(admin_required), db: AsyncSession = Depends(get_db)):
    return await produto_repo.listar_admin(db)

@router.post("/produtos", response_model=ProdutoOut, status_code=201)
async def criar_produto(body: ProdutoIn, _: dict = Depends(admin_required), db: AsyncSession = Depends(get_db)):
    return await produto_repo.criar(db, body.model_dump())

@router.put("/produtos/{produto_id}", response_model=ProdutoOut)
async def editar_produto(produto_id: int, body: ProdutoIn, _: dict = Depends(admin_required), db: AsyncSession = Depends(get_db)):
    p = await produto_repo.atualizar(db, produto_id, body.model_dump())
    if not p:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return p

@router.delete("/produtos/{produto_id}", status_code=204)
async def deletar_produto(produto_id: int, _: dict = Depends(admin_required), db: AsyncSession = Depends(get_db)):
    if not await produto_repo.remover(db, produto_id):
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

@router.get("/cupons", response_model=list[CupomOut])
async def listar_cupons(_: dict = Depends(admin_required), db: AsyncSession = Depends(get_db)):
    return await cupom_repo.listar(db)

@router.get("/cupons/{cupom_id}", response_model=CupomOut)
async def detalhe_cupom(cupom_id: int, _: dict = Depends(admin_required), db: AsyncSession = Depends(get_db)):
    c = await cupom_repo.buscar_por_id(db, cupom_id)
    if not c:
        raise HTTPException(status_code=404, detail="Cupom não encontrado.")
    return c

@router.post("/cupons", response_model=CupomOut, status_code=201)
async def criar_cupom(body: CupomIn, _: dict = Depends(admin_required), db: AsyncSession = Depends(get_db)):
    dados = body.model_dump()
    dados["usos_restantes"] = dados["usos_maximos"]
    return await cupom_repo.criar(db, dados)

@router.put("/cupons/{cupom_id}", response_model=CupomOut)
async def editar_cupom(cupom_id: int, body: CupomIn, _: dict = Depends(admin_required), db: AsyncSession = Depends(get_db)):
    atual = await cupom_repo.buscar_por_id(db, cupom_id)
    if not atual:
        raise HTTPException(status_code=404, detail="Cupom não encontrado.")
    dados = body.model_dump()
    dados["usos_restantes"] = max(0, dados["usos_maximos"] - (atual.usos_maximos - atual.usos_restantes))
    return await cupom_repo.atualizar(db, cupom_id, dados)

@router.delete("/cupons/{cupom_id}", status_code=204)
async def deletar_cupom(cupom_id: int, _: dict = Depends(admin_required), db: AsyncSession = Depends(get_db)):
    if not await cupom_repo.remover(db, cupom_id):
        raise HTTPException(status_code=404, detail="Cupom não encontrado.")

@router.patch("/cupons/{cupom_id}/status", response_model=CupomOut)
async def status_cupom(cupom_id: int, body: dict, _: dict = Depends(admin_required), db: AsyncSession = Depends(get_db)):
    if body.get("status") not in ("ativo", "inativo"):
        raise HTTPException(status_code=422, detail="Status inválido.")
    c = await cupom_repo.atualizar(db, cupom_id, {"status": body["status"]})
    if not c:
        raise HTTPException(status_code=404, detail="Cupom não encontrado.")
    return c