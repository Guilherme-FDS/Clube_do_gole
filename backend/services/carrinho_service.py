# services/carrinho_service.py
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from repositories import carrinho_repo, produto_repo, plano_repo
from services.plano_service import enriquecer_plano


async def adicionar(db: AsyncSession, usuario_id: int, produto_id: int, plano_id: int, quantidade: int) -> tuple[bool, str]:
    plano = await plano_repo.buscar(db, plano_id)
    if not plano or not plano.ativo:
        return False, "Plano não encontrado ou inativo."
    if plano.id_produto != produto_id:
        return False, "Plano não pertence a este produto."

    produto = await produto_repo.buscar(db, produto_id)
    if not produto or not produto.ativo:
        return False, "Produto não encontrado ou inativo."

    dados_plano = enriquecer_plano(plano)
    valor_unitario = Decimal(str(plano.preco_base))
    valor_total = Decimal(str(dados_plano["preco_total"]))

    existente = await carrinho_repo.buscar_existente(db, usuario_id, produto_id, plano.recorrencia)
    if existente:
        nova_qtd = existente.quantidade + quantidade
        novo_total = round(valor_total / existente.quantidade * nova_qtd, 2) if existente.quantidade else valor_total
        await carrinho_repo.atualizar_item(db, existente.id, nova_qtd, novo_total)
        return True, f"Quantidade de {produto.nome} atualizada para {nova_qtd}!"

    await carrinho_repo.adicionar(db, {
        "id_usuario": usuario_id,
        "id_produto": produto_id,
        "id_plano": plano_id,
        "nome_produto": produto.nome,
        "descricao": produto.descricao,
        "plano": plano.recorrencia,
        "quantidade": quantidade,
        "valor_unitario": valor_unitario,
        "valor_total": valor_total,
        "status": "em processo",
    })
    return True, f"{produto.nome} adicionado ao carrinho!"


async def atualizar_quantidade(db: AsyncSession, usuario_id: int, item_id: int, nova_quantidade: int) -> tuple[bool, str, float, float]:
    item = await carrinho_repo.buscar_item(db, item_id, usuario_id)
    if not item:
        return False, "Item não encontrado.", 0, 0

    if item.id_plano:
        plano = await plano_repo.buscar(db, item.id_plano)
        if plano:
            dados = enriquecer_plano(plano)
            novo_valor = round(Decimal(str(dados["preco_total"])) / 1 * nova_quantidade, 2)
        else:
            novo_valor = round(Decimal(str(item.valor_unitario)) * nova_quantidade, 2)
    else:
        novo_valor = round(Decimal(str(item.valor_unitario)) * nova_quantidade, 2)

    await carrinho_repo.atualizar_item(db, item_id, nova_quantidade, novo_valor)
    total_geral = await carrinho_repo.total(db, usuario_id)
    return True, "Quantidade atualizada!", float(novo_valor), total_geral