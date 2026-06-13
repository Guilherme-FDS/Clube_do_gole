# routes/pagamentos.py
import hashlib
import hmac
import logging
from datetime import datetime
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from database.engine import get_db
from repositories import pagamento_repo
from services import mercadopago_service, venda_service
from utils.auth import admin_required
from config import get_settings

router = APIRouter(prefix="/api/pagamentos", tags=["pagamentos"])
settings = get_settings()
logger = logging.getLogger("clube_do_gole.webhook")


def _verificar_assinatura_mp(request: Request, body_bytes: bytes) -> bool:
    """Valida o header x-signature enviado pelo Mercado Pago.
    Retorna True se não houver header (ambientes de teste sem assinatura)."""
    signature_header = request.headers.get("x-signature")
    if not signature_header or not settings.mp_access_token:
        return True  # sem header = ambiente de teste, deixar passar
    try:
        parts = dict(p.split("=", 1) for p in signature_header.split(",") if "=" in p)
        ts = parts.get("ts", "")
        v1 = parts.get("v1", "")
        data_id = request.query_params.get("data.id") or request.query_params.get("id", "")
        manifest = f"id:{data_id};request-id:{request.headers.get('x-request-id','')};ts:{ts};"
        expected = hmac.new(
            settings.mp_access_token.encode(),
            manifest.encode(),
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(expected, v1)
    except Exception:
        return False


@router.post("/webhook")
async def webhook_mercadopago(request: Request, db: AsyncSession = Depends(get_db)):
    """Notificação do Mercado Pago. Chega como query params (?topic=payment&id=X)
    ou como JSON {"type": "payment", "data": {"id": X}}. Sempre responde 200
    para o MP não reenviar infinitamente."""
    if not settings.mp_configured:
        return {"ok": False}

    body_bytes = await request.body()
    if not _verificar_assinatura_mp(request, body_bytes):
        logger.warning("Webhook MP rejeitado: assinatura inválida")
        return {"ok": False}

    payment_id = request.query_params.get("id") or request.query_params.get("data.id")
    topic = request.query_params.get("topic") or request.query_params.get("type")
    if not payment_id:
        try:
            body = await request.json()
            topic = body.get("type") or body.get("topic")
            payment_id = (body.get("data") or {}).get("id")
        except Exception:
            return {"ok": False}

    if topic != "payment" or not payment_id:
        return {"ok": True}  # outros eventos (merchant_order etc.) são ignorados

    try:
        info = await mercadopago_service.buscar_pagamento(str(payment_id))
    except Exception:
        return {"ok": False}

    venda_id = info.get("external_reference")
    if not venda_id:
        return {"ok": True}

    pagamentos = await pagamento_repo.buscar_por_venda(db, int(venda_id))
    if pagamentos:
        dados = {
            "status": info["status"],
            "metodo": info["metodo"],
            "gateway_id": info["gateway_id"],
        }
        if info["pago_em"]:
            dados["pago_em"] = datetime.fromisoformat(info["pago_em"].replace("Z", "+00:00")).replace(tzinfo=None)
        await pagamento_repo.atualizar_gateway(db, pagamentos[0].id, dados)

    if info["status"] == "aprovado":
        await venda_service.aprovar_venda(db, int(venda_id))

    return {"ok": True}


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