# services/assinatura_service.py
from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from repositories import assinatura_repo


CICLOS_PLANO = {
    "mensal": 30,
    "semestral": 180,
    "anual": 365,
}


async def criar_assinatura(
    db: AsyncSession,
    id_cliente: int,
    id_venda: int,
    id_produto: int | None,
    plano: str,
) -> dict:
    hoje = date.today()
    dias = CICLOS_PLANO.get(plano, 30)

    assinatura = await assinatura_repo.criar(db, {
        "id_cliente": id_cliente,
        "id_venda_origem": id_venda,
        "id_produto": id_produto,
        "plano": plano,
        "status": "ativa",
        "data_inicio": hoje,
        "proximo_ciclo": hoje + timedelta(days=dias),
    })

    return {"id_assinatura": assinatura.id, "plano": plano, "data_inicio": hoje.isoformat()}


async def cancelar_assinatura(db: AsyncSession, id_assinatura: int) -> None:
    await assinatura_repo.atualizar_status(db, id_assinatura, "cancelada")


async def listar_por_cliente(db: AsyncSession, id_cliente: int) -> list[dict]:
    assinaturas = await assinatura_repo.buscar_por_cliente(db, id_cliente)
    return [_serializar(a) for a in assinaturas]


async def listar_todas(db: AsyncSession) -> list[dict]:
    assinaturas = await assinatura_repo.listar_todas(db)
    return [_serializar(a) for a in assinaturas]


def _serializar(a) -> dict:
    return {
        "id": a.id,
        "id_cliente": a.id_cliente,
        "id_produto": a.id_produto,
        "plano": a.plano,
        "status": a.status,
        "data_inicio": a.data_inicio.isoformat() if a.data_inicio else None,
        "data_fim": a.data_fim.isoformat() if a.data_fim else None,
        "proximo_ciclo": a.proximo_ciclo.isoformat() if a.proximo_ciclo else None,
        "criado_em": a.criado_em.isoformat(),
    }

async def atualizar_status(db: AsyncSession, id_assinatura: int, status: str) -> None:
    await assinatura_repo.atualizar_status(db, id_assinatura, status)