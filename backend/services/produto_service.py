from database.connection import fetchall, fetchone, execute


def listar_todos():
    return fetchall("SELECT * FROM produtos ORDER BY id")


def listar_por_tipo(tipo):
    return fetchall("SELECT * FROM produtos WHERE tipo = %s ORDER BY id", (tipo.lower(),))


def buscar_por_id(produto_id):
    return fetchone("SELECT * FROM produtos WHERE id = %s", (produto_id,))


def adicionar(dados):
    execute("""
        INSERT INTO produtos (nome, tipo, descricao, preco, imagem, estoque)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        dados.get("nome"),
        dados.get("tipo"),
        dados.get("descricao"),
        dados.get("preco", 0),
        dados.get("imagem", ""),
        dados.get("estoque", 0),
    ))


def atualizar(produto_id, dados):
    execute("""
        UPDATE produtos
        SET nome=%s, tipo=%s, descricao=%s, preco=%s, imagem=%s, estoque=%s, atualizado_em=NOW()
        WHERE id=%s
    """, (
        dados.get("nome"),
        dados.get("tipo"),
        dados.get("descricao"),
        dados.get("preco", 0),
        dados.get("imagem", ""),
        dados.get("estoque", 0),
        produto_id,
    ))


def remover(produto_id):
    execute("DELETE FROM produtos WHERE id = %s", (produto_id,))


def decrementar_estoque(produto_id, quantidade):
    execute("""
        UPDATE produtos
        SET estoque = GREATEST(0, estoque - %s), atualizado_em=NOW()
        WHERE id = %s
    """, (quantidade, produto_id))