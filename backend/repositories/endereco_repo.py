from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from database.models import Endereco


async def listar(db: AsyncSession, usuario_id: int) -> list[Endereco]:
    return list((await db.scalars(
        select(Endereco).where(Endereco.id_cliente == usuario_id)
        .order_by(Endereco.principal.desc(), Endereco.id)
    )).all())

async def buscar(db: AsyncSession, endereco_id: int, usuario_id: int) -> Endereco | None:
    return await db.scalar(
        select(Endereco).where(Endereco.id == endereco_id, Endereco.id_cliente == usuario_id)
    )

async def criar(db: AsyncSession, usuario_id: int, dados: dict) -> Endereco:
    dados = dados.copy()
    existentes = await listar(db, usuario_id)
    principal = dados.pop("principal", False) or len(existentes) == 0
    if principal: await _desmarcar(db, usuario_id)
    e = Endereco(id_cliente=usuario_id, principal=principal, **dados)
    db.add(e); await db.flush(); await db.refresh(e)
    return e

async def atualizar(db: AsyncSession, endereco_id: int, usuario_id: int, dados: dict) -> Endereco | None:
    dados = dados.copy()
    e = await buscar(db, endereco_id, usuario_id)
    if not e: return None
    principal = dados.pop("principal", False)
    if principal: await _desmarcar(db, usuario_id)
    for k, v in dados.items(): setattr(e, k, v)
    if principal: e.principal = True
    await db.flush(); await db.refresh(e)
    return e

async def remover(db: AsyncSession, endereco_id: int, usuario_id: int) -> tuple[bool, str]:
    existentes = await listar(db, usuario_id)
    if len(existentes) <= 1: return False, "Não é possível excluir o único endereço."
    e = await buscar(db, endereco_id, usuario_id)
    if not e: return False, "Endereço não encontrado."
    era_principal = e.principal
    await db.delete(e); await db.flush()
    if era_principal:
        restante = await db.scalar(select(Endereco).where(Endereco.id_cliente == usuario_id).limit(1))
        if restante: restante.principal = True; await db.flush()
    return True, "Endereço excluído."

async def definir_principal(db: AsyncSession, endereco_id: int, usuario_id: int) -> tuple[bool, str]:
    e = await buscar(db, endereco_id, usuario_id)
    if not e: return False, "Endereço não encontrado."
    await _desmarcar(db, usuario_id)
    e.principal = True; await db.flush()
    return True, "Endereço principal definido."

async def _desmarcar(db: AsyncSession, usuario_id: int) -> None:
    await db.execute(update(Endereco).where(Endereco.id_cliente == usuario_id).values(principal=False))