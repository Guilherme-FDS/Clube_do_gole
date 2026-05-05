from database.connection import fetchall, fetchone, execute


def listar_do_usuario(usuario_id):
    return fetchall("""
        SELECT * FROM enderecos WHERE id_cliente=%s ORDER BY principal DESC, id
    """, (int(usuario_id),))


def buscar(endereco_id, usuario_id):
    return fetchone("""
        SELECT * FROM enderecos WHERE id=%s AND id_cliente=%s
    """, (int(endereco_id), int(usuario_id)))


def adicionar(usuario_id, dados, definir_principal=False):
    usuario_id = int(usuario_id)
    meus = listar_do_usuario(usuario_id)

    if not meus:
        definir_principal = True

    if definir_principal:
        execute("""
            UPDATE enderecos SET principal='nao' WHERE id_cliente=%s
        """, (usuario_id,))

    execute("""
        INSERT INTO enderecos
            (id_cliente, tipo, cep, endereco, numero, complemento,
             bairro, cidade, estado, pais, principal)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        usuario_id,
        dados.get("tipo", "residencial"),
        dados.get("cep", ""),
        dados.get("endereco", ""),
        dados.get("numero", ""),
        dados.get("complemento", ""),
        dados.get("bairro", ""),
        dados.get("cidade", ""),
        dados.get("estado", ""),
        dados.get("pais", "Brasil"),
        "sim" if definir_principal else "nao",
    ))
    return True, "Endereço adicionado com sucesso!"


def atualizar(endereco_id, usuario_id, dados, definir_principal=False):
    usuario_id = int(usuario_id)
    endereco = buscar(endereco_id, usuario_id)
    if not endereco:
        return False, "Endereço não encontrado."

    if definir_principal:
        execute("""
            UPDATE enderecos SET principal='nao' WHERE id_cliente=%s
        """, (usuario_id,))

    execute("""
        UPDATE enderecos
        SET tipo=%s, cep=%s, endereco=%s, numero=%s, complemento=%s,
            bairro=%s, cidade=%s, estado=%s, pais=%s, principal=%s
        WHERE id=%s AND id_cliente=%s
    """, (
        dados.get("tipo", "residencial"),
        dados.get("cep", ""),
        dados.get("endereco", ""),
        dados.get("numero", ""),
        dados.get("complemento", ""),
        dados.get("bairro", ""),
        dados.get("cidade", ""),
        dados.get("estado", ""),
        dados.get("pais", "Brasil"),
        "sim" if definir_principal else "nao",
        int(endereco_id),
        usuario_id,
    ))
    return True, "Endereço atualizado com sucesso!"


def remover(endereco_id, usuario_id):
    usuario_id = int(usuario_id)
    meus = listar_do_usuario(usuario_id)

    if len(meus) <= 1:
        return False, "Você não pode excluir seu único endereço."

    endereco = buscar(endereco_id, usuario_id)
    if not endereco:
        return False, "Endereço não encontrado."

    execute("""
        DELETE FROM enderecos WHERE id=%s AND id_cliente=%s
    """, (int(endereco_id), usuario_id))

    # Se era principal, promove o próximo
    if endereco.get("principal") == "sim":
        restante = fetchone("""
            SELECT id FROM enderecos WHERE id_cliente=%s LIMIT 1
        """, (usuario_id,))
        if restante:
            execute("""
                UPDATE enderecos SET principal='sim' WHERE id=%s
            """, (restante["id"],))

    return True, "Endereço excluído com sucesso!"


def definir_principal(endereco_id, usuario_id):
    usuario_id = int(usuario_id)
    if not buscar(endereco_id, usuario_id):
        return False, "Endereço não encontrado."
    execute("""
        UPDATE enderecos SET principal='nao' WHERE id_cliente=%s
    """, (usuario_id,))
    execute("""
        UPDATE enderecos SET principal='sim' WHERE id=%s AND id_cliente=%s
    """, (int(endereco_id), usuario_id))
    return True, "Endereço principal definido com sucesso!"