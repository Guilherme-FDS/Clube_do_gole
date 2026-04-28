from config import Config
from backend.utils import csv_helper as csv

CAMPOS_CLIENTE = ["id", "cpf", "nome", "sobrenome", "data_nascimento", "email", "senha", "telefone"]
CAMPOS_ADM = ["id", "nome", "email", "senha", "tipo"]

def autenticar_admin(email, senha):
    admins = csv.ler(Config.USUARIOS_ADM)
    return next((a for a in admins if a.get("email") == email and a.get("senha") == senha), None)

def autenticar_cliente(email, senha):
    clientes = csv.ler(Config.USUARIOS_CLIENTE)
    return next((c for c in clientes if c.get("email") == email and c.get("senha") == senha), None)

def email_ja_cadastrado(email):
    return any(c.get("email") == email for c in csv.ler(Config.USUARIOS_CLIENTE))

def cpf_ja_cadastrado(cpf):
    return any(c.get("cpf") == cpf for c in csv.ler(Config.USUARIOS_CLIENTE))

def cadastrar_cliente(dados):
    clientes = csv.ler(Config.USUARIOS_CLIENTE)
    dados["id"] = csv.proximo_id(clientes)
    clientes.append(dados)
    csv.salvar(Config.USUARIOS_CLIENTE, clientes, CAMPOS_CLIENTE)
    return dados

def buscar_cliente_por_id(usuario_id):
    clientes = csv.ler(Config.USUARIOS_CLIENTE)
    return next((c for c in clientes if c["id"] == str(usuario_id)), None)

def atualizar_cliente(usuario_id, novos_dados):
    clientes = csv.ler(Config.USUARIOS_CLIENTE)
    for cliente in clientes:
        if cliente["id"] == str(usuario_id):
            cliente.update(novos_dados)
            csv.salvar(Config.USUARIOS_CLIENTE, clientes, CAMPOS_CLIENTE)
            return True
    return False

def alterar_senha(usuario_id, senha_atual, nova_senha):
    clientes = csv.ler(Config.USUARIOS_CLIENTE)
    cliente = next((c for c in clientes if c["id"] == str(usuario_id)), None)
    if not cliente:
        return False, "Usuário não encontrado."
    if cliente.get("senha") != senha_atual:
        return False, "Senha atual incorreta."
    if len(nova_senha) < 6:
        return False, "A senha deve ter pelo menos 6 caracteres."
    cliente["senha"] = nova_senha
    csv.salvar(Config.USUARIOS_CLIENTE, clientes, CAMPOS_CLIENTE)
    return True, "Senha alterada com sucesso!"