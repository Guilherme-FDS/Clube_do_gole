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

    valor_original_total = Decimal("0")
    valor_final_total    = Decimal("0")
    itens_venda          = []

    for item in itens:
        valor_unitario = Decimal(str(item.valor_unitario))
        quantidade     = item.quantidade
        plano          = item.plano
        mult           = settings.multiplicadores_plano.get(plano, 1)
        desc_plano     = Decimal(str(settings.descontos_plano.get(plano, 0)))

        valor_original     = valor_unitario * mult * quantidade
        valor_apos_plano   = valor_original * (1 - desc_plano)
        valor_final        = max(Decimal("0"), valor_apos_plano * (1 - Decimal(str(desconto_cupom)) / 100))

        valor_original_total += valor_original
        valor_final_total    += valor_final

        itens_venda.append({
            "id_produto":    item.id_produto,
            "nome_produto":  item.nome_produto,
            "plano":         plano,
            "quantidade":    quantidade,
            "valor_unitario": round(valor_unitario * mult, 2),
            "valor_total":   round(valor_final, 2),
        })

        await produto_repo.decrementar_estoque(db, item.id_produto, quantidade)

    desconto_total = (
        (valor_original_total - valor_final_total) / valor_original_total * 100
        if valor_original_total else Decimal("0")
    )

    await venda_repo.criar(db, {
        "id_usuario":       usuario_id,
        "valor_original":   round(valor_original_total, 2),
        "valor_desconto":   round(valor_original_total - valor_final_total, 2),
        "valor_total":      round(valor_final_total, 2),
        "desconto_aplicado": round(desconto_total, 2),
        "cupom_aplicado":   codigo_cupom or None,
    }, itens_venda)

    await carrinho_repo.finalizar_itens(db, usuario_id, ids_itens)

    if codigo_cupom:
        await cupom_repo.consumir_atomico(db, codigo_cupom)

    return True, f"{len(itens)} item(ns) finalizado(s) com sucesso!"


async def pedidos_do_usuario(db: AsyncSession, usuario_id: int) -> list[dict]:
    vendas = await venda_repo.pedidos_do_usuario(db, usuario_id)
    result = []
    for v in vendas:
        valor_original = float(v.valor_original or 0)
        valor_total    = float(v.valor_total or 0)
        result.append({
            "id":                v.id,
            "data":              v.data.isoformat(),
            "valor_total":       valor_total,
            "valor_sem_desconto": valor_original,
            "desconto_aplicado": float(v.desconto_aplicado or 0),
            "cupom_aplicado":    v.cupom_aplicado or "",
            "economia":          max(0, valor_original - valor_total),
            "itens": [
                {
                    "id_produto":   i.id_produto,
                    "nome_produto": i.produto.nome if i.produto else "Produto não encontrado",
                    "imagem":       i.produto.imagem if i.produto else None,
                    "quantidade":   i.quantidade,
                    "plano":        i.plano,
                    "valor_total":  float(i.valor_total),
                    "desconto_recorrencia": settings.descontos_plano.get(i.plano, 0) * 100,
                }
                for i in v.itens
            ],
        })
    return result