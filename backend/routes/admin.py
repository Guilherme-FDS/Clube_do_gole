# routes/admin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.engine import get_db
from repositories import auth_repo, produto_repo, endereco_repo, venda_repo, cupom_repo, plano_repo
from schemas import ProdutoIn, ProdutoOut, CupomIn, CupomOut, ClienteAdminOut, EnderecoOut, PlanoIn, PlanoOut
from utils.auth import admin_required
from services.plano_service import enriquecer_plano

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/dashboard")
async def dashboard(_: dict = Depends(admin_required), db: AsyncSession = Depends(get_db)):
    return await venda_repo.dashboard(db)


@router.get("/vendas/{venda_id}")
async def detalhe_venda(venda_id: int, _: dict = Depends(admin_required), db: AsyncSession = Depends(get_db)):
    venda = await venda_repo.detalhe_admin(db, venda_id)
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada.")
    return venda


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
    return {
        "cliente": ClienteAdminOut.model_validate(cliente),
        "enderecos": [EnderecoOut.model_validate(e) for e in enderecos],
        "pedidos": pedidos,
    }


# ── Produtos ───────────────────────────────────────────────────────────────────

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


@router.patch("/produtos/{produto_id}/status", response_model=ProdutoOut)
async def status_produto(produto_id: int, body: dict, _: dict = Depends(admin_required), db: AsyncSession = Depends(get_db)):
    p = await produto_repo.atualizar(db, produto_id, {"ativo": body.get("ativo", True)})
    if not p:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return p


# ── Planos ─────────────────────────────────────────────────────────────────────

@router.get("/produtos/{produto_id}/planos", response_model=list[PlanoOut])
async def listar_planos(produto_id: int, _: dict = Depends(admin_required), db: AsyncSession = Depends(get_db)):
    return [enriquecer_plano(p) for p in await plano_repo.listar_por_produto(db, produto_id, apenas_ativos=False)]


@router.post("/produtos/{produto_id}/planos", response_model=PlanoOut, status_code=201)
async def criar_plano(produto_id: int, body: PlanoIn, _: dict = Depends(admin_required), db: AsyncSession = Depends(get_db)):
    p = await produto_repo.buscar(db, produto_id)
    if not p:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    dados = body.model_dump()
    dados["id_produto"] = produto_id
    return enriquecer_plano(await plano_repo.criar(db, dados))


@router.put("/planos/{plano_id}", response_model=PlanoOut)
async def editar_plano(plano_id: int, body: PlanoIn, _: dict = Depends(admin_required), db: AsyncSession = Depends(get_db)):
    p = await plano_repo.atualizar(db, plano_id, body.model_dump())
    if not p:
        raise HTTPException(status_code=404, detail="Plano não encontrado.")
    return enriquecer_plano(p)


@router.delete("/planos/{plano_id}", status_code=204)
async def deletar_plano(plano_id: int, _: dict = Depends(admin_required), db: AsyncSession = Depends(get_db)):
    if not await plano_repo.remover(db, plano_id):
        raise HTTPException(status_code=404, detail="Plano não encontrado.")


@router.patch("/planos/{plano_id}/status", response_model=PlanoOut)
async def status_plano(plano_id: int, body: dict, _: dict = Depends(admin_required), db: AsyncSession = Depends(get_db)):
    p = await plano_repo.atualizar(db, plano_id, {"ativo": body.get("ativo", True)})
    if not p:
        raise HTTPException(status_code=404, detail="Plano não encontrado.")
    return enriquecer_plano(p)


# ── Cupons ─────────────────────────────────────────────────────────────────────

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