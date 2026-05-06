import uuid
from config import Config
from database.connection import fetchall, fetchone, execute
from services import produto_service


def _is_guest(usuario_id):
    return str(usuario_id).startswith('guest_')


def _calcular_total(valor_unitario, plano, quantidade):
    mult = Config.MULTIPLICADORES_PLANO.get(plano, 1)
    desc = Config.DESCONTOS_PLANO.get(plano, 0)
    return round(valor_unitario * mult * quantidade * (1 - desc), 2)


def itens(usuario_id):
    if _is_guest(usuario_id):
        return []
    return fetchall("""
        SELECT * FROM carrinho
        WHERE id_usuario = %s AND status = 'em processo'
        ORDER BY criado_em
    """, (int(usuario_id),))


def contador(usuario_id):
    if _is_guest(usuario_id):
        return 0
    row = fetchone("""
        SELECT COUNT(*) AS total FROM carrinho
        WHERE id_usuario = %s AND status = 'em processo'
    """, (int(usuario_id),))
    return row["total"] if row else 0


def total(usuario_id):
    if _is_guest(usuario_id):
        return 0
    row = fetchone("""
        SELECT COALESCE(SUM(valor_total), 0) AS total FROM carrinho
        WHERE id_usuario = %s AND status = 'em processo'
    """, (int(usuario_id),))
    return round(float(row["total"]), 2) if row else 0


def adicionar(usuario_id, produto_id, plano, quantidade):
    if _is_guest(usuario_id):
        return False, "Faça login para adicionar itens ao carrinho."

    produto = produto_service.buscar_por_id(produto_id)
    if not produto:
        return False, "Produto não encontrado."

    try:
        valor_unitario = float(produto.get("preco", 0))
    except (ValueError, TypeError):
        return False, "Preço do produto inválido."

    if valor_unitario <= 0:
        return False, "Preço do produto inválido."

    estoque = int(produto.get("estoque", 0) or 0)
    tipo_produto = (produto.get("tipo") or "").lower()

    if estoque <= 0 and tipo_produto != "premium":
        return False, "Produto fora de estoque."
    if estoque > 0 and quantidade > estoque:
        return False, f"Quantidade indisponível. Estoque: {estoque}"

    existente = fetchone("""
        SELECT * FROM carrinho
        WHERE id_usuario=%s AND id_produto=%s AND plano=%s AND status='em processo'
    """, (int(usuario_id), int(produto_id), plano))

    if existente:
        nova_qtd = int(existente["quantidade"]) + quantidade
        if estoque > 0 and nova_qtd > estoque:
            return False, f"Quantidade indisponível. Estoque: {estoque}"
        novo_total = _calcular_total(valor_unitario, plano, nova_qtd)
        execute("""
            UPDATE carrinho SET quantidade=%s, valor_total=%s
            WHERE id_carrinho=%s
        """, (nova_qtd, novo_total, existente["id_carrinho"]))
        return True, f"Quantidade de {produto['nome']} atualizada para {nova_qtd}!"

    novo_total = _calcular_total(valor_unitario, plano, quantidade)
    execute("""
        INSERT INTO carrinho
            (id_carrinho, id_usuario, id_produto, nome_produto, descricao,
             plano, quantidade, valor_unitario, valor_total, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'em processo')
    """, (
        str(uuid.uuid4()),
        int(usuario_id),
        int(produto_id),
        produto.get("nome", ""),
        produto.get("descricao", ""),
        plano,
        quantidade,
        valor_unitario,
        novo_total,
    ))
    return True, f"{produto['nome']} adicionado ao carrinho!"


def remover_itens(usuario_id, ids_carrinho):
    if _is_guest(usuario_id) or not ids_carrinho:
        return 0
    placeholders = ",".join(["%s"] * len(ids_carrinho))
    execute(f"""
        DELETE FROM carrinho
        WHERE id_usuario=%s AND id_carrinho IN ({placeholders})
    """, (int(usuario_id), *ids_carrinho))
    return len(ids_carrinho)


def atualizar_quantidade(usuario_id, item_id, nova_quantidade):
    if _is_guest(usuario_id):
        return False, "Faça login para gerenciar o carrinho.", 0, 0

    if nova_quantidade < 1:
        return False, "Quantidade deve ser maior que zero.", 0, 0

    item = fetchone("""
        SELECT * FROM carrinho WHERE id_carrinho=%s AND id_usuario=%s
    """, (item_id, int(usuario_id)))

    if not item:
        return False, "Item não encontrado no carrinho.", 0, 0

    produto = produto_service.buscar_por_id(item["id_produto"])
    if produto:
        estoque = int(produto.get("estoque", 0) or 0)
        if estoque > 0 and nova_quantidade > estoque:
            return False, f"Quantidade indisponível. Estoque: {estoque}", 0, 0

    valor_unitario = float(item["valor_unitario"])
    novo_valor = _calcular_total(valor_unitario, item["plano"], nova_quantidade)

    execute("""
        UPDATE carrinho SET quantidade=%s, valor_total=%s WHERE id_carrinho=%s
    """, (nova_quantidade, novo_valor, item_id))

    total_geral = total(usuario_id)
    return True, "Quantidade atualizada!", novo_valor, total_geral


def limpar_usuario(usuario_id):
    if _is_guest(usuario_id):
        return
    execute("""
        DELETE FROM carrinho WHERE id_usuario=%s AND status='em processo'
    """, (int(usuario_id),))


def migrar_guest(guest_id, usuario_id):
    rows = fetchall("""
        SELECT * FROM carrinho WHERE id_usuario=%s AND status='em processo'
    """, (f"guest_{guest_id}",))
    for item in rows:
        execute("""
            UPDATE carrinho SET id_usuario=%s WHERE id_carrinho=%s
        """, (int(usuario_id), item["id_carrinho"]))
    return len(rows)


def itens_selecionados(usuario_id, ids_carrinho):
    if _is_guest(usuario_id) or not ids_carrinho:
        return []
    placeholders = ",".join(["%s"] * len(ids_carrinho))
    return fetchall(f"""
        SELECT * FROM carrinho
        WHERE id_usuario=%s AND status='em processo'
        AND id_carrinho IN ({placeholders})
    """, (int(usuario_id), *ids_carrinho))