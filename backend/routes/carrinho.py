from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import get_db
from repositories import carrinho_repo
from services import carrinho_service, venda_service, cupom_service
from schemas import AdicionarItemIn, AtualizarQuantidadeIn, FinalizarIn, CarrinhoOut
from utils.auth import login_required

router = APIRouter(prefix="/api/carrinho", tags=["carrinho"])


@router.get("/", response_model=CarrinhoOut)
async def ver(payload: dict = Depends(login_required), db: AsyncSession = Depends(get_db)):
    uid = payload["id"]
    itens = await carrinho_repo.itens_ativos(db, uid)
    total = await carrinho_repo.total(db, uid)
    return CarrinhoOut(itens=itens, total=total)


@router.get("/contador")
async def contador(payload: dict = Depends(login_required), db: AsyncSession = Depends(get_db)):
    return {"count": await carrinho_repo.contador(db, payload["id"])}


@router.post("/adicionar")
async def adicionar(body: AdicionarItemIn, payload: dict = Depends(login_required), db: AsyncSession = Depends(get_db)):
    sucesso, mensagem = await carrinho_service.adicionar(db, payload["id"], body.produto_id, body.plano_id, body.quantidade)
    if not sucesso:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=mensagem)
    return {"message": mensagem, "count": await carrinho_repo.contador(db, payload["id"])}


@router.post("/remover")
async def remover(body: dict, payload: dict = Depends(login_required), db: AsyncSession = Depends(get_db)):
    ids = body.get("ids", [])
    if not ids:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum item informado.")
    removidos = await carrinho_repo.remover_itens(db, payload["id"], ids)
    return {"removidos": removidos, "total": await carrinho_repo.total(db, payload["id"])}


@router.post("/quantidade")
async def atualizar_quantidade(body: AtualizarQuantidadeIn, payload: dict = Depends(login_required), db: AsyncSession = Depends(get_db)):
    sucesso, msg, novo_valor, total = await carrinho_service.atualizar_quantidade(db, payload["id"], body.item_id, body.quantidade)
    if not sucesso:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
    return {"message": msg, "novo_total_item": novo_valor, "total_carrinho": total}


@router.post("/finalizar")
async def finalizar(body: FinalizarIn, payload: dict = Depends(login_required), db: AsyncSession = Depends(get_db)):
    if body.cupom:
        valido, msg, _ = await cupom_service.validar(db, body.cupom)
        if not valido:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
    sucesso, mensagem, checkout_url = await venda_service.finalizar_compra(
        db, payload["id"], body.ids, body.cupom, body.desconto_cupom,
        email_cliente=payload.get("email"),
    )
    if not sucesso:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=mensagem)
    return {"message": mensagem, "checkout_url": checkout_url}


@router.get("/meus_pedidos")
async def meus_pedidos(payload: dict = Depends(login_required), db: AsyncSession = Depends(get_db)):
    return await venda_service.pedidos_do_usuario(db, payload["id"])