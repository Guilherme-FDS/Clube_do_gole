from config import Config
from utils import csv_helper as csv

CAMPOS = ["id", "codigo", "desconto_percentual", "usos_maximos", "usos_restantes", "status"]

def listar_todos():
    cupons = csv.ler(Config.CUPONS_FILE)
    for c in cupons:
        try:
            c["usos_restantes"] = int(c.get("usos_restantes", 0))
            c["desconto_percentual"] = float(c.get("desconto_percentual", 0))
        except (ValueError, TypeError):
            c["usos_restantes"] = 0
            c["desconto_percentual"] = 0.0
    return cupons

def buscar_por_id(cupom_id):
    return next((c for c in csv.ler(Config.CUPONS_FILE) if c["id"] == str(cupom_id)), None)

def buscar_por_codigo(codigo):
    return next(
        (c for c in csv.ler(Config.CUPONS_FILE) if c.get("codigo") == codigo.upper()),
        None
    )

def validar(codigo):
    """Retorna (valido, mensagem, percentual_desconto)"""
    cupom = buscar_por_codigo(codigo)
    if not cupom:
        return False, "Cupom inválido.", 0.0
    if cupom.get("status") != "ativo":
        return False, "Cupom inativo.", 0.0
    try:
        usos_restantes = int(cupom.get("usos_restantes", 0))
    except (ValueError, TypeError):
        usos_restantes = 0
    if usos_restantes <= 0:
        return False, "Cupom esgotado.", 0.0
    desconto = float(cupom.get("desconto_percentual", 0))
    return True, f"Cupom aplicado! {desconto}% de desconto.", desconto

def consumir(codigo):
    dados = csv.ler(Config.CUPONS_FILE)
    cupom = next((c for c in dados if c.get("codigo") == codigo.upper()), None)
    if not cupom:
        return False
    try:
        usos = int(cupom.get("usos_restantes", 0))
    except (ValueError, TypeError):
        return False
    if usos <= 0:
        return False
    cupom["usos_restantes"] = str(usos - 1)
    csv.salvar(Config.CUPONS_FILE, dados, CAMPOS)
    return True

def adicionar(dados):
    todos = csv.ler(Config.CUPONS_FILE)
    dados["id"] = csv.proximo_id(todos)
    todos.append(dados)
    csv.salvar(Config.CUPONS_FILE, todos, CAMPOS)
    return dados

def atualizar(cupom_id, novos_dados):
    todos = csv.ler(Config.CUPONS_FILE)
    for cupom in todos:
        if cupom["id"] == str(cupom_id):
            cupom.update(novos_dados)
            csv.salvar(Config.CUPONS_FILE, todos, CAMPOS)
            return True
    return False

def remover(cupom_id):
    todos = csv.ler(Config.CUPONS_FILE)
    novos = [c for c in todos if c["id"] != str(cupom_id)]
    if len(novos) == len(todos):
        return False
    csv.salvar(Config.CUPONS_FILE, novos, CAMPOS)
    return True

def alterar_status(cupom_id, novo_status):
    return atualizar(cupom_id, {"status": novo_status})