from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from repositories import venda_repo, carrinho_repo, produto_repo, cupom_repo
from config import get_settings

settings = get_settings()


async def finalizar_compra(
    db: AsyncSession,
    usuario_id: int,
    ids_itens: list[int],
    codigo_cupom: str = "",
    desconto_cupom: float = 0.0,
) -> tuple[bool, str]:
    itens = await carrinho_repo.buscar_por_ids(db, usuario_id, ids_itens)
    if not itens:
        return False, "Nenhum item válido para finalizar."

    for item in itens:
        valor_unitario = Decimal(str(item.valor_unitario))
        quantidade = item.quantidade
        plano = item.plano
        mult = settings.multiplicadores_plano.get(plano, 1)
        desc_plano = Decimal(str(settings.descontos_plano.get(plano, 0)))
        valor_original = valor_unitario * mult * quantidade
        valor_apos_plano = valor_original * (1 - desc_plano)
        valor_final = max(Decimal("0"), valor_apos_plano * (1 - Decimal(str(desconto_cupom)) / 100))
        desconto_total = ((valor_original - valor_final) / valor_original * 100) if valor_original else Decimal("0")

        await venda_repo.criar(db, {
            "id_usuario": usuario_id,
            "id_produto": item.id_produto,
            "quantidade": quantidade,
            "valor_original": round(valor_original, 2),
            "valor_desconto": round(valor_original - valor_final, 2),
            "valor_total": round(valor_final, 2),
            "plano": plano,
            "desconto_aplicado": round(desconto_total, 2),
            "cupom_aplicado": codigo_cupom or None,
        })
        await produto_repo.decrementar_estoque(db, item.id_produto, quantidade)

    await carrinho_repo.finalizar_itens(db, usuario_id, ids_itens)

    if codigo_cupom:
        await cupom_repo.consumir_atomico(db, codigo_cupom)

    return True, f"{len(itens)} item(ns) finalizado(s) com sucesso!"


async def pedidos_do_usuario(db: AsyncSession, usuario_id: int) -> list[dict]:
    vendas = await venda_repo.pedidos_do_usuario(db, usuario_id)
    result = []
    for v in vendas:
        valor_original = float(v.valor_original or 0)
        valor_total = float(v.valor_total or 0)
        plano = v.plano or "mensal"
        result.append({
            "id": v.id,
            "id_produto": v.id_produto,
            "nome_produto": v.produto.nome if v.produto else "Produto não encontrado",
            "quantidade": v.quantidade,
            "plano": plano,
            "data": v.data.isoformat(),
            "imagem_produto": v.produto.imagem if v.produto else None,
            "valor_total": valor_total,
            "valor_sem_desconto": valor_original,
            "desconto_aplicado": float(v.desconto_aplicado or 0),
            "desconto_recorrencia": settings.descontos_plano.get(plano, 0) * 100,
            "cupom_aplicado": v.cupom_aplicado or "",
            "economia": max(0, valor_original - valor_total),
        })
    return result