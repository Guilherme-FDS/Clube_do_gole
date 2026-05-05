import bcrypt
from database.connection import fetchall, fetchone, execute


def autenticar_admin(email, senha):
    adm = fetchone(
        "SELECT * FROM usuarios_adm WHERE email = %s", (email.lower(),)
    )
    if not adm:
        return None
    try:
        if bcrypt.checkpw(senha.encode(), adm["senha"].encode()):
            return adm
    except Exception:
        if adm["senha"] == senha:
            return adm
    return None


def autenticar_cliente(email, senha):
    cliente = fetchone(
        "SELECT * FROM usuarios_clientes WHERE email = %s", (email.lower(),)
    )
    if not cliente:
        return None
    try:
        if bcrypt.checkpw(senha.encode(), cliente["senha"].encode()):
            return cliente
    except Exception:
        if cliente["senha"] == senha:
            return cliente
    return None


def email_ja_cadastrado(email):
    return fetchone(
        "SELECT id FROM usuarios_clientes WHERE email = %s", (email.lower(),)
    ) is not None


def cpf_ja_cadastrado(cpf):
    return fetchone(
        "SELECT id FROM usuarios_clientes WHERE cpf = %s", (cpf,)
    ) is not None


def cadastrar_cliente(dados):
    senha_hash = bcrypt.hashpw(
        dados["senha"].encode(), bcrypt.gensalt()
    ).decode()
    execute("""
        INSERT INTO usuarios_clientes
            (cpf, nome, sobrenome, data_nascimento, email, senha, telefone)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        dados.get("cpf"),
        dados.get("nome"),
        dados.get("sobrenome"),
        dados.get("data_nascimento") or None,
        dados.get("email", "").lower(),
        senha_hash,
        dados.get("telefone"),
    ))
    return fetchone(
        "SELECT * FROM usuarios_clientes WHERE email = %s",
        (dados["email"].lower(),)
    )


def buscar_cliente_por_id(usuario_id):
    return fetchone(
        "SELECT * FROM usuarios_clientes WHERE id = %s", (int(usuario_id),)
    )


def atualizar_cliente(usuario_id, novos_dados):
    execute("""
        UPDATE usuarios_clientes
        SET nome=%s, sobrenome=%s, email=%s, telefone=%s, data_nascimento=%s
        WHERE id=%s
    """, (
        novos_dados.get("nome"),
        novos_dados.get("sobrenome"),
        novos_dados.get("email", "").lower(),
        novos_dados.get("telefone"),
        novos_dados.get("data_nascimento") or None,
        int(usuario_id),
    ))
    return True


def alterar_senha(usuario_id, senha_atual, nova_senha):
    cliente = buscar_cliente_por_id(usuario_id)
    if not cliente:
        return False, "Usuário não encontrado."
    try:
        ok = bcrypt.checkpw(senha_atual.encode(), cliente["senha"].encode())
    except Exception:
        ok = cliente["senha"] == senha_atual
    if not ok:
        return False, "Senha atual incorreta."
    if len(nova_senha) < 6:
        return False, "A senha deve ter pelo menos 6 caracteres."
    nova_hash = bcrypt.hashpw(nova_senha.encode(), bcrypt.gensalt()).decode()
    execute(
        "UPDATE usuarios_clientes SET senha=%s WHERE id=%s",
        (nova_hash, int(usuario_id))
    )
    return True, "Senha alterada com sucesso!"