# routes/pagamentos.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.engine import get_db
from repositories import pagamento_repo
from utils.auth import admin_required

router = APIRouter(prefix="/api/pagamentos", tags=["pagamentos"])


@router.get("/admin", dependencies=[Depends(admin_required)])
async def listar_todos(db: AsyncSession = Depends(get_db)):
    pagamentos = await pagamento_repo.listar_todos(db)
    return [_serializar(p) for p in pagamentos]


@router.get("/admin/venda/{id_venda}", dependencies=[Depends(admin_required)])
async def por_venda(id_venda: int, db: AsyncSession = Depends(get_db)):
    pagamentos = await pagamento_repo.buscar_por_venda(db, id_venda)
    return [_serializar(p) for p in pagamentos]


def _serializar(p) -> dict:
    return {
        "id": p.id,
        "id_venda": p.id_venda,
        "id_assinatura": p.id_assinatura,
        "metodo": p.metodo,
        "status": p.status,
        "valor": float(p.valor),
        "gateway_id": p.gateway_id,
        "pago_em": p.pago_em.isoformat() if p.pago_em else None,
        "criado_em": p.criado_em.isoformat(),
    }