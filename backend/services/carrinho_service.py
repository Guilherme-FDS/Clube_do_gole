from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from repositories import carrinho_repo, produto_repo
from config import get_settings

settings = get_settings()


def _calcular_total(valor_unitario: Decimal, plano: str, quantidade: int) -> Decimal:
    mult = settings.multiplicadores_plano.get(plano, 1)
    desc = settings.descontos_plano.get(plano, 0)
    return round(valor_unitario * mult * quantidade * Decimal(str(1 - desc)), 2)


async def adicionar(db: AsyncSession, usuario_id: int, produto_id: int, plano: str, quantidade: int) -> tuple[bool, str]:
    produto = await produto_repo.buscar(db, produto_id)
    if not produto:
        return False, "Produto não encontrado."
    valor_unitario = Decimal(str(produto.preco))
    if valor_unitario <= 0:
        return False, "Preço do produto inválido."
    estoque = produto.estoque or 0
    if estoque <= 0 and produto.tipo != "premium":
        return False, "Produto fora de estoque."
    if estoque > 0 and quantidade > estoque:
        return False, f"Quantidade indisponível. Estoque: {estoque}"
    existente = await carrinho_repo.buscar_existente(db, usuario_id, produto_id, plano)
    if existente:
        nova_qtd = existente.quantidade + quantidade
        if estoque > 0 and nova_qtd > estoque:
            return False, f"Quantidade indisponível. Estoque: {estoque}"
        await carrinho_repo.atualizar_item(db, existente.id, nova_qtd, _calcular_total(valor_unitario, plano, nova_qtd))
        return True, f"Quantidade de {produto.nome} atualizada para {nova_qtd}!"
    await carrinho_repo.adicionar(db, {
        "id_usuario": usuario_id, "id_produto": produto_id,
        "nome_produto": produto.nome, "descricao": produto.descricao,
        "plano": plano, "quantidade": quantidade,
        "valor_unitario": valor_unitario,
        "valor_total": _calcular_total(valor_unitario, plano, quantidade),
        "status": "em processo",
    })
    return True, f"{produto.nome} adicionado ao carrinho!"


async def atualizar_quantidade(db: AsyncSession, usuario_id: int, item_id: int, nova_quantidade: int) -> tuple[bool, str, float, float]:
    item = await carrinho_repo.buscar_item(db, item_id, usuario_id)
    if not item:
        return False, "Item não encontrado.", 0, 0
    produto = await produto_repo.buscar(db, item.id_produto)
    if produto and produto.estoque > 0 and nova_quantidade > produto.estoque:
        return False, f"Quantidade indisponível. Estoque: {produto.estoque}", 0, 0
    novo_valor = _calcular_total(Decimal(str(item.valor_unitario)), item.plano, nova_quantidade)
    await carrinho_repo.atualizar_item(db, item_id, nova_quantidade, novo_valor)
    total_geral = await carrinho_repo.total(db, usuario_id)
    return True, "Quantidade atualizada!", float(novo_valor), total_geral