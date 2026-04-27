from config import Config
from utils import csv_helper as csv

CAMPOS = ["id", "nome", "tipo", "descricao", "preco", "imagem", "estoque"]

def listar_todos():
    return csv.ler(Config.PRODUTOS_FILE)

def listar_por_tipo(tipo):
    return [p for p in listar_todos() if p.get("tipo", "").strip().lower() == tipo.lower()]

def buscar_por_id(produto_id):
    return next(
        (p for p in listar_todos() if str(p.get("id")).strip() == str(produto_id).strip()),
        None
    )

def adicionar(dados):
    produtos = listar_todos()
    dados["id"] = csv.proximo_id(produtos)
    produtos.append(dados)
    csv.salvar(Config.PRODUTOS_FILE, produtos, CAMPOS)
    return dados

def atualizar(produto_id, novos_dados):
    produtos = listar_todos()
    for produto in produtos:
        if produto["id"] == str(produto_id):
            produto.update(novos_dados)
            csv.salvar(Config.PRODUTOS_FILE, produtos, CAMPOS)
            return True
    return False

def remover(produto_id):
    produtos = listar_todos()
    novos = [p for p in produtos if p["id"] != str(produto_id)]
    if len(novos) == len(produtos):
        return False
    csv.salvar(Config.PRODUTOS_FILE, novos, CAMPOS)
    return True

def decrementar_estoque(produto_id, quantidade):
    produtos = listar_todos()
    for produto in produtos:
        if produto["id"] == str(produto_id):
            try:
                atual = int(produto.get("estoque", 0))
                produto["estoque"] = str(max(0, atual - quantidade))
            except (ValueError, TypeError):
                pass
    csv.salvar(Config.PRODUTOS_FILE, produtos, CAMPOS)