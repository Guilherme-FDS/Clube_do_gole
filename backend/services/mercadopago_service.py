# services/mercadopago_service.py
"""
Integração com o Mercado Pago via API REST (Checkout Pro).

Fluxo:
  1. finalizar_compra cria a venda com status "pendente" e chama criar_preferencia()
  2. O cliente é redirecionado ao init_point (página de pagamento do MP)
  3. O MP notifica o webhook (/api/pagamentos/webhook) quando o pagamento muda
  4. O webhook consulta buscar_pagamento() e aprova/recusa a venda

Sem MP_ACCESS_TOKEN configurado, o sistema cai no modo dev: aprova na hora.
"""
import httpx
from config import get_settings

settings = get_settings()

API_BASE = "https://api.mercadopago.com"

# payment_type_id do MP → valores aceitos pelo CHECK constraint de pagamentos.metodo
MAPA_METODO = {
    "credit_card": "cartao_credito",
    "debit_card": "cartao_credito",
    "bank_transfer": "pix",       # PIX chega como bank_transfer
    "account_money": "pix",
    "ticket": "boleto",
}

MAPA_STATUS = {
    "approved": "aprovado",
    "rejected": "recusado",
    "cancelled": "recusado",
    "refunded": "estornado",
    "charged_back": "estornado",
    # pending / in_process / authorized → pendente
}


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {settings.mp_access_token}",
        "Content-Type": "application/json",
    }


async def criar_preferencia(venda_id: int, itens: list[dict], email_cliente: str | None) -> str:
    """Cria uma preferência de Checkout Pro e retorna a URL de pagamento (init_point)."""
    payload = {
        "items": [
            {
                "title": f"{i['nome_produto']} — plano {i['plano']}",
                "quantity": i["quantidade"],
                "unit_price": float(i["valor_total"]) / i["quantidade"],
                "currency_id": "BRL",
            }
            for i in itens
        ],
        "external_reference": str(venda_id),
        "notification_url": f"{settings.backend_public_url}/api/pagamentos/webhook",
        "back_urls": {
            "success": f"{settings.frontend_url}/meus-pedidos?pagamento=sucesso",
            "pending": f"{settings.frontend_url}/meus-pedidos?pagamento=pendente",
            "failure": f"{settings.frontend_url}/meus-pedidos?pagamento=falha",
        },
        "statement_descriptor": "CLUBE DO GOLE",
    }
    if email_cliente:
        payload["payer"] = {"email": email_cliente}

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(f"{API_BASE}/checkout/preferences", json=payload, headers=_headers())
        if not r.is_success:
            import logging
            logging.getLogger("clube_do_gole.mp").error("MP 400 body: %s", r.text)
        r.raise_for_status()
        data = r.json()

    # Credenciais de teste (TEST-...) usam sandbox_init_point; produção (APP_USR-...) usa init_point
    use_sandbox = "TEST" in settings.mp_access_token.upper() or not settings.mp_access_token.startswith("APP_USR")
    if use_sandbox:
        return data.get("sandbox_init_point") or data["init_point"]
    return data.get("init_point") or data.get("sandbox_init_point", "")


async def buscar_pagamento(payment_id: str) -> dict:
    """Consulta um pagamento no MP e devolve campos já normalizados para o nosso modelo."""
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(f"{API_BASE}/v1/payments/{payment_id}", headers=_headers())
        r.raise_for_status()
        data = r.json()

    return {
        "gateway_id": str(data["id"]),
        "external_reference": data.get("external_reference"),
        "status": MAPA_STATUS.get(data.get("status"), "pendente"),
        "metodo": MAPA_METODO.get(data.get("payment_type_id"), "outro"),
        "valor": data.get("transaction_amount"),
        "pago_em": data.get("date_approved"),
        "raw": data,
    }
