import uuid
from config import Config
from backend.utils import csv_helper as csv
from backend.services import produto_service

CAMPOS = [
    "id_carrinho", "id_usuario", "id_produto", "nome_produto",
    "descricao", "plano", "quantidade", "valor_unitario",
    "valor_total", "status",
]

def _calcular_total(valor_unitario, plano, quantidade):
    mult = Config.MULTIPLICADORES_PLANO.get(plano, 1)
    desc = Config.DESCONTOS_PLANO.get(plano, 0)
    return round(valor_unitario * mult * quantidade * (1 - desc), 2)

def _itens_ativos(carrinho, usuario_id):
    return [i for i in carrinho if i["id_usuario"] == usuario_id and i["status"] == "em processo"]

def itens(usuario_id):
    return _itens_ativos(csv.ler(Config.CARRINHO_FILE), str(usuario_id))

def contador(usuario_id):
    return len(itens(str(usuario_id)))

def total(usuario_id):
    return round(sum(float(i.get("valor_total", 0)) for i in itens(str(usuario_id))), 2)

def adicionar(usuario_id, produto_id, plano, quantidade):
    usuario_id = str(usuario_id)
    produto = produto_service.buscar_por_id(produto_id)
    if not produto:
        return False, "Produto não encontrado."

    try:
        valor_unitario = float(produto.get("preco", 0))
    except (ValueError, TypeError):
        return False, "Preço do produto inválido."

    if valor_unitario <= 0:
        return False, "Preço do produto inválido."

    try:
        estoque = int(produto.get("estoque", 0))
    except (ValueError, TypeError):
        estoque = 0

    tipo_produto = produto.get("tipo", "").lower()
    if estoque <= 0 and tipo_produto != "premium":
        return False, "Produto fora de estoque."
    if estoque > 0 and quantidade > estoque:
        return False, f"Quantidade indisponível. Estoque: {estoque}"

    carrinho = csv.ler(Config.CARRINHO_FILE)

    for item in carrinho:
        if (
            item["id_usuario"] == usuario_id
            and str(item["id_produto"]).strip() == str(produto_id).strip()
            and item["plano"] == plano
            and item["status"] == "em processo"
        ):
            nova_qtd = int(item["quantidade"]) + quantidade
            if estoque > 0 and nova_qtd > estoque:
                return False, f"Quantidade indisponível. Estoque: {estoque}"
            item["quantidade"] = str(nova_qtd)
            item["valor_total"] = str(_calcular_total(valor_unitario, plano, nova_qtd))
            csv.salvar(Config.CARRINHO_FILE, carrinho, CAMPOS)
            return True, f"Quantidade de {produto['nome']} atualizada para {nova_qtd}!"

    carrinho.append({
        "id_carrinho": str(uuid.uuid4()),
        "id_usuario": usuario_id,
        "id_produto": produto_id,
        "nome_produto": produto.get("nome", ""),
        "descricao": produto.get("descricao", ""),
        "plano": plano,
        "quantidade": str(quantidade),
        "valor_unitario": str(valor_unitario),
        "valor_total": str(_calcular_total(valor_unitario, plano, quantidade)),
        "status": "em processo",
    })
    csv.salvar(Config.CARRINHO_FILE, carrinho, CAMPOS)
    return True, f"{produto['nome']} adicionado ao carrinho!"

def remover_itens(usuario_id, ids_carrinho):
    usuario_id = str(usuario_id)
    carrinho = csv.ler(Config.CARRINHO_FILE)
    novos = [i for i in carrinho if not (i["id_usuario"] == usuario_id and i["id_carrinho"] in ids_carrinho)]
    removidos = len(carrinho) - len(novos)
    if removidos > 0:
        csv.salvar(Config.CARRINHO_FILE, novos, CAMPOS)
    return removidos

def atualizar_quantidade(usuario_id, item_id, nova_quantidade):
    usuario_id = str(usuario_id)
    if nova_quantidade < 1:
        return False, "Quantidade deve ser maior que zero.", 0, 0

    carrinho = csv.ler(Config.CARRINHO_FILE)
    item = next((i for i in carrinho if i["id_carrinho"] == item_id and i["id_usuario"] == usuario_id), None)
    if not item:
        return False, "Item não encontrado no carrinho.", 0, 0

    produto = produto_service.buscar_por_id(item["id_produto"])
    if produto:
        try:
            estoque = int(produto.get("estoque", 0))
            if estoque > 0 and nova_quantidade > estoque:
                return False, f"Quantidade indisponível. Estoque: {estoque}", 0, 0
        except (ValueError, TypeError):
            pass

    valor_unitario = float(item["valor_unitario"])
    novo_valor = _calcular_total(valor_unitario, item["plano"], nova_quantidade)
    item["quantidade"] = str(nova_quantidade)
    item["valor_total"] = str(novo_valor)
    csv.salvar(Config.CARRINHO_FILE, carrinho, CAMPOS)

    total_geral = round(sum(
        float(i["valor_total"]) for i in carrinho
        if i["id_usuario"] == usuario_id and i["status"] == "em processo"
    ), 2)
    return True, "Quantidade atualizada!", novo_valor, total_geral

def limpar_usuario(usuario_id):
    usuario_id = str(usuario_id)
    carrinho = csv.ler(Config.CARRINHO_FILE)
    novos = [i for i in carrinho if not (i["id_usuario"] == usuario_id and i["status"] == "em processo")]
    csv.salvar(Config.CARRINHO_FILE, novos, CAMPOS)

def migrar_guest(guest_id, usuario_id):
    usuario_id = str(usuario_id)
    carrinho = csv.ler(Config.CARRINHO_FILE)
    migrados = 0
    for item in carrinho:
        if item["id_usuario"] == f"guest_{guest_id}" and item["status"] == "em processo":
            item["id_usuario"] = usuario_id
            migrados += 1
    if migrados > 0:
        csv.salvar(Config.CARRINHO_FILE, carrinho, CAMPOS)
    return migrados

def itens_selecionados(usuario_id, ids_carrinho):
    usuario_id = str(usuario_id)
    carrinho = csv.ler(Config.CARRINHO_FILE)
    return [
        i for i in carrinho
        if i["id_usuario"] == usuario_id
        and i["status"] == "em processo"
        and i["id_carrinho"] in ids_carrinho
    ]