from backend.database.connection import fetchall, fetchone, execute


def listar_todos():
    return fetchall("SELECT * FROM cupons ORDER BY id")


def buscar_por_id(cupom_id):
    return fetchone("SELECT * FROM cupons WHERE id = %s", (cupom_id,))


def buscar_por_codigo(codigo):
    return fetchone("SELECT * FROM cupons WHERE codigo = %s", (codigo.upper(),))


def validar(codigo):
    """Retorna (valido, mensagem, percentual_desconto)"""
    cupom = buscar_por_codigo(codigo)
    if not cupom:
        return False, "Cupom inválido.", 0.0
    if cupom.get("status") != "ativo":
        return False, "Cupom inativo.", 0.0
    if cupom.get("usos_restantes", 0) <= 0:
        return False, "Cupom esgotado.", 0.0
    desconto = float(cupom.get("desconto_percentual", 0))
    return True, f"Cupom aplicado! {desconto}% de desconto.", desconto


def consumir(codigo):
    cupom = buscar_por_codigo(codigo)
    if not cupom or cupom.get("usos_restantes", 0) <= 0:
        return False
    execute("""
        UPDATE cupons SET usos_restantes = usos_restantes - 1 WHERE codigo = %s
    """, (codigo.upper(),))
    return True


def adicionar(dados):
    execute("""
        INSERT INTO cupons (codigo, desconto_percentual, usos_maximos, usos_restantes, status)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        dados.get("codigo", "").upper(),
        dados.get("desconto_percentual", 0),
        dados.get("usos_maximos", 1),
        dados.get("usos_restantes", 1),
        dados.get("status", "ativo"),
    ))


def atualizar(cupom_id, dados):
    execute("""
        UPDATE cupons
        SET codigo=%s, desconto_percentual=%s, usos_maximos=%s, usos_restantes=%s, status=%s
        WHERE id=%s
    """, (
        dados.get("codigo", "").upper(),
        dados.get("desconto_percentual", 0),
        dados.get("usos_maximos", 1),
        dados.get("usos_restantes", 1),
        dados.get("status", "ativo"),
        cupom_id,
    ))


def remover(cupom_id):
    execute("DELETE FROM cupons WHERE id = %s", (cupom_id,))


def alterar_status(cupom_id, novo_status):
    execute("UPDATE cupons SET status = %s WHERE id = %s", (novo_status, cupom_id))