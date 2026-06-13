# services/venda_service.py
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from repositories import venda_repo, carrinho_repo, produto_repo, cupom_repo, pagamento_repo
from services.assinatura_service import criar_assinatura
import asyncio
import logging
from services import mercadopago_service
from utils.email import send_pedido_confirmado, send_pagamento_aprovado
from config import get_settings

logger = logging.getLogger("clube_do_gole.venda")

settings = get_settings()


async def finalizar_compra(
    db: AsyncSession,
    usuario_id: int,
    ids_itens: list[int],
    codigo_cupom: str = "",
    desconto_cupom: float = 0.0,
    email_cliente: str | None = None,
) -> tuple[bool, str, str | None]:
    """
    Cria a venda e inicia o pagamento.

    Com Mercado Pago configurado: venda nasce "pendente" e retorna a URL de
    checkout (init_point) — assinatura só é ativada quando o webhook aprovar.
    Sem MP (modo dev): aprova tudo na hora, como antes.
    """
    itens = await carrinho_repo.buscar_por_ids(db, usuario_id, ids_itens)
    if not itens:
        return False, "Nenhum item válido para finalizar.", None

    valor_original_total = Decimal("0")
    valor_final_total    = Decimal("0")
    itens_venda          = []

    for item in itens:
        valor_unitario = Decimal(str(item.valor_unitario))
        quantidade     = item.quantidade
        plano          = item.plano
        mult           = settings.multiplicadores_plano.get(plano, 1)
        desc_plano     = Decimal(str(settings.descontos_plano.get(plano, 0)))

        valor_original   = valor_unitario * mult * quantidade
        valor_apos_plano = valor_original * (1 - desc_plano)
        valor_final      = max(Decimal("0"), valor_apos_plano * (1 - Decimal(str(desconto_cupom)) / 100))

        valor_original_total += valor_original
        valor_final_total    += valor_final

        itens_venda.append({
            "id_produto":     item.id_produto,
            "nome_produto":   item.nome_produto,
            "plano":          plano,
            "quantidade":     quantidade,
            "valor_unitario": round(valor_unitario * mult, 2),
            "valor_total":    round(valor_final, 2),
        })

        await produto_repo.decrementar_estoque(db, item.id_produto, quantidade)

    desconto_total = (
        (valor_original_total - valor_final_total) / valor_original_total * 100
        if valor_original_total else Decimal("0")
    )

    usar_mp = settings.mp_configured

    venda = await venda_repo.criar(db, {
        "id_usuario":        usuario_id,
        "status":            "pendente" if usar_mp else "pago",
        "valor_original":    round(valor_original_total, 2),
        "valor_desconto":    round(valor_original_total - valor_final_total, 2),
        "valor_total":       round(valor_final_total, 2),
        "desconto_aplicado": round(desconto_total, 2),
        "cupom_aplicado":    codigo_cupom or None,
    }, itens_venda)

    await pagamento_repo.criar(db, {
        "id_venda": venda.id,
        "metodo":   "outro",
        "status":   "pendente" if usar_mp else "aprovado",
        "valor":    round(valor_final_total, 2),
    })

    await carrinho_repo.finalizar_itens(db, usuario_id, ids_itens)

    # Email de pedido recebido (não bloqueia resposta)
    if email_cliente:
        asyncio.create_task(send_pedido_confirmado(
            email_cliente,
            nome=email_cliente.split("@")[0],
            venda_id=venda.id,
            valor_total=float(valor_final_total),
            itens=itens_venda,
        ))

    if not usar_mp:
        # Modo dev sem gateway: aprova imediatamente
        await aprovar_venda(db, venda.id)
        return True, f"{len(itens)} item(ns) finalizado(s) com sucesso!", None

    try:
        checkout_url = await mercadopago_service.criar_preferencia(
            venda.id, itens_venda, email_cliente
        )
    except Exception as e:
        logger.exception(f"Erro ao criar preferência MP para venda #{venda.id}: {e}")
        return False, "Erro ao iniciar pagamento no Mercado Pago. Tente novamente.", None

    return True, "Redirecionando para o pagamento...", checkout_url


async def aprovar_venda(db: AsyncSession, venda_id: int) -> None:
    """Efetiva a venda após pagamento aprovado: ativa assinaturas e consome cupom.

    Idempotente — se a venda já está paga, não faz nada (webhooks repetem)."""
    venda = await venda_repo.buscar(db, venda_id)
    if not venda or venda.status == "pago":
        return

    venda.status = "pago"

    for item in venda.itens:
        await criar_assinatura(
            db,
            id_cliente=venda.id_usuario,
            id_venda=venda.id,
            id_produto=item.id_produto,
            plano=item.plano,
        )

    if venda.cupom_aplicado:
        await cupom_repo.consumir_atomico(db, venda.cupom_aplicado)

    # Email de pagamento aprovado
    if venda.cliente and venda.itens:
        plano_principal = venda.itens[0].plano
        asyncio.create_task(send_pagamento_aprovado(
            venda.cliente.email,
            nome=venda.cliente.nome,
            venda_id=venda.id,
            valor_total=float(venda.valor_total),
            plano=plano_principal,
        ))


async def pedidos_do_usuario(db: AsyncSession, usuario_id: int) -> list[dict]:
    vendas = await venda_repo.pedidos_do_usuario(db, usuario_id)
    result = []
    for v in vendas:
        valor_original = float(v.valor_original or 0)
        valor_total    = float(v.valor_total or 0)
        result.append({
            "id":                 v.id,
            "data":               v.data.isoformat(),
            "valor_total":        valor_total,
            "valor_sem_desconto": valor_original,
            "desconto_aplicado":  float(v.desconto_aplicado or 0),
            "cupom_aplicado":     v.cupom_aplicado or "",
            "economia":           max(0, valor_original - valor_total),
            "itens": [
                {
                    "id_produto":           i.id_produto,
                    "nome_produto":         i.produto.nome if i.produto else "Produto não encontrado",
                    "imagem":               None,
                    "quantidade":           i.quantidade,
                    "plano":                i.plano,
                    "valor_total":          float(i.valor_total),
                    "desconto_recorrencia": settings.descontos_plano.get(i.plano, 0) * 100,
                }
                for i in v.itens
            ],
        })
    return result